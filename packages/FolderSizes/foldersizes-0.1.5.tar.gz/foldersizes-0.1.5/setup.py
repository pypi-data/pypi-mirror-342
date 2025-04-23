import os
from setuptools import setup, find_packages

def get_version():
    version_file = os.path.join(os.path.dirname(__file__), 'foldersizes', 'filesizze.py')
    with open(version_file) as f:
        for line in f:
            if line.startswith('__version__'):
                delim = '"' if '"' in line else "'"
                return line.split(delim)[1]
    raise RuntimeError("Unable to find version string.")

setup(
    name="FolderSizes",  # Name of your package
    version=get_version(),  # Dynamically fetch version from filesizze.py
    packages=find_packages(),  # Find all packages in the folder
    install_requires=[  # List of dependencies, e.g., click
        "click",
    ],
    entry_points={
        'console_scripts': [
            'foldersizes = foldersizes.filesizze:dirsizes',  # Correct reference to the module
        ],
    },
    license="MIT",  # SPDX license expression
    description="A simple script to list folder sizes",  # Short description
    long_description=open('README.md').read(),  # Read the README file for a detailed description
    long_description_content_type='text/markdown',  # File type for long description
    author="Carter Struck",
    author_email="carterstruckm@gmail.com",  # Replace with your email
    url="https://github.com/cartaR02/FolderSizes",  # URL to the project (typically GitHub)
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Example license
        "Operating System :: OS Independent",
    ],
)