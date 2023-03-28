# -*- coding: utf-8 -*-
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="asn1PERser",
    version="0.4.1",
    author="Maciej Pikuła",
    author_email="erupikus@gmail.com",
    description="Parse ASN.1 schemas into Python code and encode/decode them using PER encoder",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/erupikus/asn1PERser",
    keywords = "asn asn1 asn.1 PER decoder encoder",
    packages=setuptools.find_packages(),
    package_data={
        '': ['*.txt']
    },
    install_requires=[
        "pyasn1>=0.4.7",
        "pyparsing>=2.4.7",
        "Jinja2>=2.10.0",
        "future>=0.18.2",
    ],
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
