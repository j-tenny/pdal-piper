from setuptools import setup

setup(
    name='pdal-piper',
    version='0.1.1',
    packages=['pdal_piper'],
    package_data={'pdal_piper': ['data/usgs_3dep_resources.geojson']},
    include_package_data=True,
    url='',
    license='',
    author='Johnathan Tenny (j-tenny)',
    author_email='',
    description='Pythonic interface and utilities for PDAL (Point Data Abstraction Library) and USGS 3DEP lidar download.')
