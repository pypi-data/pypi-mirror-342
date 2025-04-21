from setuptools import setup, find_namespace_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="shangshanAI",
    version="0.1.19",
    author="tonysu",
    author_email="suguta55@gmail.com",
    description="一个用于从GitLab下载和处理模型的Python SDK",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/你的用户名/shangshanAI",
    packages=find_namespace_packages(include=['shangshanAI*']),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "requests>=2.25.0",
        "tqdm>=4.65.0",  # 进度条支持
        "PyJWT>=2.0.0",  # JWT 支持
        "httpx>=0.24.0",  # HTTP 客户端
        "typing-extensions>=4.0.0",  # 类型提示扩展
        "pydantic>=1.10.0",  # 数据验证
        "aiohttp>=3.8.0",  # 异步 HTTP 客户端
        "anyio>=3.0.0",  # 异步 IO 支持
        "cachetools>=5.2.0",
    ],
    project_urls={
        "Bug Tracker": "https://github.com/你的用户名/shangshanAI/issues",
        "Documentation": "https://github.com/你的用户名/shangshanAI#readme",
        "Source Code": "https://github.com/你的用户名/shangshanAI",
    },
    entry_points={"console_scripts": ["shangshanAI=shangshanAI.modelscope.cli.cli:run_cmd"]},
)