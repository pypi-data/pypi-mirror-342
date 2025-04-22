from setuptools import setup, find_packages
import os

setup(
    name="clarasr",
    version="0.1.6",
    packages=find_packages(),
    install_requires=[
        "SpeechRecognition>=3.10.0",
        "PyAudio>=0.2.13",
        "numpy>=1.24.0",
        "torch>=2.0.0",
        "requests>=2.31.0",
    ],
    author="Krystof KikoStudios Hrdy",
    author_email="your.email@example.com",
    description="A Python package for speech recognition. ",
    long_description=open("README.md").read() if os.path.exists("README.md") else "",
    long_description_content_type="text/markdown",
    url="https://github.com/kikostudios/clarasr",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)   