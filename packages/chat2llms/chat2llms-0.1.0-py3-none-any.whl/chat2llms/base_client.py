from abc import ABC, abstractmethod
from typing import List, Dict, Tuple

import requests
import logging
import yaml
import os

# 配置日志记录
logging.basicConfig(
    filename="chat_history.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# 加载配置文件
def load_config(config_path: str = "config.yaml") -> Dict:
    """加载配置文件"""
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except (FileNotFoundError, yaml.YAMLError) as e:
        logger.error(f"配置文件加载失败: {str(e)}")
        raise

# == 基础类定义 ==
class BaseClient(ABC):
    """Base class for large language model clients.

    Args:
        provider (str): The provider of the LLM model.
        config (Dict): The model parameters of the LLM model.

    Attributes:
        provider (str): The provider.
        config (Dict): Other parameters.        
    """

    def __init__(self, provider: str, config: Dict = None):
        """初始化客户端配置"""

        providers = {"gemini", "openai", "grok", "deepseek"}

        if provider not in providers:
            print("Unknown provider, Using DeepSeek instead")
            self.provider = "deepseek" 
        else:
            self.provider = provider

        config = load_config()
        self.timeout = config[self.provider].get("timeout", 30)
        self.max_retries = config[self.provider].get("max_retries", 3)
        self.max_history = config[self.provider].get("max_history", 10)  # 保留最近10轮对话
               
        if self.provider == "openai":
            self.api_key = config[self.provider].get("api_key", os.getenv("OPENAI_API_KEY")) 
            self.base_url = config[self.provider].get("base_url", "https://api.openai.com/v1")
            self.model_name = config[self.provider].get("model", "gpt-4")

        elif self.provider == "gemini":
            self.api_key = config[self.provider].get("api_key", os.getenv("GEMINI_API_KEY")) 
            self.base_url = config[self.provider].get(
                "base_url", "https://generativelanguage.googleapis.com/v1beta"
            )
            self.model_name = config[self.provider].get("model", "gemini-1.5-pro")

        elif self.provider == "grok":
            self.api_key = config[self.provider].get("api_key", os.getenv("XAI_API_KEY")) 
            self.base_url = config[self.provider].get("base_url", "https://api.x.ai/v1")
            self.model_name = config[self.provider].get("model", "grok-2-latest")

        else:
            self.api_key = config[self.provider].get("api_key", os.getenv("DEEPSEEK_API_KEY"))
            self.base_url = config[self.provider].get("base_url", "https://api.deepseek.com")
            self.model_name = config[self.provider].get("model", "deepseek-chat")

        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

        if self.provider == "gemini":
            self.headers.pop("Authorization")
