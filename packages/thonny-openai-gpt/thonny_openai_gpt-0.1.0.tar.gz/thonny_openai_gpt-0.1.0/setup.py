from setuptools import setup, find_packages

setup(
    name="thonny-openai-gpt",
    version="0.1.0",
    description="OpenAI GPT 助手插件 for Thonny IDE",
    long_description="""
    Thonny IDE 的 OpenAI GPT 助手插件，提供聊天面板和程式碼分析功能。
    可以快速分析程式碼、解答問題，並且提供良好的使用者介面。
    """,
    author="Oliver0804",
    author_email="icetzsr@gmail.com",
    url="https://github.com/Oliver0804/thonny_openai_gpt",
    packages=find_packages("."),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Environment :: Plugins",
        "Intended Audience :: Education",
        "Intended Audience :: Developers",
    ],
    install_requires=["openai>=0.27.0"],
    python_requires=">=3.7",
    platforms=["Windows", "macOS", "Linux"],
    keywords=["thonny", "openai", "gpt", "chatgpt", "plugin", "ide", "education"],
    entry_points={
        "thonny.plugins": [
            "thonny_openai_gpt = thonny_openai_gpt:load_plugin"
        ]
    }
)
