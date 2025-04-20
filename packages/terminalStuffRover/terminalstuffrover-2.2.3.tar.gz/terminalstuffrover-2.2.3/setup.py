from setuptools import setup, find_packages

setup(
    name="terminalStuffRover",
    version="2.2.3",
    packages=find_packages(),
    install_requires=[],
    author="Selman Yalçın",
    author_email="selmanyalcin16@gmail.com",
    description="A silly little terminal toy for printing goofy stuff.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "Topic :: Software Development :: Libraries :: Python Modules",
    ],

    keywords=["terminal", "fun", "random", "silly", "print","rover","ascii"],
    python_requires=">=3.6",
)

