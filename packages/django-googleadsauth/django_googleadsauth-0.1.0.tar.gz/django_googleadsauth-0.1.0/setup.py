#!/usr/bin/env python
import os
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="django-googleadsauth",
    version="0.1.0",
    author="Tarek Walid",
    author_email="tarek@otomatika.tech",
    description="Django app for Google Ads API authentication and basic functionality",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tarikwaleed/django-googleadsauth",
    project_urls={
        "Bug Tracker": "https://github.com/tarikwaleed/django-googleadsauth/issues",
        "Documentation": "https://github.com/tarikwaleed/django-googleadsauth#readme",
        "Source Code": "https://github.com/tarikwaleed/django-googleadsauth",
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4.0",
        "Framework :: Django :: 4.1",
        "Framework :: Django :: 4.2",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    package_dir={"": "."},
    packages=find_packages(where="."),
    include_package_data=True,
    python_requires=">=3.7",
    install_requires=[
        "Django>=3.2",
        "google-ads>=18.0.0",
        "google-auth-oauthlib>=0.4.6",
        "google-api-python-client>=2.0.0",
        "google-auth>=2.0.0",
        "djangorestframework>=3.12.0",
        "requests>=2.25.0",
    ],
    keywords=[
        "django",
        "google ads",
        "google api",
        "authentication",
        "oauth2",
        "campaign management",
    ],
    zip_safe=False,
)
