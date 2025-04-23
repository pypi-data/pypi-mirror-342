from setuptools import setup, find_packages

setup(
    name="enderlit_crypto",
    version="1.0.1",
    author="Enderlit",
    description=" шифратор-дешифратор от Enderlit",
    packages=find_packages(),
    python_requires=">=3.6",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
