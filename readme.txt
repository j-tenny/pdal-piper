Note: updating or modifying this package requires PDAL/PDAL as a submodule in order to read from its documentation.
Use git submodule update --init --recursive to download or update pdal.

Tips on submodules: https://github.com/PDAL/PDAL.git

The main dependency is pdal. Geopandas is an optional dependency required to use the USGS_3dep_Finder class.

## Example

In this example, we will find public lidar data on an online server, download data, clean it, canopy height statistics, and write files locally.

## Find point cloud data
First we need to get some data to work with. I will show one method to pull data from an online server. First, we must define an area of interest using a bounding box `[xmin, ymin, xmax, ymax]`.

In the first cell, I demonstrate how you can extract a bounding box from an interactive map using ipyleaflet (`conda install ipyleaflet`). Alternatively, you can skip this step and input a bounding box manually.


```python
import ipyleaflet

basemap = ipyleaflet.TileLayer(url='https://services.arcgisonline.com/arcgis/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}')
m = ipyleaflet.Map(center=[39, -100], zoom=5, scroll_wheel_zoom=True, basemap=basemap)
m.add(ipyleaflet.WMSLayer(url='https://index.nationalmap.gov:443/arcgis/services/3DEPElevationIndex/MapServer/WmsServer?',
                          layers='23',opacity=.5,name='USGS 3DEP overlay'))
m.add(ipyleaflet.LayersControl())
bbox = None
def handle_draw(target, action, geo_json):
    global bbox
    coords = geo_json['geometry']['coordinates'][0]
    bbox = [coords[0][0], coords[0][1], coords[2][0], coords[2][1]]
draw_control = ipyleaflet.DrawControl(rectangle={'shapeOptions': {'color': '#0000FF'}},
    polyline={}, polygon={}, circle={}, circlemarker={}, marker={}
)
draw_control.on_draw(handle_draw)
m.add_control(draw_control)
m
```

![Interactive map image](example_interactive_map.png)

```python
# Print bounding box selected in interactive map
bbox

# If you want manually input a bounding box, uncomment the line below and edit the values
#bbox = [-120.742342, 39.512467, -120.731442, 39.518311]
```




    [-120.742342, 39.512467, -120.731442, 39.518311]



Next, we can search the USGS 3DEP catalog to find publicly available point clouds that overlap our area of interest using `pdal_piper.USGS_3dep_Finder`. USGS 3DEP is stored in Entwine Point Tile (.ept) format which means we can efficiently download small segments of the point cloud using a url.


```python
import pdal_piper
finder = pdal_piper.USGS_3dep_Finder(bbox,'EPSG:4326')
finder.search_result
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>name</th>
      <th>id</th>
      <th>count</th>
      <th>area</th>
      <th>url</th>
      <th>geometry</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1208</th>
      <td>USGS_LPC_CA_NoCAL_Wildfires_B1_2018</td>
      <td>1208</td>
      <td>86376910091</td>
      <td>608175.903458</td>
      <td>https://s3-us-west-2.amazonaws.com/usgs-lidar-...</td>
      <td>POLYGON ((-120.74234 39.51831, -120.73144 39.5...</td>
    </tr>
  </tbody>
</table>
</div>




```python
# Here we select the URL for the dataset in the first row.
# Alternatively, we could use a loop and download all of the available datasets.
url = finder.search_result.iloc[0,4]
url
```




    'https://s3-us-west-2.amazonaws.com/usgs-lidar-public/USGS_LPC_CA_NoCAL_Wildfires_B1_2018/ept.json'



## Define tile set
To improve computational efficiency and scalability, we can divide our area of interest into a set of tiles using a Tiler object. We specify the total extent of the tileset and the size of each tile. Notice, our extents are defined by geographic coordinates (degrees lat/lon) but we defined the tile size in meters, therefore, we set `convert_units=True`. `get_tiles()` gives us some options to format the tiles. We select the first tile from the upper left corner as a test.


```python
tiler = pdal_piper.Tiler(extents = bbox, tile_size=100, buffer=0, convert_units=True, crs='EPSG:4326')
tile_bounds = tiler.get_tiles(format_as_pdal_str=True,flatten=False)
first_tile_bounds = tile_bounds[0,0]
first_tile_bounds
```




    '([-120.742342, -120.74117760947595], [39.517410999099994, 39.518311], [-9999, 9999])/EPSG:4326'



## Define processing pipeline
We need to create a processing pipeline that defines all actions we want PDAL to execute. Each action in the pipeline is described by a 'stage'. In other workflows, the stages are combined in a json-like object, stored as a text file, and run through PDAL via the command line interface. In contrast, `pdal_piper` makes the experience more Pythonic by providing a Python class with built-in documentation for each stage. We use these classes to define each stage, then combine the stages in a list, then pass the list into a Piper object. The Piper object will format the json text and pass it to PDAL for execution.


```python
# Import the stages
import pdal_piper.stages as pps

# Define processing pipeline for the first tile
stages = [
    # Read point cloud data from online source
    pps.readers_ept(filename=url, bounds=first_tile_bounds),
    # Find and remove outliers
    pps.filters_outlier(method='statistical',mean_k=12,multiplier=2.2),
    pps.filters_range(limits='Classification[0:6]'),
    # Calculate height above ground for veg points
    pps.filters_hag_delaunay(),
    # Save point cloud to disk
    pps.writers_copc(filename='D:/DataWork/ALS_test/my_points.laz', extra_dims='all'),
    # Calculate canopy metrics
    pps.writers_gdal(filename='D:/DataWork/ALS_test/canopy_metrics.tif', resolution=1,
                     dimension='HeightAboveGround', output_type='all', binmode=True)
]

# Create Piper object that handles formatting
piper = pdal_piper.Piper(stages)

# View pipeline in json formatting
piper.to_json()
```




    '[{"type": "readers.ept", "filename": "https://s3-us-west-2.amazonaws.com/usgs-lidar-public/USGS_LPC_CA_NoCAL_Wildfires_B1_2018/ept.json", "bounds": "([-120.742342, -120.74117760947595], [39.517410999099994, 39.518311], [-9999, 9999])/EPSG:4326"}, {"type": "filters.outlier", "method": "statistical", "mean_k": 12, "multiplier": 2.2}, {"type": "filters.range", "limits": "Classification[0:6]"}, {"type": "filters.hag_delaunay"}, {"type": "writers.copc", "filename": "D:/DataWork/ALS_test/my_points.laz", "extra_dims": "all"}, {"type": "writers.gdal", "filename": "D:/DataWork/ALS_test/canopy_metrics.tif", "binmode": true, "resolution": 1, "output_type": "all", "dimension": "HeightAboveGround"}]'




```python
# Execute pipeline for first tile as a test
pipeline = piper.to_pdal_pipeline()
pipeline.execute()
# If the log is empty, that is good. Otherwise, errors will show up in the log.
pipeline.log
```




    ''



Lastly, we can run the pipeline on all files in the tile set. Tile bounds in the reader stage will automatically be assigned from the unique tile bounds. File names in the writer stages will automatically be assigned a unique value by inserting tile indices between the file basename and the file extension. Pipelines are executed in parallel processes.

Note, if `Tiler.buffer>0` and the `filters_crop` stage is used in the pipeline, the filter will automatically use the buffered tile extents in the reader and the unbuffered tile extents in the crop filter. In this special case, the CRS of the Tiler must match the CRS of the point cloud.


```python
# Execute pipeline for all tiles
logs = tiler.execute_piper(piper=piper)
[log for log in logs if log != '']
```




    []



From here, additional analysis can be carried out with your software of choice.
