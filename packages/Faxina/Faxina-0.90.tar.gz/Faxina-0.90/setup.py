from setuptools import setup, find_packages


setup(
    name="Faxina",
    version="0.90",
    author="Vladik",
    author_email="vladhruzd25@gmail.com",
    description="Faxina - engine 3d for python 2.4. It Faxina Version not install on python x.3 and higher",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2.4",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires=">=2.4, <3"
)