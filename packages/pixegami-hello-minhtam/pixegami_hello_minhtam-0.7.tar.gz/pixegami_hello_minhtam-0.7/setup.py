from setuptools import setup, find_packages

with open("README.md", mode="r") as file:
    description = file.read()

MYLIB_NAME = "pixegami_hello_minhtam"
__version__ = "0.7"


setup(
    name=MYLIB_NAME,
    version=__version__,
    packages=find_packages(),
    install_requires=[],
    long_description=description,
    long_description_content_type="text/markdown",
)
