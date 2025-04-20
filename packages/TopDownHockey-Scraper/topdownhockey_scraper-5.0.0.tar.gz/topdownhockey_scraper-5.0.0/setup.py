from distutils.core import setup

from setuptools import find_packages

import os

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="TopDownHockey_Scraper", # Replace with your own username
    version="5.0.0",
    author="Patrick Bacon",
    author_email="patrick.s.bacon@gmail.com",
    description="The TopDownHockey Scraper",
    long_description=long_description,
    license = 'MIT',
    long_description_content_type="text/markdown",
    url="https://github.com/TopDownHockey/TopDownHockey_Scraper",
    project_urls={
        "Bug Tracker": "https://github.com/TopDownHockey/TopDownHockey_Scraper/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=['TopDownHockey_Scraper'],
    python_requires=">=3.6",
    install_requires = [
    'numpy',
    'pandas',
    'bs4',
    'datetime',
    'seaborn',
    'matplotlib',
    'xmltodict',
    'lxml',
    'natsort'
]
)



#if __name__ == '__main__':
 #   setup(**setup_args, install_requires=install_requires)
