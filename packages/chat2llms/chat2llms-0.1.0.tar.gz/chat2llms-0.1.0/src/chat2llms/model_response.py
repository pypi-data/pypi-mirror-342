import os
import datetime
from markdown import markdown
from typing import List, Dict, Tuple
import requests
import json

from abc import ABC, abstractmethod

from .base_client import BaseClient, logger

import openai
import google.generativeai as genai

# === 响应处理类 ===
class ModelResponse(BaseClient):
    """Class to handle responses from a specific LLM for a given prompt.

    Args:
        client (BaseClient): The LLM client instance.
        prompt (str): The input prompt for the LLM.

    Attributes:
        client (BaseClient): The LLM client.
        prompt (str): The input prompt.
    """

    def __init__(self, client: BaseClient, prompt: str = None):
        self.client = client
        self.prompt = prompt
        self._response = None
        # self.response = None

        self.latency = 0  # latency=time.time() - start
        self.tokens = 0  # tokens=len(response.text.split())
        self.error = None

        self.history: List[Dict] = []  # 存储完整对话历史
        self.max_history = 20  # 最大保留历史轮次

    """无历史响应"""

    @abstractmethod
    def call_api(self, prompt):
        """调用模型API的抽象方法"""
        raise NotImplementedError()

    def get_model_name(self):
        """获取模型响应"""
        return self.client.model_name

    def get_prompt_str(self):
        """获取提示词"""
        return self.prompt

    def api_response(self, prompt: str):
        """获取模型响应"""
        if not self._response:
            try:
                self.prompt = prompt
                self._response = self.call_api(prompt)
            except Exception as e:
                self._response = f"Error: {str(e)}"
        return self._response

    """历史响应"""
    @abstractmethod
    def get_response(
        self,
        prompt: str,
        history: List[Dict] = None,
        temperature: float = 0.7,
        max_tokens: int = 4000,
    ) -> str:
        """同步生成回复"""
        raise NotImplementedError()

    @abstractmethod
    def get_response_history(
        self, prompt: str, history: List[Dict] = None
    ) -> Tuple[str, List[Dict]]:
        """发送消息并返回响应和更新后的历史"""
        pass

    def _build_messages(self, prompt: str, history: List[Dict]) -> List[Dict]:
        """构造对话历史（可被子类重写）"""
        messages = history.copy()
        messages.append({"role": "user", "content": prompt})
        return messages


class OpenAIResponse(ModelResponse):
    """OpenAI API 客户端实现"""

    def call_api(self, prompt):
        client = openai.OpenAI(
            api_key=self.client.api_key, base_url=self.client.base_url
        )
        response = client.chat.completions.create(
            model=self.client.model_name, messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content

    """直接调用 OpenAI API 底层接口"""

    def get_response(self, prompt, history=None, temperature=0.7, max_tokens=4000):
        if not self._response:
            try:
                self.prompt = prompt
                messages = self._build_messages(prompt, history or [])
                response = requests.post(
                    f"{self.client.base_url}/chat/completions",
                    headers=self.client.headers,
                    json={
                        "model": self.client.model_name,
                        "messages": messages,
                        "temperature": temperature,
                        "max_tokens": max_tokens,
                    },
                )
                result = response.json()
                self._response = result["choices"][0]["message"]["content"]
            except Exception as e:
                self._response = f"Error: {str(e)}"
        return self._response

    def get_response_history(
        self, message: str, history: List[Dict] = []
    ) -> Tuple[str, List[Dict]]:

        new_history = self._update_history(history, message, role="user")

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.client.api_key}",
        }

        payload = {
            "model": self.client.model_name,
            "messages": new_history[-self.client.max_history * 2 :],  # 保留最近的对话
        }

        for attempt in range(self.client.max_retries):
            try:
                response = requests.post(
                    f"{self.client.base_url}/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=self.client.timeout,
                )
                response.raise_for_status()
                response_data = response.json()
                assistant_message = response_data["choices"][0]["message"][
                    "content"
                ].strip()

                updated_history = self._update_history(
                    new_history, assistant_message, role="assistant"
                )
                return (
                    assistant_message,
                    updated_history[-self.client.max_history * 2 :],
                )

            except requests.exceptions.RequestException as e:
                logger.warning(
                    f"API请求失败，尝试 {attempt + 1}/{self.client.max_retries}: {str(e)}"
                )
                if attempt == self.client.max_retries - 1:
                    raise RuntimeError("API请求超过最大重试次数") from e

            except (KeyError, IndexError, TypeError) as e:
                logger.error(f"响应解析错误: {str(e)}")
                raise RuntimeError("服务器返回了无效的响应格式") from e

        return "", history

    def _build_messages(self, prompt: str, history: List[Dict]) -> List[Dict]:
        return [*history, {"role": "user", "content": prompt}]

    def _update_history(
        self, history: List[Dict], content: str, role: str
    ) -> List[Dict]:
        """更新对话历史"""
        return history + [{"role": role, "content": content}]


