import os
import re
import time
from dataclasses import dataclass
from typing import Dict, List, Optional

import numpy as np
import matplotlib.pyplot as plt

import spacy
import difflib
from difflib import SequenceMatcher

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
# from sentence_transformers import SentenceTransformer, util

from .model_response import ModelResponse, OpenAIResponse, GeminiResponse

##################################

@dataclass
class ModelAnswer:
    """模型响应数据结构"""

    model_name: str
    answer: str  # answer=response.text
    latency: float  # latency=time.time() - start
    tokens: int  # tokens=len(response.text.split())
    error: Optional[str] = None

class AnswerComparator:
    """Class to compare responses from LLMs for the same question.

    Args:
        list[ModelResponse]: The LLM responses.

    """
    
    def __init__(self, responses: List[ModelResponse], question: str = None):

        self.model_names = [r.get_model_name() for r in responses]
        self.responses = responses
        self.question = question

        self.vectorizer = TfidfVectorizer(stop_words="english")

        # # 初始化模型（用于相似度计算）
        # self.sim_model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

    def get_answers(self, question: str) -> List[ModelAnswer]:
        """获取多模型响应"""
        answers = [self.get_model_answer(question, r) for r in self.responses]
        return answers

    def get_model_answer(self, question: str, response: ModelResponse):
        """获取模型响应"""
        model_name = response.get_model_name()
        try:
            start = time.time()
            answer = response.get_response(question)
            return ModelAnswer(
                model_name=model_name,
                answer=answer,
                latency=time.time() - start,
                tokens=len(answer.split()),
            )
        except Exception as e:
            return ModelAnswer(model_name, "", 0, 0, str(e))

    def analyze_answers(self, responses: List[ModelAnswer]) -> Dict:
        """执行对比分析"""
        valid_responses = [r for r in responses if not r.error]

        # 语义相似度分析
        answers = [r.answer for r in valid_responses]
        tfidf = self.vectorizer.fit_transform(answers)
        similarity = cosine_similarity(tfidf)

        # 关键差异提取
        differences = self._extract_differences(answers)

        return {
            "similarity_matrix": similarity,
            "performance": {
                r.model_name: {"latency": r.latency, "tokens": r.tokens}
                for r in valid_responses
            },
            "key_differences": differences,
            "errors": [r for r in responses if r.error],
        }

    def _extract_differences(self, answers: List[str]) -> List[str]:
        """提取关键差异点"""
        noun_phrases = []
        for ans in answers:
            phrases = re.findall(
                r"\b[A-Z][a-z]+\s[A-Z][a-z]+\b|\b\w+ion\b|\b\w+ment\b", ans
            )
            noun_phrases.extend(phrases)

        unique_phrases = list(set(noun_phrases))
        return [
            phrase
            for phrase in unique_phrases
            if sum(1 for ans in answers if phrase in ans) < len(answers)
        ][:5]

    def generate_report(self, analysis: Dict, question: str) -> str:
        """生成分析报告"""
        report = [
            f"# 问题分析报告\n**问题**: {question}\n",
            "## 性能对比",
            *self._format_performance(analysis["performance"]),
            "\n## 语义相似度",
            self._format_matrix(analysis["similarity_matrix"]),
            "\n## 关键差异点",
            *[f"- {diff}" for diff in analysis["key_differences"]],
            "\n## 错误日志",
            *self._format_errors(analysis["errors"]),
        ]
        return "\n".join(report)

    def _format_performance(self, perf: Dict) -> List[str]:
        return [
            f"### {model}\n"
            f"- 响应时间: {data['latency']:.2f}s\n"
            f"- Token使用量: {data['tokens']}"
            for model, data in perf.items()
        ]

    def _format_matrix(self, matrix: np.ndarray) -> str:
        return (
            "```\n" + "\n".join(["\t".join(map(str, row)) for row in matrix]) + "\n```"
        )

    def _format_errors(self, errors: List[ModelAnswer]) -> List[str]:
        return [f"- {err.model_name}: {err.error}" for err in errors if err.error]


