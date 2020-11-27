from setuptools import find_packages, setup

setup(
    name="django-crawfish",
    packages=find_packages(exclude=["tests", "tests.*"]),
    version="0.0.0",  # Don't change this manually, use bumpversion instead,
    description="",
    author="Crawford Leeds",
    author_email="crawford@crawfordleeds.com",
    classifiers=[
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ]
)