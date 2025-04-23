# setup.py

from setuptools import setup, find_packages

setup(
    name="mleasypro",
    version="0.1.0",
    author="Abu Junior Vandi",
    description="A simple machine learning library for researchers",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "scikit-learn",
        "numpy"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
