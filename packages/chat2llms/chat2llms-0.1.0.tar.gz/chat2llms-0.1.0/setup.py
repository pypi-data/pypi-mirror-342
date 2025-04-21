import os
from setuptools import setup, find_packages

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname), encoding='utf-8').read()

setup(
    name='chat2llms', # 包的名称
    version='0.1.0', # 包的版本号 - 发布新版本时需要更新
    author='scitao', # 作者姓名
    author_email='goldollarch@gmail.com', # 作者邮箱
    description='A framework for comparing responses from different large language models.', # 包的简短描述
    long_description=read('README.md'), # 包的详细描述，从 README.md 读取
    long_description_content_type='text/markdown', # 详细描述的格式
    url='https://github.com/goldollarch/chat2llms', # 项目的主页或其他相关 URL
    packages=find_packages(where='src'), # 查找 src 目录下的所有包
    package_dir={'': 'src'}, # 指定包的根目录在 src 下
    install_requires=[ # 项目运行时依赖的第三方库
        'requests',
        # 根据您的项目实际需要添加其他库
        # 例如，如果您需要特定的 LLM 客户端，可能需要它们的 SDK：
        # 'openai>=1.0.0',
        # 'google-generativeai>=0.5.0',
        # 'deepseek>=1.0.0', # 假设有这样的库
    ],
    classifiers=[ # 包的分类信息，对用户搜索和理解包很有帮助
        'Development Status :: 3 - Alpha', # 开发状态
        'Intended Audience :: Developers', # 目标受众
        'License :: OSI Approved :: MIT License', # 许可证信息 (请根据您的实际许可证修改)
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Text Processing :: Linguistic',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.7', # 要求的最低 Python 版本
    entry_points={ # 定义命令行入口点 (如果您有命令行工具)
        'console_scripts': [
            'chat2llms=chat2llms.cli.cli_click:main' # 示例，如果您的 CLI 入口在这里
        ]
    },
    # 如果您的包包含非代码文件 (如数据文件)，可能需要 package_data 或 include_package_data
    # include_package_data=True,
    # package_data={
    #     'chat2llms': ['data/*.json'], # 示例：包含 chat2llms 包内的 data 目录下的 json 文件
    # },
)