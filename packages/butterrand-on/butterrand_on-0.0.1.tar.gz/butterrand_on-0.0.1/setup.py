from setuptools import setup, find_packages

setup(
    name="butterrand-on",
    version="0.0.1",
    packages=find_packages(),
    author="Bùi Phong Phú",
    author_email="omerasutvailworkit@gmail.com",
    description="Random number generator based on butterfly effect and chaotic maps",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/OmeraGod/butterrand-on",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ],
    python_requires=">=3.6",
)
