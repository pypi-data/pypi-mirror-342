from setuptools import setup, find_packages

setup(
    name="dynarr",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[],
    author="Ryan Flores",
    author_email="ryanmigul@gmail.com",
    description="A dynamic way of storing things, what, I don't know",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.7",
)
