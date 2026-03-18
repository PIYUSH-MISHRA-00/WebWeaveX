from setuptools import setup, find_packages

setup(
    name="webweavex",
    version="0.1.0",
    description="WebWeaveX web crawler and extraction toolkit",
    packages=find_packages(where="core"),
    package_dir={"": "core"},
    install_requires=[
        "beautifulsoup4>=4.12.0",
        "certifi>=2024.0.0",
        "fastapi>=0.110.0",
        "httpx>=0.27.0",
        "pydantic>=2.7.0",
    ],
)
