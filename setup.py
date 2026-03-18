from pathlib import Path

from setuptools import find_packages, setup


ROOT = Path(__file__).resolve().parent
README = (ROOT / "README.md").read_text(encoding="utf-8")


setup(
  name="webweavex",
  version="0.1.0",
  description="AI-native web crawler with API, CLI, and multi-language SDKs",
  long_description=README,
  long_description_content_type="text/markdown",
  url="https://github.com/PIYUSH-MISHRA-00/WebWeaveX",
  project_urls={
    "Documentation": "https://piyush-mishra-00.github.io/WebWeaveX/",
    "Source": "https://github.com/PIYUSH-MISHRA-00/WebWeaveX",
    "Tracker": "https://github.com/PIYUSH-MISHRA-00/WebWeaveX/issues",
  },
  license="Apache-2.0",
  classifiers=[
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Topic :: Internet :: WWW/HTTP",
    "Topic :: Software Development :: Libraries",
    "Topic :: Text Processing :: Markup :: HTML",
  ],
  keywords=[
    "crawler",
    "scraper",
    "rag",
    "knowledge-graph",
    "sdk",
    "web-crawling",
    "fastapi",
  ],
  package_dir={"": "core"},
  packages=find_packages(where="core"),
  python_requires=">=3.11",
  install_requires=[
    "beautifulsoup4>=4.12.0",
    "certifi>=2024.0.0",
    "fastapi>=0.110.0",
    "httpx>=0.27.0",
    "pydantic>=2.7.0",
    "redis>=5.0.0",
    "uvicorn>=0.29.0",
  ],
  entry_points={
    "console_scripts": [
      "webweavex=webweavex.cli:main",
    ],
  },
  include_package_data=True,
)
