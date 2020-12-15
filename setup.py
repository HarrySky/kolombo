import os
import re

from setuptools import find_packages, setup


def get_version(package):
    """
    Return package version as listed in `__version__` in `__init__.py`.
    """
    with open(os.path.join(package, "__init__.py")) as f:
        return re.search("__version__ = ['\"]([^'\"]+)['\"]", f.read()).group(1)


def get_long_description():
    """
    Return the README.
    """
    with open("README.md", encoding="utf8") as f:
        return f.read()


setup(
    name="kolombo",
    python_requires=">=3.7",
    version=get_version("kolombo"),
    description="Kolombo - easy to manage mail server 💌",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    url="https://github/HarrySky/kolombo",
    license="Apache License 2.0",
    author="Igor Nehoroshev",
    author_email="hi@neigor.me",
    maintainer="Igor Nehoroshev",
    maintainer_email="hi@neigor.me",
    packages=find_packages(),
    # Use MANIFEST.in for data files
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        # Fast async event loop
        "uvloop==0.14.0",
        # For CLI
        "typer==0.3.2",
        "rich==9.3.0",
        # ORM
        "ormar==0.7.1",
        "databases==0.4.1",
        "aiosqlite==0.16.0",
        # Passwords hashing
        "cryptography==3.2.1",
        # For API
        "fastapi==0.62.0",
        "uvicorn==0.12.3",
        # Since 0.12.0 uvicorn does not install httptools (and uvloop)
        "httptools==0.1.*",
    ],
    entry_points={"console_scripts": ["kolombo = kolombo:cli"]},
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Communications :: Email",
        "Typing :: Typed",
    ],
)
