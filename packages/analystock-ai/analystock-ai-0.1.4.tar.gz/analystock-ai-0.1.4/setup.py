from setuptools import setup, find_packages
import setuptools


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='analystock-ai',
    version='0.1.4',
    author="Antoine Perrin",
    author_email="antoine.perrin@analystock.ai",
    description='Public client API for Analystock.ai REST API',
    package_dir={'': 'src'},
    packages=find_packages(where="src"),
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=["requests"],
    url="https://github.com/ahgperrin/analystock-api",
    python_requires='>=3.6',
)