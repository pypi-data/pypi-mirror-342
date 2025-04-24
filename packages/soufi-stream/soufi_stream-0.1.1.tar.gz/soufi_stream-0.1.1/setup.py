from setuptools import setup, find_packages
import os

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="soufi-stream", 
    version="0.1.1",
    author="Soufiyane AIT MOULAY",
    author_email="soufiyane.aitmoulay@gmail.com",
    description="A customizable audio recorder component for Streamlit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/soufiiyane/streamlit-realtime-recorder",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "soufi_stream": ["templates/*.html"],  # Changed to match package name
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
    install_requires=[
        "streamlit>=1.0.0",
    ],
)