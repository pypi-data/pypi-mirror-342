from setuptools import setup, find_namespace_packages
import os

# Read requirements from requirements.txt
with open('requirements.txt') as f:
    requirements = [line.strip() for line in f if not line.startswith('#') and line.strip()]

# Read long description from README
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="buildtogether",
    version="0.2.1",
    description="A collaborative project management tool for AI and software development teams with sprint tracking, task management, and issue resolution features",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Marko Stankovic",
    author_email="m@marko.la",  # Update with your email
    url="https://github.com/markoinla/buildtogether",  # Update with your repo
    packages=find_namespace_packages(include=["app*", "buildtogether*"]),
    include_package_data=True,
    package_data={
        "": ["templates/**/*", "static/**/*"],
    },
    install_requires=requirements,
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "btg=buildtogether.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
) 