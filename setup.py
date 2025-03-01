from setuptools import setup

setup(
    name='pdal-piper',
    version='0.1.3',
    packages=['pdal_piper'],
    package_data={'pdal_piper': ['data/usgs_3dep_resources.geojson']},
    include_package_data=True,
    url='https://github.com/j-tenny/pdal-piper',
    license='',
    author='Johnathan Tenny (j-tenny)',
    author_email='',
    description='Python interface and utilities for PDAL (Point Data Abstraction Library) and USGS 3DEP lidar download.')