class GeminiResponse(ModelResponse):

    def init_google_genai(self):
        genai.configure(api_key=self.client.api_key)
        self.model = genai.GenerativeModel(self.client.model_name)

    """Gemini API 客户端实现"""

    def call_api(self, prompt):
        self.init_google_genai()
        response = self.model.generate_content(prompt)
        return response.text

    # 使用 request 直接调用 Gemini API 底层接口。
    # 底层接口：​由 Google 提供的 HTTP REST 或 gRPC 端点，如
    # https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent
    # 开发者可以直接通过 HTTP 请求调用，无需依赖特定语言的库。适合需要灵活性的高级用户或跨语言集成。

    def get_response(self, prompt, history=None, temperature=0.7, max_tokens=4000):
        if not self._response:
            try:
                self.prompt = prompt
                messages = self._build_messages(prompt, history or [])
                response = requests.post(
                    f"{self.client.base_url}/models/{self.client.model_name}:generateContent?key={self.client.api_key}",
                    headers=self.client.headers,
                    json={
                        "contents": messages,
                        "generationConfig": {
                            "temperature": temperature,
                            "maxOutputTokens": max_tokens,
                        },
                    },
                )
                result = response.json()
                self._response = result["candidates"][0]["content"]["parts"][0]["text"]
            except Exception as e:
                self._response = f"Error: {str(e)}"
        return self._response

    def get_response_history(self, prompt: str, history=None) -> Tuple[str, List[Dict]]:
        """执行带历史管理的对话"""
        try:
            # 构造请求头
            headers = {
                "Content-Type": "application/json",
                "x-goog-api-key": self.client.api_key,
            }

            # 添加当前对话到历史
            self.history.append({"type": "chat", "role": "user", "content": prompt})

            # 发送API请求
            response = requests.post(
                f"{self.client.base_url}/models/{self.client.model_name}:generateContent",
                headers=headers,
                json=self._build_payload(prompt),
            )
            response.raise_for_status()

            # 解析响应
            ai_response = self._parse_response(response.json())

            # 记录AI响应历史
            self.history.append(
                {"type": "chat", "role": "model", "content": ai_response}
            )

            return ai_response, self.history

        except requests.exceptions.RequestException as e:
            # 网络错误处理
            self.history.append({"type": "system", "content": f"网络错误: {str(e)}"})
            return f"API请求失败: {str(e)}"

        except json.JSONDecodeError:
            # JSON解析错误
            return "响应解析失败"

    def _build_messages(self, prompt, history):
        # Gemini的messages结构不同
        return [
            {"parts": [{"text": msg["content"]}], "role": msg["role"].upper()}
            for msg in super()._build_messages(prompt, history)
        ]

    def _build_payload(self, prompt: str) -> Dict:
        """构造包含聊天历史的请求体"""
        parts = [{"text": prompt}]

        # 添加历史上下文（排除系统指令）
        context = [
            {"role": entry["role"], "parts": [{"text": entry["content"]}]}
            for entry in self.history[-self.max_history :]
            if entry["type"] == "chat"
        ]

        return {
            "contents": context + [{"role": "user", "parts": parts}],
            "generationConfig": {"temperature": 0.9, "maxOutputTokens": 4000},
        }

    def _parse_response(self, response: Dict) -> str:
        """解析API响应并提取文本内容"""
        try:
            return response["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError) as e:
            raise ValueError(f"无效的API响应结构: {str(e)}")
