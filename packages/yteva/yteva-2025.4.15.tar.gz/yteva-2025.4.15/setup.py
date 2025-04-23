from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="yteva",
    version="2025.4.15",
    packages=find_packages(),
    install_requires=[
        "aiohttp",
        "requests",
        "httpx==0.25.0",
        "beautifulsoup4",
    ],
    author="dev eva",
    author_email="source205eva@gmail.com",
    description="yteva library for downloading audio and videos from YouTube and details about them.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://t.me/yteva_lib",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
