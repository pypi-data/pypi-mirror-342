from setuptools import setup, find_packages

setup(
    name="mcp-dispatch",
    version="0.1.6",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "mcp-core>=0.1.6",
        "pydantic>=1.8.0",
        "requests>=2.25.0"
    ],
    author="baiyx",
    author_email="baiyx@example.com",
    description="MCP dispatch tool for external vehicle dispatching",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/mcp-dispatch",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
) 