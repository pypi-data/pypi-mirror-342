from setuptools import setup, find_packages

with open("README.md", mode="r") as file:
    description = file.read()


setup(
    name="pixegami_hello_minhtam",
    version="0.4",
    packages=find_packages(),
    install_requires=[],
    entry_points={"console_scripts": ["pixegami-hello = pixegami_hello:hello"]},
    long_description=description,
    long_description_content_type="text/markdown",
)
