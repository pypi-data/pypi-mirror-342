from setuptools import setup, find_packages

setup(
    name="searchnarwhal",
    version="0.1.0",
    author="Zohan Haque",
    author_email="zohanuhaque@gmail.com",
    description="a browser engine built in python",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/zohanhaqu/searchnarwhal",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.13',
)
