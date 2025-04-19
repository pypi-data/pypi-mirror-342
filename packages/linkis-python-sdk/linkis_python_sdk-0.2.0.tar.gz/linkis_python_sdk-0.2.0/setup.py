from setuptools import setup, find_packages
import re

# 从__init__.py中读取版本号
with open("linkis_python_sdk/__init__.py", "r", encoding="utf-8") as f:
    version_match = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', f.read())
    version = version_match.group(1) if version_match else "0.1.0"

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="linkis-python-sdk",
    version=version,
    author="rogerhuang",
    author_email="haungli1279@163.com",
    description="Python SDK for Linkis Service",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/huangli1279/linkis-python-sdk",
    project_urls={
        "Bug Tracker": "https://github.com/huangli1279/linkis-python-sdk/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[
        "requests>=2.25.0",
        "pandas>=1.0.0",
        "redis>=4.0.0",
        "aiohttp>=3.7.0",
    ],
) 