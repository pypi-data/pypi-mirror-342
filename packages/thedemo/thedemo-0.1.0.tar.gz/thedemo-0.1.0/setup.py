from setuptools import setup, find_packages

setup(
    name="thedemo",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["click"],
    entry_points={
        "console_scripts": [
            "thedemo = thedemo.cli:main",
        ],
    },
    author="Your Name",
    description="A demo CLI tool for PyPI testing",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    python_requires=">=3.6",
)
