from setuptools import setup, find_packages
import os

# Zorg dat long_description ook werkt als README.md ontbreekt
def read_readme():
    try:
        return open("README.md", encoding="utf-8").read()
    except FileNotFoundError:
        return "🐾 Pupdater: A Django Admin pip manager."

setup(
    name="pupdater",
    version="1.01",
    packages=find_packages(),
    include_package_data=True,
    license="BSD-3-Clause",
    description="🐾 Pupdater: A Django Admin pip manager.",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    author="Wilko Rietveld",
    author_email="wilkorietveld@icloud.com",
    url="https://github.com/WilkoRi/pupdater",
    classifiers=[
        "Framework :: Django",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Environment :: Web Environment",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    install_requires=[
        "django>=3.2",
    ],
    python_requires=">=3.7",
)