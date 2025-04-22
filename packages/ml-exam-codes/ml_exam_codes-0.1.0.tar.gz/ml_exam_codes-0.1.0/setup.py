# setup.py
from setuptools import setup, find_packages

setup(
    name="ml_exam_codes",
    version="0.1.0",
    author="MIHIR",
    author_email="roykumarmihir798@gmail.com",
    description="A library containing ML code snippets for exam preparation",

   
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
