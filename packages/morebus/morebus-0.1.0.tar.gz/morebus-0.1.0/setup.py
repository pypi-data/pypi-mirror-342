from setuptools import setup, find_packages

setup(
    name="morebus",
    version="0.1.0",
    packages=find_packages(),
    author="DevmevLp",
    author_email="d7272581@gmail.com",
    description="Create A MoreBus Server from Python Library",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
