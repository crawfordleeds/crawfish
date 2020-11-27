import os, io
from setuptools import find_packages, setup, Command

NAME = "django-crawfish"
DESCRIPTION = "pending..."
URL = "https://gitlab.com/crawfordleeds/crawfish"
EMAIL = "crawford@crawfordleeds.com"
AUTHOR = "Crawford Leeds"
REQUIRES_PYTHON = ">=3.6.0"

# Dont' manually change the version here. Use bumpversion instead
VERSION = "0.0.0"

# Required packages for this module
REQUIRED = []

# Optional packages
EXTRAS = {"dev": ["black==20.8b1"]}

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long description
try:
    with io.open(os.path.join(here, "README.md"), encoding="utf-8") as f:
        long_description = f"\n{f.read()}"
except FileNotFoundError:
    long_description = DESCRIPTION

setup(
    name=NAME,
    version=VERSION,  # Don't change this manually, use bumpversion instead,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=["tests", "tests.*"]),
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    install_required=REQUIRED,
    extras_require=EXTRAS,
    include_package_data=True,
    license="MIT",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience : Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
)
