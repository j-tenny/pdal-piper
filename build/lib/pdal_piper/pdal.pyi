class Reader:
    def arrow(self,filename = None, count = 18446744073709551615, override_srs = None, default_srs = None, metadata = 'false', geoarrow_dimension_name = 'xyz', format = '', option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """Arrow Reader

        Options:
            filename: Name of file to read
            count: Maximum number of points read
            override_srs: Spatial reference to apply to data
            default_srs: Spatial reference to apply to data if one cannot be inferred
            metadata: 
            geoarrow_dimension_name: 
            format: 
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def bpf(self,filename = None, count = 18446744073709551615, override_srs = None, default_srs = None, fix_dims = 'true', option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """"Binary Point Format" (BPF) reader support. BPF is a simple 
DoD and research format that is used by some sensor and 
processing chains.

        Options:
            filename: Name of file to read
            count: Maximum number of points read
            override_srs: Spatial reference to apply to data
            default_srs: Spatial reference to apply to data if one cannot be inferred
            fix_dims: Make invalid dimension names valid by changing invalid characters to '_'
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def copc(self,filename = None, count = 18446744073709551615, override_srs = None, default_srs = None, bounds = None, requests = 2, resolution = None, polygon = None, header = None, query = None, ogr = None, fix_dims = 'true', vlr = 'true', keep_alive = 10, srs_vlr_order = None, nosrs = 'false', option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """COPC Reader

        Options:
            filename: Name of file to read
            count: Maximum number of points read
            override_srs: Spatial reference to apply to data
            default_srs: Spatial reference to apply to data if one cannot be inferred
            bounds: Retangular clip region
            requests: Number of worker threads
            resolution: Resolution limit
            polygon: Bounding polygon(s) to crop requests
            header: Header fields to forward with HTTP requests
            query: Query parameters to forward with HTTP requests
            ogr: OGR filter geometries
            fix_dims: Make invalid dimension names valid by changing invalid characters to '_'
            vlr: Read LAS VLRs and add to metadata.
            keep_alive: Number of chunks to keep alive in memory when working
            srs_vlr_order: Preference order to read SRS VLRs (list of 'wkt1', 'wkt2' or 'projjson'
            nosrs: Skip reading/processing file SRS
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def draco(self,filename = None, count = 18446744073709551615, override_srs = None, default_srs = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """Read data from a Draco array.

        Options:
            filename: Name of file to read
            count: Maximum number of points read
            override_srs: Spatial reference to apply to data
            default_srs: Spatial reference to apply to data if one cannot be inferred
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def e57(self,filename = None, count = 18446744073709551615, override_srs = None, default_srs = None, extra_dims = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """Reader for E57 files

        Options:
            filename: Name of file to read
            count: Maximum number of points read
            override_srs: Spatial reference to apply to data
            default_srs: Spatial reference to apply to data if one cannot be inferred
            extra_dims: Extra dimensions to read from E57 point cloud.
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def ept(self,filename = None, count = 18446744073709551615, override_srs = None, default_srs = None, bounds = None, origin = None, requests = 15, resolution = None, addons = None, polygon = None, header = None, query = None, ogr = None, ignore_unreadable = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """EPT Reader

        Options:
            filename: Name of file to read
            count: Maximum number of points read
            override_srs: Spatial reference to apply to data
            default_srs: Spatial reference to apply to data if one cannot be inferred
            bounds: Bounds to fetch
            origin: Origin of source file to fetch
            requests: Number of worker threads
            resolution: Resolution limit
            addons: Mapping of addon dimensions to their output directory
            polygon: Bounding polygon(s) to crop requests
            header: Header fields to forward with HTTP requests
            query: Query parameters to forward with HTTP requests
            ogr: OGR filter geometries
            ignore_unreadable: Ignore errors for missing point data nodes
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def faux(self,filename = None, count = 18446744073709551615, override_srs = None, default_srs = None, bounds = '([0, 1], [0, 1], [0, 1])', mean_x = None, mean_y = None, mean_z = None, stdev_x = 1, stdev_y = 1, stdev_z = 1, mode = None, number_of_returns = None, seed = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """Faux Reader

        Options:
            filename: Name of file to read
            count: Maximum number of points read
            override_srs: Spatial reference to apply to data
            default_srs: Spatial reference to apply to data if one cannot be inferred
            bounds: X/Y/Z limits
            mean_x: X mean
            mean_y: Y mean
            mean_z: Z mean
            stdev_x: X standard deviation
            stdev_y: Y standard deviation
            stdev_z: Z standard deviation
            mode: Point creation mode
            number_of_returns: Max number of returns
            seed: Random generator seed
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def fbi(self,filename = None, count = 18446744073709551615, override_srs = None, default_srs = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """Fbi Reader

        Options:
            filename: Name of file to read
            count: Maximum number of points read
            override_srs: Spatial reference to apply to data
            default_srs: Spatial reference to apply to data if one cannot be inferred
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def gdal(self,filename = None, count = 18446744073709551615, override_srs = None, default_srs = None, header = None, memorycopy = 'false', gdalopts = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """Read GDAL rasters as point clouds.

        Options:
            filename: Name of file to read
            count: Maximum number of points read
            override_srs: Spatial reference to apply to data
            default_srs: Spatial reference to apply to data if one cannot be inferred
            header: A comma-separated list of dimension IDs to map raster bands to dimension id
            memorycopy: Load the given raster file entirely to memory
            gdalopts: GDAL driver options (name=value,name=value...)
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def hdf(self,filename = None, count = 18446744073709551615, override_srs = None, default_srs = None, dimensions = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """HDF Reader

        Options:
            filename: Name of file to read
            count: Maximum number of points read
            override_srs: Spatial reference to apply to data
            default_srs: Spatial reference to apply to data if one cannot be inferred
            dimensions: Map of HDF path to PDAL dimension
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def i3s(self,filename = None, count = 18446744073709551615, override_srs = None, default_srs = None, obb = None, threads = 4, dimensions = None, min_density = '-1', max_density = '-1', option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """I3S Reader

        Options:
            filename: Name of file to read
            count: Maximum number of points read
            override_srs: Spatial reference to apply to data
            default_srs: Spatial reference to apply to data if one cannot be inferred
            obb: Oriented bounding box of clip region.
            threads: Number of threads to be used.
            dimensions: Dimensions to be used in pulls
            min_density: Minimum point density
            max_density: Maximum point density
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def icebridge(self,filename = None, count = 18446744073709551615, override_srs = None, default_srs = None, metadata = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """NASA HDF5-based IceBridge ATM reader. 
See http://nsidc.org/data/docs/daac/icebridge/ilatm1b/index.html 
for more information.

        Options:
            filename: Name of file to read
            count: Maximum number of points read
            override_srs: Spatial reference to apply to data
            default_srs: Spatial reference to apply to data if one cannot be inferred
            metadata: Metadata file
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def ilvis2(self,filename = None, count = 18446744073709551615, override_srs = None, default_srs = None, mapping = 'All', metadata = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """ILVIS2 Reader

        Options:
            filename: Name of file to read
            count: Maximum number of points read
            override_srs: Spatial reference to apply to data
            default_srs: Spatial reference to apply to data if one cannot be inferred
            mapping: Mapping for values
            metadata: Metadata file
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def las(self,filename = None, count = 18446744073709551615, override_srs = None, default_srs = None, extra_dims = None, compression = 'EITHER', use_eb_vlr = None, ignore_vlr = None, ignore_missing_vlrs = None, start = None, fix_dims = 'true', nosrs = None, threads = 7, srs_vlr_order = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """ASPRS LAS 1.0 - 1.4 read support

        Options:
            filename: Name of file to read
            count: Maximum number of points read
            override_srs: Spatial reference to apply to data
            default_srs: Spatial reference to apply to data if one cannot be inferred
            extra_dims: Dimensions to assign to extra byte data
            compression: Decompressor to use
            use_eb_vlr: Use extra bytes VLR for 1.0 - 1.3 files
            ignore_vlr: VLR userid/recordid to ignore
            ignore_missing_vlrs: Ignore any missing VLRs rather than throwing an error
            start: Point at which reading should start (0-indexed).
            fix_dims: Make invalid dimension names valid by changing invalid characters to '_'
            nosrs: Skip reading/processing file SRS
            threads: Thread pool size
            srs_vlr_order: Preference order to read SRS VLRs
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def memoryview(self,filename = None, count = 18446744073709551615, override_srs = None, default_srs = None, order = 'row', shape = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """Memory View Reader

        Options:
            filename: Name of file to read
            count: Maximum number of points read
            override_srs: Spatial reference to apply to data
            default_srs: Spatial reference to apply to data if one cannot be inferred
            order: Order of synthetic X/Y/Z values ('row' or 'column').
            shape: Shape of memory (depth, rows, columns).
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def nitf(self,filename = None, count = 18446744073709551615, override_srs = None, default_srs = None, extra_dims = None, compression = 'EITHER', use_eb_vlr = None, ignore_vlr = None, ignore_missing_vlrs = None, start = None, fix_dims = 'true', nosrs = None, threads = 7, srs_vlr_order = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """NITF Reader

        Options:
            filename: Name of file to read
            count: Maximum number of points read
            override_srs: Spatial reference to apply to data
            default_srs: Spatial reference to apply to data if one cannot be inferred
            extra_dims: Dimensions to assign to extra byte data
            compression: Decompressor to use
            use_eb_vlr: Use extra bytes VLR for 1.0 - 1.3 files
            ignore_vlr: VLR userid/recordid to ignore
            ignore_missing_vlrs: Ignore any missing VLRs rather than throwing an error
            start: Point at which reading should start (0-indexed).
            fix_dims: Make invalid dimension names valid by changing invalid characters to '_'
            nosrs: Skip reading/processing file SRS
            threads: Thread pool size
            srs_vlr_order: Preference order to read SRS VLRs
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def obj(self,filename = None, count = 18446744073709551615, override_srs = None, default_srs = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """Obj Reader

        Options:
            filename: Name of file to read
            count: Maximum number of points read
            override_srs: Spatial reference to apply to data
            default_srs: Spatial reference to apply to data if one cannot be inferred
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def optech(self,filename = None, count = 18446744073709551615, override_srs = None, default_srs = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """Optech reader support.

        Options:
            filename: Name of file to read
            count: Maximum number of points read
            override_srs: Spatial reference to apply to data
            default_srs: Spatial reference to apply to data if one cannot be inferred
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def pcd(self,filename = None, count = 18446744073709551615, override_srs = None, default_srs = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """Read data in the Point Cloud Library (PCL) format.

        Options:
            filename: Name of file to read
            count: Maximum number of points read
            override_srs: Spatial reference to apply to data
            default_srs: Spatial reference to apply to data if one cannot be inferred
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def pgpointcloud(self,filename = None, count = 18446744073709551615, override_srs = None, default_srs = None, table = None, connection = None, column = 'pa', schema = None, where = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """Read data from pgpointcloud format. "query" option needs to be a 
SQL statement selecting the data.

        Options:
            filename: Name of file to read
            count: Maximum number of points read
            override_srs: Spatial reference to apply to data
            default_srs: Spatial reference to apply to data if one cannot be inferred
            table: Table name
            connection: Connection string
            column: Column name
            schema: Schema name
            where: Where clause for selection
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def ply(self,filename = None, count = 18446744073709551615, override_srs = None, default_srs = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """Read ply files.

        Options:
            filename: Name of file to read
            count: Maximum number of points read
            override_srs: Spatial reference to apply to data
            default_srs: Spatial reference to apply to data if one cannot be inferred
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def pts(self,filename = None, count = 18446744073709551615, override_srs = None, default_srs = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """Pts Reader

        Options:
            filename: Name of file to read
            count: Maximum number of points read
            override_srs: Spatial reference to apply to data
            default_srs: Spatial reference to apply to data if one cannot be inferred
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def ptx(self,filename = None, count = 18446744073709551615, override_srs = None, default_srs = None, discard_missing_points = 'true', option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """Ptx Reader

        Options:
            filename: Name of file to read
            count: Maximum number of points read
            override_srs: Spatial reference to apply to data
            default_srs: Spatial reference to apply to data if one cannot be inferred
            discard_missing_points: Skip over missing input points with XYZ values of "0 0 0".
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def qfit(self,filename = None, count = 18446744073709551615, override_srs = None, default_srs = None, flip_coordinates = None, scale_z = '0.001', option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """QFIT Reader

        Options:
            filename: Name of file to read
            count: Maximum number of points read
            override_srs: Spatial reference to apply to data
            default_srs: Spatial reference to apply to data if one cannot be inferred
            flip_coordinates: Flip coordinates from 0-360 to -180-180
            scale_z: Z scale. Use 0.001 to go from mm to m
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def sbet(self,filename = None, count = 18446744073709551615, override_srs = None, default_srs = None, angles_as_degrees = 'true', option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """SBET Reader

        Options:
            filename: Name of file to read
            count: Maximum number of points read
            override_srs: Spatial reference to apply to data
            default_srs: Spatial reference to apply to data if one cannot be inferred
            angles_as_degrees: Convert all angles to degrees
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def slpk(self,filename = None, count = 18446744073709551615, override_srs = None, default_srs = None, obb = None, threads = 4, dimensions = None, min_density = '-1', max_density = '-1', option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """SLPK Reader

        Options:
            filename: Name of file to read
            count: Maximum number of points read
            override_srs: Spatial reference to apply to data
            default_srs: Spatial reference to apply to data if one cannot be inferred
            obb: Oriented bounding box of clip region.
            threads: Number of threads to be used.
            dimensions: Dimensions to be used in pulls
            min_density: Minimum point density
            max_density: Maximum point density
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def smrmsg(self,filename = None, count = 18446744073709551615, override_srs = None, default_srs = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """SBET smrmsg Reader

        Options:
            filename: Name of file to read
            count: Maximum number of points read
            override_srs: Spatial reference to apply to data
            default_srs: Spatial reference to apply to data if one cannot be inferred
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def stac(self,filename = None, count = 18446744073709551615, override_srs = None, default_srs = None, asset_names = 'data', date_ranges = None, bounds = None, properties = None, items = None, catalogs = None, collections = None, validate_schema = 'false', header = None, query = None, reader_args = None, requests = 8, catalog_schema_url = 'https://schemas.stacspec.org/v1.0.0/catalog-spec/json-schema/catalog.json', collection_schema_url = 'https://schemas.stacspec.org/v1.0.0/collection-spec/json-schema/collection.json', feature_schema_url = 'https://schemas.stacspec.org/v1.0.0/item-spec/json-schema/item.json', option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """STAC Reader

        Options:
            filename: Name of file to read
            count: Maximum number of points read
            override_srs: Spatial reference to apply to data
            default_srs: Spatial reference to apply to data if one cannot be inferred
            asset_names: List of asset names to look for in data consumption. Default: 'data'
            date_ranges: Date ranges to include in your search. Dates areformatted according to RFC 3339. Eg. dates'[["min1","max1"],...]'
            bounds: Bounding box to select stac items by. This will propogate down through all readers being used.
            properties: Map of STAC property names to regular expression values. ie. {"pc:type": "(lidar|sonar)"}. Selected items will match all properties.
            items: List of Item ID regexes to select STAC items based on.
            catalogs: List of Catalog ID regexes to select STAC items based on.
            collections: List of Collection ID regexes to select STAC items based on.
            validate_schema: Use JSON schema to validate your STAC objects. Default: false
            header: Header fields to forward with HTTP requests
            query: Query parameters to forward with HTTP requests
            reader_args: Map of reader arguments to their values to pass through.
            requests: Number of threads for fetching JSON files, Default: 8
            catalog_schema_url: URL of catalog schema you'd like to use for JSON schema validation.
            collection_schema_url: URL of collection schema you'd like to use for JSON schema validation.
            feature_schema_url: URL of feature schema you'd like to use for JSON schema validation.
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def terrasolid(self,filename = None, count = 18446744073709551615, override_srs = None, default_srs = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """TerraSolid Reader

        Options:
            filename: Name of file to read
            count: Maximum number of points read
            override_srs: Spatial reference to apply to data
            default_srs: Spatial reference to apply to data if one cannot be inferred
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def text(self,filename = None, count = 18446744073709551615, override_srs = None, default_srs = None, separator = 32, header = None, skip = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """Text Reader

        Options:
            filename: Name of file to read
            count: Maximum number of points read
            override_srs: Spatial reference to apply to data
            default_srs: Spatial reference to apply to data if one cannot be inferred
            separator: Separator character that overrides special character found in header line
            header: Use this string as the header line.
            skip: Skip this number of lines before attempting to read the header.
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def tiledb(self,filename = None, count = 18446744073709551615, override_srs = None, default_srs = None, config_file = None, chunk_size = 1000000, stats = 'false', bbox3d = None, bbox4d = None, end_timestamp = 18446744073709551615, start_timestamp = 0, strict = 'true', option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """Read data from a TileDB array.

        Options:
            filename: Name of file to read
            count: Maximum number of points read
            override_srs: Spatial reference to apply to data
            default_srs: Spatial reference to apply to data if one cannot be inferred
            config_file: TileDB configuration file location
            chunk_size: TileDB read chunk size
            stats: Dump TileDB query stats to stdout
            bbox3d: Bounding box subarray to read from TileDB in format([minx, maxx], [miny, maxy], [minz, maxz])
            bbox4d: Bounding box subarray to read from TileDB in format([minx, maxx], [miny, maxy], [minz, maxz], [min_gpstime, max_gpstime] )
            end_timestamp: TileDB array timestamp
            start_timestamp: TileDB array timestamp
            strict: Raise an error for unsupported attributes
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def tindex(self,filename = None, count = 18446744073709551615, override_srs = None, default_srs = None, lyr_name = 'pdal', srs_column = '', tindex_name = 'location', sql = None, bounds = None, polygon = None, t_srs = 'EPSG:4326', filter_srs = 'EPSG:4326', dialect = 'OGRSQL', reader_args = None, where = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """TileIndex Reader

        Options:
            filename: Name of file to read
            count: Maximum number of points read
            override_srs: Spatial reference to apply to data
            default_srs: Spatial reference to apply to data if one cannot be inferred
            lyr_name: OGR layer name from which to read tile index layer
            srs_column: Column to use to override a file's SRS
            tindex_name: OGR column name from which to read tile index location
            sql: OGR-compatible SQL statement for querying tile index layer
            bounds: Bounds box to limit query window. Format: '([xmin,xmax],[ymin,ymax])'
            polygon: Well-known text description of bounds to limit query
            t_srs: Transform SRS of tile index geometry
            filter_srs: Transforms any wkt or boundary option to this coordinate system before filtering or reading data.
            dialect: OGR SQL dialect to use when querying tile index layer
            reader_args: Map of reader arguments to their values to pass through.
            where: OGR SQL filter clause to use on the layer. It only works in combination with tile index layers that are defined with lyr_name
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


class Filter:
    def approximatecoplanar(self,knn = 8, thresh1 = 25, thresh2 = 6, where_merge = 'auto', where = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """Estimates the planarity of a neighborhood of points using eigenvalues.

        Options:
            knn: k-Nearest Neighbors
            thresh1: Threshold 1
            thresh2: Threshold 2
            where_merge: If 'where' option is set, describes how skipped points should be merged with kept points in standard mode.
            where: Expression describing points to be passed to this filter
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def assign(self,assignment = None, condition = None, value = None, where_merge = 'auto', where = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """Assign values for a dimension range to a specified value.

        Options:
            assignment: Values to assign to dimensions based on range.
            condition: Condition for assignment based on range.
            value: Value to assign to dimension based on expression.
            where_merge: If 'where' option is set, describes how skipped points should be merged with kept points in standard mode.
            where: Expression describing points to be passed to this filter
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def chipper(self,capacity = 5000, where_merge = 'auto', where = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """Organize points into spatially contiguous, squarish, and non-overlapping chips.

        Options:
            capacity: Maximum number of points per cell
            where_merge: If 'where' option is set, describes how skipped points should be merged with kept points in standard mode.
            where: Expression describing points to be passed to this filter
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def cluster(self,min_points = 1, max_points = 18446744073709551615, tolerance = 1, is3d = 'true', where_merge = 'auto', where = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """Extract and label clusters using Euclidean distance.

        Options:
            min_points: Min points per cluster
            max_points: Max points per cluster
            tolerance: Radius
            is3d: Perform cluster extraction in 3D?
            where_merge: If 'where' option is set, describes how skipped points should be merged with kept points in standard mode.
            where: Expression describing points to be passed to this filter
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def colorinterp(self,dimension = 'Z', minimum = 'NaN', maximum = 'NaN', clamp = 'false', ramp = 'pestel_shades', invert = 'false', mad = 'false', mad_multiplier = '1.4862', k = 0, where_merge = 'auto', where = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """Assigns RGB colors based on a dimension and a ramp

        Options:
            dimension: Dimension to interpolate
            minimum: Minimum value to use for scaling
            maximum: Maximum value to use for scaling
            clamp: Clamp and color values outside the range [minimum, maximum]
            ramp: GDAL-readable color ramp image to use
            invert: Invert the ramp direction
            mad: Use Median Absolute Deviation to compute ramp bounds in combination with 'k' 
            mad_multiplier: MAD threshold multiplier
            k: Number of deviations to compute minimum/maximum 
            where_merge: If 'where' option is set, describes how skipped points should be merged with kept points in standard mode.
            where: Expression describing points to be passed to this filter
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def colorization(self,raster = None, dimensions = None, where_merge = 'auto', where = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """Fetch and assign RGB color information from a GDAL-readable datasource.

        Options:
            raster: Raster filename
            dimensions: Dimensions to use for colorization
            where_merge: If 'where' option is set, describes how skipped points should be merged with kept points in standard mode.
            where: Expression describing points to be passed to this filter
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def covariancefeatures(self,knn = 10, threads = 1, feature_set = 'dimensionality', stride = 1, radius = None, min_k = 3, mode = 'sqrtnormalized', optimized = 'false', where_merge = 'auto', where = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """Filter that calculates local features based on the covariance matrix of a point's neighborhood.

        Options:
            knn: k-Nearest neighbors
            threads: Number of threads used to run this filter
            feature_set: Set of features to be computed
            stride: Compute features on strided neighbors
            radius: Radius for nearest neighbor search
            min_k: Minimum number of neighbors in radius
            mode: Raw, normalized, or sqrt of eigenvalues
            optimized: Use OptimalKNN or OptimalRadius?
            where_merge: If 'where' option is set, describes how skipped points should be merged with kept points in standard mode.
            where: Expression describing points to be passed to this filter
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def crop(self,outside = None, a_srs = None, bounds = None, point = None, distance = None, polygon = None, where_merge = 'auto', where = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """Filter points inside or outside a bounding box or a polygon

        Options:
            outside: Whether we keep points inside or outside of the bounding region
            a_srs: Spatial reference for bounding region
            bounds: Point box for cropped points
            point: Center of circular/spherical crop region.  Use with 'distance'.
            distance: Crop with this distance from 2D or 3D 'point'
            polygon: Bounding polying for cropped points
            where_merge: If 'where' option is set, describes how skipped points should be merged with kept points in standard mode.
            where: Expression describing points to be passed to this filter
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def csf(self,smooth = 'true', step = '0.65', threshold = '0.5', hdiff = '0.3', resolution = 1, rigidness = 3, iterations = 500, ignore = None, returns = 'last, only', debug = 'false', dir = None, where_merge = 'auto', where = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """Cloth Simulation Filter (Zhang et al., 2016)

        Options:
            smooth: Slope postprocessing?
            step: Time step
            threshold: Classification threshold
            hdiff: Height difference threshold
            resolution: Cloth resolution
            rigidness: Rigidness
            iterations: Max iterations
            ignore: Ignore values
            returns: Include last returns?
            debug: Enable debugging output and use the dir argument
            dir: Optional output directory for debugging
            where_merge: If 'where' option is set, describes how skipped points should be merged with kept points in standard mode.
            where: Expression describing points to be passed to this filter
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def dbscan(self,min_points = 6, eps = 1, dimensions = 'X, Y, Z', where_merge = 'auto', where = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """DBSCAN Clustering.

        Options:
            min_points: Min points per cluster
            eps: Epsilon
            dimensions: Dimensions to cluster
            where_merge: If 'where' option is set, describes how skipped points should be merged with kept points in standard mode.
            where: Expression describing points to be passed to this filter
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def decimation(self,step = 1, offset = None, limit = 18446744073709551615, where_merge = 'auto', where = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """Rank decimation filter. Keep every Nth point

        Options:
            step: Points to delete between each kept point
            offset: Index of first point to consider including in output
            limit: Index of last point to consider including in output
            where_merge: If 'where' option is set, describes how skipped points should be merged with kept points in standard mode.
            where: Expression describing points to be passed to this filter
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def delaunay(self,where_merge = 'auto', where = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """Perform Delaunay triangulation of a pointcloud

        Options:
            where_merge: If 'where' option is set, describes how skipped points should be merged with kept points in standard mode.
            where: Expression describing points to be passed to this filter
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def dem(self,limits = None, raster = None, band = 1, where_merge = 'auto', where = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """Filter points about an elevation surface

        Options:
            limits: Dimension limits for filtering
            raster: GDAL-readable raster to use for DEM
            band: Band number to filter (count from 1)
            where_merge: If 'where' option is set, describes how skipped points should be merged with kept points in standard mode.
            where: Expression describing points to be passed to this filter
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def divider(self,mode = 'partition', count = None, capacity = None, where_merge = 'auto', where = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """Divide points into approximately equal sized groups based on a simple scheme

        Options:
            mode: A mode of 'partition' will write sequential points to an output view until the view meets its predetermined size. 'round_robin' mode will iterate through the output views as it writes sequential points.
            count: Number of output views
            capacity: Maximum number of points in each output view
            where_merge: If 'where' option is set, describes how skipped points should be merged with kept points in standard mode.
            where: Expression describing points to be passed to this filter
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def eigenvalues(self,knn = 8, normalize = 'false', stride = 1, radius = None, min_k = 3, where_merge = 'auto', where = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """Returns the eigenvalues for a given point, based on its k-nearest neighbors.

        Options:
            knn: k-Nearest neighbors
            normalize: Normalize eigenvalues?
            stride: Compute features on strided neighbors
            radius: Radius for nearest neighbor search
            min_k: Minimum number of neighbors in radius
            where_merge: If 'where' option is set, describes how skipped points should be merged with kept points in standard mode.
            where: Expression describing points to be passed to this filter
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def elm(self,cell = 10, class = 7, threshold = 1, where_merge = 'auto', where = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """Marks low points as noise.

        Options:
            cell: Cell size
            class: Class to use for noise points
            threshold: Threshold value
            where_merge: If 'where' option is set, describes how skipped points should be merged with kept points in standard mode.
            where: Expression describing points to be passed to this filter
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def estimaterank(self,knn = 8, thresh = '0.01', where_merge = 'auto', where = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """Computes the rank of a neighborhood of points.

        Options:
            knn: k-Nearest Neighbors
            thresh: Threshold
            where_merge: If 'where' option is set, describes how skipped points should be merged with kept points in standard mode.
            where: Expression describing points to be passed to this filter
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def expression(self,expression = None, where_merge = 'auto', where = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """Pass only points given an expression

        Options:
            expression: Conditional expression describing points to be passed to this filter
            where_merge: If 'where' option is set, describes how skipped points should be merged with kept points in standard mode.
            where: Expression describing points to be passed to this filter
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def expressionstats(self,expressions = None, dimension = None, where_merge = 'auto', where = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """Accumulate count statistics for a given dimension for an array of expressions

        Options:
            expressions: Conditional expressions describing points to be passed to this filter
            dimension: Dimension on which apply expression to calculate statistics
            where_merge: If 'where' option is set, describes how skipped points should be merged with kept points in standard mode.
            where: Expression describing points to be passed to this filter
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def faceraster(self,resolution = None, origin_x = None, origin_y = None, width = None, height = None, mesh = None, nodata = 'NaN', max_triangle_edge_length = 'Infinity', where_merge = 'auto', where = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """Face Raster Filter

        Options:
            resolution: Cell edge size in units of X/Y
            origin_x: X origin for grid
            origin_y: Y origin for grid
            width: Number of cells in the X direction
            height: Number of cells in the Y direction
            mesh: Mesh name
            nodata: No data value
            max_triangle_edge_length: Max triangle edge length
            where_merge: If 'where' option is set, describes how skipped points should be merged with kept points in standard mode.
            where: Expression describing points to be passed to this filter
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def ferry(self,dimensions = None, where_merge = 'auto', where = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """Copy data from one dimension to another.

        Options:
            dimensions: List of dimensions to ferry
            where_merge: If 'where' option is set, describes how skipped points should be merged with kept points in standard mode.
            where: Expression describing points to be passed to this filter
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def fps(self,count = 1000, where_merge = 'auto', where = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """Farthest point sampling filter

        Options:
            count: Target number of points after sampling
            where_merge: If 'where' option is set, describes how skipped points should be merged with kept points in standard mode.
            where: Expression describing points to be passed to this filter
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def geomdistance(self,geometry = None, dimension = 'distance', ring = 'false', ogr = None, where_merge = 'auto', where = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """Compute the distance for points to a given geometry

        Options:
            geometry: Geometries to test
            dimension: Dimension to create to place distance values
            ring: Compare edges (demote polygons to linearrings)
            ogr: OGR filter geometries
            where_merge: If 'where' option is set, describes how skipped points should be merged with kept points in standard mode.
            where: Expression describing points to be passed to this filter
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def georeference(self,trajectory_file = None, trajectory_options = None, scan2imu = None, reverse = 'false', time_offset = 0, coordinate_system = 'NED', where_merge = 'auto', where = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """Georeferencing filter

        Options:
            trajectory_file: Path to trajectory file
            trajectory_options: Trajectory reader option
            scan2imu: Transformation from scanner to imu
            reverse: reverse georeferencing
            time_offset: time offset between trajectory and scanner timestamps
            coordinate_system: scan2imu coordinate system
            where_merge: If 'where' option is set, describes how skipped points should be merged with kept points in standard mode.
            where: Expression describing points to be passed to this filter
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def gpstimeconvert(self,conversion = None, start_date = '', wrap = 'false', wrapped = 'false', where_merge = 'auto', where = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """Convert between GPS Time, GPS Standard Time, and GPS Week Seconds

        Options:
            conversion: time conversion type
            start_date: GMT start date of data in 'YYYY-MM-DD' format
            wrap: reset output week seconds to zero on Sundays
            wrapped: input weeks seconds reset to zero on Sundays
            where_merge: If 'where' option is set, describes how skipped points should be merged with kept points in standard mode.
            where: Expression describing points to be passed to this filter
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def greedyprojection(self,multiplier = None, radius = None, num_neighbors = 100, min_angle = '0.1745329252', max_angle = '2.094395102', eps_angle = '0.7853981634', where_merge = 'auto', where = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """Greedy Triangulation filter

        Options:
            multiplier: Nearest neighbor distance multiplier
            radius: Search radius for neighbors
            num_neighbors: Number of nearest neighbors to consider
            min_angle: Minimum angle for created triangles
            max_angle: Maximum angle for created triangles
            eps_angle: Max normal difference angle for triangulation consideration
            where_merge: If 'where' option is set, describes how skipped points should be merged with kept points in standard mode.
            where: Expression describing points to be passed to this filter
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def gridDecimation(self,resolution = 1, output_type = 'max', value = None, where_merge = 'auto', where = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """keep max or min points in a grid

        Options:
            resolution: Cell edge size, in units of X/Y
            output_type: Point keept into the cells ('min', 'max')
            value: Value to assign to dimension based on expression.
            where_merge: If 'where' option is set, describes how skipped points should be merged with kept points in standard mode.
            where: Expression describing points to be passed to this filter
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def groupby(self,dimension = None, where_merge = 'auto', where = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """Split data categorically by dimension.

        Options:
            dimension: Dimension containing data to be grouped
            where_merge: If 'where' option is set, describes how skipped points should be merged with kept points in standard mode.
            where: Expression describing points to be passed to this filter
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def h3(self,resolution = None, where_merge = 'auto', where = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """Compute H3 indexes for points

        Options:
            resolution: H3 resolution parameter
            where_merge: If 'where' option is set, describes how skipped points should be merged with kept points in standard mode.
            where: Expression describing points to be passed to this filter
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def hag_delaunay(self,count = 10, allow_extrapolation = 'true', where_merge = 'auto', where = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """Computes height above ground using delaunay interpolation of ground returns.

        Options:
            count: The number of points to fetch to determine the ground point [Default: 10].
            allow_extrapolation: Allow extrapolation for points outside of the local triangulations. [Default: true].
            where_merge: If 'where' option is set, describes how skipped points should be merged with kept points in standard mode.
            where: Expression describing points to be passed to this filter
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def hag_dem(self,raster = None, band = 1, zero_ground = 'true', where_merge = 'auto', where = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """Computes height above ground using a DEM raster.

        Options:
            raster: GDAL-readable raster to use for DEM (uses band 1, starting from 1)
            band: Band number to filter (count from 1)
            zero_ground: If true, set HAG of ground-classified points to 0 rather than comparing Z value to raster DEM
            where_merge: If 'where' option is set, describes how skipped points should be merged with kept points in standard mode.
            where: Expression describing points to be passed to this filter
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def hag_nn(self,count = 1, max_distance = None, allow_extrapolation = 'true', where_merge = 'auto', where = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """Computes height above ground using nearest-neighbor ground-classified returns.

        Options:
            count: The number of points to fetch to determine the ground point [Default: 1].
            max_distance: Ground points beyond this distance will not influence nearest neighbor interpolation of height above ground.[Default: None]
            allow_extrapolation: If true and count > 1, allow extrapolation [Default: true].
            where_merge: If 'where' option is set, describes how skipped points should be merged with kept points in standard mode.
            where: Expression describing points to be passed to this filter
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def head(self,count = 10, invert = 'false', where_merge = 'auto', where = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """Return N points from beginning of the point cloud.

        Options:
            count: Number of points to return from beginning.  If 'invert' is true, number of points to drop from the beginning.
            invert: If true, 'count' specifies the number of points to skip from the beginning.
            where_merge: If 'where' option is set, describes how skipped points should be merged with kept points in standard mode.
            where: Expression describing points to be passed to this filter
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def hexbin(self,sample_size = 5000, threshold = 15, output_tesselation = None, edge_size = None, edge_length = None, precision = 8, hole_cull_area_tolerance = None, smooth = 'true', preserve_topology = 'true', density = '', where_merge = 'auto', where = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """Tessellate the point's X/Y domain and determine point density and/or point boundary.

        Options:
            sample_size: Sample size for auto-edge length calculation
            threshold: Required cell density
            output_tesselation: Write tesselation to output metadata
            edge_size: Synonym for 'edge_length' (deprecated)
            edge_length: Length of hex edge
            precision: Output precision
            hole_cull_area_tolerance: Tolerance area to apply to holes before cull
            smooth: Smooth boundary output
            preserve_topology: Preserve topology when smoothing
            density: Emit a density tessellation GeoJSON FeatureCollection in metadata
            where_merge: If 'where' option is set, describes how skipped points should be merged with kept points in standard mode.
            where: Expression describing points to be passed to this filter
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def icp(self,max_iter = 100, rt = '0.99999', tt = '9e-08', mse_abs = '1e-12', max_similar = 0, max_dist = None, init = None, where_merge = 'auto', where = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """Iterative Closest Point (ICP) registration.

        Options:
            max_iter: Maximum number of iterations
            rt: Rotation threshold
            tt: Translation threshold
            mse_abs: Absolute threshold for MSE
            max_similar: Max number of similar transforms to consider converged
            max_dist: Maximum correspondence distance
            init: Initial transformation matrix
            where_merge: If 'where' option is set, describes how skipped points should be merged with kept points in standard mode.
            where: Expression describing points to be passed to this filter
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def info(self,point = None, query = None, where_merge = 'auto', where = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """Gather basic info about points.

        Options:
            point: Point to dump
--point="1-5,10,100-200" (0 indexed)
            query: Return points in order of distance from the specified location (2D or 3D)
--query Xcoord,Ycoord[,Zcoord][/count]
            where_merge: If 'where' option is set, describes how skipped points should be merged with kept points in standard mode.
            where: Expression describing points to be passed to this filter
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def iqr(self,k = '1.5', dimension = None, where_merge = 'auto', where = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """Interquartile Range Filter

        Options:
            k: Number of deviations
            dimension: Dimension on which to calculate statistics
            where_merge: If 'where' option is set, describes how skipped points should be merged with kept points in standard mode.
            where: Expression describing points to be passed to this filter
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def label_duplicates(self,dimensions = None, where_merge = 'auto', where = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """Label duplicate points

        Options:
            dimensions: Dimensions to use to declare points as duplicate
            where_merge: If 'where' option is set, describes how skipped points should be merged with kept points in standard mode.
            where: Expression describing points to be passed to this filter
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def litree(self,min_points = 10, min_height = 3, radius = 100, where_merge = 'auto', where = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """Li Tree Filter

        Options:
            min_points: Minimum number of points in a tree cluster
            min_height: Minimum height above ground to start a tree cluster
            radius: Dummy point located outside this approximate radius
            where_merge: If 'where' option is set, describes how skipped points should be merged with kept points in standard mode.
            where: Expression describing points to be passed to this filter
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def lloydkmeans(self,k = 10, dimensions = 'X, Y, Z', maxiters = 10, where_merge = 'auto', where = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """Extract and label clusters using K-means (Lloyd's algorithm).

        Options:
            k: Number of clusters to segment
            dimensions: Dimensions to cluster
            maxiters: Maximum number of iterations
            where_merge: If 'where' option is set, describes how skipped points should be merged with kept points in standard mode.
            where: Expression describing points to be passed to this filter
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def locate(self,dimension = None, minmax = 'max', where_merge = 'auto', where = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """Return a single point with min/max value in the named dimension.

        Options:
            dimension: Dimension in which to locate max
            minmax: Whether to search for the minimum or maximum value
            where_merge: If 'where' option is set, describes how skipped points should be merged with kept points in standard mode.
            where: Expression describing points to be passed to this filter
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def lof(self,minpts = 10, where_merge = 'auto', where = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """LOF Filter

        Options:
            minpts: Minimum number of points
            where_merge: If 'where' option is set, describes how skipped points should be merged with kept points in standard mode.
            where: Expression describing points to be passed to this filter
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def mad(self,k = 2, dimension = None, mad_multiplier = '1.4862', where_merge = 'auto', where = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """Median Absolute Deviation Filter

        Options:
            k: Number of deviations
            dimension: Dimension on which to calculate statistics
            mad_multiplier: MAD threshold multiplier
            where_merge: If 'where' option is set, describes how skipped points should be merged with kept points in standard mode.
            where: Expression describing points to be passed to this filter
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def merge(self,where_merge = 'auto', where = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """Merge data from two different readers into a single stream.

        Options:
            where_merge: If 'where' option is set, describes how skipped points should be merged with kept points in standard mode.
            where: Expression describing points to be passed to this filter
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def miniball(self,knn = 8, threads = 1, where_merge = 'auto', where = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """Miniball (Kutz et al., 2003)

        Options:
            knn: k-Nearest neighbors
            threads: Number of threads used to run this filter
            where_merge: If 'where' option is set, describes how skipped points should be merged with kept points in standard mode.
            where: Expression describing points to be passed to this filter
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def mongo(self,expression = None, where_merge = 'auto', where = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """Pass only points that pass a logic filter.

        Options:
            expression: Logical query expression
            where_merge: If 'where' option is set, describes how skipped points should be merged with kept points in standard mode.
            where: Expression describing points to be passed to this filter
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def mortonorder(self,reverse = 'false', where_merge = 'auto', where = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """Morton or z-order sorting of points. See http://en.wikipedia.org/wiki/Z-order_curve for more detail.

        Options:
            reverse: Reverse Morton
            where_merge: If 'where' option is set, describes how skipped points should be merged with kept points in standard mode.
            where: Expression describing points to be passed to this filter
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def neighborclassifier(self,domain = None, k = None, candidate = None, dimension = 'Classification', where_merge = 'auto', where = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """Re-assign some point attributes based KNN voting

        Options:
            domain: Selects which points will be subject to KNN-based assignment
            k: Number of nearest neighbors to consult
            candidate: candidate file name
            dimension: Dimension on which votes are calculated (treated as an integer).
            where_merge: If 'where' option is set, describes how skipped points should be merged with kept points in standard mode.
            where: Expression describing points to be passed to this filter
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def nndistance(self,mode = 'kthavg', k = 10, where_merge = 'auto', where = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """NN-Distance Filter

        Options:
            mode: Distance computation mode (kth, avg)
            k: k neighbors
            where_merge: If 'where' option is set, describes how skipped points should be merged with kept points in standard mode.
            where: Expression describing points to be passed to this filter
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def normal(self,knn = 8, viewpoint = None, always_up = 'true', refine = 'false', where_merge = 'auto', where = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """Normal Filter

        Options:
            knn: k-Nearest Neighbors
            viewpoint: Viewpoint as WKT or GeoJSON
            always_up: Normals always oriented with positive Z?
            refine: Refine normals using minimum spanning tree propagation?
            where_merge: If 'where' option is set, describes how skipped points should be merged with kept points in standard mode.
            where: Expression describing points to be passed to this filter
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def optimalneighborhood(self,min_k = 10, max_k = 14, where_merge = 'auto', where = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """OptimalNeighborhood Filter

        Options:
            min_k: Minimum k-Nearest Neighbors
            max_k: Maximum k-Nearest Neighbors
            where_merge: If 'where' option is set, describes how skipped points should be merged with kept points in standard mode.
            where: Expression describing points to be passed to this filter
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def outlier(self,method = 'statistical', min_k = 2, radius = 1, mean_k = 8, multiplier = 2, class = 7, where_merge = 'auto', where = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """Outlier removal

        Options:
            method: Method [default: statistical]
            min_k: Minimum number of neighbors in radius
            radius: Radius
            mean_k: Mean number of neighbors
            multiplier: Standard deviation threshold
            class: Class to use for noise points
            where_merge: If 'where' option is set, describes how skipped points should be merged with kept points in standard mode.
            where: Expression describing points to be passed to this filter
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def overlay(self,dimension = None, datasource = None, column = None, query = None, layer = None, bounds = None, threads = 1, where_merge = 'auto', where = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """Assign values to a dimension based on the extent of an OGR-readable data  source or an OGR SQL query.

        Options:
            dimension: Dimension on which to filter
            datasource: OGR-readable datasource for Polygon or Multipolygon data
            column: OGR datasource column from which to read the attribute.
            query: OGR SQL query to execute on the datasource to fetch geometry and attributes
            layer: Datasource layer to use
            bounds: Bounds to limit query using with OGR_L_SetSpatialFilter
            threads: Number of threads used to run this filter
            where_merge: If 'where' option is set, describes how skipped points should be merged with kept points in standard mode.
            where: Expression describing points to be passed to this filter
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def planefit(self,knn = 8, threads = 1, where_merge = 'auto', where = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """Plane Fit (Kutz et al., 2003)

        Options:
            knn: k-Nearest neighbors
            threads: Number of threads used to run this filter
            where_merge: If 'where' option is set, describes how skipped points should be merged with kept points in standard mode.
            where: Expression describing points to be passed to this filter
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def pmf(self,cell_size = 1, exponential = 'true', ignore = None, initial_distance = '0.15', returns = 'last, only', max_distance = '2.5', max_window_size = 33, slope = 1, where_merge = 'auto', where = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """Progressive morphological filter

        Options:
            cell_size: Cell size
            exponential: Exponential growth of window size?
            ignore: Ignore values
            initial_distance: Initial distance
            returns: Include only returns?
            max_distance: Maximum distance
            max_window_size: Maximum window size
            slope: Slope
            where_merge: If 'where' option is set, describes how skipped points should be merged with kept points in standard mode.
            where: Expression describing points to be passed to this filter
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def poisson(self,density = None, depth = 8, where_merge = 'auto', where = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """Poisson Surface Reconstruction Filter

        Options:
            density: Output density estimates
            depth: Maximum depth of the octree used for reconstruction
            where_merge: If 'where' option is set, describes how skipped points should be merged with kept points in standard mode.
            where: Expression describing points to be passed to this filter
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def projpipeline(self,out_srs = None, reverse_transfo = 'false', coord_op = None, where_merge = 'auto', where = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """Transform coordinates using Proj pipeline string, WKT2 coordinate operations or URN definition

        Options:
            out_srs: Output spatial reference
            reverse_transfo: Wether the coordinate operation should be evaluated in the reverse path
            coord_op: Coordinate operation (Proj pipeline or WKT2 string or urn definition)
            where_merge: If 'where' option is set, describes how skipped points should be merged with kept points in standard mode.
            where: Expression describing points to be passed to this filter
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def radialdensity(self,radius = 1, where_merge = 'auto', where = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """RadialDensity Filter

        Options:
            radius: Radius
            where_merge: If 'where' option is set, describes how skipped points should be merged with kept points in standard mode.
            where: Expression describing points to be passed to this filter
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def randomize(self,seed = 0, where_merge = 'auto', where = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """Randomize points in a view.

        Options:
            seed: Random number generator seed
            where_merge: If 'where' option is set, describes how skipped points should be merged with kept points in standard mode.
            where: Expression describing points to be passed to this filter
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def range(self,limits = None, where_merge = 'auto', where = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """Pass only points given a dimension/range.

        Options:
            limits: Range limits
            where_merge: If 'where' option is set, describes how skipped points should be merged with kept points in standard mode.
            where: Expression describing points to be passed to this filter
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def reciprocity(self,knn = 8, threads = 1, where_merge = 'auto', where = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """Returns the percentage of neighbors that do NOT have the query point as a neighbor

        Options:
            knn: k-Nearest neighbors
            threads: Number of threads used to run this filter
            where_merge: If 'where' option is set, describes how skipped points should be merged with kept points in standard mode.
            where: Expression describing points to be passed to this filter
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def relaxationdartthrowing(self,decay = '0.9', radius = 1, terminal_radius = '0.001', count = 1000, shuffle = 'true', seed = None, where_merge = 'auto', where = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """Subsampling filter

        Options:
            decay: Decay rate
            radius: Minimum radius (initial)
            terminal_radius: Minimum radius (terminal)
            count: Target number of points after sampling
            shuffle: Shuffle points prior to sampling?
            seed: Random number generator seed
            where_merge: If 'where' option is set, describes how skipped points should be merged with kept points in standard mode.
            where: Expression describing points to be passed to this filter
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def reprojection(self,out_srs = None, in_srs = None, in_axis_ordering = '', out_axis_ordering = '', in_coord_epoch = None, out_coord_epoch = None, error_on_failure = None, where_merge = 'auto', where = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """Reproject data using GDAL from one coordinate system to another.

        Options:
            out_srs: Output spatial reference
            in_srs: Input spatial reference
            in_axis_ordering: Axis ordering override for in_srs
            out_axis_ordering: Axis ordering override for out_srs
            in_coord_epoch: Input coordinate epoch for transformation
            out_coord_epoch: Output coordinate epoch for transformation
            error_on_failure: Throw an exception if we can't reproject any point
            where_merge: If 'where' option is set, describes how skipped points should be merged with kept points in standard mode.
            where: Expression describing points to be passed to this filter
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def returns(self,groups = 'last', where_merge = 'auto', where = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """Split data by return order

        Options:
            groups: Comma-separated list of return number groupings ('first', 'last', 'intermediate', or 'only')
            where_merge: If 'where' option is set, describes how skipped points should be merged with kept points in standard mode.
            where: Expression describing points to be passed to this filter
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def sample(self,cell = None, radius = None, dimension = None, origin_x = None, origin_y = None, origin_z = None, where_merge = 'auto', where = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """Subsampling filter

        Options:
            cell: Cell size
            radius: Minimum radius
            dimension: Emit 1 or 0 whether a point was sampled into this newly created dimension instead of culling points
            origin_x: Voxelization origin X (default to first point)
            origin_y: Voxelization origin Y (default to first point)
            origin_z: Voxelization origin Z (default to first point)
            where_merge: If 'where' option is set, describes how skipped points should be merged with kept points in standard mode.
            where: Expression describing points to be passed to this filter
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def separatescanline(self,groupby = 1, where_merge = 'auto', where = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """Split data by scan line.

        Options:
            groupby: Number of lines to be grouped by
            where_merge: If 'where' option is set, describes how skipped points should be merged with kept points in standard mode.
            where: Expression describing points to be passed to this filter
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def shell(self,command = None, where_merge = 'auto', where = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """Execute a shell operation inline with PDAL pipeline steps

        Options:
            command: Command to run
            where_merge: If 'where' option is set, describes how skipped points should be merged with kept points in standard mode.
            where: Expression describing points to be passed to this filter
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def skewnessbalancing(self,where_merge = 'auto', where = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """Bartels & Wei Skewness Balancing

        Options:
            where_merge: If 'where' option is set, describes how skipped points should be merged with kept points in standard mode.
            where: Expression describing points to be passed to this filter
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def smrf(self,cell = 1, slope = '0.15', scalar = '1.25', threshold = '0.5', cut = 0, dir = None, ignore = None, returns = 'last, only', classbits = None, window = None, where_merge = 'auto', where = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """Simple Morphological Filter (Pingel et al., 2013)

        Options:
            cell: Cell size?
            slope: Percent slope?
            scalar: Elevation scalar?
            threshold: Elevation threshold?
            cut: Cut net size?
            dir: Optional output directory for debugging
            ignore: Ignore values
            returns: Include last returns?
            classbits: Ignore synthetic|keypoint|withheld classification bits?
            window: Max window size?
            where_merge: If 'where' option is set, describes how skipped points should be merged with kept points in standard mode.
            where: Expression describing points to be passed to this filter
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def sort(self,dimensions = None, order = 'ASCDESC', algorithm = 'NORMALSTABLE', where_merge = 'auto', where = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """Sort data based on a given dimension.

        Options:
            dimensions: Dimensions and ordering on which to sort
            order: Sort order ASC(ending) or DESC(ending)
            algorithm: NORMAL (default) or STABLE
            where_merge: If 'where' option is set, describes how skipped points should be merged with kept points in standard mode.
            where: Expression describing points to be passed to this filter
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def sparsesurface(self,radius = 1, where_merge = 'auto', where = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """Sparse Surface Filter

        Options:
            radius: Mask neighbor points as low noise
            where_merge: If 'where' option is set, describes how skipped points should be merged with kept points in standard mode.
            where: Expression describing points to be passed to this filter
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def splitter(self,length = 1000, origin_x = 'NaN', origin_y = 'NaN', buffer = 0, where_merge = 'auto', where = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """Split data based on a X/Y box length.

        Options:
            length: Edge length of cell
            origin_x: X origin for a cell
            origin_y: Y origin for a cell
            buffer: Size of buffer (overlap) to include around each tile.
            where_merge: If 'where' option is set, describes how skipped points should be merged with kept points in standard mode.
            where: Expression describing points to be passed to this filter
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def stats(self,dimensions = None, enumerate = None, global = None, count = None, advanced = None, commonsrs = 'EPSG:4326', where_merge = 'auto', where = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """Compute statistics about each dimension (mean, min, max, etc.)

        Options:
            dimensions: Dimensions on which to calculate statistics
            enumerate: Dimensions whose values should be enumerated
            global: Dimensions to compute global stats (median, mad, mode)
            count: Dimensions whose values should be counted
            advanced: Calculate skewness and kurtosis
            commonsrs: Common SRS to use for normalizing bounding boxes
            where_merge: If 'where' option is set, describes how skipped points should be merged with kept points in standard mode.
            where: Expression describing points to be passed to this filter
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def straighten(self,polyline = None, reverse = 'false', offset = 0, where_merge = 'auto', where = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """Straighten filter

        Options:
            polyline: Track polyline to straigthen, LineStringZM, with m value is roll in radians
            reverse: Set to true if you the to unstraighten.
            offset: Use a global offset, so that straighten X starts with that value
            where_merge: If 'where' option is set, describes how skipped points should be merged with kept points in standard mode.
            where: Expression describing points to be passed to this filter
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def streamcallback(self,where_merge = 'auto', where = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """Provide a hook for a simple point-by-point callback.

        Options:
            where_merge: If 'where' option is set, describes how skipped points should be merged with kept points in standard mode.
            where: Expression describing points to be passed to this filter
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def tail(self,count = 10, invert = None, where_merge = 'auto', where = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """Return N points from end of the point cloud.

        Options:
            count: Number of points to return from end. If 'invert' is true, number of points to drop from the end.
            invert: If true, 'count' specifies the number of points at the end to drop.
            where_merge: If 'where' option is set, describes how skipped points should be merged with kept points in standard mode.
            where: Expression describing points to be passed to this filter
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def trajectory(self,dtr = '0.001', dts = '0.001', minsep = '0.01', tblock = 1, tout = '0.01', where_merge = 'auto', where = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """SRI Trajectory calculator

        Options:
            dtr: Multi-return sampling interval (secs) (inf = don't sample)
            dts: Single return sampling interval (secs) (inf = don't sample)
            minsep: Minimum separation (meters) of returns considered
            tblock: Block size for cubic spline (secs)
            tout: Output data interval (secs)
            where_merge: If 'where' option is set, describes how skipped points should be merged with kept points in standard mode.
            where: Expression describing points to be passed to this filter
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def transformation(self,invert = 'false', matrix = None, override_srs = None, where_merge = 'auto', where = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """Transform each point using a 4x4 transformation matrix

        Options:
            invert: Apply inverse transformation
            matrix: Transformation matrix
            override_srs: Spatial reference to apply to data.
            where_merge: If 'where' option is set, describes how skipped points should be merged with kept points in standard mode.
            where: Expression describing points to be passed to this filter
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def voxelcenternearestneighbor(self,cell = 1, where_merge = 'auto', where = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """Voxel Center Nearest Neighbor Filter

        Options:
            cell: Cell size
            where_merge: If 'where' option is set, describes how skipped points should be merged with kept points in standard mode.
            where: Expression describing points to be passed to this filter
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def voxelcentroidnearestneighbor(self,cell = 1, where_merge = 'auto', where = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """Voxel Centroid Nearest Neighbor Filter

        Options:
            cell: Cell size
            where_merge: If 'where' option is set, describes how skipped points should be merged with kept points in standard mode.
            where: Expression describing points to be passed to this filter
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def voxeldownsize(self,cell = '0.001', mode = 'center', where_merge = 'auto', where = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """First Entry Voxel Filter

        Options:
            cell: Cell size
            mode: Method for downsizing : center / first
            where_merge: If 'where' option is set, describes how skipped points should be merged with kept points in standard mode.
            where: Expression describing points to be passed to this filter
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def zsmooth(self,radius = 1, medianpercent = 50, dim = None, where_merge = 'auto', where = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """Zsmooth Filter

        Options:
            radius: Radius in X/Y plane in which to find neighboring points
            medianpercent: Location (percent) in neighbor list at which to find neighbor Z value (min == 0, max == 100, median == 50, etc.)
            dim: Name of dimension in which to store statistic
            where_merge: If 'where' option is set, describes how skipped points should be merged with kept points in standard mode.
            where: Expression describing points to be passed to this filter
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


class Writer:
    def arrow(self,filename = None, format = 'feather', geoarrow_dimension_name = 'xyz', batch_size = 262144, write_pipeline_metadata = 'true', geoparquet_version = '1.0.0', where_merge = 'auto', where = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """Arrow Writer

        Options:
            filename: Output filename
            format: Output format ('feather','parquet','geoparquet')
            geoarrow_dimension_name: Dimension name for GeoArrow xyz struct
            batch_size: Arrow batch size
            write_pipeline_metadata: Write PDAL metadata to schema
            geoparquet_version: GeoParquet version string
            where_merge: If 'where' option is set, describes how skipped points should be merged with kept points in standard mode.
            where: Expression describing points to be passed to this filter
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def bpf(self,filename = None, compression = None, header_data = None, format = 'Dimension', coord_id = 'auto', bundledfile = None, output_dims = None, offset_x = None, offset_y = None, offset_z = None, scale_x = 1, scale_y = 1, scale_z = 1, where_merge = 'auto', where = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """"Binary Point Format" (BPF) writer support. BPF is a simple 
DoD and research format that is used by some sensor and 
processing chains.

        Options:
            filename: Output filename
            compression: Output compression
            header_data: Base64-encoded header data
            format: Output format
            coord_id: UTM coordinate ID
            bundledfile: List of files to bundle in output
            output_dims: Output dimensions
            offset_x: X offset
            offset_y: Y offset
            offset_z: Z offset
            scale_x: X scale
            scale_y: Y scale
            scale_z: Z scale
            where_merge: If 'where' option is set, describes how skipped points should be merged with kept points in standard mode.
            where: Expression describing points to be passed to this filter
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def copc(self,filename = None, forward = None, filesource_id = 0, global_encoding = 0, project_id = None, system_id = 'PDAL\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', software_id = 'PDAL 2.8.3 (Releas)\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', creation_doy = 60, creation_year = 2025, scale_x = '.01', scale_y = '.01', scale_z = '.01', offset_x = None, offset_y = None, offset_z = None, vlrs = None, pipeline = None, fixed_seed = None, a_srs = None, threads = None, enhanced_srs_vlrs = 'false', extra_dims = None, where_merge = 'auto', where = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """COPC Writer

        Options:
            filename: Output filename
            forward: Dimensions to forward from LAS reader
            filesource_id: File source ID number.
            global_encoding: Global encoding byte
            project_id: Project ID
            system_id: System ID
            software_id: Software ID
            creation_doy: Creation day of year
            creation_year: Creation year
            scale_x: X scale factor
            scale_y: Y scale factor
            scale_z: Z scale factor
            offset_x: X offset
            offset_y: Y offset
            offset_z: Z offset
            vlrs: List of VLRs to set
            pipeline: Emit a JSON-represetation of the pipeline as a VLR
            fixed_seed: Fix the random seed
            a_srs: Spatial reference to use to write output
            threads: 
            enhanced_srs_vlrs: Write WKT2 and PROJJSON as VLR?
            extra_dims: List of dimension names to write in addition to those of the point format or 'all' for all available dimensions
            where_merge: If 'where' option is set, describes how skipped points should be merged with kept points in standard mode.
            where: Expression describing points to be passed to this filter
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def draco(self,filename = None, dimensions = None, quantization = None, where_merge = 'auto', where = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """Write data using Draco.

        Options:
            filename: Output filename
            dimensions: Json mapping of pdal dimensions to desired data types
            quantization: Json mapping of Draco Attributes to desired quantization level
            where_merge: If 'where' option is set, describes how skipped points should be merged with kept points in standard mode.
            where: Expression describing points to be passed to this filter
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def e57(self,filename = None, double_precision = None, extra_dims = None, where_merge = 'auto', where = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """E57 format support.

        Options:
            filename: Output filename
            double_precision: Double precision for storage (false by default)
            extra_dims: Extra dimensions to write to E57 data
            where_merge: If 'where' option is set, describes how skipped points should be merged with kept points in standard mode.
            where: Expression describing points to be passed to this filter
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def ept_addon(self,addons = None, threads = None, where_merge = 'auto', where = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """EPT Writer

        Options:
            addons: Mapping of output locations to their dimension names
            threads: Number of worker threads
            where_merge: If 'where' option is set, describes how skipped points should be merged with kept points in standard mode.
            where: Expression describing points to be passed to this filter
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def fbi(self,filename = None, where_merge = 'auto', where = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """FBI Writer

        Options:
            filename: Output filename
            where_merge: If 'where' option is set, describes how skipped points should be merged with kept points in standard mode.
            where: Expression describing points to be passed to this filter
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def gdal(self,filename = None, resolution = None, radius = None, power = 1, gdaldriver = 'GTiff', gdalopts = None, output_type = 'all', data_type = 'double', window_size = None, nodata = 'NaN', dimension = 'Z', bounds = None, origin_x = None, origin_y = None, width = None, height = None, override_srs = None, default_srs = None, metadata = None, pdal_metadata = 'false', binmode = 'false', allow_empty = 'false', where_merge = 'auto', where = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """Write a point cloud as a GDAL raster.

        Options:
            filename: Output filename
            resolution: Cell edge size, in units of X/Y
            radius: Radius from cell center to use to locate influencing points
            power: Power parameter for weighting points when using IDW
            gdaldriver: GDAL writer driver name
            gdalopts: GDAL driver options (name=value,name=value...)
            output_type: Statistics produced ('min', 'max', 'mean', 'idw', 'count', 'stdev' or 'all')
            data_type: Data type for output grid ('int8', 'uint64', 'float', etc.)
            window_size: Cell distance for fallback interpolation
            nodata: No data value
            dimension: Dimension to use
            bounds: Bounds of data. [deprecated]
            origin_x: X origin for grid.
            origin_y: Y origin for grid.
            width: Number of cells in the X direction.
            height: Number of cells in the Y direction.
            override_srs: Spatial reference to apply to data
            default_srs: Spatial reference to apply to data if one cannot be inferred
            metadata: GDAL metadata to set on the raster, in the form 'NAME=VALUE,NAME2=VALUE2,NAME3=VALUE3'
            pdal_metadata: Write PDAL metadata as to GDAL PAM XML Metadata?
            binmode: Use binning mode for computing statistics and ignore distance and neighborhood
            allow_empty: Allow writing GDAL output that do not have any pixel values (no points)
            where_merge: If 'where' option is set, describes how skipped points should be merged with kept points in standard mode.
            where: Expression describing points to be passed to this filter
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def gltf(self,filename = None, metallic = None, roughness = None, red = None, green = None, blue = None, alpha = 1, double_sided = None, colors = None, normals = None, where_merge = 'auto', where = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """Gltf Writer

        Options:
            filename: Output filename
            metallic: Metallic factor [0-1]
            roughness: Roughness factor [0-1]
            red: Base red factor [0-1]
            green: Base green factor [0-1]
            blue: Base blue factor [0-1]
            alpha: Alpha factor [0-1]
            double_sided: Whether the material should be applied to both sides of the faces.
            colors: Write color data for each vertex.  Note that most renderers will interpolate the color of each vertex across a face, so this may look odd.
            normals: Write vertex normals
            where_merge: If 'where' option is set, describes how skipped points should be merged with kept points in standard mode.
            where: Expression describing points to be passed to this filter
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def las(self,filename = None, a_srs = None, compression = 'false', discard_high_return_numbers = None, extra_dims = None, forward = None, filesource_id = 0, major_version = 1, minor_version = 4, dataformat_id = 7, format = 7, global_encoding = 0, project_id = None, system_id = 'PDAL\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', software_id = 'PDAL 2.8.3 (Releas)\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', creation_doy = 60, creation_year = 2025, pdal_metadata = 'false', scale_x = '.01', scale_y = '.01', scale_z = '.01', offset_x = None, offset_y = None, offset_z = None, vlrs = None, enhanced_srs_vlrs = 'false', where_merge = 'auto', where = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """ASPRS LAS 1.0 - 1.4 writer

        Options:
            filename: Output filename
            a_srs: Spatial reference to use to write output
            compression: Use LAZ compression when writing file
            discard_high_return_numbers: Discard points with out-of-spec return numbers.
            extra_dims: List of dimension names to write in addition to those of the point format or 'all' for all available dimensions
            forward: Dimensions to forward from LAS reader
            filesource_id: File source ID number.
            major_version: LAS major version
            minor_version: LAS minor version
            dataformat_id: Point format
            format: Point format
            global_encoding: Global encoding byte
            project_id: Project ID
            system_id: System ID
            software_id: Software ID
            creation_doy: Creation day of year
            creation_year: Creation year
            pdal_metadata: Write PDAL metadata as VLR?
            scale_x: X scale factor
            scale_y: Y scale factor
            scale_z: Z scale factor
            offset_x: X offset
            offset_y: Y offset
            offset_z: Z offset
            vlrs: List of VLRs to set
            enhanced_srs_vlrs: Write WKT2 and PROJJSON as VLR?
            where_merge: If 'where' option is set, describes how skipped points should be merged with kept points in standard mode.
            where: Expression describing points to be passed to this filter
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def nitf(self,filename = None, a_srs = None, compression = 'false', discard_high_return_numbers = None, extra_dims = None, forward = None, filesource_id = 0, major_version = 1, minor_version = 4, dataformat_id = 7, format = 7, global_encoding = 0, project_id = None, system_id = 'PDAL\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', software_id = 'PDAL 2.8.3 (Releas)\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', creation_doy = 60, creation_year = 2025, pdal_metadata = 'false', scale_x = '.01', scale_y = '.01', scale_z = '.01', offset_x = None, offset_y = None, offset_z = None, vlrs = None, enhanced_srs_vlrs = 'false', clevel = 03, stype = 'BF01', ostaid = 'PDAL', ftitle = None, fsclas = 'U', oname = None, ophone = None, fsctlh = None, fsclsy = None, isclas = 'U', idatim = None, iid2 = None, fscltx = None, aimidb = None, acftb = None, where_merge = 'auto', where = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """NITF Writer

        Options:
            filename: Output filename
            a_srs: Spatial reference to use to write output
            compression: Use LAZ compression when writing file
            discard_high_return_numbers: Discard points with out-of-spec return numbers.
            extra_dims: List of dimension names to write in addition to those of the point format or 'all' for all available dimensions
            forward: Dimensions to forward from LAS reader
            filesource_id: File source ID number.
            major_version: LAS major version
            minor_version: LAS minor version
            dataformat_id: Point format
            format: Point format
            global_encoding: Global encoding byte
            project_id: Project ID
            system_id: System ID
            software_id: Software ID
            creation_doy: Creation day of year
            creation_year: Creation year
            pdal_metadata: Write PDAL metadata as VLR?
            scale_x: X scale factor
            scale_y: Y scale factor
            scale_z: Z scale factor
            offset_x: X offset
            offset_y: Y offset
            offset_z: Z offset
            vlrs: List of VLRs to set
            enhanced_srs_vlrs: Write WKT2 and PROJJSON as VLR?
            clevel: Complexity level
            stype: Standard type
            ostaid: Origination station ID
            ftitle: File title
            fsclas: File/data segment classification
            oname: Originator's name
            ophone: Originator's phone number
            fsctlh: File control and handling
            fsclsy: File security classification system
            isclas: File security classification
            idatim: Image date and time
            iid2: Image identifier 2
            fscltx: File classification text
            aimidb: Additional (airborne) image ID
            acftb: Aircraft information
            where_merge: If 'where' option is set, describes how skipped points should be merged with kept points in standard mode.
            where: Expression describing points to be passed to this filter
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def null(self,where_merge = 'auto', where = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """Null writer.  Provides a sink for points in a pipeline.  It's the same as sending pipeline output to /dev/null.

        Options:
            where_merge: If 'where' option is set, describes how skipped points should be merged with kept points in standard mode.
            where: Expression describing points to be passed to this filter
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def ogr(self,filename = None, multicount = 1, measure_dim = None, ogrdriver = '', ogr_options = None, attr_dims = None, where_merge = 'auto', where = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """Write a point cloud as a set of OGR points/multipoints

        Options:
            filename: Output filename
            multicount: Group 'multicount' points into a structure
            measure_dim: Use dimensions as a measure value
            ogrdriver: OGR writer driver name
            ogr_options: OGR layer creation options
            attr_dims: Dimension to use as attributes, 'all' for all. Incompatible with multicount>1
            where_merge: If 'where' option is set, describes how skipped points should be merged with kept points in standard mode.
            where: Expression describing points to be passed to this filter
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def pcd(self,filename = None, compression = 'ascii', keep_unspecified = 'true', order = None, precision = 2, where_merge = 'auto', where = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """Write data in the Point Cloud Library (PCL) format.

        Options:
            filename: Output filename
            compression: Level of PCD compression to use (ascii, binary, compressed)
            keep_unspecified: Write all dimensions
            order: Dimension order
            precision: ASCII precision
            where_merge: If 'where' option is set, describes how skipped points should be merged with kept points in standard mode.
            where: Expression describing points to be passed to this filter
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def pgpointcloud(self,output_dims = None, offset_x = None, offset_y = None, offset_z = None, scale_x = 1, scale_y = 1, scale_z = 1, connection = None, table = None, column = 'pa', schema = None, compression = 'dimensional', overwrite = None, srid = 4326, pcid = None, pre_sql = None, post_sql = None, where_merge = 'auto', where = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """Write points to PostgreSQL pgpointcloud output

        Options:
            output_dims: Output dimensions
            offset_x: X offset
            offset_y: Y offset
            offset_z: Z offset
            scale_x: X scale
            scale_y: Y scale
            scale_z: Z scale
            connection: Connection string
            table: Table name
            column: Column name
            schema: Schema name
            compression: Compression type
            overwrite: Whether data should be overwritten
            srid: SRID
            pcid: PCID
            pre_sql: SQL to execute before query
            post_sql: SQL to execute after query
            where_merge: If 'where' option is set, describes how skipped points should be merged with kept points in standard mode.
            where: Expression describing points to be passed to this filter
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def ply(self,filename = None, storage_mode = 'ascii', dims = None, faces = None, sized_types = 'true', precision = 3, where_merge = 'auto', where = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """ply writer

        Options:
            filename: Output filename
            storage_mode: PLY Storage Mode
            dims: Dimension names
            faces: Write faces
            sized_types: Write types as size-explicit strings (e.g. 'uint32')
            precision: Output precision
            where_merge: If 'where' option is set, describes how skipped points should be merged with kept points in standard mode.
            where: Expression describing points to be passed to this filter
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def raster(self,filename = None, gdaldriver = 'GTiff', gdalopts = None, rasters = None, data_type = 'double', nodata = 'NaN', where_merge = 'auto', where = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """Write a raster.

        Options:
            filename: Output filename
            gdaldriver: GDAL driver name
            gdalopts: GDAL driver options (name=value,name=value...)
            rasters: List of raster names to write as bands.
            data_type: Data type for output grid ('int8', 'uint64', 'float', etc.)
            nodata: No data value
            where_merge: If 'where' option is set, describes how skipped points should be merged with kept points in standard mode.
            where: Expression describing points to be passed to this filter
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def sbet(self,filename = None, angles_are_degrees = 'true', where_merge = 'auto', where = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """SBET Writer

        Options:
            filename: Output filename
            angles_are_degrees: Angles coming into the writer are in degrees
            where_merge: If 'where' option is set, describes how skipped points should be merged with kept points in standard mode.
            where: Expression describing points to be passed to this filter
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def text(self,filename = None, format = 'CSV', jscallback = None, keep_unspecified = 'true', order = None, write_header = 'true', newline = '\n', delimiter = ',', quote_header = 'true', precision = 3, where_merge = 'auto', where = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """Text Writer

        Options:
            filename: Output filename
            format: Output format
            jscallback: 
            keep_unspecified: Write all dimensions
            order: Dimension order
            write_header: Whether a header should be written
            newline: String to use as newline
            delimiter: Dimension delimiter
            quote_header: Whether a header should be quoted
            precision: Output precision
            where_merge: If 'where' option is set, describes how skipped points should be merged with kept points in standard mode.
            where: Expression describing points to be passed to this filter
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


    def tiledb(self,filename = None, config_file = None, cell_order = 'auto', tile_order = 'row-major', data_tile_capacity = 100000, x_tile_size = 0, y_tile_size = 0, z_tile_size = 0, time_tile_size = 0, x_domain_st = 0, x_domain_end = 0, y_domain_st = 0, y_domain_end = 0, z_domain_st = 0, z_domain_end = 0, time_domain_st = 0, time_domain_end = 0, scale_x = '0.01', scale_y = '0.01', scale_z = '0.01', offset_x = 0, offset_y = 0, offset_z = 0, chunk_size = 1000000, stats = 'false', filter_profile = 'balanced', compression = None, compression_level = '-1', filters = '{}', append = 'false', use_time_dim = 'false', time_first = 'false', timestamp = 18446744073709551615, combine_bit_fields = 'true', allow_dups = 'true', where_merge = 'auto', where = None, option_file = None, log = None, user_data = None, inputs = None, tag = None):
        """Write data using TileDB.

        Options:
            filename: Output filename
            config_file: TileDB configuration file location
            cell_order: TileDB cell order
            tile_order: TileDB tile order
            data_tile_capacity: TileDB tile capacity
            x_tile_size: TileDB tile size
            y_tile_size: TileDB tile size
            z_tile_size: TileDB tile size
            time_tile_size: TileDB tile size
            x_domain_st: TileDB start of domain in X
            x_domain_end: TileDB end of domain in X
            y_domain_st: TileDB start of domain in Y
            y_domain_end: TileDB end of domain in Y
            z_domain_st: TileDB start of domain in Z
            z_domain_end: TileDB end of domain in Z
            time_domain_st: TileDB start of domain in GpsTime
            time_domain_end: TileDB end of domain in GpsTime
            scale_x: Scale factor to use for default x float-scale filter
            scale_y: Scale factor to use for default y float-scale fitler
            scale_z: Scale factor to use for default z float-scale filter
            offset_x: Add offset to use for default x float-scale filter
            offset_y: Add offset to use for default y float-scale filter
            offset_z: Add offset to use fo default x float-scale filter
            chunk_size: Point cache size for chunked writes
            stats: Dump TileDB query stats to stdout
            filter_profile: Filter profile to use for compression filters
            compression: TileDB compression type for attributes
            compression_level: TileDB compression level
            filters: Specify filter and level per dimension/attribute
            append: Append to existing TileDB array
            use_time_dim: Use GpsTime coordinate data as array dimension
            time_first: If writing 4D array with XYZ and Time, choose to put time dim first or last (default)
            timestamp: TileDB array timestamp
            combine_bit_fields: Combine all bit fields into a single 2 byte attribute
            allow_dups: Allow duplicate points (default is True)
            where_merge: If 'where' option is set, describes how skipped points should be merged with kept points in standard mode.
            where: Expression describing points to be passed to this filter
            option_file: File from which to read additional options
            log: Debug output filename
            user_data: User JSON
            inputs: 
            tag: 
        """


