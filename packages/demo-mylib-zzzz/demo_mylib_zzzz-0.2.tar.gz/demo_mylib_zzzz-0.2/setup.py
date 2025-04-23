from setuptools import setup, find_packages

with open("README.md", mode="r") as file:
    description = file.read()

MYLIB_NAME = "demo_mylib_zzzz"
__version__ = "0.2"


setup(
    name=MYLIB_NAME,
    version=__version__,
    packages=find_packages(),
    install_requires=[],
    long_description=description,
    long_description_content_type="text/markdown",
)
