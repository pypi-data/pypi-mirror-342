from setuptools import setup, find_packages

setup(
    name="FolderSizes",  # Name of your package
    version="0.1.2",  # Version number
    packages=find_packages(),  # Find all packages in the folder
    install_requires=[  # List of dependencies, e.g., click
        "click",
    ],
    entry_points={
        'console_scripts': [
            'foldersizes = foldersizes.filesizze:dirsizes',  # This defines the CLI command
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