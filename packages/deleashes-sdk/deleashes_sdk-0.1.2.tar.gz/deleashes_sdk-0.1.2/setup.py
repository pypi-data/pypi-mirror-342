from setuptools import setup, find_packages
import os

# Чтение README.md для long_description
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="deleashes-sdk",
    version="0.1.2",
    description="SDK for Deleashes feature flag management service",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="exp1rms",
    author_email="imExpelliarmus@yandex.ru",
    url="https://github.com/explrms/DeleashesSDK-python",
    project_urls={
        "Bug Tracker": "https://github.com/explrms/DeleashesSDK-python/issues",
        "Documentation": "https://github.com/explrms/DeleashesSDK-python",
        "Source Code": "https://github.com/explrms/DeleashesSDK-python",
    },
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    install_requires=[
        "requests>=2.25.0",
    ],
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Software Development :: Libraries",
    ],
    keywords="feature flags, feature toggles, a/b testing, release management",
)
