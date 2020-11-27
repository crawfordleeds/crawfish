import os
import io
import sys
from setuptools import find_packages, setup, Command
from shutil import rmtree

NAME = "django-crawfish"
DESCRIPTION = "pending..."
URL = "https://gitlab.com/crawfordleeds/crawfish"
EMAIL = "crawford@crawfordleeds.com"
AUTHOR = "Crawford Leeds"
REQUIRES_PYTHON = ">=3.6"

# Dont' manually change the version here. Use bumpversion instead
VERSION = "0.0.0"

# Required packages for this module
REQUIRED = ["Django>=2.2"]

# Optional packages
EXTRAS = {
    "dev": [
        "black==20.8b1",
        "bumpversion==0.6.0",  # This will also install bump2version
    ]
}

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long description
try:
    with io.open(os.path.join(here, "README.md"), encoding="utf-8") as f:
        long_description = f"\n{f.read()}"
except FileNotFoundError:
    long_description = DESCRIPTION


class UploadCommand(Command):
    """Support setup.py upload"""

    description = "Build and publish the package."
    user_options = []

    @staticmethod
    def status(s):
        """Print in bold"""
        print("\033[1m{0}\033[0m".format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status("Removing previous builds...")
            rmtree(os.path.join(here, "dist"))
        except OSError:
            pass

        self.status("Build source and wheel (universal) distribution...")
        os.system("{0} setup.py sdist bdist_wheel --universal".format(sys.executable))

        self.status("Upload the package to PyPI via Twine...")
        os.system("twine upload dist/*")


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
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    include_package_data=True,
    license="MIT",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    cmdclass={"upload": UploadCommand},
)
