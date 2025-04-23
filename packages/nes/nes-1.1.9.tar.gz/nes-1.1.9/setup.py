#!/usr/bin/env python
from nes import __version__
from setuptools import find_packages
from setuptools import setup


with open("README.md", "r") as f:
    long_description = f.read()


REQUIREMENTS = {
    'install': [
        'geopandas',
        'rtree>=0.9.0',
        'pandas',
        'netcdf4',
        'numpy',
        'pyproj',
        'setuptools',
        'scipy',
        'filelock',
        'eccodes',
        'mpi4py',
        'shapely',
        'python-dateutil'
    ],
    'setup': [
        'setuptools_scm',
    ],
}


setup(
    name='nes',
    license='Apache License 2.0',
    version=__version__,
    description='NES (NetCDF for Earth Science) is a library designed to operate, read, and write NetCDF datasets in a parallel and efficient yet transparent way for the user, using domain decomposition as the parallelization strategy with customizable axis splitting.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Carles Tena Medina, Alba Vilanova Cortezón, Carmen Piñero Megías",
    author_email='carles.tena@bsc.es, alba.vilanova@bsc.es, carmen.pinero@bsc.es',
    url='https://earth.bsc.es/gitlab/es/nes',
    keywords=['Python', 'NetCDF4', 'Grib2', 'Earth'],
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Atmospheric Science",
        "Intended Audience :: Science/Research",
        "Natural Language :: English"
    ],
    package_data={'': [
        'README.md',
        'CHANGELOG.rst',
        'LICENSE',
    ]
    },
    setup_requires=REQUIREMENTS['setup'],
    install_requires=REQUIREMENTS['install'],
    python_requires=">=3.7",

    entry_points={
        "console_scripts": [
            "nes_reorder_longitudes=nes.utilities.reorder_longitudes_cli:reorder_longitudes_cli",
        ]
    }
)