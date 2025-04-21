import datetime
from typing import Dict, List

from markdown import markdown

import os
import subprocess
import re

# from difflib import Differ

SAVE_PATH = "docs/refers/Chats"  # 保存目录

class WriteMarkDown:
    def __init__(self, filename: str):

        self._init_md_structure(filename)

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"{SAVE_PATH}/{filename}_{timestamp}.md"
        self.output_path = output_path

    def _init_md_structure(self, filename: str):
        """初始化Markdown文档结构"""
        self.md_content = [
            f"# {filename}\n",
            f"**生成时间**: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n",
        ]

    def add_comparison_table(
        self, metrics: Dict[str, List[float]], model_names: List[str]
    ):
        """
        添加指标对比表格
        :param metrics: 指标字典 {指标名称: [模型1值, 模型2值...]}
        :param model_names: 模型名称列表
        """
        # 生成表头
        header = "| 指标 " + " ".join([f"| {name} " for name in model_names]) + "|"
        separator = "|-----" + " ".join(["|----" for _ in model_names]) + "|"

        # 生成数据行
        rows = []
        for metric, values in metrics.items():
            row = f"| ​**{metric}** " + " ".join([f"| {v} " for v in values]) + "|"
            rows.append(row)

        # 组装表格
        table = [header, separator] + rows
        self.md_content.extend(["\n## 性能对比\n"] + table)

    def add_conclusion(self, conclusions: List[str], highlight: str = None):
        """
        添加分析结论
        :param conclusions: 结论条目列表
        :param highlight: 需要高亮显示的关键结论
        """
        conclusion_section = ["\n## 最终结论\n"]
        for item in conclusions:
            conclusion_section.append(f"- {item}")

        if highlight:
            conclusion_section.append(f"\n**关键结论**: {highlight}")

        self.md_content.extend(conclusion_section)

    def save(self, mode: str = "w"):
        """保存Markdown文件"""
        with open(self.output_path, mode, encoding="utf-8") as f:
            f.write("\n".join(self.md_content))

    def add_section(self, title: str, content: str, level: int = 2):
        """添加自定义章节"""
        prefix = "#" * level
        self.md_content.append(f"\n{prefix} {title}\n{content}")

    def add_plot(self, plot_path: str, caption: str = ""):
        """插入本地图片"""
        self.md_content.append(f"\n![{caption}]({plot_path})")

    def add_diff_analysis(self, text_a: str, text_b: str):
        """文本差异对比"""
        differ = Differ()
        diff = list(differ.compare(text_a.split(), text_b.split()))
        self.add_section("响应差异分析", "```diff\n" + "\n".join(diff) + "\n```")

    def add_response(self, question: str, model: str, answer: str):
        """保存对话记录到Markdown文件"""

        self.add_section("用户提问", question)
        self.add_section(f"{model}模型回复", answer)


def convert_with_pandoc(input_path, output_path):
    try:
        subprocess.run(
            [
                "pandoc",
                "-s",
                input_path,
                "-t",
                "markdown+hard_line_breaks+pipe_tables",
                "-o",
                output_path,
                "--extract-media=./images",
            ],
            check=True,
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"转换错误: {str(e)}")
        return False


def docx_to_sphinx_rst(docx_path, rst_path):
    # Step 1: 使用 Pandoc 转换基础格式
    subprocess.run(
        [
            "pandoc",
            "--extract-media=./_static",
            "--shift-heading-level-by=1",
            "-t",
            "rst+auto_identifiers",
            "-o",
            rst_path,
            docx_path,
        ],
        check=True,
    )

    # Step 2: 后处理优化
    with open(rst_path, "r+", encoding="utf-8") as f:
        content = f.read()

        # 修复表格对齐问题
        content = re.sub(r"(\+-+)+\+", lambda m: m.group().replace("-", "="), content)

        # 转换 Word 注释为 Sphinx 警告框
        content = re.sub(r"^\.\.\scomment::", ".. warning::", content, flags=re.M)

        # 添加 docutils 特殊指令支持
        if ".. code-block::" in content:
            content = ".. highlight:: python\n\n" + content

        f.seek(0)
        f.write(content)
        f.truncate()


def md_to_rst(md_path, rst_path):
    # Step 1: 使用 Pandoc 转换
    subprocess.run(
        [
            "pandoc",
            "-f",
            "markdown+yaml_metadata_block",
            "-t",
            "rst",
            "-o",
            rst_path,
            md_path,
        ],
        check=True,
    )

    # Step 2: 格式修正
    with open(rst_path, "r+", encoding="utf-8") as f:
        content = f.read()

        # 修复代码块语法
        content = re.sub(r"^\.\. code::\s*$", ".. code-block::", content, flags=re.M)

        # 转换表格格式
        content = re.sub(r"(\+-+)+\+", lambda m: m.group().replace("-", "="), content)

        # 修正图片路径
        content = re.sub(r"!$$(.*?)$$$(.*?)$", r".. image:: \2\n   :alt: \1", content)

        f.seek(0)
        f.write(content)
        f.truncate()


# 使用示例

if __name__ == "__main__":
    # # 初始化分析器
    # analyzer = WriteMarkDown("comparison")

    # # 添加性能对比表格
    # metrics = {
    #     "准确率(%)": [92.3, 89.7],
    #     "推理速度(ms)": [15.2, 28.4],
    #     "内存占用(GB)": [1.2, 0.8],
    #     "F1 Score": [0.88, 0.85]
    # }
    # analyzer.add_comparison_table(metrics, ["GPT-4", "DeepSeek-R1"])

    # # 添加结论
    # conclusions = [
    #     "GPT-4在精度指标上全面领先",
    #     "DeepSeek-R1在内存效率方面表现优异",
    #     "两者响应速度均满足实时需求"
    # ]
    # analyzer.add_conclusion(conclusions,
    #                       highlight="推荐高精度场景使用GPT-4，资源受限环境选择DeepSeek-R1")

    # # 添加自定义分析模块
    # analyzer.add_section(
    #     "错误案例分析",
    #     "```python\n# 典型错误示例\nprint(f'1 + 1 = {1+1=}')  # DeepSeek-R1输出格式问题\n```"
    # )

    # text_a = "GPT-4在精度指标上全面领先"
    # text_b = "DeepSeek-R1在内存指标方面表现优异"
    # analyzer.add_diff_analysis(text_a, text_b)

    # caption = "cenjoy"
    # plot_path = "docs/source/_static/cenjoy.png"
    # analyzer.add_plot(plot_path, caption)

    # # 生成最终报告
    # analyzer.save()

    # # 文档转换使用示例
    input_path = "xcenjoy.docx"
    output_path = "xcenjoy.md"
    convert_with_pandoc(input_path, output_path)

    # input_path = "Letter.docx"
    # output_path = "Letter.rst"
    # docx_to_sphinx_rst(input_path, output_path)

    # input_path = "Letter_cn.md"
    # output_path = "Letter_cn.rst"
    # md_to_rst(input_path, output_path)

    # # rstfromdocx
    # os.system("rstfromdocx -lurg 项目概要.docx")