# #############################

class AnswerAnalyzer:
    """Class to compare responses from two LLMs for the same prompt.

    Args:
        response1 (ModelResponse): The first LLM response.
        response2 (ModelResponse): The second LLM response.

    Attributes:
        response1 (ModelResponse): The first response object.
        response2 (ModelResponse): The second response object.
        nlp (spacy.language.Language): SpaCy NLP model (optional).
    """

    def __init__(self, response1: ModelResponse, response2: ModelResponse, question: str = None):

        self.question = question
        self.response1 = response1
        self.response2 = response2

        self.nlp: Optional[spacy.language.Language] = None

        try:
            self.nlp = spacy.load("en_core_web_sm")
        except ImportError:
            print("SpaCy not installed or model not found. Install with: pip install spacy && python -m spacy download en_core_web_sm")

    def compute_similarity(self) -> float:
        """Compute similarity between two responses using SequenceMatcher.

        Returns:
            float: Similarity score etween 0.0 and 1.0.
        """
        question = self.question
        text1 = self.response1.get_response(question)
        text2 = self.response2.get_response(question)
        
        matcher = SequenceMatcher(None, text1, text2)
        return matcher.ratio()

    def compute_semantic_similarity(self) -> float:
        """Compute semantic similarity using Spacy.

        Returns:
            float: Semantic similarity score between 0.0 and 1.0, or -1.0 if SpaCy is unavailable.
        """
        if self.nlp is None:
            return -1.0
        
        question = self.question
        text1 = self.response1.get_response(question)
        text2 = self.response2.get_response(question)
        
        doc1 = self.nlp(text1)
        doc2 = self.nlp(text2)
        return doc1.similarity(doc2)

    def highlight_differences(self) -> str:
        """Highlight differences between two responses.

        Returns:
            str: A formatted string showing both responses.
        """

        question = self.question
        text1 = self.response1.get_response(question)
        text2 = self.response2.get_response(question)
        
        return f"Response 1 ({self.response1.get_model_name()}):\n{text1}\n\nResponse 2 ({self.response2.get_model_name()}):\n{text2}"

    def save_comparison_to_csv(self, filename: str):
        import csv
        question = self.question
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Prompt', 'Model1', 'Response1', 'Model2', 'Response2', 'Text Similarity', 'Semantic Similarity'])
            writer.writerow([
                question,
                self.response1.get_model_name(),
                self.response1.get_response(question),
                self.response2.get_model_name(),
                self.response2.get_response(question),
                self.compute_similarity(),
                self.compute_semantic_similarity()
            ])

    def plot_similarity(self):
        similarities = [self.compute_similarity(), self.compute_semantic_similarity()]
        labels = ['Text Similarity', 'Semantic Similarity']
        plt.bar(labels, similarities)
        plt.ylim(0, 1)
        plt.title('Response Similarity Comparison')
        plt.savefig('similarity_plot.png')
        plt.show()

class MultiAnswerAnalyzer:
    """Class to compare responses from LLMs for the same prompt.
    
    Args:
        list[ModelResponse]: The LLM responses.

    Attributes:
        list[ModelResponse]: many LLMs, not only two.
    
    Methods:
        compare_all(): compare responses.
        
    """

    def __init__(self, responses: list[ModelResponse], question: str = None):
        """Initialize MultiAnswerAnalyzer.
        
        Args:
            list[ModelResponse]: The LLM responses.

        Attributes:
            list[ModelResponse]: many LLMs, not only two.
        
        """

        self.question = question
        self.responses = responses
        

    def compare_all(self):
        for i in range(len(self.responses)):
            for j in range(i + 1, len(self.responses)):
                analyzer = AnswerAnalyzer(self.responses[i], self.responses[j], self.question)
                print(f"Comparing {self.responses[i].get_model_name()} vs {self.responses[j].get_model_name()}")
                print(analyzer.highlight_differences())
