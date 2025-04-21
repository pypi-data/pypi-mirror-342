from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="yt-cookie-manager",
    version="0.1.0",
    author="kidoocoder",
    author_email="your.email@example.com",
    description="YouTube Cookie Manager for Telegram Music Bots",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kidoocoder/ytdlp",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
)