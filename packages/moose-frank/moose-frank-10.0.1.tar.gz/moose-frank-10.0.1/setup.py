#!/usr/bin/env python

from setuptools import find_packages, setup


version = "10.0.1"

setup(
    name="moose-frank",
    packages=find_packages(),
    version=version,
    description="A Python package packed with tools that are commonly used in "
    "Moose projects.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Sven Groot (Moose / Digital Agency)",
    author_email="sven@wearemoose.com",
    url="https://gitlab.com/mediamoose/moose-frank/tree/v{}".format(version),
    download_url="https://gitlab.com/mediamoose/moose-frank/repository/v{}/archive.tar.gz".format(
        version
    ),
    include_package_data=True,
    install_requires=["django>=4.2.20"],
    extras_require={
        "graphene": [
            "graphene-django>=3.0",
            "graphene-file-upload>=1.3",
            "graphene>=3.2",
        ],
        "gcloud": [
            "django-storages[google]>=1.13.2",
        ],
    },
    license="MIT",
    zip_safe=False,
    keywords=["moose", "frank", "frankenstein"],
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Framework :: Django",
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4.2",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
