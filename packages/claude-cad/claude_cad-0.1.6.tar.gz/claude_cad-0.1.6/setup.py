from setuptools import setup, find_packages

setup(
    name="claude_cad",
    version="0.1.6",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "cadquery>=2.0.0",
        "mcp>=1.6.0",
    ],
    entry_points={
        "console_scripts": [
            "claude_cad=claude_cad.server:main",
            "claude-cad=claude_cad.server:main",
        ],
    },
    author="Bronson Dunbar",
    author_email="bronson@example.com",
    description="An MCP plugin for creating 3D models with Claude AI using CadQuery",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/bronson/claude_cad",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.9",
    project_urls={
        "Bug Tracker": "https://github.com/bronson/claude_cad/issues",
        "Documentation": "https://github.com/bronson/claude_cad#readme",
        "Source Code": "https://github.com/bronson/claude_cad",
    },
)
