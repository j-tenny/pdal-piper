import warnings
from typing import Sequence, Union, Iterable,Tuple
import numpy as np
import pdal


class Tiler:
    """
    Class to divide an area into tiles and execute pdal pipelines on each tile
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
            tiles_temp =  np.empty((tiles.shape[0],tiles.shape[1]), dtype=object)
            for i in range(self.n_tiles_x):
                for j in range(self.n_tiles_y):
                    tiles_temp[i, j] = format_pdal_bounds_str(tiles[i, j], self.crs)
            tiles = tiles_temp

        if flatten:
            tiles = tiles.ravel()

        return tiles


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

def read_pdal(filepath,bounds=None,calculate_height=True,reproject_to=None)->Tuple['pd.DataFrame',str]:
    """Read a file to a dataframe with pdal. Returns pl.DataFrame and crs

    Args:
        filepath (str): Path to ALS file readable by pdal. Type is inferred by extension.
        bounds (str): Clip extents of the resource in 2 or 3 dimensions, formatted as pdal-compatible string,
            e.g.: ([xmin, xmax], [ymin, ymax], [zmin, zmax]). If omitted, the entire dataset will be selected.
            The bounds can be followed by a slash (‘/’) and a spatial reference specification to apply to the bounds.
        calculate_height (bool): Calculate height above ground for each point using Delauney triangulation
        reproject_to (str): Reproject to this CRS. Use format 'EPSG:5070' or PROJ. If None, no reprojection will be done.
                """
    import pdal
    import pandas as pd

    result=0

    filters = []
    if bounds is not None:
        filters.append(pdal.Reader(filepath, bounds=bounds))
    else:
        filters.append(pdal.Reader(filepath))

    if reproject_to is not None:
        filters.append(pdal.Filter.reprojection(out_srs=reproject_to))

    if calculate_height:
        count = 10
        while result == 0 and count < 100:
            filters_temp = filters + [pdal.Filter.hag_delaunay(count=count)]
            try:
                pipeline = pdal.Pipeline(filters_temp)
                result = pipeline.execute()
            except:
                count *= 2
    else:
        pipeline = pdal.Pipeline(filters)
        pipeline.execute()

    return pd.DataFrame(pipeline.arrays[0]), pipeline.srswkt2



def format_pdal_bounds_str(extents, crs=None):
    """Reformat as ([xmin,xmax],[ymin,ymax])/{crs_str}"""
    if crs is None:
        import warnings
        warnings.warn('If crs is not provided, ensure extents crs matches data source crs')
        crs = ''
    else:
        try:
            crs = '/' + str(crs.to_wkt())
        except:
            crs = '/' + str(crs)
    return str(tuple([[float(extents[0]), float(extents[2])],
                      [float(extents[1]), float(extents[3])],
                      [-9999,9999]])) + crs

class USGS_3dep_Finder:
    """Object for searching the USGS 3DEP catalog

    Attributes:
        search_result (geodataframe): records for point cloud datasets intersecting the search area
    """

    def __init__(self, preload_entwine=False):
        """Initialize USGS_3dep_Finder and downloads current resource geojson"""
        import requests
        import geopandas
        self.search_result = None

        if preload_entwine:
            url = "https://raw.githubusercontent.com/hobuinc/usgs-lidar/master/boundaries/resources.geojson"
            response = requests.get(url)
            response.raise_for_status()  # Raises an exception for HTTP errors
            self.usgs = geopandas.read_file(response.text)

    def search_3dep(self,search_area:Union[Sequence[float],'geoseries','geometry'],crs=None, search_type='entwine', n_threads=None):
        """Search for USGS 3DEP resources that overlap with a search area

        Args:

            search_area: bounding box [xmin,ymin,xmax,ymax], point coordinate [x,y], geoseries, or shapely geometry

            crs: proj-compatible coordinate reference system associated with search area

            search_type: If 'entwine', searches https://usgs.entwine.io and returns a record for each entwine resource
                intersecting the search area. If 'science-base', searches https://www.sciencebase.gov/catalog/item/4f70ab64e4b058caae3f8def
                and returns a record for each .laz tile intersecting the search area.

            n_threads: Number of threads to use for parallel processing of science-base requests. Default None results
                in max_workers = min(32, os.cpu_count() + 4).
        """
        import geopandas
        import pandas as pd
        import shapely
        from shapely.geometry import Polygon,Point
        from shapely.geometry.base import BaseGeometry
        import requests
        import time

        # Interpret search area as a geometry
        if hasattr(search_area,'geometry'):
            geom = search_area.geometry
        elif hasattr(search_area, "__geo_interface__"):
            geom = search_area
        elif hasattr(search_area,'__getitem__'):
            if len(search_area) == 2:
                geom = Point(search_area[0],search_area[1])
            elif len(search_area) == 4:
                geom = Polygon.from_bounds(search_area[0],search_area[1],search_area[2],search_area[3])
        else:
            raise ValueError('Search area must be geoseries, shapely geometry, or sequence of length 2 (x, y) or 4 (xmin, ymin, xmax, ymax)')

        # Create geoseries from geom and crs
        if crs is None and hasattr(search_area,'crs'):
            crs = search_area.crs
        search_area = geopandas.GeoSeries(geom, crs=crs)

        # Perform search of entwine resources
        if search_type == 'entwine':
            return self._search_entwine(search_area)

        # Perform search of science-base resources
        elif search_type == 'science-base':
            return self._search_science_base(search_area, n_threads=n_threads)
        else:
            raise ValueError("search_type must be 'entwine' or 'science-base'")

    def _search_entwine(self, search_area):
        import geopandas

        if hasattr(self,'usgs') is False:
            self.usgs = geopandas.read_file(
                "https://raw.githubusercontent.com/hobuinc/usgs-lidar/master/boundaries/resources.geojson"
            )

        self.search_area = search_area.to_crs(self.usgs.crs)
        search_area_proj = search_area.to_crs('EPSG:8857')

        self.search_result = self.usgs[self.search_area.union_all().intersects(self.usgs.geometry)]
        search_result_proj = self.search_result.to_crs('EPSG:8857')
        self.search_result.insert(2, 'pts_per_m2', search_result_proj['count'] / search_result_proj.area)
        self.search_result.insert(4, 'total_area_ha', search_result_proj.area / 10000)

        if search_area_proj.area.sum() > 1:
            self.search_result = geopandas.clip(self.search_result, self.search_area)
            coverage = self.search_result.to_crs('EPSG:8857').area / search_area_proj.area.sum() * 100
            self.search_result.insert(2, 'pct_coverage', coverage)
        else:
            self.search_result.insert(2, 'pct_coverage', 100)

        self.search_result = self.search_result.sort_values(by=['pct_coverage', 'pts_per_m2'], ascending=False)

        return self.search_result

    def _search_science_base(self, search_area, n_threads=None):
        import geopandas
        import pandas as pd
        import time
        import requests
        from requests.adapters import HTTPAdapter
        from urllib3.util.retry import Retry
        if n_threads is not None and n_threads != 1:
            from concurrent.futures import ThreadPoolExecutor, as_completed

        self.search_area = search_area.to_crs(4326)
        spatial_query = f'spatialQuery={self.search_area.geometry.iloc[0].wkt}'

        # Define resource url and search parameters
        BASE_URL = "https://www.sciencebase.gov/catalog/items"
        PARENT_ID = "4f70ab64e4b058caae3f8def"

        params = {
            "parentId": PARENT_ID,
            "format": "json",
            "filter": spatial_query,
            "max": 500,
            "offset": 0
        }

        # Dynamically size the connection pool to match or exceed threads
        pool_size = max(50, n_threads) if isinstance(n_threads, int) else 50

        session = requests.Session()
        # Added 520-525 to handle WAF/Cloudflare intermittent drops
        retries = Retry(
            total=5,
            backoff_factor=1.5,  # Slightly increased backoff for government APIs
            status_forcelist=[429, 500, 502, 503, 504, 520, 521, 522, 523, 524, 525],
            allowed_methods=["HEAD", "GET", "OPTIONS"]  # Explicitly allow retrying GETs
        )
        adapter = HTTPAdapter(max_retries=retries, pool_connections=pool_size, pool_maxsize=pool_size)
        session.mount("https://", adapter)
        session.mount("http://", adapter)

        n_failures = 0
        recs_all = []

        while True:
            try:
                resp = session.get(BASE_URL, params=params, timeout=30)  # 900s is too long; 30s is safer
                resp.raise_for_status()
                data = resp.json()

                items = data.get("items", [])
                if not items:
                    break

                ids = [item['id'] for item in items]

                if n_threads in (None, 0, 1):
                    for item_id in ids:
                        recs_all.append(self._summarize_science_base_item(item_id, session))
                else:
                    with ThreadPoolExecutor(max_workers=n_threads) as executor:
                        futures = [executor.submit(self._summarize_science_base_item, i, session) for i in ids]
                        recs_all.extend([f.result() for f in as_completed(futures)])

                if len(items) < params["max"]:
                    break
                params["offset"] += params["max"]

            except Exception as e:
                print(f'Failed to retrieve page starting at {params["offset"]}: {e}')
                if n_failures < 10:  # Reduced from 60 to prevent endless hanging
                    print('Trying again in 10s...')
                    time.sleep(10)
                    n_failures += 1
                else:
                    print('Giving up after 10 pagination tries')
                    break

        self.id_failed = [item for item in recs_all if isinstance(item, str)]
        recs_all = [item for item in recs_all if isinstance(item, dict)]

        if not recs_all:
            print("Warning: No records successfully retrieved.")
            return None

        recs_all = pd.DataFrame(recs_all).drop_duplicates()
        geom = geopandas.points_from_xy(recs_all['lon'], recs_all['lat'], crs=4326)
        self.search_result = geopandas.GeoDataFrame(recs_all, geometry=geom, crs=4326)

        return self.search_result

    def _summarize_science_base_item(self, item_id, session=None):
        """Summarize metadata for a science-base lidar tile item. Returns dict if successful, else returns the id."""
        import requests

        item_url = f"https://www.sciencebase.gov/catalog/item/{item_id}?format=json"

        try:
            # Rely on the session's urllib3 Retry logic rather than a custom while-loop
            if session is None:
                resp = requests.get(item_url, timeout=30)
            else:
                resp = session.get(item_url, timeout=30)

            resp.raise_for_status()
            item_json = resp.json()

            # Safely extract bounding box
            bb = item_json.get('spatial', {}).get('boundingBox', {})
            if not bb:
                raise ValueError("Missing bounding box data")

            x = (bb.get('minX', 0) + bb.get('maxX', 0)) / 2
            y = (bb.get('minY', 0) + bb.get('maxY', 0)) / 2

            # Safely extract dates using next() with a default fallback
            dates = item_json.get('dates', [])
            date_start = next((d.get('dateString') for d in dates if d.get('type') == 'Start'), None)
            date_end = next((d.get('dateString') for d in dates if d.get('type') == 'End'), None)

            # Safely extract download URL
            links = item_json.get('webLinks', [])
            url = next((link.get('uri') for link in links if link.get('type') == 'download'), None)

            name = item_json.get('title', '')
            project_tile = name.replace('USGS Lidar Point Cloud ', '').split()

            tile = project_tile[-1] if project_tile else ''
            project = ' '.join(project_tile[:-1]) if len(project_tile) > 1 else ''

            return {
                'lon': x,
                'lat': y,
                'project': project,
                'tile': tile,
                'date_start': date_start,
                'date_end': date_end,
                'url': url
            }

        except Exception as e:
            # We only land here if network retries totally failed OR parsing failed
            print(f"Failed to retrieve/parse metadata for {item_url} \n {e}")
            return item_id


    def select_url(self,index):
        """Select url from self.search_result using row index"""
        return self.search_result['url'].iloc[index]



