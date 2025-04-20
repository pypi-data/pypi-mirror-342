# setup.py
from setuptools import setup, find_packages

setup(
    name="api_k",  # Name of the package
    version="0.1.0",    # Version of the package
    description="A simple Flask API to manage items",  # Short description
    author="Baskar",  # Your name
    author_email="newtonbaskar@example.com",  # Your email
    packages=find_packages(),  # Automatically find packages
    install_requires=[  # List of dependencies
        "Flask",
    ],
    classifiers=[  # Classifiers to categorize the project
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Python version requirement
)
