from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

classifiers = [
    'Development Status :: 3 - Alpha',
    "Intended Audience :: Developers",
    "Intended Audience :: Science/Research",
    "Programming Language :: Python :: 3 :: Only",  # Specify Python 3 only
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Topic :: Scientific/Engineering",
    "Topic :: Software Development",
]

setup(
    name='gps2gtfs',
    packages=find_packages(),
    version='0.0.2-rc3',
    description='A Python package to process raw GPS data of public transit and transform to GTFS format.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/aaivu/gps2gtfs',
    keywords=['GTFS', 'GPS', 'travel time', 'Public Transit', 'Heterogeneous traffic condition', 'ITS'],
    author='AAIVU',
    author_email='helloaaivu@gmail.com',
    license='MIT',
    classifiers=classifiers,
    python_requires=">=3.6",
    install_requires=['pandas', 'geopandas', 'numpy'],
    project_urls={
        "Homepage": "https://github.com/aaivu/gps2gtfs",
        "Source": "https://github.com/aaivu/gps2gtfs",
        "Download": "https://pypi.org/project/gps2gtfs/",
        "Documentation": "https://github.com/aaivu/gps2gtfs/blob/master/README.md",
        "Bug Tracker": "https://github.com/aaivu/gps2gtfs/issues",
    }
)
