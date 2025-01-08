import warnings
from typing import Sequence, Union, Iterable

import numpy as np

import pdal_piper
from pdal_piper.stages import _GenericStage


class Piper:
    """
    Class to construct pdal pipelines from a series of stages

    Attributes:
        stages (list[dict]): A json-like representation of the stages that make up the pipeline
    """

    def __init__(self,stages:Union[Iterable,None]=None):
        """Initialize instance of Piper with a list of stages (or input None to leave empty)"""

        self.stages = []

        if type(stages) is Piper:
            self.stages = Piper.stages
        elif stages is None:
            pass
        else:
            try:
                self.extend_stages(stages)
            except:
                raise TypeError("Input must be a list of pdal_piper stages or None")

    def __repr__(self):
        """String representation in json format"""
        self.to_json()

    def insert_stage(self,stage:"_GenericStage",index=0):
        """Insert a stage into the stages list at the specified index position"""
        rec = {'type':stage.name}
        for arg in stage.args:
            rec[arg[0]] = arg[1]
        self.stages.insert(index, rec)

    def append_stage(self,stage:"_GenericStage"):
        """Append a stage to the end of the stages list"""
        if isinstance(stage, _GenericStage):
            rec = {'type':stage.name}
            for arg in stage.args:
                rec[arg[0]] = arg[1]
            self.stages.append(rec)
        else:
            raise TypeError("Input must be an instance of a pdal_piper stage")

    def extend_stages(self,stages:Iterable):
        """Extend stages list using a list of additional stages"""
        for stage in stages:
            self.append_stage(stage)

    def pop_stage(self,index):
        """Pop a stage from the stages list based on index position"""
        return self.stages.pop(index)

    def print_stage_types(self):
        """Print stage type from list of stages"""
        stage_types = [stage['type'] for stage in self.stages]
        print(stage_types)

    def to_json(self):
        """Return json string representation of the pipeline"""
        import json
        return json.dumps(self.stages)

    def to_pdal_pipeline(self):
        """Return executable pdal.Pipeline object"""
        import pdal
        return pdal.Pipeline(self.to_json())

