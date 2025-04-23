
from setuptools import setup, find_packages

setup(
        name="api-public-nordicite",
        version="0.0.1",
        author="ymarega",
        author_email="ymarega@nordikeau.com",
        url="https://github.com/Nordikeau-Innovation/Library_Python_Api_Public_Nordicite",
        description="Un package pour extraire les données via api public nordicité",
        packages=find_packages(),
        readme = "README.md",
        install_requires = ["requests>=2.32.3 "],
        python_requires=">=3.9",
        classifiers=[
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        ]
)
