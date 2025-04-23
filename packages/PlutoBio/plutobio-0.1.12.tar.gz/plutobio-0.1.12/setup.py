from setuptools import setup, find_packages

setup(
    name="PlutoBio",
    version="0.1.11",
    author="Pluto Team",
    description="A Python SDK for Pluto.bio",
    packages=find_packages(exclude=["*tests*", "scripts", "examples"]),
    install_requires=["requests", "pandas"],
    python_requires=">=3.10, <4",
    keywords=["PlutoBio", "SDK", "API", "Biosciences", "Pluto"],
)