class Tiler:
    """
    Class to divide an area into tiles and perform pdal pipelines on each tile
    Attributes:
        extents (tuple[float]): 2D geographic extents of tile set [xmin, ymin, xmax, ymax]
        tile_size (tuple[float]): size of each tile
        buffer (float): pad distance applied to each tile
        crs (str): coordinate reference system in well-known text (wkt) format
        n_tiles_x (int): number of tiles in x direction
        n_tiles_y (int): number of tiles in y direction
        tiles (np.array): array of tile extents indexed by increasing x and decreasing y
    """

    def __init__(self,extents:Sequence[float],
                 tile_size:Union[float,Sequence[float]],
                 buffer:float=0.,
                 crs:str=None,
                 convert_units=False):
        """
        Initialize Tiler instance

        Args:
            extents (Sequence[float]): 2D geographic extents of tile set [xmin, ymin, xmax, ymax]
            tile_size (float | Sequence[float]): size of each tile as square or [x_width, y_width]
            buffer (float): padding distance applied around edge of each tile
            crs (str): coordinate reference system in well-known text (wkt) format
            convert_units (bool): Use convert_units=True if extents use geographic coordinates (degrees lat/lon) but
                                  tile size and buffer use meters. Otherwise, all units must match.
        """

        # Assign tile size and buffer
        if hasattr(tile_size,'__getitem__') and len(tile_size)==2:
            self.tile_size = (float(tile_size[0]), float(tile_size[1]))
        else:
            self.tile_size = (float(tile_size), float(tile_size))
        self.buffer = float(buffer)
        self.crs = crs

        # Assign extents
        if len(extents) == 4:
            self.extents = tuple(extents)
        else:
            raise ValueError('Extents must be sequence of length 4 (xmin, ymin, xmax, ymax)')

        # Convert units of tile size and buffer from meters to degrees lat/lon
        if convert_units:
            import math
            meters_per_degree_lat = 111111
            lat = math.radians(self.extents[1])
            meters_per_degree_lon = abs(111320 * math.cos(lat))

            self.tile_size = (self.tile_size[0] / meters_per_degree_lon,
                              self.tile_size[1] / meters_per_degree_lat)

            # Take larger value of difference in lat vs difference in lon
            self.buffer = max(self.buffer / meters_per_degree_lat, self.buffer / meters_per_degree_lon)
        else:
            if (self.extents[1] < 360) and ((self.tile_size[0] > 5) or (self.buffer>1)):
                import warnings
                warnings.warn(
                    'Use convert_units=True if extents use geographic coordinates but tile size and buffer use meters',
                    UserWarning)

        # Generate tiles
        self.create_tiles()

    def create_tiles(self):
        """
        Create an array of tile extents indexed by increasing x and decreasing y
        """
        import numpy as np

        self.n_tiles_x = int((self.extents[2] - self.extents[0]) // self.tile_size[0])
        self.n_tiles_y = int((self.extents[3] - self.extents[1]) // self.tile_size[1])

        # Compute extents for each row and column
        tile_x_indices = np.arange(self.n_tiles_x)
        tile_y_indices = np.arange(self.n_tiles_y)

        col_min = self.extents[0] + tile_x_indices * self.tile_size[0] - self.buffer
        col_max = self.extents[0] + (tile_x_indices + 1) * self.tile_size[0] + self.buffer
        row_max = self.extents[3] - tile_y_indices * self.tile_size[1] + self.buffer
        row_min = self.extents[3] - (tile_y_indices + 1) * self.tile_size[1] - self.buffer

        # Expand combinations of columns and rows
        cols_min, rows_min = np.meshgrid(col_min, row_min, indexing='ij')
        cols_max, rows_max = np.meshgrid(col_max, row_max, indexing='ij')

        # Combine into one array
        self.tiles = np.stack((cols_min, rows_min, cols_max, rows_max), axis=-1)

    def get_tiles(self,remove_buffer=False,format_as_pdal_str=False,flatten=False):
        """Get array of tile extents with specified formatting

        Args:
            remove_buffer (bool): remove buffer from tiles
            format_as_pdal_str (bool): format tile extents as pdal-compatible string ([xmin,xmax],[ymin,ymax])/{crs_str}
            flatten (bool): if False, return tiles within rows (increasing x) and columns (decreasing y)
        """
        tiles = self.tiles.copy()

        if remove_buffer:
            tiles[:,:,0]+=self.buffer
            tiles[:,:,1]+=self.buffer
            tiles[:,:,2]-=self.buffer
            tiles[:,:,3]-=self.buffer

        if format_as_pdal_str:
            # Get crs string
            if self.crs is None:
                #import warnings
                #warnings.warn('If crs is not provided, ensure extents crs matches data source crs', UserWarning)
                crs_str = ''
            else:
                try:
                    crs_str = '/' + str(self.crs.to_wkt())
                except:
                    crs_str = '/' + str(self.crs)
            tiles_temp =  np.empty((tiles.shape[0],tiles.shape[1]), dtype=object)
            for i in range(self.n_tiles_x):
                for j in range(self.n_tiles_y):
                    tiles_temp[i, j] = format_pdal_bounds_str(tiles[i, j], crs_str)
            tiles = tiles_temp

        if flatten:
            tiles = tiles.ravel()

        return tiles

    def execute_piper(self,piper:Piper,max_workers=None):
        """Applies a Piper object to all tiles, substituting 'bounds' arg in reader and 'filename' arg in writer

        piper (Piper): Piper object containing a reader that supports the 'bounds' arg and a writer that supports the
                       'filename' arg. If the filters.crop stage is included and buffer>0, the unbuffered tile extents
                        will be used as cropping bounds.
        output_path (str): path to output file, e.g. 'output_folder/result.las'. Row and column indexes will be added
                        automatically preceeding the file extension.
        max_workers (int): maximum number of processes to run in parallel. If None, defaults to os.cpu_count() / 2.
                        If memory usage by each process is high and memory is limited, may need to decrease this value.
        """
        import os
        from copy import deepcopy

        # Get variables used to assign filenames
        filename_pad = len(str(max(self.n_tiles_x,self.n_tiles_y)))

        # Look for presence of crop filter and buffer to determine if cropping will occur
        if self.buffer>=0:
            crop = False
            for stage in piper.stages:
                if stage['type'] == 'filters.crop':
                    crop = True
                    break

        # Get tiles
        tiles = self.get_tiles(remove_buffer=False,format_as_pdal_str=True,flatten=False)
        if crop:
            tiles_no_buffer = self.get_tiles(remove_buffer=True,format_as_pdal_str=True,flatten=False)
        else:
            tiles_no_buffer = tiles

        pipes = list()
        # Get pipeline for each tile
        for i in range(self.n_tiles_x):
            for j in range(self.n_tiles_y):
                # Replace values for this tile
                piper_cur = deepcopy(piper)
                for stage in piper_cur.stages:
                    if 'reader' in stage['type']:
                        stage['bounds'] = tiles[i, j]
                    if 'writer' in stage['type']:
                        basename, ext = os.path.splitext(stage['filename'])
                        stage['filename'] = f'{basename}_{i:0{filename_pad}}_{j:0{filename_pad}}{ext}'
                    if stage['type'] == 'filters.crop' and crop:
                        stage['bounds'] = tiles_no_buffer[i, j]
                pipes.append(piper_cur.to_pdal_pipeline())


        return execute_pipelines_parallel(pipes,max_workers=max_workers)


def execute_pipelines_parallel(pipelines:Iterable,max_workers:int=None):
    """Execute a list of pdal pipelines using parallel processes

    Default value for max_workers is `os.cpu_count() / 2`"""

    from concurrent.futures import ProcessPoolExecutor
    import os
    if max_workers is None:
        max_workers = os.cpu_count() / 2
    # Execute pipelines in parallel
    with ProcessPoolExecutor(max_workers=int(max_workers)) as executor:
        log_results = list(executor.map(_execute_pipeline, pipelines))
    return log_results

def _execute_pipeline(pipeline):
    pipeline.execute()
    return pipeline.log


def format_pdal_bounds_str(extents, crs_str):
    """Reformat as ([xmin,xmax],[ymin,ymax])/{crs_str}"""
    return str(tuple([[float(extents[0]), float(extents[2])],
                      [float(extents[1]), float(extents[3])],
                      [-9999,9999]])) + crs_str

class USGS_3dep_Finder:

    def __init__(self,search_area,crs=None,clip_results=True):
        import geopandas
        import shapely
        from shapely.geometry import Polygon,Point
        import importlib.resources as resources

        if (type(search_area) is list) or (type(search_area) is tuple):
            if len(search_area) == 2:
                geom = Point(search_area[0],search_area[1])
            elif len(search_area) == 4:
                geom = Polygon.from_bounds(search_area[0],search_area[1],search_area[2],search_area[3])
            else:
                raise ValueError('Search area must be geopandas objects, shapely geometry, or list or tuple of length 2 (x, y) or 4 (xmin, ymin, xmax, ymax)')
            search_area = geopandas.GeoSeries(geom, crs=crs)

        elif type(search_area) is shapely.Geometry:
            search_area = geopandas.GeoSeries(search_area, crs=crs)

        with resources.open_binary('pdal_piper.data', 'usgs_3dep_resources.geojson') as f:
            usgs = geopandas.read_file(f)

        search_area = search_area.to_crs(usgs.crs)
        self.search_result = usgs[search_area.union_all().intersects(usgs.geometry)]
        self.search_area = search_area

        if clip_results:
            self.search_result = geopandas.clip(self.search_result, self.search_area)

        self.search_result.insert(3, 'area', self.search_result.to_crs('EPSG:8857').area)

    def download_copc(self,filepath,merge=True):
        from pdal_piper import stages
        pipe = Piper()
        for i in range(len(self.search_result)):
            pipe.append_stage(stages.readers_ept(filename=self.search_result['url'].iloc[0],
                                                 polygon = self.search_area.union_all().wkt + '/' + self.search_area.crs.to_wkt()))
        if (len(self.search_result) > 1) and merge:
            pipe.append_stage(stages.filters_merge())

        pipe.append_stage(stages.writers_copc(filename=filepath))
        return pipe.execute()
