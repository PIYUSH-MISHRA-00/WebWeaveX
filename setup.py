from setuptools import setup, find_packages

setup(
    name="webweavex",
    version="0.1.0",
    packages=find_packages(where="core"),
    package_dir={"": "core"},
)
