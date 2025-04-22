
from setuptools import setup, find_packages

setup(
    name="mseep-skydeckai-code",
    version="0.1.34",
    description="This MCP server provides a comprehensive set of tools for AI-driven Development workflows including file operations, code analysis, code linting, multi-language execution, Git operations, web content fetching with HTML-to-markdown conversion, multi-engine web search, code content searching, and system information retrieval.",
    author="mseep",
    author_email="support@skydeck.ai",
    url="",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=['mcp>=1.6.0', 'tree-sitter>=0.24.0', 'tree-sitter-c-sharp>=0.23.1', 'tree-sitter-cpp>=0.23.4', 'tree-sitter-go>=0.23.4', 'tree-sitter-java>=0.23.5', 'tree-sitter-javascript>=0.23.1', 'tree-sitter-kotlin>=1.1.0', 'tree-sitter-php>=0.23.11', 'tree-sitter-python>=0.23.6', 'tree-sitter-ruby>=0.23.1', 'tree-sitter-rust==0.23.2', 'tree-sitter-typescript>=0.23.2', 'GitPython>=3.1.44', 'psutil>=7.0.0', 'mss>=10.0.0', 'pygetwindow>=0.0.9', 'pyobjc-framework-Quartz>=11.0', 'pillow>=11.1.0', 'requests>=2.32.3', 'html2text>=2025.4.15', 'beautifulsoup4>=4.13.3'],
    keywords=["mseep"] + ['mcp', 'development', 'ai', 'aidd', 'code-analysis', 'code'],
)
