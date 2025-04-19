from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="quickchat_sdk",
    version="0.1.1",
    author="GoofyMooCow",
    description="A simple SDK for interfacing with the Quick Chat chatting platform.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "requests",
        "websocket-client",
    ],
    license="MIT",
    python_requires=">=3.6",
    url='https://github.com/qc1159/quickchat-python-sdk',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
