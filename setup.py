import os
import re

from setuptools import find_packages, setup

# Only Kolombo CLI requirements are installed by default
with open("requirements.txt") as reqs:
    required = reqs.read().splitlines()


def get_version(package):
    """Return package version as listed in `__version__` in `__init__.py`"""
    with open(os.path.join(package, "__init__.py")) as f:
        return re.search("__version__ = ['\"]([^'\"]+)['\"]", f.read()).group(1)


def get_long_description():
    """Return the README"""
    with open("README.md", encoding="utf8") as f:
        return f.read()


setup(
    name="kolombo",
    python_requires=">=3.8",
    version=get_version("kolombo"),
    description="Kolombo - CLI for easy mail server managing 💌",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/HarrySky/kolombo",
    project_urls={
        "Documentation": "https://docs.neigor.me/kolombo",
        "Changelog": "https://github/HarrySky/kolombo/blob/main/README.md",
        "Source": "https://github.com/HarrySky/kolombo",
        "Tracker": "https://github.com/HarrySky/kolombo/issues",
    },
    license="Apache License 2.0",
    author="Igor Nehoroshev",
    author_email="hi@neigor.me",
    maintainer="Igor Nehoroshev",
    maintainer_email="hi@neigor.me",
    packages=find_packages(exclude=["tests"]),
    # Use MANIFEST.in for data files
    include_package_data=True,
    zip_safe=False,
    install_requires=required,
    entry_points={"console_scripts": ["kolombo = kolombo.bin:kolombo_cli"]},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Communications :: Email",
        "Typing :: Typed",
    ],
)
