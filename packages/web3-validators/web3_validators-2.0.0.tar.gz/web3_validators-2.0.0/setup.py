from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="web3_validators", 
    version="2.0.0",         
    author="zeus",     
    author_email="zeus@protonmail.com", 
    description="A utility package for transferring crypto assets across different blockchains", 
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zeus",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent", 
    ],
    python_requires=">=3.7",
    install_requires=[
        "web3>=6.0.0",
        "solana>=0.29.0",
        "solders>=0.16.0",
    ],
)