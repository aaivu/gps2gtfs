from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

classifiers = [
    'Development Status :: 3 - Alpha',
    "Programming Language :: Python :: 3",
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
]

setup(
    name='gps2gtfs',
    packages=['gps2gtfs'],
    version='0.0.1',
    description='Extracting travel time information from Bus GPS raw data',
    long_description=long_description,
    url='https://github.com/aaivu/gps2gtfs',
    keywords=['gtfs', 'GPS', 'travel time', 'bus trave time'],  # Keywords that define your package best
    author='AAIVU',
    author_email='helloaaivu@gmail.com',
    license='MIT',
    classifiers=classifiers,
    package_dir={"": "src"},
    python_requires=">=3.6",
    install_requires=['pandas', 'geopandas', 'numpy']
)
