from setuptools import setup, find_packages

setup(
    name="intern_package",  
    version="0.1",
    description="A package for numerical operations using NumPy",
    author="ARUN",
    author_email="ARUN@gmail.com",
    packages=find_packages(), 
    install_requires=[
        "numpy>=1.21.0",  
    ],
)
