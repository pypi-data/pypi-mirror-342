from setuptools import setup, find_packages
from pathlib import Path

long_description = (Path(__file__).parent / "README.md").read_text(encoding="utf-8")

setup(
    name="craftscript",
    version="1.0.1",
    author="Your Name",
    author_email="your.email@example.com",
    description="Minecraft数据包与KubeJS脚本生成工具",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/craftscript",
    
    # 自动发现所有包（包括子包）
    packages=find_packages(include=["craftscript*"]),
    
    package_data={
        "craftscript": [
            "templates/*.json",
        ]
    },
    python_requires=">=3.8",
    install_requires=[],
    entry_points={"console_scripts": [],},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "Topic :: Games/Entertainment",
        "Topic :: Software Development :: Code Generators"
    ],
    
    # 项目关键词
    keywords=[
        "minecraft",
        "datapack",
        "kubejs",
        "modding"
    ]
)