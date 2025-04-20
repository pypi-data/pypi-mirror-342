import codecs
import os
from setuptools import setup, find_packages

# 安全读取README.md（处理编码和路径问题）
here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="fei_cpp_library",
    version="0.1.5",
    author="Fei Dong",  # 添加作者信息
    author_email="x24181242@student.ncirl.ie",  # 添加作者邮箱
    description="A C++/Python hybrid library",  # 添加简短描述
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[ 
        "requests>=2.25.1",  # 建议添加版本约束
        "boto3>=1.16.0"
    ],
    classifiers=[
        "Development Status :: 4 - Beta",  # 添加开发阶段
        "Intended Audience :: Developers",  # 添加目标用户
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
    ],
    python_requires=">=3.6",
    url="https://github.com/x24181242/CloudTaskManager",  # 添加项目URL
    keywords=["cpp", "python", "hybrid"],  # 添加关键词
    project_urls={  # 添加额外URL
        "Documentation": "https://github.com/x24181242/CloudTaskManager",
        "Source": "https://github.com/x24181242/CloudTaskManager",
    },
)