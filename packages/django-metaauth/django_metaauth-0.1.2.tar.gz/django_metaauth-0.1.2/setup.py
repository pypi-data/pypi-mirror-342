import os
from setuptools import find_packages, setup

# Read the contents of your README file
with open(os.path.join(os.path.dirname(__file__), "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="django-metaauth",
    version="0.1.2",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Django>=3.2",
        "requests>=2.25.0",
    ],
    python_requires=">=3.8",
    author="Tarek Walid",
    author_email="tarek@otomatika.tech",
    description="A Django app for Meta (Facebook) API authentication",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tarikwaleed/django-metaauth",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4.0",
        "Framework :: Django :: 4.1",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)

