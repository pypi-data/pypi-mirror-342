from setuptools import setup, find_packages
from setuptools import setup
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="marketDP",
    version="0.2.0",
    description="simple python code for predicting markets",
    author="navidpgg",
    packages=find_packages(),
    install_requires=[
        'scikit-learn',
        'numpy',
    ],  # List dependencies here
    long_description=long_description,
    long_description_content_type='text/markdown',
)
