"""Setup configuration for Termis package."""

import setuptools
from termis.utils.constants import VERSION

with open("readme.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="termis",
    version=VERSION,
    author="Smith Gajjar",
    author_email="smith.gajjar@gmail.com",
    description="Snap your setup into place by automating your iTerm layouts and workflows",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/smithg09/termis",
    packages=setuptools.find_namespace_packages(include=["termis", "termis.*"]),
    install_requires=[
        "iterm2>=1.1",
        "PyYAML>=5.3.1",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Topic :: Terminals :: Terminal Emulators/X Terminals",
    ],
    python_requires='>=3.7.0',
    license="MIT",
    entry_points={
        "console_scripts": [
            "termis=termis.termis:main"
        ]
    }
)
