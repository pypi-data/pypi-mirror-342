from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="agentid",
    version="0.1.5",
    description="连接Au互联网络的库，让你的应用可以连接到Au网络",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="liwenjiang",
    author_email="19169495461@163.com",
    url="https://github.com/yourusername/server-message",
    packages=find_packages(),
    package_data={
        'agentid.db': ['*.db', '*.py'],  # 包含db目录下的所有.db和.py文件
    },
    include_package_data=True,
    install_requires=[],
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Networking",
    ],
    keywords="agentid 2 network",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/server-message/issues",
        "Source": "https://github.com/yourusername/server-message",
    },
)