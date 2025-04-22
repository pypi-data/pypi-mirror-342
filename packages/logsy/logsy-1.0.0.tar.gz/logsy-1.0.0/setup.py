from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="logsy",
    version="1.0.0",
    description="Emoji-powered terminal logger with box formatting.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Prateek Gupta",
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
