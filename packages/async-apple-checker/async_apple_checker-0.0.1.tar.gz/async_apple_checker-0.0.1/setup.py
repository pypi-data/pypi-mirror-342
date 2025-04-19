from setuptools import setup, find_packages

setup(
    name="async-apple-checker",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[
        "async-lru>=2.0.5",
        "aiohttp>=3.11.16",
        "cryptography>=44.0.2"
    ],
    description="A package to check apple related certificates (p12 & mobileprovision) asyncronously.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="jainamoswal",
    author_email="me@jainam.me",
    url="https://github.com/jainamoswal/asycn-apple-checker",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
)