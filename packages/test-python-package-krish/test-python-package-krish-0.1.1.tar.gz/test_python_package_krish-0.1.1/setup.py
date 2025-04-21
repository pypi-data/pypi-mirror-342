from setuptools import setup, find_packages

setup(
    name="test-python-package-krish",
    version="0.1.1",
    author="Krishan",
    author_email="krishi87@gmail.com",
    description="A toy package example",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/krisctl/test_python_package",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
