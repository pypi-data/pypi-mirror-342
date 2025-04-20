#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from setuptools import setup, find_packages

# Definisci le dipendenze condizionali
requires = [
    "psutil>=5.9.0",
]

# Aggiungi wmi come dipendenza solo per Windows
if sys.platform.startswith('win'):
    requires.append("wmi>=1.5.1")

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="devid-pyfetch",  # Cambiato da "pyfetch" a "devid-pyfetch"
    version="0.1.0",
    author="PyFetch Team",
    author_email="devidrru@gmail.com",  # Sostituisci con un email reale
    description="Un fork di Neofetch scritto in Python che mostra informazioni di sistema con ASCII art",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dddevid/pyfetch",  # Sostituisci con l'URL reale del repository
    packages=find_packages(),
    py_modules=["pyfetch", "ascii_art", "config", "system_info"],
    install_requires=requires,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Topic :: System :: Monitoring",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "pyfetch=pyfetch:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)