# pdal-piper

Type stubs and utilities PDAL (Point Data Abstraction Library) and USGS 3DEP.

## Overview

**Type stubs for PDAL**: Adds support for IntelliSense and inline documentation to the `pdal-python` package for better 
IDE support when developing pdal pipelines in PyCharm, VSCode, etc. After installing `pdal-piper`, your IDE should be able
to recognize objects like `pdal.Reader.copc()` and provide descriptions of the input parameters.

**USGS 3DEP utilities**: Search the current USGS 3DEP airborne lidar catalog and find URLs for Entwine Point 
Tiles that overlap a search area.

**Parallel processing**: Utilities for slicing search areas into tiles and processing them in parallel.

*Note, the original version of this package included its own data structures for pipelines and stages. The revised 
version is designed for built-in pdal-python pipeline and stage objects.

## Installation

Basic Install:

```
conda install -c conda-forge pdal pdal-python gdal geopandas 
pip install pdal-piper
```

It is strongly recommended that you make use of Conda’s environment management system and install PDAL in a separate
environment (i.e., not the base environment). Instructions can be found on the Conda website.

Intellisense and inline documentation support is enabled by inserting the file `pipeline.pyi` into the `pdal-python` 
install directory (see "stub files", [PEP 484](https://peps.python.org/pep-0484/)). The `pipeline.pyi` file should be 
generated and inserted automatically when pdal_piper is installed. If needed, you can regenerate and reinsert this file
by running pdal_piper.skeletons.generate_skeletons(). You may also need to restart your IDE and/or regenerate indexes or
clear the local cache.

## Example

