import setuptools
import os

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

version = {}
with open("src/d4k_ms_service/__info__.py") as fp:
    exec(fp.read(), version)

setuptools.setup(
    name="d4k-ms-service",
    version=version["__package_version__"],
    author="D Iberson-Hurst",
    author_email="",
    description="A python package containing classes for logging errors",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=['pydantic', 'httpx', 'markdown', 'neo4j', 'd4k-ms-base', 'fastapi'],
    packages=setuptools.find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.10",
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
)
