from setuptools import setup, find_packages

setup(
    name="pankajsimplecalc",                  # Choose a unique name
    version="0.2.0",
    packages=find_packages(),
    install_requires=[],                       # List dependencies if any
    author="Pankaj",
    author_email="pankajshk123@gmail.com",
    description="A simple calculator package for basic arithmetic",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    #url="https://github.com/yourusername/simple-calculator",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
