from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
]

setup(
    name='gps2gtfs',
    version='0.0.1',
    description='Extracting travel time information from Bus GPS raw data',
    long_description=long_description,
    url='',
    author='AAIVU',
    author_email='',
    license='MIT',
    classifiers=classifiers,
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=['pandas', 'geopandas']
)
