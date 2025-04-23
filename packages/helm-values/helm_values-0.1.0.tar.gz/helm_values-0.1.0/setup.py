from setuptools import setup

setup(
    name="helm-values",  # Must be globally unique on PyPI
    version="0.1.0",
    py_modules=["values"],
    install_requires=["pyyaml"],
    author="Your Name",
    description="Load and merge Helm values files",
    python_requires=">=3.7",
)
