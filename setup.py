from setuptools import setup, find_packages

setup(
    name="quant-greeks-cli",
    version="0.1",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    entry_points={
        "console_scripts": ["quant-greeks=quant_greeks.cli:main"]
    },
    install_requires=["scipy"],
)