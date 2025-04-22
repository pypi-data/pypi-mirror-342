from setuptools import setup, find_packages

setup(
    name="euriai",
    version="0.2.1",
    description="Python client for EURI LLM API (euron.one) with CLI and interactive wizard",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="euron.one",
    author_email="sudhanshu@euron.one",
    packages=find_packages(),
    install_requires=[
        "requests"
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "euriai=euriai.cli:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
    ],
    license="MIT",
)
