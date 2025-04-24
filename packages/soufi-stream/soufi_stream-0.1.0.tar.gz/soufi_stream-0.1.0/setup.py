from setuptools import setup, find_packages
import os

# Read the contents of the README file
with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

# Package setup
setup(
    name="soufi_stream",
    version="0.1.0",
    author="Soufiyane AIT MOULAY",
    author_email="soufiyane.aitmoulay@gmail.com",
    description="A customizable audio recorder component for Streamlit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/soufiiyane/streamlit-realtime-recorder",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "streamlit_audio_recorder": ["templates/*.html"],
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