from setuptools import setup, find_packages

setup(
    name="quant-greeks-cli",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.21",
        "scipy>=1.7"
    ],
)