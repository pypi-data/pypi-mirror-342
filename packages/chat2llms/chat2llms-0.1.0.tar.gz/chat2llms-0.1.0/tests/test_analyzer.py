import pytest

import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__),'..') )

from src.chat2llms.analyzer import AnswerAnalyzer
from src.chat2llms.model_response import OpenAIResponse, GeminiResponse
from src.chat2llms.base_client import BaseClient

def test_semantic_similarity():
    gemini = BaseClient("gemini")
    deepseek = BaseClient("deepseek")
    question = "What is 2 + 2?"
    gemini_response = GeminiResponse(gemini)
    deepseek_response = OpenAIResponse(deepseek)
    analyzer = AnswerAnalyzer(gemini_response, deepseek_response, question)
    semantic_sim = analyzer.compute_semantic_similarity()
    assert semantic_sim >= -1.0  # -1.0 if SpaCy is unavailable
    
    # 使用示例
if __name__ == "__main__":

    # 初始化客户端
    gemini = BaseClient("gemini")
    deepseek = BaseClient("deepseek")

    # 获取响应
    question = "What is 2 + 2?"
    gemini_response = GeminiResponse(gemini)
    deepseek_response = OpenAIResponse(deepseek)
    analyzer = AnswerAnalyzer(gemini_response, deepseek_response, question)
    
    print(f"Similarity: {analyzer.compute_similarity():.2f}")
    print(f"semantic_sim: {analyzer.compute_semantic_similarity():.2f}")
    print(analyzer.highlight_differences())
