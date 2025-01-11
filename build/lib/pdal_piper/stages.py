class _GenericStage:
  def __init__(self,name, **kwargs):
      if 'classification' in kwargs.keys():
          kwargs['class'] = kwargs['classification']
          del (kwargs['classification'])
      self.name = name
      self.args = tuple(kwargs.items())
      self.args = tuple([arg for arg in self.args if (arg[1] is not None)])

class expression(_GenericStage):
    """
---
orphan: true
---

(pdal_expression)=

# Expression Syntax

The PDAL expression syntax is a subset of that found in a great many programming languages.
Specifically, it uses a limited set of operators from the C language. Dimension names
can be used where a variable or constant would be used. Double-precision constants are
supported.

All mathematical operations are done with double-precision floating point. There is no
automatic conversion of numeric values to logical values.  For example, the following is
not permitted:

```
((Intensity > 0) && Classification)
```

Instead, you must write:

```
((Intensity > 0) && (Classification != 0))
```

## Mathematical Operators

```{eval-rst}
.. list-table::
    :widths: 10 30 30
    :header-rows: 1

    * - Operator
      - Function
      - Example
    * - `*`
      - Multiplication
      - Intensity * 64.0
    * - /
      - Division
      - Green / 255
    * - `+`
      - Addition
      - Classification + 255
    * - `-`
      - Subtraction
      - X /- 64215.2
```

## Logical Operators

```{eval-rst}
.. list-table::
    :widths: 10 30 30
    :header-rows: 1

    * - Operator
      - Function
      - Example
    * - !
      - Not
      - !(X < 25)
    * - `>`
      - Greater
      - X > 52.523
    * - >=
      - Greater Than or Equal
      - X >= 52.523
    * - `<`
      - Less
      - Y < -28.456
    * - <=
      - Less Than or Equal
      - X <= 0
    * - ==
      - Equal
      - Classification == 7
    * - !=
      - Not Equal
      - Classification != 7
    * - &&
      - And
      - Classification == 7 && Intensity > 64
    * - ||
      - Or
      - Classification == 7 || Classification == 8
```

The order or operations is as listed, which matches that of the C language. Parentheses are
supported to alter the order of operations.

## Examples

```
((Classification == 7 || Classification == 8) && NumberOfReturns == 1)
```

Selects points with a classification of 7 or 8 and number of returns equal to 1.  Note
that in this case the parentheses are necessary.

```
X > 2500 && X < 4700 && Y > 0
```

Selects points with an X between 2500 and 4700 and a positive Y value.

```
(NumberOfReturns > 1 && ReturnNumber == 1)
```

Selects "first" returns from a laser pulse.

```
!(NumberOfReturns == 1)
```

Selects only those points where the laser pulse generated multiple returns.
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('expression', **args)
 
class filters_approximatecoplanar(_GenericStage):
    """
(filters.approximatecoplanar)=

# filters.approximatecoplanar

The **approximate coplanar filter** implements a portion of the algorithm
presented
in {cite:p}`limberger2015real`. Prior to clustering points, the authors first apply an
approximate coplanarity test, where points that meet the following criteria are
labeled as approximately coplanar.

$$
/lambda_2 > (s_{/alpha}/lambda_1) /&/& (s_{/beta}/lambda_2) > /lambda_3
$$

$/lambda_1$, $/lambda_2$, $/lambda_3$ are the eigenvalues of
a neighborhood of points (defined by `knn` nearest neighbors) in ascending
order. The threshold values $s_{/alpha}$ and $s_{/beta}$ are
user-defined and default to 25 and 6 respectively.

The filter returns a point cloud with a new dimension `Coplanar` that
indicates those points that are part of a neighborhood that is approximately
coplanar (1) or not (0).

```{eval-rst}
.. embed::
```

## Example

The sample pipeline presented below estimates the planarity of a point based on
its eight nearest neighbors using the approximate coplanar filter. A
{ref}`filters.range` stage then filters out any points that were not
deemed to be coplanar before writing the result in compressed LAZ.

```json
[
    "input.las",
    {
        "type":"filters.approximatecoplanar",
        "knn":8,
        "thresh1":25,
        "thresh2":6
    },
    {
        "type":"filters.range",
        "limits":"Coplanar[1:1]"
    },
    "output.laz"
]
```

## Options

knn

: The number of k-nearest neighbors. /[Default: 8/]

thresh1

: The threshold to be applied to the smallest eigenvalue. /[Default: 25/]

thresh2

: The threshold to be applied to the second smallest eigenvalue. /[Default: 6/]

```{include} filter_opts.md
```
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('filters.approximatecoplanar', **args)
 
class filters_assign(_GenericStage):
    """
(filters.assign)=

# filters.assign

The assign filter allows you set the value of a dimension for all points
to a provided value that pass a range filter.

```{embed}
```

```{streamable}
```

```{note}
The `assignment` and `condition` options are deprecated and may be removed in a
future release.
```



(assignment_expressions)=

# Assignment Expressions

The assignment expression syntax is an expansion on the {ref}`PDAL expression <pdal_expression>` syntax
that provides for assignment of values to points. The generic expression is:

```
"value" : "Dimension = ValueExpression [WHERE ConditionalExpression)]"
```

`Dimension` is the name of a PDAL dimension.

A `ValueExpression` consists of constants, dimension names and mathematical operators
that evaluates to a numeric value.  The supported mathematical operations are addition(`+`),
subtraction(`-`), multiplication(`*`) and division(`//`).

A {ref}`ConditionalExpression <pdal_expression>` is an optional boolean value that must
evaluate to `true` for the `ValueExpression` to be applied.

```{note}
As of PDAL 2.7.0, assignment to a dimension that does not exist will cause
it to be created. It will always be created with type double, however.
```

# Example 1

```json
[
    "input.las",
    {
        "type": "filters.assign",
        "value" : "Red = Red / 256"
    },
    "output.laz"
]
```

This scales the `Red` value by 1/256. If the input values are in the range 0 - 65535, the output
value will be in the range 0 - 255.

# Example 2

```json
[
    "input.las",
    {
        "type": "filters.assign",
        "value" : [
            "Red = Red * 256",
            "Green = Green * 256",
            "Blue = Blue * 256"
        ]
    },
    "output.laz"
]
```

This scales the values of Red, Green and Blue by 256. If the input values are in the range 0 - 255, the output
value will be in the range 0 - 65535. This can be handy when creating a {ref}`COPC <writers.copc>` file which
(as defined in LAS 1.4) needs color values scaled in that range.

# Example 3

```json
[
    "input.las",
    {
        "type": "filters.assign",
        "value": [
            "Classification = 2 WHERE HeightAboveGround < 5",
            "Classification = 1 WHERE HeightAboveGround >= 5"
        ]
    },
    "output.laz"
]
```

This sets the classification of points to either `Ground` or `Unassigned` depending on the
value of the `HeightAboveGround` dimension.

# Example 4

```json
[
    "input.las",
    {
        "type": "filters.assign",
        "value": [
            "X = 1",
            "X = 2 WHERE X > 10"
        ]
    },
    "output.laz"
]
```

This sets the value of `X` for all points to 1. The second statement is essentially ignored
since the first statement sets the `X` value of all points to 1 and therefore no points
the `ConditionalExpression` of the second statement.

## Options

assignment

: A {ref}`range <ranges>` followed by an assignment of a value (see example).
  Can be specified multiple times.  The assignments are applied sequentially
  to the dimension value as set when the filter began processing. /[Required/]

condition

: A single {ref}`ranges <ranges>` that a point's values must pass in order
  for the assignment to be performed. /[Default: none/] /[Deprecated - use 'value'/]

value

: A list of {ref}`assignment expressions <assignment_expressions>` to be applied to points.
  The list of values is evaluated in order. /[Default: none/]

```{include} filter_opts.md
```
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('filters.assign', **args)
 
class filters_chipper(_GenericStage):
    """
(filters.chipper)=

# filters.chipper

The **Chipper Filter** takes a single large point cloud and converts it
into a set
of smaller clouds, or chips. The chips are all spatially contiguous and
non-overlapping, so the result is an irregular tiling of the input data.

```{note}
Each chip will have approximately, but not exactly, the [capacity] point
count specified.
```

```{seealso}
The {ref}`PDAL split command <split_command>` utilizes the
{ref}`filters.chipper` to split data by capacity.
```

```{figure} filters.chipper.img1.png
:alt: Points before chipping
:scale: 100 %

Before chipping, the points are all in one collection.
```

```{figure} filters.chipper.img2.png
:alt: Points after chipping
:scale: 100 %

After chipping, the points are tiled into smaller contiguous chips.
```

Chipping is usually applied to data read from files (which produce one large
stream of points) before the points are written to a database (which prefer
data segmented into smaller blocks).

```{eval-rst}
.. embed::
```

## Example

```json
[
    "example.las",
    {
        "type":"filters.chipper",
        "capacity":"400"
    },
    {
        "type":"writers.pgpointcloud",
        "connection":"dbname='lidar' user='user'"
    }
]
```

## Options

capacity

: How many points to fit into each chip. The number of points in each chip will
  not exceed this value, and will sometimes be less than it. /[Default: 5000/]

```{include} filter_opts.md
```
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('filters.chipper', **args)
 
class filters_cluster(_GenericStage):
    """
(filters.cluster)=

# filters.cluster

The Cluster filter first performs Euclidean Cluster Extraction on the input
`PointView` and then labels each point with its associated cluster ID.
It creates a new dimension `ClusterID` that contains the cluster ID value.
Cluster IDs start with the value 1.  Points that don't belong to any
cluster will are given a cluster ID of 0.

```{eval-rst}
.. embed::
```

## Example

```json
[
    "input.las",
    {
        "type":"filters.cluster"
    },
    {
        "type":"writers.bpf",
        "filename":"output.bpf",
        "output_dims":"X,Y,Z,ClusterID"
    }
]
```

## Options

min_points

: Minimum number of points to be considered a cluster. /[Default: 1/]

max_points

: Maximum number of points to be considered a cluster. /[Default: 2^64 - 1/]

tolerance

: Cluster tolerance - maximum Euclidean distance for a point to be added to the
  cluster. /[Default: 1.0/]

is3d

: By default, clusters are formed by considering neighbors in a 3D sphere, but
  if `is3d` is set to false, it will instead consider neighbors in a 2D
  cylinder (XY plane only). /[Default: true/]

```{include} filter_opts.md
```
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('filters.cluster', **args)
 
class filters_colorinterp(_GenericStage):
    """
(filters.colorinterp)=

# filters.colorinterp

The color interpolation filter assigns scaled RGB values from an image based on
a given dimension.  It provides three possible approaches:

1. You provide a [minimum] and [maximum], and the data are scaled for the
   given [dimension] accordingly.
2. You provide a [k] and a [mad] setting, and the scaling is set based on
   Median Absolute Deviation.
3. You provide a [k] setting and the scaling is set based on the
   [k]-number of standard deviations from the median.

You can provide your own [GDAL]-readable image for the scale color factors,
but a number of pre-defined ramps are embedded in PDAL.  The default ramps
provided by PDAL are 256x1 RGB images, and might be a good starting point for
creating your own scale factors. See [Default Ramps] for more information.

```{note}
{ref}`filters.colorinterp` will use the entire band to scale the colors.
```

```{eval-rst}
.. embed::
```

## Example

```json
[
    "uncolored.las",
    {
      "type":"filters.colorinterp",
      "ramp":"pestel_shades",
      "mad":true,
      "k":1.8,
      "dimension":"Z"
    },
    "colorized.las"
]
```

```{figure} ../images/pestel_scaled_helheim.png
:scale: 80%

Image data with interpolated colors based on `Z` dimension and `pestel_shades`
ramp.
```

## Default Ramps

PDAL provides a number of default color ramps you can use in addition to
providing your own. Give the ramp name as the [ramp] option to the filter
and it will be used. Otherwise, provide a [GDAL]-readable raster filename.

### `awesome_green`

```{image} ../images/awesome-green.png
:alt: awesome-green color ramp
:scale: 400%
```

### `black_orange`

```{image} ../images/black-orange.png
:alt: black-orange color ramp
:scale: 400%
```

### `blue_orange`

```{image} ../images/blue-orange.png
:alt: blue-orange color ramp
:scale: 400%
```

### `blue_hue`

```{image} ../images/blue-hue.png
:alt: blue-hue color ramp
:scale: 400%
```

### `blue_orange`

```{image} ../images/blue-orange.png
:alt: blue-orange color ramp
:scale: 400%
```

### `blue_red`

```{image} ../images/blue-red.png
:alt: blue-red color ramp
:scale: 400%
```

### `heat_map`

```{image} ../images/heat-map.png
:alt: heat-map color ramp
:scale: 400%
```

### `pestel_shades`

```{image} ../images/pestel-shades.png
:alt: pestel-shades color ramp
:scale: 400%
```

## Options

ramp

: The raster file to use for the color ramp. Any format supported by [GDAL]
  may be read.  Alternatively, one of the default color ramp names can be
  used. /[Default: "pestel_shades"/]

dimension

: A dimension name to use for the values to interpolate colors. /[Default: "Z"/]

minimum

: The minimum value to use to scale the data. If none is specified, one is
  computed from the data. If one is specified but a [k] value is also
  provided, the [k] value will be used.

maximum

: The maximum value to use to scale the data. If none is specified, one is
  computed from the data. If one is specified but a [k] value is also
  provided, the [k] value will be used.

invert

: Invert the direction of the ramp? /[Default: false/]

k

: Color based on the given number of standard deviations from the median. If
  set, [minimum] and [maximum] will be computed from the median and setting
  them will have no effect.

mad

: If true, [minimum] and [maximum] will be computed by the median absolute
  deviation. See {ref}`filters.mad` for discussion. /[Default: false/]

mad_multiplier

: MAD threshold multiplier. Used in conjunction with [k] to threshold the
  differencing. /[Default: 1.4862/]

```{include} filter_opts.md
```

[gdal]: http://www.gdal.org
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('filters.colorinterp', **args)
 
class filters_colorization(_GenericStage):
    """
(filters.colorization)=

# filters.colorization

The colorization filter populates dimensions in the point buffer using input
values read from a raster file. Commonly this is used to add Red/Green/Blue
values to points from an aerial photograph of an area. However, any band can be
read from the raster and applied to any dimension name desired.

```{figure} filters.colorization.img1.jpg
:alt: Points after colorization
:scale: 50 %

After colorization, points take on the colors provided by the input image
```

```{note}
[GDAL] is used to read the color information and any GDAL-readable
supported [format] can be read.
```

The bands of the raster to apply to each are selected using the "band" option,
and the values of the band may be scaled before being written to the dimension.
If the band range is 0-1, for example, it might make sense to scale by 256 to
fit into a traditional 1-byte color value range.

```{eval-rst}
.. embed::
```

```{eval-rst}
.. streamable::
```

## Example

```json
[
    "uncolored.las",
    {
      "type":"filters.colorization",
      "dimensions":"Red:1:1.0, Blue, Green::256.0",
      "raster":"aerial.tif"
    },
    "colorized.las"
]
```

## Considerations

Certain data configurations can cause degenerate filter behavior.
One significant knob to adjust is the `GDAL_CACHEMAX` environment
variable. One driver which can have issues is when a [TIFF] file is
striped vs. tiled. GDAL's data access in that situation is likely to
cause lots of re-reading if the cache isn't large enough.

Consider a striped TIFF file of 286mb:

```
-rw-r-----@  1 hobu  staff   286M Oct 29 16:58 orth-striped.tif
```

```json
[
    "colourless.laz",
    {
      "type":"filters.colorization",
      "raster":"orth-striped.tif"
    },
    "coloured-striped.las"
]
```

Simple application of the {ref}`filters.colorization` using the striped [TIFF]
with a 268mb {ref}`readers.las` file will take nearly 1:54.

```
[hobu@pyro knudsen (master)]$ time ~/dev/git/pdal/bin/pdal pipeline -i striped.json

real    1m53.477s
user    1m20.018s
sys 0m33.397s
```

Setting the `GDAL_CACHEMAX` variable to a size larger than the TIFF file
dramatically speeds up the color fetching:

```
[hobu@pyro knudsen (master)]$ export GDAL_CACHEMAX=500
[hobu@pyro knudsen (master)]$ time ~/dev/git/pdal/bin/pdal pipeline striped.json

real    0m19.034s
user    0m15.557s
sys 0m1.102s
```

## Options

raster

: The raster file to read the band from. Any [format] supported by
  [GDAL] may be read.

dimensions

: A comma separated list of dimensions to populate with values from the raster
  file. Dimensions will be created if they don't already exist.  The format
  of each dimension is /<name>:/<band_number>:/<scale_factor>.
  Either or both of band number and scale factor may be omitted as may ':'
  separators if the data is not ambiguous.  If not supplied, band numbers
  begin at 1 and increment from the band number of the previous dimension.
  If not supplied, the scaling factor is 1.0.
  /[Default: "Red:1:1.0, Green:2:1.0, Blue:3:1.0"/]

```{include} filter_opts.md
```

[format]: https://www.gdal.org/formats_list.html
[gdal]: http://www.gdal.org
[tiff]: http://www.gdal.org/frmt_gtiff.html
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('filters.colorization', **args)
 
class filters_covariancefeatures(_GenericStage):
    """
(filters.covariancefeatures)=

# filters.covariancefeatures

This filter implements various local feature descriptors that are based on the
covariance matrix of a point's neighborhood.

The user can pick a set of feature descriptors by setting the `feature_set`
option. The [dimensionality] set of feature descriptors introduced below is the
default. The user can also provide a comma-separated list of features to
explicitly itemize those covariance features they wish to be computed. This can
be combined with any suppported presets like "Dimensionality".  Specifying "all"
will compute all available features.

Supported features include:

- Anisotropy
- DemantkeVerticality
- Density
- Eigenentropy
- Linearity
- Omnivariance
- Planarity
- Scattering
- EigenvalueSum
- SurfaceVariation
- Verticality

```{note}
Density requires both `OptimalKNN` and `OptimalRadius` which can be
computed by running {ref}`filters.optimalneighborhood` prior to
`filters.covariancefeatures`.
```

## Example #1

```json
[
    "input.las",
    {
        "type":"filters.covariancefeatures",
        "knn":8,
        "threads": 2,
        "feature_set": "Dimensionality"
    },
    {
        "type":"writers.bpf",
        "filename":"output.bpf",
        "output_dims":"X,Y,Z,Linearity,Planarity,Scattering,Verticality"
    }
]
```

## Example #2

```json
[
    "input.las",
    {
        "type":"filters.optimalneighborhood"
    },
    {
        "type":"filters.covariancefeatures",
        "knn":8,
        "threads": 2,
        "optimized":true,
        "feature_set": "Linearity,Omnivariance,Density"
    },
    {
        "type":"writers.las",
        "minor_version":4,
        "extra_dims":"all",
        "forward":"all",
        "filename":"output.las"
    }
]
```

## Options

knn

: The number of k nearest neighbors used for calculating the covariance matrix.
  /[Default: 10/]

threads

: The number of threads to use. Only valid in {ref}`standard mode <processing_modes>`. /[Default: 1/]

feature_set

: A comma-separated list of individual features or feature presets (e.g.,
  "Dimensionality") to be computed. To compute all available features, specify
  "all". /[Default: "Dimensionality"/]

stride

: When finding k nearest neighbors, stride determines the sampling rate. A
  stride of 1 retains each neighbor in order. A stride of two selects every
  other neighbor and so on. /[Default: 1/]

min_k

: Minimum number of neighbors in radius (radius search only). /[Default: 3/]

radius

: If radius is specified, neighbors will be obtained by radius search rather
  than k nearest neighbors, subject to meeting the minimum number of neighbors
  (`min_k`).

mode

: By default, features are computed using the standard deviation along each
  eigenvector, i.e., using the square root of the computed eigenvalues
  (`mode="SQRT"`). `mode` also accepts "Normalized" which normalizes
  eigenvalue such that they sum to one, or "Raw" such that the eigenvalues are
  used directly. /[Default: "SQRT"/]

optimized

: `optimized` can be set to `true` to enable computation of features using
  precomputed optimal neighborhoods (found in the `OptimalKNN` dimension).
  Requires {ref}`filters.optimalneighborhood` be run prior to this stage.
  /[Default: false/]

```{include} filter_opts.md
```

(dimensionality)=

### Dimensionality feature set

The features introduced in {cite:p}`demantke2011dimensionality` describe the shape of the
neighborhood, indicating whether the local geometry is more linear (1D), planar
(2D) or volumetric (3D) while the one introduced in {cite:p}`guinard2017weakly` adds the
idea of a structure being vertical.

The dimensionality filter introduces the following four descriptors that are
computed from the covariance matrix of a point's neighbors (as defined by
`knn` or `radius`):

- linearity - higher for long thin strips
- planarity - higher for planar surfaces
- scattering - higher for complex 3d neighbourhoods
- verticality - higher for vertical structures, highest for thin vertical strips

It introduces four new dimensions that hold each one of these values:
`Linearity`, `Planarity`, `Scattering` and `Verticality`.
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('filters.covariancefeatures', **args)
 
class filters_cpd(_GenericStage):
    """
(filters.cpd)=

# filters.cpd

<!-- Missing citations in references.bib, make sure to add. Also the syntax is wrong here. -->

The **Coherent Point Drift (CPD) filter** uses the algorithm of
{cite}`Myronenko` algorithm to
compute a rigid, nonrigid, or affine transformation between datasets.  The
rigid and affine are what you'd expect; the nonrigid transformation uses Motion
Coherence Theory {cite}`Yuille1998` to "bend" the points to find a best
alignment.

```{note}
CPD is computationally intensive and can be slow when working with many
points (i.e. > 10,000).  Nonrigid is significantly slower
than rigid and affine.
```

The first input to the change filter are considered the "fixed" points, and all
subsequent inputs are "moving" points.  The output from the change filter are
the "moving" points after the calculated transformation has been applied, one
point view per input.  Any additional information about the cpd registration,
e.g. the rigid transformation matrix, will be placed in the stage's metadata.

## When to use CPD vs ICP

Summarized from the [Non-rigid point set registration: Coherent Point Drift](http://graphics.stanford.edu/courses/cs468-07-winter/Papers/nips2006_0613.pdf) paper.

- CPD outperforms the ICP in the presence of noise and outliers by the use of
  a probabilistic assignment of correspondences between pointsets, which is
  innately more robust than the binary assignment used in ICP.
- CPD does not work well for large in-plane rotation, such transformation can
  be first compensated by other well known global registration techniques before
  CPD algorithm is carried out
- CPD is most effective when estimating smooth non-rigid transformations.

```{eval-rst}
.. plugin::
```

## Examples

```json
[
    "fixed.las",
    "moving.las",
    {
        "type": "filters.cpd",
        "method": "rigid"
    },
    "output.las"
]
```

If [](method) is not provided, the cpd filter will default to using the
rigid registration method.  To get the transform matrix, you'll need to
use the "metadata" option of the pipeline command:

```
$ pdal pipeline cpd-pipeline.json --metadata cpd-metadata.json
```

The metadata output might start something like:

```json
{
    "stages":
    {
        "filters.cpd":
        {
            "iterations": 10,
            "method": "rigid",
            "runtime": 0.003839,
            "sigma2": 5.684342128e-16,
            "transform": "           1 -6.21722e-17  1.30104e-18  5.29303e-11-8.99346e-17            1  2.60209e-18 -3.49247e-10 -2.1684e-19  1.73472e-18            1 -1.53477e-12           0            0            0            1"
        },
    },
```

```{seealso}
{ref}`filters.transformation` to apply a transform to other points.
{ref}`filters.icp` for deterministic binary point pair assignments.
```

## Options

(method)=
method

: Change detection method to use.
  Valid values are "rigid", "affine", and "nonrigid".
  /[Default: "rigid""/]

```{include} filter_opts.md
```

<!-- ```{eval-rst}
.. bibliography:: references.bib
```

[coherent point drift (cpd)]: https://github.com/gadomski/cpd -->
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('filters.cpd', **args)
 
class filters_crop(_GenericStage):
    """
(filters.crop)=

# filters.crop

The **crop filter** removes points that fall outside or inside a
cropping bounding
box (2D or 3D), polygon, or point+distance.  If more than one bounding region is
specified, the filter will pass all input points through each bounding region,
creating an output point set for each input crop region.

```{eval-rst}
.. embed::
```

```{eval-rst}
.. streamable::
```

The provided bounding regions are assumed to have the same spatial reference
as the points unless the option [a_srs] provides an explicit spatial reference
for bounding regions.
If the point input consists of multiple point views with differing
spatial references, one is chosen at random and assumed to be the
spatial reference of the input bounding region.  In this case a warning will
be logged.

## Example 1

This example crops an input point cloud using a square polygon.

```json
[
    "file-input.las",
    {
        "type":"filters.crop",
        "bounds":"([0,1000000],[0,1000000])"
    },
    {
        "type":"writers.las",
        "filename":"file-cropped.las"
    }
]
```

## Example 2

This example crops all points more than 500 units in any direction from a point.

```json
[
    "file-input.las",
    {
        "type":"filters.crop",
        "point":"POINT(0 0 0)",
        "distance": 500
    },
    {
        "type":"writers.las",
        "filename":"file-cropped.las"
    }
]
```

## Options

bounds

: The extent of the clipping rectangle in the format
  `"([xmin, xmax], [ymin, ymax])"`.  This option can be specified more than
  once by placing values in an array.

  ```{note}
  3D bounds can be given in the form `([xmin, xmax], [ymin, ymax], [zmin, zmax])`.
  ```

  ```{warning}
  If a 3D bounds is given to the filter, a 3D crop will be attempted, even
  if the Z values are invalid or inconsistent with the data.
  ```

polygon

: The clipping polygon, expressed in a well-known text string,
  eg: `"POLYGON((0 0, 5000 10000, 10000 0, 0 0))"`.  This option can be
  specified more than once by placing values in an array.

ogr

: A JSON object representing an OGR query to fetch polygons to use for filtering. The polygons
  fetched from the query are treated exactly like those specified in the `polygon` option.
  The JSON object is specified as follows:

```{include} ogr_json.md
```



outside

: Invert the cropping logic and only take points outside the cropping
  bounds or polygon. /[Default: false/]

point

: An array of WKT or GeoJSON 2D or 3D points (eg: `"POINT(0 0 0)"`). Requires [distance].

distance

: Distance (radius) in units of common X, Y, and Z {ref}`dimensions` in combination with [point]. Passing a 2D point will crop using a circle. Passing a 3D point will crop using a sphere.

a_srs

: Indicates the spatial reference of the bounding regions.  If not provided,
  it is assumed that the spatial reference of the bounding region matches
  that of the points.

```{include} filter_opts.md
```

## Notes

1. See {ref}`workshop-clipping`: and {ref}`clipping` for example usage scenarios for {ref}`filters.crop`.
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('filters.crop', **args)
 
class filters_csf(_GenericStage):
    """
(filters.csf)=

# filters.csf

The **Cloth Simulation Filter (CSF)** classifies ground points based on the
approach outlined in {cite:p}`zhang2016easy`.

```{eval-rst}
.. embed::
```

## Example

The sample pipeline below uses CSF to segment ground and non-ground returns,
using default options, and writing only the ground returns to the output file.

```json
[
    "input.las",
    {
        "type":"filters.csf"
    },
    {
        "type":"filters.range",
        "limits":"Classification[2:2]"
    },
    "output.laz"
]
```

## Options

resolution

: Cloth resolution. /[Default: **1.0**/]

ignore

: A {ref}`range <ranges>` of values of a dimension to ignore.

returns

: Return types to include in output.  Valid values are "first", "last",
  "intermediate" and "only". /[Default: **"last, only"**/]

threshold

: Classification threshold. /[Default: **0.5**/]

hdiff

: Height difference threshold. /[Default: **0.3**/]

smooth

: Perform slope post-processing? /[Default: **true**/]

step

: Time step. /[Default: **0.65**/]

rigidness

: Rigidness. /[Default: **3**/]

iterations

: Maximum number of iterations. /[Default: **500**/]

```{include} filter_opts.md
```
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('filters.csf', **args)
 
class filters_dbscan(_GenericStage):
    """
(filters.dbscan)=

# filters.dbscan

The DBSCAN filter performs Density-Based Spatial Clustering of Applications
with Noise (DBSCAN) {cite:p}`ester1996density` and labels each point with its associated
cluster ID. Points that do not belong to a cluster are given a Cluster ID of
-1. The remaining clusters are labeled as integers starting from 0.

```{eval-rst}
.. embed::
```

```{versionadded} 2.1
```

## Example

```json
[
    "input.las",
    {
        "type":"filters.dbscan",
        "min_points":10,
        "eps":2.0,
        "dimensions":"X,Y,Z"
    },
    {
        "type":"writers.bpf",
        "filename":"output.bpf",
        "output_dims":"X,Y,Z,ClusterID"
    }
]
```

## Options

min_points

: The minimum cluster size `min_points` should be greater than or equal to
  the number of dimensions (e.g., X, Y, and Z) plus one. As a rule of thumb,
  two times the number of dimensions is often used. /[Default: 6/]

eps

: The epsilon parameter can be estimated from a k-distance graph (for k =
  `min_points` minus one). `eps` defines the Euclidean distance that will
  be used when searching for neighbors. /[Default: 1.0/]

dimensions

: Comma-separated string indicating dimensions to use for clustering. /[Default: X,Y,Z/]

```{include} filter_opts.md
```
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('filters.dbscan', **args)
 
class filters_decimation(_GenericStage):
    """
(filters.decimation)=

# filters.decimation

The **decimation filter** retains every Nth point from an input point view.

```{eval-rst}
.. embed::
```

```{eval-rst}
.. streamable::
```

## Example

```json
[
    {
        "type": "readers.las",
        "filename": "larger.las"
    },
    {
        "type":"filters.decimation",
        "step": 10
    },
    {
        "type":"writers.las",
        "filename":"smaller.las"
    }
]
```

## Options

step

: Number of points to skip between each sample point.  A step of 1 will skip
  no points.  A step of 2 will skip every other point.  A step of 100 will
  reduce the input by ~99%. A step of 1.6 will retain `100 / 1.6 = 62.5%` of
  the points. /[Default: 1.0/]

offset

: Point index to start sampling.  Point indexes start at 0.  /[Default: 0/]

limit

: Point index at which sampling should stop (exclusive).  /[Default: No limit/]

```{include} filter_opts.md
```
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('filters.decimation', **args)
 
class filters_delaunay(_GenericStage):
    """
(filters.delaunay)=

# filters.delaunay

The **Delaunay Filter** creates a triangulated mesh fulfilling the Delaunay
condition from a collection of points.

The filter is implemented using the [delaunator-cpp] library, a C++ port of
the JavaScript [Delaunator] library.

The filter currently only supports 2D Delaunay triangulation, using the `X`
and `Y` dimensions of the point cloud.

```{eval-rst}
.. embed::
```

## Example

```json
[
    "input.las",
    {
        "type": "filters.delaunay"
    },
    {
        "type": "writers.ply",
        "filename": "output.ply",
        "faces": true
    }
]
```

## Options

```{include} filter_opts.md
```

[delaunator]: https://github.com/mapbox/delaunator
[delaunator-cpp]: https://github.com/delfrrr/delaunator-cpp
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('filters.delaunay', **args)
 
class filters_dem(_GenericStage):
    """
(filters.dem)=

# filters.dem

The **DEM filter** uses a source raster to keep point cloud data within
a each cell within a computed range.
For example, atmospheric or MTA noise in a scene can be quickly
removed by keeping all data within 100m above and 20m below a preexisting
elevation model.

```{eval-rst}
.. embed::
```

## Example

```json
[
    {
        "type":"filters.dem",
        "raster":"dem.tif",
        "limits":"Z[20:100]"
    }
]
```

## Options

limits

: A {ref}`range <ranges>` that defines the dimension and the magnitude above
  and below the value of the given dimension to filter.

  For example "Z/[20:100/]" would keep all `Z` point cloud values that are
  within 100 units above and 20 units below the elevation model value at the
  given `X` and `Y` value.

raster

: [GDAL readable raster] data to use for filtering.

band

: GDAL Band number to read (count from 1) /[Default: 1/]

```{include} filter_opts.md
```

[gdal]: http://gdal.org
[gdal readable raster]: http://www.gdal.org/formats_list.html
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('filters.dem', **args)
 
class filters_divider(_GenericStage):
    """
(filters.divider)=

# filters.divider

The **Divider Filter** breaks a point view into a set of smaller point views
based on simple criteria.  The number of subsets can be specified explicitly,
or one can specify a maximum point count for each subset.  Additionally,
points can be placed into each subset sequentially (as they appear in the
input) or in round-robin fashion.

Normally points are divided into subsets to facilitate output by writers
that support creating multiple output files with a template (LAS and BPF
are notable examples).

```{eval-rst}
.. embed::
```

## Example

This pipeline will create 10 output files from the input file readers.las.

```json
[
    "example.las",
    {
        "type":"filters.divider",
        "count":"10"
    },
    {
        "type":"writers.las",
        "filename":"out_#.las"
    }
]
```

## Options

mode

: A mode of "partition" will write sequential points to an output view until
  the view meets its predetermined size. "round_robin" mode will iterate
  through the output views as it writes sequential points.
  /[Default: "partition"/]

count

: Number of output views.  /[Default: none/]

capacity

: Maximum number of points in each output view.  Views will contain
  approximately equal numbers of points.  /[Default: none/]

```{include} filter_opts.md
```

```{warning}
You must specify exactly one of either [count] or [capacity].
```
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('filters.divider', **args)
 
class filters_eigenvalues(_GenericStage):
    """
(filters.eigenvalues)=

# filters.eigenvalues

The **eignvalue filter** returns the eigenvalues for a given point,
based on its k-nearest neighbors.

The filter produces three new dimensions (`Eigenvalue0`, `Eigenvalue1`, and
`Eigenvalue2`), which can be analyzed directly, or consumed by downstream
stages for more advanced filtering. The eigenvalues are sorted in ascending
order.

The eigenvalue decomposition is performed using Eigen's
[SelfAdjointEigenSolver].

```{eval-rst}
.. embed::

```

## Example

This pipeline demonstrates the calculation of the eigenvalues. The newly created
dimensions are written out to BPF for further inspection.

```json
[
    "input.las",
    {
        "type":"filters.eigenvalues",
        "knn":8
    },
    {
        "type":"writers.bpf",
        "filename":"output.bpf",
        "output_dims":"X,Y,Z,Eigenvalue0,Eigenvalue1,Eigenvalue2"
    }
]
```

## Options

knn

: The number of k-nearest neighbors. /[Default: 8/]

normalize

: Normalize eigenvalues such that the sum is 1. /[Default: false/]

```{include} filter_opts.md
```

[selfadjointeigensolver]: https://eigen.tuxfamily.org/dox/classEigen_1_1SelfAdjointEigenSolver.html
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('filters.eigenvalues', **args)
 
class filters_elm(_GenericStage):
    """
(filters.elm)=

# filters.elm

The Extended Local Minimum (ELM) filter marks low points as noise. This filter
is an implementation of the method described in {cite:p}`chen2012upward`.

ELM begins by rasterizing the input point cloud data at the given {ref}`cell` size.
Within each cell, the lowest point is considered noise if the next lowest point
is a given threshold above the current point. If it is marked as noise, the
difference between the next two points is also considered, marking points as
noise if needed, and continuing until another neighbor is found to be within the
threshold. At this point, iteration for the current cell stops, and the next
cell is considered.

```{eval-rst}
.. embed::
```

## Example #1

The following PDAL pipeline applies the ELM filter, using a {ref}`cell` size of 20
and
applying the {ref}`classification <class>` code of 18 to those points
determined to be noise.

```json
{
  "pipeline":[
    "input.las",
    {
      "type":"filters.elm",
      "cell":20.0,
      "class":18
    },
    "output.las"
  ]
}
```

## Example #2

This variation of the pipeline begins by assigning a value of 0 to all
classifications, thus resetting any existing classifications. It then proceeds
to compute ELM with a {ref}`threshold` value of 2.0, and finishes by extracting all
returns that are not marked as noise.

```json
[
    "input.las",
    {
        "type":"filters.assign",
        "assignment":"Classification[:]=0"
    },
    {
        "type":"filters.elm",
        "threshold":2.0
    },
    {
        "type":"filters.range",
        "limits":"Classification![7:7]"
    },
    "output.las"
]
```

## Options

(cell)=
cell

: Cell size. /[Default: 10.0/]

(class)=
class

: Classification value to apply to noise points. /[Default: 7/]

(threshold)=
threshold

: Threshold value to identify low noise points. /[Default: 1.0/]

```{include} filter_opts.md
```
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('filters.elm', **args)
 
class filters_estimaterank(_GenericStage):
    """
(filters.estimaterank)=

# filters.estimaterank

The **rank estimation filter** uses singular value decomposition (SVD) to
estimate the rank of a set of points. Point sets with rank 1 correspond
to linear features, while sets with rank 2 correspond to planar features.
Rank 3 corresponds to a full 3D feature. In practice this can be used alone, or
possibly in conjunction with other filters to extract features (e.g.,
buildings, vegetation).

Two parameters are required to estimate rank (though the default values will be
suitable in many cases). First, the [knn] parameter defines the number of
points to consider when computing the SVD and estimated rank. Second, the
[thresh] parameter is used to determine when a singular value shall be
considered non-zero (when the absolute value of the singular value is greater
than the threshold).

The rank estimation is performed on a pointwise basis, meaning for each point
in the input point cloud, we find its [knn] neighbors, compute the SVD, and
estimate rank. The filter creates a new dimension called `Rank`
that can be used downstream of this filter stage in the pipeline. The type of
writer used will determine whether or not the `Rank` dimension itself can be
saved to disk.

```{eval-rst}
.. embed::
```

## Example

This sample pipeline estimates the rank of each point using this filter
and then filters out those points where the rank is three using
{ref}`filters.range`.

```json
[
    "input.las",
    {
        "type":"filters.estimaterank",
        "knn":8,
        "thresh":0.01
    },
    {
        "type":"filters.range",
        "limits":"Rank![3:3]"
    },
    "output.laz"
]
```

## Options

knn

: The number of k-nearest neighbors. /[Default: 8/]

thresh

: The threshold used to identify nonzero singular values. /[Default: 0.01/]

```{include} filter_opts.md
```
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('filters.estimaterank', **args)
 
class filters_expression(_GenericStage):
    """
(filters.expression)=

# filters.expression

The **Expression Filter** applies filtering to the input point cloud
based on a set of criteria on the given dimensions.

```{eval-rst}
.. embed::
```

```{eval-rst}
.. streamable::
```

## Example

This example passes through all points whose `Z` value is in the
range /[0,100/]
and whose `Classification` equals 2 (corresponding to ground in LAS).

```json
[
    "input.las",
    {
        "type":"filters.expression",
        "expression":"(Z >= 0 && Z <= 100) && Classification == 2"
    },
    {
        "type":"writers.las",
        "filename":"filtered.las"
    }
]
```

The equivalent pipeline invoked via the PDAL `translate` command would be

```bash
$ pdal translate -i input.las -o filtered.las -f range --filters.expression.expression="(Z >= 0 && Z <= 100) && Classification == 2"
```

## Options

expression

: An {ref}`expression <pdal_expression>` that limits points passed to a filter.
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('filters.expression', **args)
 
class filters_expressionstats(_GenericStage):
    """
(filters.expressionstats)=

# filters.expressionstats

The {ref}`filters.expressionstats` stage computes counting summary for a single
dimension for a given set of expressions. This is useful for summarizing dimensions
that are conveniently countable.

```{eval-rst}
.. embed::
```

```{eval-rst}
.. streamable::
```

```{warning}
The `dimension` selected should be an integer, not floating point dimension.
Additionally, a dimension with lots of unique values is likely to generate a
many entries in the map. This may not be what you want.
```

## Example

```json
{
    "pipeline": [{
        "bounds": "([-10190065.06156413, -10189065.06156413], [5109498.61041016, 5110498.61041016])",
        "filename": "https://s3-us-west-2.amazonaws.com/usgs-lidar-public/IA_Eastern_1_2019/ept.json",
        "requests": "16",
        "type": "readers.ept"
    },
    {
        "type": "filters.stats"
    },
    {
        "type": "filters.expressionstats",
        "dimension":"Classification",
        "expressions":["Withheld == 1", "Keypoint == 1", "Overlap == 1", "Synthetic == 1"]
    },
    {
        "filename": "hobu-office.laz",
        "type": "writers.copc"
    }]
}
```

### Output

```json
{
  "dimension": "Classification",
  "statistic":
  [
    {
      "expression": "(Keypoint==1.000000)",
      "position": 0
    },
    {
      "expression": "(Overlap==1.000000)",
      "position": 1
    },
    {
      "bins":
      [
        {
          "count": 154,
          "value": 1
        }
      ],
      "expression": "(Synthetic==1.000000)",
      "position": 2
    },
    {
      "bins":
      [
        {
          "count": 313615,
          "value": 1
        },
        {
          "count": 6847,
          "value": 7
        },
        {
          "count": 4425,
          "value": 18
        }
      ],
      "expression": "(Withheld==1.000000)",
      "position": 3
    }
  ]
}
```

#### Options

dimension

: The dimension on which to apply the expressions.

expressions

: An array of expressions to apply.

```{include} filter_opts.md
```
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('filters.expressionstats', **args)
 
class filters_faceraster(_GenericStage):
    """
(filters.faceraster)=

# filters.faceraster

The **FaceRaster filter** creates a raster from a point cloud using an
algorithm based on an existing triangulation.  Each raster cell
is given a value that is an interpolation of the known values of the containing
triangle.  If the raster cell center is outside of the triangulation, it is
assigned the [nodata] value.  Use `writers.raster` to write the output.

The extent of the raster can be defined by using the [origin_x], [origin_y], [width] and
[height] options. If these options aren't provided the raster is sized to contain the
input data.

```{eval-rst}
.. embed::

```

## Basic Example

This  pipeline reads the file autzen_trim.las and creates a raster based on a
Delaunay trianguation of the points. It then creates a raster, interpolating values
based on the vertices of the triangle that contains each raster cell center.

```json
[
    "pdal/test/data/las/autzen_trim.las",
    {
        "type": "filters.delaunay"
    },
    {
        "type": "filters.faceraster",
        "resolution": 2,
        "width": 500,
        "height": 500,
        "origin_x": 636000,
        "origin_y": 849000
    }
]
```

## Options

resolution

: Length of raster cell edges in X/Y units.  /[Required/]

`` _`nodata` ``

: The value to use for a raster cell if no data exists in the input data
  with which to compute an output cell value. Note that this value may be
  different from the value used for nodata when the raster is written.
  /[Default: NaN/]

mesh

: Name of the triangulation to use for interpolation.  If not provided, the first
  triangulation associated with the input points will be used. /[Default: None/]

origin_x

: X origin (lower left corner) of the grid. /[Default: None/]

origin_y

: Y origin (lower left corner) of the grid. /[Default: None/]

width

: Number of cells in the X direction. /[Default: None/]

height

: Number of cells in the Y direction. /[Default: None/]

max_triangle_edge_length

: Maximum triangle edge length; triangles larger than this size will not be
  rasterized. /[Default: Infinity/]

```{include} filter_opts.md
```
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('filters.faceraster', **args)
 
class filters_ferry(_GenericStage):
    """
(filters.ferry)=

# filters.ferry

The ferry filter copies data from one dimension to another, creates new
dimensions or both.

The filter is guided by a list of 'from' and 'to' dimensions in the format
/<from>=>/<to>.  Data from the 'from' dimension is copied to the 'to' dimension.
The 'from' dimension must exist.  The 'to' dimension can be pre-existing or
will be created by the ferry filter.

Alternatively, the format =>/<to> can be used to create a new dimension without
copying data from any source.  The values of the 'to' dimension are default
initialized (set to 0).

```{eval-rst}
.. embed::
```

```{eval-rst}
.. streamable::
```

## Example 1

In this scenario, we are making copies of the `X` and `Y` dimensions
into the
dimensions `StatePlaneX` and `StatePlaneY`.  Since the reprojection
filter will
modify the dimensions `X` and `Y`, this allows us to maintain both the
pre-reprojection values and the post-reprojection values.

```json
[
    "uncompressed.las",
    {
        "type":"readers.las",
        "spatialreference":"EPSG:2993",
        "filename":"../las/1.2-with-color.las"
    },
    {
        "type":"filters.ferry",
        "dimensions":"X => StatePlaneX, Y=>StatePlaneY"
    },
    {
        "type":"filters.reprojection",
        "out_srs":"EPSG:4326+4326"
    },
    {
        "type":"writers.las",
        "scale_x":"0.0000001",
        "scale_y":"0.0000001",
        "filename":"colorized.las"
    }
]
```

## Example 2

The ferry filter is being used to add a dimension `Classification` to points
so that the value can be set to '2' and written as a LAS file.

```json
[
    {
          "type": "readers.gdal",
          "filename": "somefile.tif"
    },
    {
          "type": "filters.ferry",
          "dimensions": "=>Classification"
    },
    {
          "type": "filters.assign",
          "assignment": "Classification[:]=2"
    },
    "out.las"
]
```

## Options

dimensions

: A list of dimensions whose values should be copied.
  The format of the option is /<from>=>/<to>, /<from>=>/<to>,...
  Spaces are ignored.
  'from' can be left empty, in which case the 'to' dimension is created and
  default-initialized.  'to' dimensions will be created if necessary.

  Note: the old syntax that used '=' instead of '=>' between dimension names
  is still supported.

```{include} filter_opts.md
```
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('filters.ferry', **args)
 
class filters_fps(_GenericStage):
    """
(filters.fps)=

# filters.fps

The **Farthest Point Sampling Filter** adds points from the input to the output
`PointView` one at a time by selecting the point from the input cloud that is
farthest from any point currently in the output.

```{seealso}
{ref}`filters.sample` produces a similar result, but while
`filters.sample` allows us to target a desired separation of points via
the `radius` parameter at the expense of knowing the number of points in
the output, `filters.fps` allows us to specify exactly the number of
output points at the expense of knowing beforehand the spacing between
points.
```

```{eval-rst}
.. embed::
```

## Options

count

: Desired number of output samples. /[Default: 1000/]

```{include} filter_opts.md
```
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('filters.fps', **args)
 
class filters_geomdistance(_GenericStage):
    """
(filters.geomdistance)=

# filters.geomdistance

The geomdistance filter computes the distance between a given polygon
and points.

```{eval-rst}
.. embed::
```

```{eval-rst}
.. streamable::

```

## Example 1

This example computes the 2D distance of points to the given geometry.

```json
[
    "autzen.las",
    {
        "type":"filters.geomdistance",
        "geometry":"POLYGON ((636889.412951239268295 851528.512293258565478 422.7001953125,636899.14233423944097 851475.000686757150106 422.4697265625,636899.14233423944097 851475.000686757150106 422.4697265625,636928.33048324030824 851494.459452757611871 422.5400390625,636928.33048324030824 851494.459452757611871 422.5400390625,636928.33048324030824 851494.459452757611871 422.5400390625,636976.977398241520859 851513.918218758190051 424.150390625,636976.977398241520859 851513.918218758190051 424.150390625,637069.406536744092591 851475.000686757150106 438.7099609375,637132.647526245797053 851445.812537756282836 425.9501953125,637132.647526245797053 851445.812537756282836 425.9501953125,637336.964569251285866 851411.759697255445644 425.8203125,637336.964569251285866 851411.759697255445644 425.8203125,637473.175931254867464 851158.795739248627797 435.6298828125,637589.928527257987298 850711.244121236610226 420.509765625,637244.535430748714134 850511.791769731207751 420.7998046875,636758.066280735656619 850667.461897735483944 434.609375,636539.155163229792379 851056.63721774588339 422.6396484375,636889.412951239268295 851528.512293258565478 422.7001953125))",
    },
    "dimension":"distance",
    {
        "type":"writers.las",
        "filename":"with-distance.las"
    }
]
```

```{figure} ../images/filters.geomdistance-normal-mode.png
:alt: Normal mode distance of Autzen to selection
:scale: 75%

Normal distance mode causes any points *within* the given polygon to have a distance of 0.
```

```{figure} ../images/filters.geomdistance-ring-mode.png
:alt: Ring mode distance of Autzen to selection
:scale: 75%

`ring` of `True` causes the polygon external ring to be used
for distance computation, resulting in distances **inside** the
polygon to be computed.
```

## Options

geometry

: The polygon, expressed in a well-known text string,
  eg: `"POLYGON((0 0, 5000 10000, 10000 0, 0 0))"`.

dimension

: The dimension to write the distance into
  bounds or polygon. /[Default: distance/]

ogr

: An `ogr` block (described in {ref}`readers.ept`)

ring

: Use the outer ring of the polygon (so as to get distances to the exterior
  ring instead of all points inside the polygon having distance `0`).
  /[Default: false/]

```{include} filter_opts.md
```
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('filters.geomdistance', **args)
 
class filters_georeference(_GenericStage):
    """
(filters.georeference)=

# filters.georeference

The **georeference filter** georeferences point cloud expressed in scanner coordinates,
using `GpsTime` Dimension as a synchronisation reference with a given trajectory.

```{eval-rst}
.. streamable::
```

```{note}
This filter expects trajectory to :

- contains `X`, `Y`, `Z`, `Roll`, `Pitch`, `Yaw`, `WanderAngle` and `GpsTime` ;
- have coordinates expressed in `WGS84` system (EPSG:4979) ;
- have all its angle values expressed in radians.
```

## Examples

```json
[
    "input.rxp",
    {
        "type": "filters.georeference",
        "trajectory_file" : "sbet.out",
        "trajectory_options": {
          "type": "readers.sbet",
          "angles_as_degrees": false
      },
        "scan2imu" : "-0.555809 0.545880 0.626970 0.053833
        0.280774 0.833144 -0.476484 -0.830238
        -0.782459 -0.088797 -0.616338 -0.099672
        0.000000 0.000000 0.000000 1.000000"
    },
    {
      "type" : "filters.reprojection",
      "in_srs" : "EPSG:4979",
      "out_srs" : "EPSG:2154+5720"
    },
    "georeference.las"
]
```

## Options

trajectory_file

: path to a sbet trajectory file. /[Mandatory/]

trajectory_options

: JSON object with keys of reader options and the values to pass through. /[Default: {}/]

scan2imu

: 4x4 transformation matrix from scanner frame to body imu. By default expressed in NED coordinates. /[Mandatory/]

reverse

: revert georeferencing (go back to scanner frame). /[Default: false/]

time_offset

: timestamp offset between trajectory and scanner GpsTime. /[Default: 0/]

coordinate_system

: Two right-handed variants exist for Local tangent plane coordinates: east, north, up (ENU) coordinates and north, east, down (NED). /[Default : NED/]

```{include} filter_opts.md
```
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('filters.georeference', **args)
 
class filters_gpstimeconvert(_GenericStage):
    """
(filters.gpstimeconvert)=

# filters.gpstimeconvert

The **gpstimeconvert** filter converts between three GPS time standards found in
lidar data:

1. GPS time (gt)
2. GPS standard time (gst), also known as GPS adjusted time
3. GPS week seconds (gws)
4. GPS day seconds (gds)

Since GPS week seconds are ambiguous (they reset to 0 at the start of each new
GPS week or each day), care must be taken when they are the source or destination of a
conversion:

- When converting from GPS week seconds, the GPS week number must be known. This
  is accomplished by specifying the [start_date] (in the GMT time zone) on which
  the data collection started. The filter will resolve the ambiguity using the
  supplied start date.
- When converting from GPS week seconds and the times span a new GPS week, the
  presence or absence of week second wrapping must be specified with the
  [wrapped] option. Wrapped week seconds reset to 0 at the start of a new week;
  unwrapped week seconds are allowed to exceed 604800 (60x60x24x7) seconds.
- When converting to GPS week seconds, the week second wrapping preference
  should be specified with the [wrap] option.
- When converting from GPS day seconds and the times span a new day, the [wrapped] option
  reset to 0 and midnight or are allowed to exceed 86400 (60x60x24) seconds.
- When converting to GPS day seconds, the day second wrapping preference should
  also be specified with the [wrap] option.

```{note}
The filter assumes points are ordered by ascending time, which can be
accomplished by running {ref}`filters.sort` prior to
`filters.gpstimeconvert`. Note that GPS week second times that span a new
GPS week should not be sorted unless they are unwrapped.
One can use `wrapped_tolerance` if points `GpsTime` is not stricly increasing, i.e. 
wrapping is detected only if `GpsTime` difference is higher than `wrapped_tolerance`.
```

```{streamable}
```

## Example #1

Convert from GPS time to GPS standard time.

```json
[
    "input.las",
    {
        "type":"filters.gpstimeconvert",
        "conversion":"gt2gst"
    },
    "output.las"
]
```

## Example #2

Convert from GPS standard time to unwrapped GPS week seconds.

```json
[
    "input.las",
    {
        "type":"filters.sort",
        "dimension":"GpsTime",
        "order":"ASC"
    },
    {
        "type":"filters.gpstimeconvert",
        "in_time":"gst",
        "out_time": "gws",
        "wrap":false
    }
]
```

## Example #3

Convert from wrapped GPS week seconds to GPS time.

```json
[
    "input.las",
    {
        "type":"filters.gpstimeconvert",
        "in_time":"gws",
        "out_time": "gt",
        "start_date":"2020-12-12",
        "wrapped":true
    },
    "output.las"
]
```

## Options

conversion (deprecated)

: The time conversion. Must follow the pattern: "{in_time}2{out_time}". Can't be used with "in_time" and "out_time" /[Required/]

in_time

: The input time standard ("gt","gst","gws" or "gds"). Must be used with
 "out_time". Can't be used with "conversion" /[Required/]

out_time

: The output time standard ("gt","gst","gws" or "gds"). Must be used with 
"in_time". Can't be used with "conversion" /[Required/]

start_date

: When the input times are in GPS week seconds, the date on which the data
  collection started must be supplied in the GMT time zone. Must be in
  "YYYY-MM-DD" format. /[Required for the "gws2gt" and "gws2gst" conversions/]

wrap

: Whether to output wrapped (true) or unwrapped (false) GPS week/day seconds.
  /[Default: false/]

wrapped

: Specifies whether input GPS week/day seconds are wrapped (true) or unwrapped
  (false). /[Default: false/]

wrapped_tolerance

: use `wrapped_tolerance` if points `GpsTime` is not stricly increasing, i.e. 
  wrapping is detected only if `GpsTime` difference is higher than `wrapped_tolerance`.
   /[Default: 1.0/]
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('filters.gpstimeconvert', **args)
 
class filters_greedyprojection(_GenericStage):
    """
(filters.greedyprojection)=

# filters.greedyprojection

The **Greedy Projection Filter** creates a mesh (triangulation) in
an attempt to reconstruct the surface of an area from a collection of points.

GreedyProjectionTriangulation is an implementation of a greedy triangulation
algorithm for 3D points based on local 2D projections. It assumes locally
smooth
surfaces and relatively smooth transitions between areas with different point
densities.  The algorithm itself is identical to that used in the [PCL]
library.

```{eval-rst}
.. embed::
```

## Example

```json
[
    "input.las",
    {
        "type": "filters.greedyprojection",
        "multiplier": 2,
        "radius": 10
    },
    {
        "type":"writers.ply",
        "faces":true,
        "filename":"output.ply"
    }
]
```

## Options

multiplier

: Nearest neighbor distance multiplier. /[Required/]

radius

: Search radius for neighbors. /[Required/]

num_neighbors

: Number of nearest neighbors to consider. /[Required/]

min_angle

: Minimum angle for created triangles. /[Default: 10 degrees/]

max_angle

: Maximum angle for created triangles. /[Default: 120 degrees/]

eps_angle

: Maximum normal difference angle for triangulation consideration. /[Default: 45 degrees/]

```{include} filter_opts.md
```

[pcl]: https://pcl.readthedocs.io/projects/tutorials/en/master/greedy_projection.html
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('filters.greedyprojection', **args)
 
class filters_griddecimation(_GenericStage):
    """
(filters.griddecimation)=

# filters.griddecimation

The **grid decimation filter** transform only one point in each cells of a grid calculated from the points cloud and a resolution therm. The transformation is done by the value information. The selected point could be the highest or the lowest point on the cell. It can be used, for exemple, to quickly filter vegetation points in order to keep only the canopy points.

```{eval-rst}
.. embed::
```

## Example

This example transform highest points of classification 5 in classification 9, on a grid of 0.75m square.

```json
[
   "file-input.las",
  {
      "type": "filters.gridDecimation",
      "output_type":"max",
      "resolution": "0.75",
      "where":"Classification==5",
      "value":"Classification=9"
  },
  {
        "type":"writers.las",
        "filename":"file-output.las"
  }
]
```

## Options

output_type

: The type of points transform by the value information. The value should be `"max"` for transform the highest point, or `"min"` for the lowest. /[Default: false/]

resolution

: The resolution of the cells in meter. /[Default: 1./]

value

: A list of {ref}`assignment expressions <assignment_expressions>` to be applied to points.
  The list of values is evaluated in order. /[Default: none/]

```{include} filter_opts.md
```
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('filters.griddecimation', **args)
 
class filters_groupby(_GenericStage):
    """
(filters.groupby)=

# filters.groupby

The **Groupby Filter** takes a single `PointView` as its input and
creates a `PointView` for each category in the named [dimension] as
its output.

```{eval-rst}
.. embed::
```

## Example

The following pipeline will create a set of LAS files, where each file contains
only points of a single `Classification`.

```json
[
    "input.las",
    {
        "type":"filters.groupby",
        "dimension":"Classification"
    },
    "output_#.las"
]
```

```{note}
By default the groups are ordered according to the order of first occurance within the input. To change this, use `filters.sort` first to order the points according to `dimension`.
```

## Options

dimension

: The dimension containing data to be grouped.

```{include} filter_opts.md
```
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('filters.groupby', **args)
 
class filters_h3(_GenericStage):
    """
(filters.h3)=

# filters.h3

The **H3 filter** adds a [H3](https://h3geo.org/docs/api/indexing/) ID at a given `resolution`. The
`uint64_t` integer corresponds to the [H3 index](https://h3geo.org/docs/core-library/latLngToCellDesc) of the point.

```{eval-rst}
.. streamable::
```

```{warning}
{ref}`filters.h3` internally depends on being able to reproject the coordinate system to `EPSG:4326`.
If the data does not have coordinate system information, the filter will throw an error.
```

## Options

resolution

: The H3 resolution /[Default: 0/]
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('filters.h3', **args)
 
class filters_hag_delaunay(_GenericStage):
    """
(filters.hag_delaunay)=

# filters.hag_delaunay

The **Height Above Ground Delaunay filter** takes as input a point cloud with
`Classification` set to 2 for ground points.  It creates a new dimension,
`HeightAboveGround`, that contains the normalized height values.

```{note}
We expect ground returns to have the classification value of 2 in keeping
with the [ASPRS Standard LIDAR Point Classes](http://www.asprs.org/a/society/committees/standards/LAS_1_4_r13.pdf).
```

Ground points may be generated by {ref}`filters.pmf` or {ref}`filters.smrf`,
but you can use any method you choose, as long as the ground returns are
marked.

Normalized heights are a commonly used attribute of point cloud data. This can
also be referred to as *height above ground* (HAG) or *above ground level*
(AGL) heights. In the end, it is simply a measure of a point's relative height
as opposed to its raw elevation value.

The filter creates a delaunay triangulation of the [count] ground points
closest to the non-ground point in question.  If the non-ground point is within
the triangulated area, the assigned `HeightAboveGround` is the difference
between its `Z` value and a ground height interpolated from the three
vertices of the containing triangle.  If the non-ground point is outside of the
triangulated area, its `HeightAboveGround` is calculated as the difference
between its `Z` value and the `Z` value of the nearest ground point.

Choosing a value for [count] is difficult, as placing the non-ground point in
the triangulated area depends on the layout of the nearby points.  If, for
example, all the ground points near a non-ground point lay on one side of that
non-ground point, finding a containing triangle will fail.

```{eval-rst}
.. embed::
```

## Example #1

Using the autzen dataset (here shown colored by elevation), which already has
points classified as ground

```{image} ./images/autzen-elevation.png
:height: 400px
```

we execute the following pipeline

```json
[
    "autzen.laz",
    {
        "type":"filters.hag_delaunay"
    },
    {
        "type":"writers.laz",
        "filename":"autzen_hag_delaunay.laz",
        "extra_dims":"HeightAboveGround=float32"
    }
]
```

which is equivalent to the `pdal translate` command

```
$ pdal translate autzen.laz autzen_hag_delaunay.laz hag_delaunay /
    --writers.las.extra_dims="HeightAboveGround=float32"
```

In either case, the result, when colored by the normalized height instead of
elevation is

```{image} ./images/autzen-hag-delaunay.png
:height: 400px
```

## Options

count

: The number of ground neighbors to consider when determining the height
  above ground for a non-ground point.  /[Default: 10/]

allow_extrapolation

: If false and a non-ground point lies outside of the bounding box of
  all ground points, its `HeightAboveGround` is set to 0.  If true
  and `delaunay` is set, the `HeightAboveGround` is set to the
  difference between the heights of the non-ground point and nearest
  ground point.  /[Default: false/]

```{include} filter_opts.md
```
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('filters.hag_delaunay', **args)
 
class filters_hag_dem(_GenericStage):
    """
(filters.hag_dem)=

# filters.hag_dem

The **Height Above Ground (HAG) Digital Elevation Model (DEM) filter** loads
a GDAL-readable raster image specifying the DEM. The `Z` value of each point
in the input is compared against the value at the corresponding X,Y location
in the DEM raster. It creates a new dimension, `HeightAboveGround`, that
contains the normalized height values.

Normalized heights are a commonly used attribute of point cloud data. This can
also be referred to as *height above ground* (HAG) or *above ground level* (AGL)
heights. In the end, it is simply a measure of a point's relative height as
opposed to its raw elevation value.

```{eval-rst}
.. embed::
```

```{eval-rst}
.. streamable::
```

## Example #1

Using the autzen dataset (here shown colored by elevation)

```{image} ./images/autzen-elevation.png
:height: 400px
```

we generate a DEM based on the points already classified as ground

```
$ pdal translate autzen.laz autzen_dem.tif range /
    --filters.range.limits="Classification[2:2]" /
    --writers.gdal.output_type="idw" /
    --writers.gdal.resolution=6 /
    --writers.gdal.window_size=24
```

and execute the following pipeline

```json
[
    "autzen.laz",
    {
        "type":"filters.hag_dem",
        "raster": "autzen_dem.tif"
    },
    {
        "type":"writers.las",
        "filename":"autzen_hag_dem.laz",
        "extra_dims":"HeightAboveGround=float32"
    }
]
```

which is equivalent to the `pdal translate` command

```
$ pdal translate autzen.laz autzen_hag_dem.laz hag_dem /
    --filters.hag_dem.raster=autzen_dem.tif /
    --writers.las.extra_dims="HeightAboveGround=float32"
```

In either case, the result, when colored by the normalized height instead of
elevation is

```{image} ./images/autzen-hag-dem.png
:height: 400px
```

## Options

raster

: GDAL-readable raster to use for DEM.

band

: GDAL Band number to read (count from 1).
  /[Default: 1/]

zero_ground

: If true, set HAG of ground-classified points to 0 rather than comparing
  `Z` value to raster DEM.
  /[Default: true/]

```{include} filter_opts.md
```
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('filters.hag_dem', **args)
 
class filters_hag_nn(_GenericStage):
    """
(filters.hag_nn)=

# filters.hag_nn

The **Height Above Ground Nearest Neighbor filter** takes as input a point
cloud with `Classification` set to 2 for ground points.  It creates a new
dimension, `HeightAboveGround`, that contains the normalized height values.

```{note}
We expect ground returns to have the classification value of 2 in keeping
with the [ASPRS Standard LIDAR Point Classes](http://www.asprs.org/a/society/committees/standards/LAS_1_4_r13.pdf).
```

Ground points may be generated by {ref}`filters.pmf` or {ref}`filters.smrf`,
but you can use any method you choose, as long as the ground returns are
marked.

Normalized heights are a commonly used attribute of point cloud data. This can
also be referred to as *height above ground* (HAG) or *above ground level*
(AGL) heights. In the end, it is simply a measure of a point's relative height
as opposed to its raw elevation value.

The filter finds the [count] ground points nearest the non-ground point under
consideration.  It calculates an average ground height weighted by the distance
of each ground point from the non-ground point.  The `HeightAboveGround` is
the difference between the `Z` value of the non-ground point and the
interpolated ground height.

```{eval-rst}
.. embed::
```

## Example #1

Using the autzen dataset (here shown colored by elevation), which already has
points classified as ground

```{image} ./images/autzen-elevation.png
:height: 400px
```

we execute the following pipeline

```json
[
    "autzen.laz",
    {
        "type":"filters.hag_nn"
    },
    {
        "type":"writers.laz",
        "filename":"autzen_hag_nn.laz",
        "extra_dims":"HeightAboveGround=float32"
    }
]
```

which is equivalent to the `pdal translate` command

```
$ pdal translate autzen.laz autzen_hag_nn.laz hag_nn /
    --writers.las.extra_dims="HeightAboveGround=float32"
```

In either case, the result, when colored by the normalized height instead of
elevation is

```{image} ./images/autzen-hag-nn.png
:height: 400px
```

## Example #2

In the previous example, we chose to write `HeightAboveGround` using the
`extra_dims` option of {ref}`writers.las`. If you'd instead like to overwrite
your Z values, then follow the height filter with {ref}`filters.ferry` as shown

```json
[
    "autzen.laz",
    {
        "type":"filters.hag_nn"
    },
    {
        "type":"filters.ferry",
        "dimensions":"HeightAboveGround=>Z"
    },
    "autzen-height-as-Z.laz"
]
```

## Example #3

If you don't yet have points classified as ground, start with {ref}`filters.pmf`
or {ref}`filters.smrf` to label ground returns, as shown

```json
[
    "autzen.laz",
    {
        "type":"filters.smrf"
    },
    {
        "type":"filters.hag_nn"
    },
    {
        "type":"filters.ferry",
        "dimensions":"HeightAboveGround=>Z"
    },
    "autzen-height-as-Z-smrf.laz"
]
```

## Options

count

: The number of ground neighbors to consider when determining the height
  above ground for a non-ground point.  /[Default: 1/]

max_distance

: Use only ground points within `max_distance` of non-ground point when
  performing neighbor interpolation.  /[Default: None/]

allow_extrapolation

: If false and a non-ground point lies outside of the bounding box of all
  ground points, its `HeightAboveGround` is set to 0.  If true,
  extrapolation is used to assign the `HeightAboveGround` value.  /[Default:
  false/]

```{include} filter_opts.md
```
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('filters.hag_nn', **args)
 
class filters_head(_GenericStage):
    """
(filters.head)=

# filters.head

The **Head filter** returns a specified number of points from the beginning
of a `PointView`.

```{note}
If the requested number of points exceeds the size of the point cloud, all
points are passed with a warning.
```

```{eval-rst}
.. embed::

```

## Example #1

Thin a point cloud by first shuffling the point order with
{ref}`filters.randomize` and then picking the first 10000 using the HeadFilter.

```json
[
    {
        "type":"filters.randomize"
    },
    {
        "type":"filters.head",
        "count":10000
    }
]
```

## Example #2

Compute height above ground and extract the ten highest points.

```json
[
    {
        "type":"filters.smrf"
    },
    {
        "type":"filters.hag_nn"
    },
    {
        "type":"filters.sort",
        "dimension":"HeightAboveGround",
        "order":"DESC"
    },
    {
        "type":"filters.head",
        "count":10
    }
]
```

```{seealso}
{ref}`filters.tail` is the dual to {ref}`filters.head`.
```

## Options

count

: Number of points to return. /[Default: 10/]

```{include} filter_opts.md
```
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('filters.head', **args)
 
class filters_hexbin(_GenericStage):
    """
(filters.hexbin)=

# filters.hexbin

A common questions for users of point clouds is what the spatial extent of a
point cloud collection is. Files generally provide only rectangular bounds, but
often the points inside the files only fill up a small percentage of the area
within the bounds.

```{figure} filters.hexbin.img1.jpg
:alt: Hexbin derived from input point buffer
:scale: 50 %

Hexbin output shows boundary of actual points in point buffer, not
just rectangular extents.
```

In addition to the original method of processing hexbins, density surfaces and
boundaries can be processed using [H3]. This references hexbin products to a 
global grid of fixed hexagons at 16 [resolutions], allowing joins and comparisons
with other H3 datasets. When writing to a file with `density`, a unique [H3Index]
is provided for each hexagon. Boundary smoothing is disabled for H3, and
`h3_resolution` is used in place of `edge_length`.

The hexbin filter reads a point stream and writes out a metadata record that
contains a boundary, expressed as a well-known text polygon. The filter counts
the points in each hexagonal area to determine if that area should be included
as part of the boundary.  In
order to write out the metadata record, the *pdal* pipeline command must be
invoked using the "--pipeline-serialization" option:

```{eval-rst}
.. streamable::
```

As an alternative to writing geometry to metadata, GDAL OGR can write to
any [OGR-compatible] vector driver by specifying a filename with the `density` 
or `boundary` options. A valid driver that matches the file extension can be
specified with `ogrdriver`; default is GeoJSON.

## Example 1

The following pipeline file and command produces an JSON output file
containing the pipeline's metadata, which includes the result of running
the hexbin filter:

```
[
    "/Users/me/pdal/test/data/las/autzen_trim.las",
    {
        "type" : "filters.hexbin"
    }
]
```

```
$ pdal pipeline hexbin-pipeline.json --metadata hexbin-out.json
```

```none
{
  "stages":
  {
    "filters.hexbin":
    {
      "area": 746772.7543,
      "avg_pt_per_sq_unit": 22.43269935,
      "avg_pt_spacing": 2.605540869,
      "boundary": "MULTIPOLYGON (((636274.38924399 848834.99817891, 637242.52219686 848834.99817891, 637274.79329529 849226.26445367, 637145.70890157 849338.05481789, 637242.52219686 849505.74036422, 636016.22045656 849505.74036422, 635983.94935813 849114.47408945, 636113.03375184 848890.89336102, 636274.38924399 848834.99817891)))",
      "boundary_json": { "type": "MultiPolygon", "coordinates": [ [ [ [ 636274.38924399, 848834.99817891 ], [ 637242.52219686, 848834.99817891 ], [ 637274.79329529, 849226.26445367 ], [ 637145.70890157, 849338.05481789 ], [ 637242.52219686, 849505.74036422 ], [ 636016.22045656, 849505.74036422 ], [ 635983.94935813, 849114.47408945 ], [ 636113.03375184, 848890.89336102 ], [ 636274.38924399, 848834.99817891 ] ] ] ] },
      "density": 0.1473004999,
      "edge_length": 0,
      "estimated_edge": 111.7903642,
      "hex_offsets": "MULTIPOINT (0 0, -32.2711 55.8952, 0 111.79, 64.5422 111.79, 96.8133 55.8952, 64.5422 0)",
      "sample_size": 5000,
      "threshold": 15
    }
},
...
```

## Example 2

As a convenience, the `pdal info` command will produce similar output:

```
$ pdal info --boundary /Users/me/test/data/las/autzen_trim.las
```

```json
{
  "boundary":
  {
    "area": 746772.7543,
    "avg_pt_per_sq_unit": 22.43269935,
    "avg_pt_spacing": 2.605540869,
    "boundary": "MULTIPOLYGON (((636274.38924399 848834.99817891, 637242.52219686 848834.99817891, 637274.79329529 849226.26445367, 637145.70890157 849338.05481789, 637242.52219686 849505.74036422, 636016.22045656 849505.74036422, 635983.94935813 849114.47408945, 636113.03375184 848890.89336102, 636274.38924399 848834.99817891)))",
    "boundary_json": { "type": "MultiPolygon", "coordinates": [ [ [ [ 636274.38924399, 848834.99817891 ], [ 637242.52219686, 848834.99817891 ], [ 637274.79329529, 849226.26445367 ], [ 637145.70890157, 849338.05481789 ], [ 637242.52219686, 849505.74036422 ], [ 636016.22045656, 849505.74036422 ], [ 635983.94935813, 849114.47408945 ], [ 636113.03375184, 848890.89336102 ], [ 636274.38924399, 848834.99817891 ] ] ] ] },
    "density": 0.1473004999,
    "edge_length": 0,
    "estimated_edge": 111.7903642,
    "hex_offsets": "MULTIPOINT (0 0, -32.2711 55.8952, 0 111.79, 64.5422 111.79, 96.8133 55.8952, 64.5422 0)",
    "sample_size": 5000,
    "threshold": 15
  },
  "filename": "//Users//acbell//pdal//test//data//las//autzen_trim.las",
  "pdal_version": "1.6.0 (git-version: 675afe)"
}
```

## Options

density

: Output a density tessellation to the specified filename. `ogrdriver` must be compatible with the filename 
  (default: GeoJSON FeatureCollection). If no file name is provided, nothing is written.

boundary

: Output the grid's boundary to the specified filename. `ogrdriver` must be compatible with the filename 
  (default: GeoJSON FeatureCollection). If no file name is provided, nothing is written.

ogrdriver

: GDAL [OGR-compatible] vector driver for writing with `density` or `boundary`. /[Default: "GeoJSON"/]

h3_grid

: Create the hexbins using [H3] hexagons. /[Default: false/]

h3_resolution

: H3 resolution level the hexagons are created at (0, coarsest - 15, finest). Auto-calculates
  resolution if none is set.

edge_length

: If not set, the hexbin filter will estimate a hex size based on a sample of
  the data. If set, hexbin will use the provided size in constructing the
  hexbins to test.

sample_size

: How many points to sample when automatically calculating the edge
  size? Only applies if `edge_length` is not explicitly set. /[Default: 5000/]

threshold

: Number of points that have to fall within a hexagon boundary before it
  is considered "in" the data set. /[Default: 15/]

precision

: Minimum number of significant digits to use in writing out the
  well-known text of the boundary polygon. /[Default: 8/]

preserve_topology

: Use GEOS SimplifyPreserveTopology instead of Simplify for polygon simplification with  `smooth` option. /[Default: true/]

smooth

: Use GEOS simplify operations to smooth boundary to a tolerance. Not compatible with H3 /[Default: true/]

```{include} filter_opts.md
```

[H3]: https://h3geo.org/
[resolutions]: https://h3geo.org/docs/core-library/restable
[H3Index]: https://h3geo.org/docs/library/index/cell
[OGR-compatible]: https://gdal.org/en/latest/drivers/vector/index.html
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('filters.hexbin', **args)
 
class filters_icp(_GenericStage):
    """
(filters.icp)=

# filters.icp

The **ICP filter** uses the Iterative Closest Point (ICP) algorithm to
calculate a **rigid** (rotation and translation) transformation that best
aligns two datasets.  The first input to the ICP filter is considered the
"fixed" points, and all subsequent points are "moving" points.  The output from
the filter are the "moving" points after the calculated transformation has been
applied, one point view per input.  The transformation matrix is inserted into
the stage's metadata.

```{note}
ICP requires the initial pose of the two point sets to be adequately close,
which is not always possible, especially when the transformation is
non-rigid.  ICP can handle limited non-rigid transformations but be aware
ICP may be unable to escape a local minimum. Consider using CPD instead.

From {cite}`Xuechen2019`:

ICP starts with an initial guess of the transformation between the two
point sets and then iterates between finding the correspondence under the
current transformation and updating the transformation with the newly found
correspondence. ICP is widely used because it is rather straightforward and
easy to implement in practice; however, its biggest problem is that it does
not guarantee finding the globally optimal transformation. In fact, ICP
converges within a very small basin in the parameter space, and it easily
becomes trapped in local minima. Therefore, the results of ICP are very
sensitive to the initialization, especially when high levels of noise and
large proportions of outliers exist.
```

## Examples

```json
[
    "fixed.las",
    "moving.las",
    {
        "type": "filters.icp"
    },
    "output.las"
]
```

To get the `transform` matrix, you'll need to use the `--metadata` option
from the pipeline command:

```
$ pdal pipeline icp-pipeline.json --metadata icp-metadata.json
```

The metadata output might start something like:

```json
{
    "stages":
    {
        "filters.icp":
        {
            "centroid": "    583394  5.2831e+06   498.152",
            "composed": "           1  2.60209e-18 -1.97906e-09       -0.374999  8.9407e-08            1  5.58794e-09      -0.614662 6.98492e-10 -5.58794e-09            1   0.033234           0            0            0            1",
            "converged": true,
            "fitness": 0.01953125097,
            "transform": "           1  2.60209e-18 -1.97906e-09       -0.375  8.9407e-08            1  5.58794e-09      -0.5625 6.98492e-10 -5.58794e-09            1   0.00411987           0            0            0            1"
        }
```

To apply this transformation to other points, the `centroid` and `transform`
metadata items can by used with `filters.transformation` in another pipeline.  First,
move the centroid of the points to (0,0,0), then apply the transform, then move
the points back to the original location.  For the above metadata, the pipeline
would be similar to:

```json
[
    {
        "type": "readers.las",
        "filename": "in.las"
    },
    {
        "type": "filters.transformation",
        "matrix": "1 0 0 -583394   0 1 0 -5.2831e+06   0 0 1 -498.152   0 0 0 1"
    },
    {
        "type": "filters.transformation",
        "matrix": "1  2.60209e-18 -1.97906e-09       -0.375  8.9407e-08            1  5.58794e-09      -0.5625 6.98492e-10 -5.58794e-09            1   0.00411987           0            0            0            1"
    },
    {
        "type": "filters.transformation",
        "matrix": "1 0 0 583394   0 1 0 5.2831e+06  0 0 1 498.152  0 0 0 1"
    },
    {
        "type": "writers.las",
        "filename": "out.las"
    }
]
```

```{note}
The `composed` metadata matrix is a composition of the three transformation steps outlined above, and can be used in a single call to `filters.transformation` as opposed to the three separate calls.
```

```{seealso}
{ref}`filters.transformation` to apply a transform to other points.
{ref}`filters.cpd` for the use of a probabilistic assignment of correspondences between pointsets.
```

## Options

max_iter

: Maximum number of iterations. /[Default: **100**/]

max_similar

: Max number of similar transforms to consider converged. /[Default: **0**/]

mse_abs

: Absolute threshold for MSE. /[Default: **1e-12**/]

rt

: Rotation threshold. /[Default: **0.99999**/]

tt

: Translation threshold. /[Default: **9e-8**/]

```{include} filter_opts.md
```
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('filters.icp', **args)
 
class filters_info(_GenericStage):
    """
(filters.info)=

# filters.info

The **Info filter** provides simple information on a point set as metadata.
It is usually invoked by the info command, rather than by user code.
The data provided includes bounds, a count of points, dimension names,
spatial reference, and points meeting a query criteria.

```{eval-rst}
.. embed::
```

```{eval-rst}
.. streamable::
```

```json
[
    "input.las",
    {
        "type":"filters.info",
        "point":"1-5"
    }
]
```

## Options

point

: A comma-separated list of single point IDs or ranges of points.  For
  example "2-6, 10, 25" selects eight points from the input set.  The first
  point has an ID of 0.  The [point] option can't be used with the [query] option.
  /[Default: no points are selected./]

query

: A specification to retrieve points near a location.  Syntax of the the
  query is X,Y/[,Z/]/[/count/] where 'X', 'Y' and 'Z' are coordinate
  locations mapping to the X, Y and Z point dimension and 'count' is the
  number of points to return.  If 'count' isn't specified, the 10 points
  nearest to the location are returned.  The [query] option can't be used
  with the [point] option. /[Default: no points are selected./]

```{include} filter_opts.md
```
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('filters.info', **args)
 
class filters_iqr(_GenericStage):
    """
(filters.iqr)=

# filters.iqr

The **Interquartile Range Filter** automatically crops the input point
cloud based on the distribution of points in the specified dimension.
The Interquartile Range (IQR) is defined as the range between
the first and third quartile (25th and 75th percentile). Upper and lower bounds
are determined by adding 1.5 times the IQR to the third quartile or subtracting
1.5 times the IQR from the first quartile. The multiplier, which defaults to
1.5, can be adjusted by the user.

```{note}
This method can remove real data, especially ridges and valleys in rugged
terrain, or tall features such as towers and rooftops in flat terrain. While
the number of deviations can be adjusted to account for such content-specific
considerations, it must be used with care.
```

```{eval-rst}
.. embed::
```

## Example

The sample pipeline below uses the filter to automatically crop the Z
dimension and remove possible outliers. The multiplier to determine high/low
thresholds has been adjusted to be less aggressive and to only crop those
outliers that are greater than the third quartile plus 3 times the IQR or are
less than the first quartile minus 3 times the IQR.

```json
[
    "input.las",
    {
        "type":"filters.iqr",
        "dimension":"Z",
        "k":3.0
    },
    "output.laz"
]
```

## Options

k

: The IQR multiplier used to determine upper/lower bounds. /[Default: 1.5/]

dimension

: The name of the dimension to filter.

```{include} filter_opts.md
```
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('filters.iqr', **args)
 
class filters_julia(_GenericStage):
    """
(filters.julia)=

# filters.julia

The **Julia Filter** allows [Julia] software to be embedded in a
{ref}`pipeline` that allows modification of PDAL points through a [TypedTables]
datatype.

The supplied julia function must take a [TypedTables] FlexTable as an argument
and return the same object (with modifications).

```{warning}
The returned Table contains all the {ref}`dimensions` of the incoming `ins` Table
```

```{eval-rst}
.. plugin::
```

```julia
 module MyModule
   using TypedTables

   function multiply_z(ins)
     for n in 1:length(ins)
       ins[n] = merge(ins[n], (; :Z => row.Z * 10.0)
     end
     return ins
   end
 end


If you want write a dimension that might not be available, you can specify
it with the add_dimension_ option:

  ::

      "add_dimension": "NewDimensionOne"

To create more than one dimension, this option also accepts an array:

  ::

      "add_dimension": [ "NewDimensionOne", "NewDimensionTwo", "NewDimensionThree" ]


You can also specify the :ref:`type <types>` of the dimension using an ``=``.
  ::

      "add_dimension": "NewDimensionOne=uint8"
```

## Filter Example

```json
[
    "file-input.las",
    {
        "type":"filters.smrf"
    },
    {
        "type":"filters.julia",
        "script":"filter_z.jl",
        "function":"filter_z",
        "module":"MyModule"
    },
    {
        "type":"writers.las",
        "filename":"file-filtered.las"
    }
]
```

The JSON pipeline file referenced the external `filter_z.jl` [Julia] script,
which removes points with the `Z` coordinate by less than 420.

```julia
module MyModule
  using TypedTables

  function filter_z(ins)
    return filter(p -> p.Z > 420, ins)
  end
end
```

## Modification Example

```json
[
    "file-input.las",
    {
        "type":"filters.smrf"
    },
    {
        "type":"filters.julia",
        "script":"multiply_z.jl",
        "function":"multiply_z",
        "module":"MyModule"
    },
    {
        "type":"writers.las",
        "filename":"file-modified.las"
    }
]
```

The JSON pipeline file referenced the external `multiply_z.jl` [Julia] script,
which scales the `Z` coordinate by a factor of 10.

```julia
module MyModule
  using TypedTables

  function multiply_z(ins)
    for n in 1:length(ins)
      ins[n] = merge(ins[n], (; :Z => row.Z * 10.0)
    end
    return ins
  end
end
```

## Options

script

: When reading a function from a separate [Julia] file, the file name to read
  from.

source

: The literal [Julia] code to execute, when the script option is
  not being used.

module

: The Julia module that is holding the function to run. /[Required/]

function

: The function to call. /[Required/]

add_dimension

: A dimension name or an array of dimension names to add to the pipeline that do not already exist.

```{include} filter_opts.md
```

[julia]: https://julialang.org/
[typedtables]: https://github.com/JuliaData/TypedTables.jl
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('filters.julia', **args)
 
class filters_label_duplicates(_GenericStage):
    """
(filters.label_duplicates)=

# filters.label_duplicates

{ref}`filters.label_duplicates` assigns a `Duplicate` {ref}`dimensions` value
to `1` if all of the dimensions listed in the `dimensions` option
for the points are equal.

```{eval-rst}
.. embed::
```

```{warning}
The filter **requires** the data to be sorted **before** the labeling can
work. It simply checks the dimensions and points in order, and if each
dimension is equal from one point to the next, it is labeled a duplicate.
The `STABLE` algorithm **must** be set or it will fail to properly label
duplicates.
```

## Example

```json
[
    "unsorted.las",
    {
        "type":"filters.sort",
        "algorithm":"STABLE",
        "dimension":"X"
    },
    {
        "type":"filters.sort",
        "algorithm":"STABLE",
        "dimension":"Y"
    },
    {
        "type":"filters.sort",
        "algorithm":"STABLE",
        "dimension":"Z"
    },
    {
        "type":"filters.sort",
        "algorithm":"STABLE",
        "dimension":"GPStime"
    },
    {
        "type":"filters.label_duplicates",
        "dimensions":"X,Y,Z,GPStime"
    },
    "duplicates.txt"
]
```

## Options

dimensions

: The {ref}`dimensions` which must be equal for the point to be declared a duplicate. /[Required/]

```{include} filter_opts.md
```
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('filters.label_duplicates', **args)
 
class filters_litree(_GenericStage):
    """
(filters.litree)=

# filters.litree

The purpose of the Li tree filter is to segment individual trees from an input
`PointView`. In the output `PointView` points that are deemed to be part of
a tree are labeled with a `ClusterID`. Tree IDs start at 1, with non-tree points
given a `ClusterID` of 0.

```{note}
The filter differs only slightly from the paper in the addition of a few
conditions on size of tree, minimum height above ground for tree seeding, and
flexible radius for non-tree seed insertion.
```

```{note}
In earlier PDAL releases (up to v2.2.0), `ClusterID` was stored in the
`TreeID` Dimemsion.
```

```{eval-rst}
.. embed::
```

## Example

The Li tree algorithm expects to visit points in descending order of
`HeightAboveGround`, which is also used in determining the minimum tree
height to consider. As such, the following pipeline precomputes
`HeightAboveGround` using {ref}`filters.hag_delaunay` and subsequently sorts
the `PointView` using this dimension.

```json
[
    "input.las",
    {
        "type":"filters.hag_delaunay"
    },
    {
        "type":"filters.sort",
        "dimension":"HeightAboveGround",
        "order":"DESC"
    },
    {
        "type":"filters.litree",
        "min_points":50,
        "min_height":10.0,
        "radius":200.0
    },
    {
        "type":"writers.las",
        "filename":"output.laz",
        "minor_version":1.4,
        "extra_dims":"all"
    }
]
```

## Options

min_points

: Minimum number of points in a tree cluster. /[Default: 10/]

min_height

: Minimum height above ground to start a tree cluster. /[Default: 3.0/]

radius

: The seed point for the non-tree cluster is the farthest point in a 2D
  Euclidean sense from the seed point for the current tree. /[Default: 100.0/]

```{include} filter_opts.md
```
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('filters.litree', **args)
 
class filters_lloydkmeans(_GenericStage):
    """
(filters.lloydkmeans)=

# filters.lloydkmeans

K-means clustering using Lloyd's algorithm labels each point with its
associated cluster ID (starting at 0).

```{eval-rst}
.. embed::
```

```{versionadded} 2.1
```

## Example

```json
[
    "input.las",
    {
        "type":"filters.lloydkmeans",
        "k":10,
        "maxiters":20,
        "dimensions":"X,Y,Z"
    },
    {
        "type":"writers.las",
        "filename":"output.laz",
        "minor_version":4,
        "extra_dims":"all"
    }
]
```

## Options

k

: The desired number of clusters. /[Default: 10/]

maxiters

: The maximum number of iterations. /[Default: 10/]

dimensions

: Comma-separated string indicating dimensions to use for clustering.
  /[Default: X,Y,Z/]

```{include} filter_opts.md
```
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('filters.lloydkmeans', **args)
 
class filters_locate(_GenericStage):
    """
(filters.locate)=

# filters.locate

The Locate filter searches the specified [dimension] for the minimum or
maximum value and returns a single point at this location. If multiple points
share the min/max value, the first will be returned. All dimensions of the
input `PointView` will be output, subject to any overriding writer options.

```{eval-rst}
.. embed::
```

## Example

This example returns the point at the highest elevation.

```json
[
    "input.las",
    {
        "type":"filters.locate",
        "dimension":"Z",
        "minmax":"max"
    },
    "output.las"
]
```

## Options

dimension

: Name of the dimension in which to search for min/max value.

minmax

: Whether to return the minimum or maximum value in the dimension.

```{include} filter_opts.md
```
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('filters.locate', **args)
 
class filters_lof(_GenericStage):
    """
(filters.lof)=

# filters.lof

The **Local Outlier Factor (LOF) filter** was introduced as a method
of determining the degree to which an object is an outlier. This filter
is an implementation of the method
described in {cite:p}`breunig2000lof`.

The filter creates three new dimensions, `NNDistance`,
`LocalReachabilityDistance` and `LocalOutlierFactor`, all of which are
double-precision floating values. The `NNDistance` dimension records the
Euclidean distance between a point and it's k-th nearest neighbor (the number
of k neighbors is set with the [minpts] option). The
`LocalReachabilityDistance` is the inverse of the mean
of all reachability distances for a neighborhood of points. This reachability
distance is defined as the max of the Euclidean distance to a neighboring point
and that neighbor's own previously computed `NNDistance`. Finally, each point
has a `LocalOutlierFactor` which is the mean of all
`LocalReachabilityDistance` values for the neighborhood. In each case, the
neighborhood is the set of k nearest neighbors.

In practice, setting the [minpts] parameter appropriately and subsequently
filtering outliers based on the computed `LocalOutlierFactor` can be
difficult. The authors present some work on establishing upper and lower bounds
on LOF values, and provide some guidelines on selecting [minpts] values, which
users of this filter should find instructive.

```{note}
To inspect the newly created, non-standard dimensions, be sure to write to an
output format that can support arbitrary dimensions, such as BPF.
```

```{note}
In earlier PDAL releases (up to v2.2.0), `NNDistance` was stored in the
`KDistance` Dimemsion.
```

```{eval-rst}
.. embed::
```

## Example

The sample pipeline below computes the LOF with a neighborhood of 20 neighbors,
followed by a range filter to crop out points whose `LocalOutlierFactor`
exceeds 1.2 before writing the output.

```json
[
    "input.las",
    {
        "type":"filters.lof",
        "minpts":20
    },
    {
        "type":"filters.range",
        "limits":"LocalOutlierFactor[:1.2]"
    },
    "output.laz"
]
```

## Options

minpts

: The number of k nearest neighbors. /[Default: 10/]

```{include} filter_opts.md
```
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('filters.lof', **args)
 
class filters_mad(_GenericStage):
    """
(filters.mad)=

# filters.mad

The **MAD filter** filter crops the input point cloud based on
the distribution of points in the specified [dimension]. Specifically, we choose
the method of median absolute deviation from the median (commonly referred to
as
MAD), which is robust to outliers (as opposed to mean and standard deviation).

```{note}
This method can remove real data, especially ridges and valleys in rugged
terrain, or tall features such as towers and rooftops in flat terrain. While
the number of deviations can be adjusted to account for such content-specific
considerations, it must be used with care.
```

```{eval-rst}
.. embed::
```

## Example

The sample pipeline below uses filters.mad to automatically crop the `Z`
dimension and remove possible outliers. The number of deviations from the
median has been adjusted to be less aggressive and to only crop those outliers
that are greater than four deviations from the median.

```json
[
    "input.las",
    {
        "type":"filters.mad",
        "dimension":"Z",
        "k":4.0
    },
    "output.laz"
]
```

## Options

k

: The number of deviations from the median. /[Default: 2.0/]

dimension

: The name of the dimension to filter.

```{include} filter_opts.md
```
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('filters.mad', **args)
 
class filters_matlab(_GenericStage):
    """
(filters.matlab)=

# filters.matlab

The **Matlab Filter** allows [Matlab] software to be embedded in a
{ref}`pipeline` that interacts with a struct array of the data and allows
you to modify those points. Additionally, some global {ref}`metadata` is also
available that Matlab functions can interact with.

The Matlab interpreter must exit and always set "ans==true" upon success. If
"ans==false", an error would be thrown and the {ref}`pipeline` exited.

```{seealso}
{ref}`writers.matlab` can be used to write `.mat` files.
```

```{note}
{ref}`filters.matlab` embeds the entire Matlab interpreter, and it
will require a fully licensed version of Matlab to execute your script.
```

```{eval-rst}
.. plugin::
```

## Example

```json
[
    {
        "filename": "test//data//las//1.2-with-color.las",
        "type": "readers.las"

    },
    {
        "type": "filters.matlab",
        "script": "matlab.m"

    },
    {
        "filename": "out.las",
        "type": "writers.las"
    }
]
```

## Options

script

: When reading a function from a separate [Matlab] file, the file name to read
  from. /[Example: "functions.m"/]

source

: The literal [Matlab] code to execute, when the script option is not
  being used.

add_dimension

: The name of a dimension to add to the pipeline that does not already exist.

struct

: Array structure name to read /[Default: "PDAL"/]

```{include} filter_opts.md
```

[matlab]: https://www.mathworks.com/products/matlab.html
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('filters.matlab', **args)
 
class filters(_GenericStage):
    """
(filters)=

# Filters

Filters operate on data as inline operations. They can remove, modify,
reorganize, and add points to the data stream as it goes by. Some filters can
only operate on dimensions they understand (consider {ref}`filters.reprojection`
doing geographic reprojection on XYZ coordinates), while others do not
interrogate the point data at all and simply reorganize or split data.

## Create

PDAL filters commonly create new dimensions (e.g., `HeightAboveGround`) or
alter existing ones (e.g., `Classification`). These filters will not
invalidate an existing KD-tree.

```{note}
We treat those filters that alter XYZ coordinates separately.
```

```{note}
When creating new dimensions, be mindful of the writer you are using and
whether or not the custom dimension can be written to disk if that is the
desired behavior.
```

### Classification

#### Ground/Unclassified

<!-- ```{toctree}
:glob: true
:hidden: true
:maxdepth: 1

filters.csf
filters.pmf
filters.skewnessbalancing
filters.smrf
filters.sparsesurface
filters.trajectory
``` -->

{ref}`filters.csf`

: Label ground/non-ground returns using {cite:p}`zhang2016easy`.

{ref}`filters.pmf`

: Label ground/non-ground returns using {cite:p}`zhang2003progressive`.

{ref}`filters.skewnessbalancing`

: Label ground/non-ground returns using {cite:p}`bartels2010threshold`.

{ref}`filters.smrf`

: Label ground/non-ground returns using {cite:p}`pingel2013improved`.

{ref}`filters.sparsesurface`

: Sparsify ground returns and label neighbors as low noise.

{ref}`filters.trajectory`

: Label ground/non-ground returns using estimate flight trajectory given
  multi-return point cloud data with timing information.

#### Noise

<!-- ```{toctree}
:glob: true
:hidden: true
:maxdepth: 1

filters.elm
filters.outlier
``` -->

{ref}`filters.elm`

: Marks low points as noise.

{ref}`filters.outlier`

: Label noise points using either a statistical or radius outlier detection.

#### Consensus

<!-- ```{toctree}
:glob: true
:hidden: true
:maxdepth: 1

filters.neighborclassifier
``` -->

{ref}`filters.neighborclassifier`

: Update pointwise classification using k-nearest neighbor consensus voting.

### Height Above Ground

<!-- ```{toctree}
:glob: true
:hidden: true
:maxdepth: 1

filters.hag_delaunay
filters.hag_dem
filters.hag_nn
``` -->

{ref}`filters.hag_delaunay`

: Compute pointwise height above ground using triangulation. Requires points to
  classified as ground/non-ground prior to estimating.

{ref}`filters.hag_dem`

: Compute pointwise height above GDAL-readable DEM raster.

{ref}`filters.hag_nn`

: Compute pointwise height above ground estimate. Requires points to be
  classified as ground/non-ground prior to estimating.

### Colorization

<!-- ```{toctree}
:glob: true
:hidden: true
:maxdepth: 1

filters.colorinterp
filters.colorization
``` -->

{ref}`filters.colorinterp`

: Assign RGB colors based on a dimension and a ramp

{ref}`filters.colorization`

: Fetch and assign RGB color information from a GDAL-readable datasource.

### Clustering

<!-- ```{toctree}
:glob: true
:hidden: true
:maxdepth: 1

filters.cluster
filters.dbscan
filters.litree
filters.lloydkmeans
``` -->

{ref}`filters.cluster`

: Extract and label clusters using Euclidean distance metric. Returns a new
  dimension `ClusterID` that indicates the cluster that a point belongs
  to. Points not belonging to a cluster are given a cluster ID of 0.

{ref}`filters.dbscan`

: Perform Density-Based Spatial Clustering of Applications with Noise
  (DBSCAN) {cite:p}`ester1996density`.

{ref}`filters.litree`

: Segment and label individual trees. Returns a new dimension `TreeID` that
  indicates the tree that a point belongs to. `TreeID` starts at 1, with
  non-tree points given a `TreeID` of 0. {cite:p}`li2012new`.

{ref}`filters.lloydkmeans`

: Perform K-means clustering using Lloyd's algorithm. Returns a new dimension
  `ClusterID` with each point being assigned to a cluster. `ClusterID`
  starts at 0. {cite:p}`lloyd1982least`.

### Pointwise Features

<!-- ```{toctree}
:glob: true
:hidden: true
:maxdepth: 1

filters.approximatecoplanar
filters.covariancefeatures
filters.eigenvalues
filters.estimaterank
filters.label_duplicates
filters.lof
filters.miniball
filters.nndistance
filters.normal
filters.optimalneighborhood
filters.planefit
filters.radialdensity
filters.reciprocity
filters.zsmooth
filters.griddecimation
``` -->

{ref}`filters.approximatecoplanar`

: Estimate pointwise planarity, based on k-nearest neighbors. Returns a new
  dimension `Coplanar` where a value of 1 indicates that a point is part of
  a coplanar neighborhood (0 otherwise).

{ref}`filters.covariancefeatures`

: Filter that calculates local features based on the covariance matrix of a
  point's neighborhood.

{ref}`filters.eigenvalues`

: Compute pointwise eigenvalues, based on k-nearest neighbors.

{ref}`filters.estimaterank`

: Compute pointwise rank, based on k-nearest neighbors.

{ref}`filters.label_duplicates`

: Label points as duplicate if the specified dimensions are equal.

{ref}`filters.lof`

: Compute pointwise Local Outlier Factor (along with K-Distance and Local
  Reachability Distance).

{ref}`filters.miniball`

: Compute a criterion for point neighbors based on the miniball algorithm.

{ref}`filters.nndistance`

: Compute a distance metric based on nearest neighbors.

{ref}`filters.normal`

: Compute pointwise normal and curvature, based on k-nearest neighbors.

{ref}`filters.optimalneighborhood`

: Compute optimal k nearest neighbors and corresponding radius by minimizing
  pointwise eigenentropy. Creates two new dimensions `OptimalKNN` and
  `OptimalRadius`.

{ref}`filters.planefit`

: Compute a deviation of a point from a manifold approximating its neighbors.

{ref}`filters.radialdensity`

: Compute pointwise density of points within a given radius.

{ref}`filters.reciprocity`

: Compute the percentage of points that are considered uni-directional
  neighbors of a point.

{ref}`filters.zsmooth`

: Compute a smoothed 'Z' value based on the 'Z' value of neighboring points.

{ref}`filters.griddecimation`

: Assign values for one point (the highest or lowest) per cell of a 2d regular grid.

### Assignment
<!-- 
```{toctree}
:glob: true
:hidden: true
:maxdepth: 1

filters.assign
filters.overlay
``` -->

{ref}`filters.assign`

: Assign values for a dimension range to a specified value.

{ref}`filters.overlay`

: Assign values to a dimension based on the extent of an OGR-readable data
  source or an OGR SQL query.

### Dimension Create/Copy

<!-- ```{toctree}
:glob: true
:hidden: true
:maxdepth: 1

filters.ferry
``` -->

{ref}`filters.ferry`

: Copy data from one dimension to another.

## Order

There are currently three PDAL filters that can be used to reorder points. These
filters will invalidate an existing KD-tree.

<!-- ```{toctree}
:glob: true
:hidden: true
:maxdepth: 1

filters.mortonorder
filters.randomize
filters.sort
``` -->

{ref}`filters.mortonorder`

: Sort XY data using Morton ordering (aka Z-order/Z-curve).

{ref}`filters.randomize`

: Randomize points in a view.

{ref}`filters.sort`

: Sort data based on a given dimension.

## Move

PDAL filters that move XYZ coordinates will invalidate an existing KD-tree.

### Registration

<!-- ```{toctree}
:glob: true
:hidden: true
:maxdepth: 1

filters.cpd
filters.icp
filters.teaser
``` -->

{ref}`filters.cpd`

: Compute and apply transformation between two point clouds using the
  Coherent Point Drift algorithm.

{ref}`filters.icp`

: Compute and apply transformation between two point clouds using the
  Iterative Closest Point algorithm.

{ref}`filters.teaser`

: Compute a rigid transformation between two point clouds using the teaser algorithm.

### Predefined

<!-- ```{toctree}
:glob: true
:hidden: true
:maxdepth: 1

filters.projpipeline
filters.reprojection
filters.transformation
filters.straighten
filters.georeference
filters.h3
``` -->

{ref}`filters.projpipeline`

: Apply coordinates operation on point triplets, based on PROJ pipeline string,
  WKT2 coordinates operations or URN definitions.

{ref}`filters.reprojection`

: Reproject data using GDAL from one coordinate system to another.

{ref}`filters.transformation`

: Transform each point using a 4x4 transformation matrix.

{ref}`filters.straighten`

: Transforms each in a new parametric coordinate system along a given poyline.

{ref}`filters.georeference`

: Georeference point cloud.

{ref}`filters.h3`

: Compute H3 index values for the Longitude/Latitude of the point cloud

## Cull

Some PDAL filters will cull points, returning a point cloud that is smaller than
the input. These filters will invalidate an existing KD-tree.

### Spatial

<!-- ```{toctree}
:glob: true
:hidden: true
:maxdepth: 1

filters.crop
filters.geomdistance
``` -->

{ref}`filters.crop`

: Filter points inside or outside a bounding box or a polygon

{ref}`filters.geomdistance`

: Compute 2D distance from a polygon to points

### Resampling

<!-- ```{toctree}
:glob: true
:hidden: true
:maxdepth: 1

filters.decimation
filters.fps
filters.relaxationdartthrowing
filters.sample
``` -->

{ref}`filters.decimation`

: Keep every Nth point.

{ref}`filters.fps`

: The Farthest Point Sampling Filter adds points from the input to the output
  PointView one at a time by selecting the point from the input cloud that is
  farthest from any point currently in the output.

{ref}`filters.relaxationdartthrowing`

: Relaxation dart throwing is a hierarchical variant of Poisson disk
  sampling, shrinking the minimum radius between iterations until the target
  number of output points is achieved.

{ref}`filters.sample`

: Perform Poisson sampling and return only a subset of the input points.

### Conditional

<!-- ```{toctree}
:glob: true
:hidden: true
:maxdepth: 1

filters.dem
filters.iqr
filters.mad
``` -->

{ref}`filters.dem`

: Remove points that are in a raster cell but have a value far from the
  value of the raster.

{ref}`filters.iqr`

: Cull points falling outside the computed Interquartile Range for a given
  dimension.

{ref}`filters.mad`

: Cull points falling outside the computed Median Absolute Deviation for a
  given dimension.

### Voxel

<!-- ```{toctree}
:glob: true
:hidden: true
:maxdepth: 1

filters.voxelcenternearestneighbor
filters.voxelcentroidnearestneighbor
filters.voxeldownsize
``` -->

{ref}`filters.voxelcenternearestneighbor`

: Return the point within each voxel that is nearest the voxel center.

{ref}`filters.voxelcentroidnearestneighbor`

: Return the point within each voxel that is nearest the voxel centroid.

{ref}`filters.voxeldownsize`

: Retain either first point detected in each voxel or center of a populated
  voxel, depending on mode argument.

### Position

<!-- ```{toctree}
:glob: true
:hidden: true
:maxdepth: 1

filters.expression
filters.head
filters.locate
filters.mongo
filters.range
filters.tail
``` -->

{ref}`filters.expression`

: Pass only points given an {ref}`expression <pdal_expression>`

{ref}`filters.head`

: Return N points from beginning of the point cloud.

{ref}`filters.locate`

: Return a single point with min/max value in the named dimension.

{ref}`filters.mongo`

: Cull points using MongoDB-style expression syntax.

{ref}`filters.range`

: Pass only points given a dimension/range.

{ref}`filters.tail`

: Return N points from end of the point cloud.

## New

PDAL filters can be used to split the incoming point cloud into subsets. These
filters will invalidate an existing KD-tree.

### Spatial

<!-- ```{toctree}
:glob: true
:hidden: true
:maxdepth: 1

filters.chipper
filters.divider
filters.splitter
``` -->

{ref}`filters.chipper`

: Organize points into spatially contiguous, squarish, and non-overlapping
  chips.

{ref}`filters.divider`

: Divide points into approximately equal sized groups based on a simple
  scheme.

{ref}`filters.splitter`

: Split data based on a X/Y box length.

### Dimension

<!-- ```{toctree}
:glob: true
:hidden: true
:maxdepth: 1

filters.gpstimeconvert
filters.groupby
filters.returns
filters.separatescanline
``` -->

{ref}`filters.gpstimeconvert`

: Convert between three LAS format GPS time standards

{ref}`filters.groupby`

: Split data categorically by dimension.

{ref}`filters.returns`

: Split data by return order (e.g., 'first', 'last', 'intermediate', 'only').

{ref}`filters.separatescanline`

: Split data based on scan lines.

## Join

Multiple point clouds can be joined to form a single point cloud. These filters
will invalidate an existing KD-tree.

<!-- ```{toctree}
:glob: true
:hidden: true
:maxdepth: 1

filters.merge
``` -->

{ref}`filters.merge`

: Merge data from two different readers into a single stream.

## Metadata

PDAL filters can be used to create new metadata. These filters will not
invalidate an existing KD-tree.

```{note}
{ref}`filters.cpd` and {ref}`filters.icp` can optionally create metadata as
well, inserting the computed transformation matrix.
```

<!-- ```{toctree}
:glob: true
:hidden: true
:maxdepth: 1

filters.hexbin
filters.info
filters.stats
filters.expressionstats
``` -->

{ref}`filters.hexbin`

: Tessellate XY domain and determine point density and/or point boundary.

{ref}`filters.info`

: Generate metadata about the point set, including a point count and
  spatial reference information.

{ref}`filters.stats`

: Compute statistics about each dimension (mean, min, max, etc.).

{ref}`filters.expressionstats`

: Apply expressions for a given dimension and summarize counts

## Mesh

Meshes can be computed from point clouds. These filters will invalidate an
existing KD-tree.

<!-- ```{toctree}
:glob: true
:hidden: true
:maxdepth: 1

filters.delaunay
filters.greedyprojection
filters.poisson
filters.faceraster
``` -->

{ref}`filters.delaunay`

: Create mesh using Delaunay triangulation.

{ref}`filters.greedyprojection`

: Create mesh using the Greedy Projection Triangulation approach.

{ref}`filters.poisson`

: Create mesh using the Poisson surface reconstruction algorithm
  {cite:p}`kazhdan2006poisson`.

{ref}`filters.faceraster`

: Create a raster from an existing triangulation.

## Languages

PDAL has three filters than can be used to pass point clouds to other
languages. These filters will invalidate an existing KD-tree.

<!-- ```{toctree}
:glob: true
:hidden: true
:maxdepth: 1

filters.matlab
filters.python
filters.julia
``` -->

{ref}`filters.matlab`

: Embed MATLAB software in a pipeline.

{ref}`filters.python`

: Embed Python software in a pipeline.

{ref}`filters.julia`

: Embed Julia software in a pipeline.

## Other

<!-- ```{toctree}
:glob: true
:hidden: true
:maxdepth: 1

filters.streamcallback
``` -->

{ref}`filters.streamcallback`

: Provide a hook for a simple point-by-point callback.
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('filters', **args)
 
class filters_merge(_GenericStage):
    """
(filters.merge)=

# filters.merge

The **Merge Filter** combines input from multiple sources into a single output.
In most cases, this happens automatically on output and use of the merge
filter is unnecessary.  However, there may be special cases where
merging points prior to a particular filter or writer is necessary
or desirable.

The merge filter will log a warning if its input point sets are based on
different spatial references.  No checks are made to ensure that points
from various sources being merged have similar dimensions or are generally
compatible.

```{eval-rst}
.. embed::
```

## Example 1

This pipeline will create an output file "output.las" that contcatenates
the points from "file1", "file2" and "file3".  Note that the explicit
use of the merge filter is unnecessary in this case (removing the merge
filter will yield the same result).

```json
[
    "file1",
    "file2",
    "file3",
    {
        "type": "filters.merge"
    },
    "output.las"
]
```

## Example 2

Here are a pair of unlikely pipelines that show one way in which a merge filter
might be used.  The first pipeline simply reads the input files "utm1.las",
"utm2.las" and "utm3.las".  Since the points from each input set are
carried separately through the pipeline, three files are created as output,
"out1.las", "out2.las" and "out3.las".  "out1.las" contains the points
in "utm1.las".  "out2.las" contains the points in "utm2.las" and "out3.las"
contains the points in "utm3.las".

```json
[
    "utm1.las",
    "utm2.las",
    "utm3.las",
    "out#.las"
]
```

Here is the same pipeline with a merge filter added.  The merge filter will
combine the points in its input: "utm1.las" and "utm2.las".  Then the result
of the merge filter is passed to the writer along with "utm3.las".  This
results in two output files: "out1.las" contains the points from "utm1.las"
and "utm2.las", while "out2.las" contains the points from "utm3.las".

```json
[
    "utm1.las",
    "utm2.las",
    {
        "type" : "filters.merge"
    },
    "utm3.las",
    "out#.las"
]
```

## Options

```{include} filter_opts.md
```
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('filters.merge', **args)
 
class filters_miniball(_GenericStage):
    """
(filters.miniball)=

# filters.miniball

The **Miniball Criterion** was introduced in {cite:p}`weyrich2004post` and is based on the
assumption that points that are distant to the cluster built by their
k-neighborhood are likely to be outliers. First, the smallest enclosing ball is
computed for the k-neighborhood, giving a center point and radius
{cite:p}`fischer2003fast`. The miniball criterion is then computed by comparing the
distance (from the current point to the miniball center) to the radius of the
miniball.

The author suggests that the Miniball Criterion is more robust than the
{ref}`Plane Fit Criterion <filters.planefit>` around high-frequency details,
but demonstrates poor outlier detection for points close to a smooth surface.

The filter creates a single new dimension, `Miniball`, that records the
Miniball criterion for the current point.

```{note}
To inspect the newly created, non-standard dimensions, be sure to write to an
output format that can support arbitrary dimensions, such as BPF.
```

```{eval-rst}
.. embed::
```

## Example

The sample pipeline below computes the Miniball criterion with a neighborhood
of 8 neighbors. We do not apply a fixed threshold to single out outliers based
on the Miniball criterion as the range of values can vary from one dataset to
another. In general, higher values indicate the likelihood of a point being an
outlier.

```json
[
    "input.las",
    {
        "type":"filters.miniball",
        "knn":8
    },
    "output.laz"
]
```

## Options

knn

: The number of k nearest neighbors. /[Default: 8/]

threads

: The number of threads to use. Only valid in {ref}`standard mode <processing_modes>`. /[Default: 1/]

```{include} filter_opts.md
```
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('filters.miniball', **args)
 
class filters_mongo(_GenericStage):
    """
(filters.mongo)=

# filters.mongo

The **Mongo Filter** applies query logic to the input
point cloud based on a MongoDB-style query expression using the
point cloud attributes.

```{eval-rst}
.. embed::
```

```{eval-rst}
.. streamable::
```

## Example

This example passes through only the points whose Classification is non-zero.

```json
[
    "input.las",
    {
        "type": "filters.mongo",
        "expression": {
            "Classification": { "$ne": 0 }
        }
    },
    "filtered.las"
]
```

This example passes through only the points whose `ReturnNumber`
is equal to the `NumberOfReturns` and the `NumberOfReturns`
is greater than 1.

```json
[
    "input.las",
    {
        "type": "filters.mongo",
        "expression": { "$and": [
            { "ReturnNumber": "NumberOfReturns" },
            { "NumberOfReturns": { "$gt": 1 } }
        ] }
    },
    "filtered.las"
]
```

## Options

expression

: A JSON query {ref}`expression <mongo_expression>` containing a combination of query comparisons
  and logical operators.

```{include} filter_opts.md
```

(mongo_expression)=

## Expression

A query expression is a combination of comparison and logical operators that
define a query which can be used to select matching points by their attribute
values.

### Comparison operators

There are 8 valid query comparison operators:

> - `$eq`: Matches values equal to a specified value.
> - `$gt`: Matches values greater than a specified value.
> - `$gte`: Matches values greater than or equal to a specified value.
> - `$lt`: Matches values less than a specified value.
> - `$lte`: Matches values less than or equal to a specified value.
> - `$ne`: Matches values not equal to a specified value.
> - `$in`: Matches any of the values specified in the array.
> - `$nin`: Matches none of the values specified in the array.

Comparison operators compare a point cloud attribute with an operand or an
array of operands.  An *operand* is either a numeric constant or a string
representing a dimension name.  For all comparison operators except for `$in`
and `$nin`, the comparison value must be a single operand.  For `$in` and
`$nin`, the value must be an array of operands.

Comparison operator specifications must be contained within an object whose key
is the dimension name to be compared.

```json
{ "Classification": { "$eq": 2 } }
```

```json
{ "Intensity": { "$gt": 0 } }
```

```json
{ "Classification": { "$in": [2, 6, 9] } }
```

The `$eq` comparison operator may be implicitly invoked by setting an
attribute name directly to a value.

```json
{ "Classification": 2 }
```

### Logical operators

There are 4 valid logical operators:

> - `$and`: Applies a logical **and** on the expressions of the array and
>   returns a match only if all expressions match.
> - `$not`: Inverts the value of the single sub-expression.
> - `$nor`: Applies a logical **nor** on the expressions of the array and
>   returns a match only if all expressions fail to match.
> - `$nor`: Applies a logical **or** on the expressions of the array and
>   returns a match if any of the expressions match.

Logical operators are used to logically combine sub-expressions.  All logical
operators except for `$not` are applied to arrays of expressions.
`$not` is applied to a single expression and negates its result.

Logical operators may be applied directly to comparison expressions or may
contain further nested logical operators.  For example:

```json
{ "$or": [
    { "Classification": 2 },
    { "Intensity": { "$gt": 0 } }
] }
```

```json
{ "$or": [
    { "Classification": 2 },
    { "$and": [
        { "ReturnNumber": "NumberOfReturns" },
        { "NumberOfReturns": { "$gt": 1 } }
    ] }
] }
```

```json
{ "$not": {
    "$or": [
        { "Classification": 2 },
        { "$and": [
            { "ReturnNumber": { "$gt": 0 } },
            { "Z": { "$lte": 42 } }
        ] }
    ] }
}
```

For any individual dimension, the logical **and** may be implicitly invoked
via multiple comparisons within the comparison object.  For example:

```json
{ "X": { "$gt": 0, "$lt": 42 } }
```
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('filters.mongo', **args)
 
class filters_mortonorder(_GenericStage):
    """
(filters.mortonorder)=

# filters.mortonorder

Sorts the XY data using [Morton ordering].

It's also possible to compute a reverse Morton code by reading the binary
representation from the end to the beginning. This way, points are sorted
with a good dispersement. For example, by successively selecting N
representative points within tiles:

```{figure} filters.mortonorder.img1.png
:alt: Reverse Morton indexing
:scale: 100 %
```

```{seealso}
See [LOPoCS] and [pgmorton] for some use case examples of the
Reverse Morton algorithm.
```

```{eval-rst}
.. embed::
```

## Example

```json
[
    "uncompressed.las",
    {
        "type":"filters.mortonorder",
        "reverse":"false"
    },
    {
        "type":"writers.las",
        "filename":"compressed.laz",
        "compression":"true"
    }
]
```

## Options

```{include} filter_opts.md
```

[lopocs]: https://github.com/Oslandia/lopocs
[morton ordering]: http://en.wikipedia.org/wiki/Z-order_curve
[pgmorton]: https://github.com/Oslandia/pgmorton
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('filters.mortonorder', **args)
 
class filters_neighborclassifier(_GenericStage):
    """
(filters.neighborclassifier)=

# filters.neighborclassifier

The **neighborclassifier filter** allows you update the value of
the classification
for specific points to a value determined by a K-nearest neighbors vote.
For each point, the [k] nearest neighbors are queried and if more than half of
them have the same value, the filter updates the selected point accordingly

For example, if an automated classification procedure put/left erroneous
vegetation points near the edges of buildings which were largely classified
correctly, you could try using this filter to fix that problem.

Similiarly, some automated classification processes result in prediction for
only a subset of the original point cloud.  This filter could be used to
extrapolate those predictions to the original.

```{eval-rst}
.. embed::
```

## Example 1

This pipeline updates the Classification of all points with classification
1 (unclassified) based on the consensus (majority) of its nearest 10 neighbors.

```json
[
    "autzen_class.las",
    {
        "type" : "filters.neighborclassifier",
        "domain" : "Classification[1:1]",
        "k" : 10
    },
    "autzen_class_refined.las"
]
```

## Example 2

This pipeline moves all the classifications from "pred.txt"
to src.las.  Any points in src.las that are not in pred.txt will be
assigned based on the closest point in pred.txt.

```json
[
    "src.las",
    {
        "type" : "filters.neighborclassifier",
        "k" : 1,
        "candidate" : "pred.txt"
    },
    "dest.las"
]
```

## Options

candidate

: A filename which points to the point cloud containing the points which
  will do the voting.  If not specified, defaults to the input of the filter.

domain

: A {ref}`range <ranges>` which selects points to be processed by the filter.
  Can be specified multiple times.  Points satisfying any range will be
  processed

k

: An integer which specifies the number of neighbors which vote on each
  selected point.

dimension

: A dimension that is treated as classification for voting purposes and whose value is
  set after voting. It is treated as an integer value. [Default: Classification]

```{include} filter_opts.md
```
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('filters.neighborclassifier', **args)
 
class filters_nndistance(_GenericStage):
    """
(filters.nndistance)=

# filters.nndistance

The NNDistance filter runs a 3-D nearest neighbor algorithm on the input
cloud and creates a new dimension, `NNDistance`, that contains a distance
metric described by the [mode] of the filter.

```{eval-rst}
.. embed::
```

## Example

```json
[
    "input.las",
    {
        "type":"filters.nndistance",
        "k":8
    },
    {
        "type":"writers.bpf",
        "filename":"output.las",
        "output_dims":"X,Y,Z,NNDistance"
    }
]
```

## Options

mode

: The mode of operation.  Either "kth", in which the distance is the euclidian
  distance of the subject point from the kth remote point or "avg" in which
  the distance is the average euclidian distance from the [k] nearest points.
  /[Default: 'kth'/]

k

: The number of k nearest neighbors to consider. /[Default: **10**/]

```{include} filter_opts.md
```
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('filters.nndistance', **args)
 
class filters_normal(_GenericStage):
    """
(filters.normal)=

# filters.normal

The **normal filter** returns the estimated normal and curvature for
a collection
of points. The algorithm first computes the eigenvalues and eigenvectors of the
collection of points, which is comprised of the k-nearest neighbors. The normal
is taken as the eigenvector corresponding to the smallest eigenvalue. The
curvature is computed as

$$
curvature = /frac{/lambda_0}{/lambda_0 + /lambda_1 + /lambda_2}
$$

where $/lambda_i$ are the eigenvalues sorted in ascending order.

The filter produces four new dimensions (`NormalX`, `NormalY`, `NormalZ`,
and `Curvature`), which can be analyzed directly, or consumed by downstream
stages for more advanced filtering.

The eigenvalue decomposition is performed using Eigen's
[SelfAdjointEigenSolver](https://eigen.tuxfamily.org/dox/classEigen_1_1SelfAdjointEigenSolver.html).

Normals will be automatically flipped towards positive Z, unless the [always_up]
flag is set to `false`. Users can optionally set any of the XYZ coordinates to
specify a custom [viewpoint] or set them all to zero to effectively disable the
normal flipping.

```{note}
By default, the Normal filter will invert normals such that they are always
pointed "up" (positive Z). If the user provides a [viewpoint], normals will
instead be inverted such that they are oriented towards the viewpoint,
regardless of the [always_up] flag. To disable all normal flipping, do not
provide a [viewpoint] and set [always_up] to false.
```

In addition to [always_up] and [viewpoint], users can run a refinement step (off
by default) that propagates normals using a minimum spanning tree. The
propagated normals can lead to much more consistent results across the dataset.

```{note}
To enable normal propagation, users can set [refine] to `true`.
```

```{eval-rst}
.. embed::
```

## Example

This pipeline demonstrates the calculation of the normal values (along with
curvature). The newly created dimensions are written out to BPF for further
inspection.

```json
[
    "input.las",
    {
        "type":"filters.normal",
        "knn":8
    },
    {
        "type":"writers.bpf",
        "filename":"output.bpf",
        "output_dims":"X,Y,Z,NormalX,NormalY,NormalZ,Curvature"
    }
]
```

## Options

knn

: The number of k-nearest neighbors. /[Default: 8/]

viewpoint

: A single WKT or GeoJSON 3D point. Normals will be inverted such that they are
  all oriented towards the viewpoint.

always_up

: A flag indicating whether or not normals should be inverted only when the Z
  component is negative. /[Default: true/]

refine

: A flag indicating whether or not to reorient normals using minimum spanning
  tree propagation. /[Default: false/]

```{include} filter_opts.md
```
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('filters.normal', **args)
 
class filters_optimalneighborhood(_GenericStage):
    """
(filters.optimalneighborhood)=

# filters.optimalneighborhood

The **Optimal Neighborhood filter** computes the eigenentropy (defined as the
Shannon entropy of the normalized eigenvalues) for a neighborhood of points in
the range `min_k` to `max_k`. The neighborhood size that minimizes the
eigenentropy is saved to a new dimension `OptimalKNN`. The corresponding
radius of the neighborhood is saved to `OptimalRadius`. These dimensions can
be written to an output file or utilized directly by
{ref}`filters.covariancefeatures`.

```{eval-rst}
.. embed::
```

## Example

```json
[
    "input.las",
    {
        "type":"filters.optimalneighborhood",
        "min_k":8,
        "max_k": 50
    },
    {
        "type":"writers.las",
        "minor_version":4,
        "extra_dims":"all",
        "forward":"all",
        "filename":"output.las"
    }
]
```

## Options

min_k

: The minimum number of k nearest neighbors to consider for optimal
  neighborhood selection. /[Default: 10/]

max_k

: The maximum number of k nearest neighbors to consider for optimal
  neighborhood selection. /[Default: 14/]
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('filters.optimalneighborhood', **args)
 
class filters_outlier(_GenericStage):
    """
(filters.outlier)=

# filters.outlier

The **outlier filter** provides two outlier filtering methods: radius and
statistical. These two approaches are discussed in further detail below.

It is worth noting that both filtering methods simply apply a classification
value of 7 to the noise points (per the [LAS specification]).
To remove the noise
points altogether, users can add a {ref}`range filter<filters.range>` to their
pipeline, downstream from the outlier filter.

```{eval-rst}
.. embed::
```

```json
{
  "type":"filters.range",
  "limits":"Classification![7:7]"
}
```

## Statistical Method

The default method for identifying outlier points is the statistical outlier method. This method requires two passes through the input `PointView`, first to compute a threshold value based on global statistics, and second to identify outliers using the computed threshold.

In the first pass, for each point $p_i$ in the input `PointView`, compute the mean distance $/mu_i$ to each of the $k$ nearest neighbors (where $k$ is configurable and specified by [mean_k]). Then,

$$
/overline{/mu} = /frac{1}{N} /sum_{i=1}^N /mu_i
$$

$$
/sigma = /sqrt{/frac{1}{N-1} /sum_{i=1}^N (/mu_i - /overline{/mu})^2}
$$

A global mean $/overline{/mu}$ of these mean distances is then computed along with the standard deviation $/sigma$. From this, the threshold is computed as

$$
t = /mu + m/sigma
$$

where $m$ is a user-defined multiplier specified by [multiplier].

We now iterate over the pre-computed mean distances $/mu_i$ and compare to computed threshold value. If $/mu_i$ is greater than the threshold, it is marked as an outlier.

$$
outlier_i = /begin{cases}
    /text{true,} /phantom{false,} /text{if } /mu_i >= t //
    /text{false,} /phantom{true,} /text{otherwise} //
/end{cases}
$$

```{figure} filters.statisticaloutlier.img1.png
:alt: Points before outlier removal
:scale: 70 %
```

Before outlier removal, noise points can be found both above and below the
scene.

```{figure} filters.statisticaloutlier.img2.png
:alt: Points after outlier removal
:scale: 60 %
```

After outlier removal, the noise points are removed.

See {cite:p}`rusu2008towards` for more information.

### Example

In this example, points are marked as outliers if the average distance to each
of the 12 nearest neighbors is below the computed threshold.

```json
[
    "input.las",
    {
        "type":"filters.outlier",
        "method":"statistical",
        "mean_k":12,
        "multiplier":2.2
    },
    "output.las"
]
```

## Radius Method

For each point $p_i$ in the input `PointView`, this method counts the
number of neighboring points $k_i$ within radius $r$ (specified by
[radius]). If $k_i<k_{min}$, where $k_{min}$ is the minimum number
of neighbors specified by [min_k], it is marked as an outlier.

$$
outlier_i = /begin{cases}
    /text{true,} /phantom{false,} /text{if } k_i < k_{min} //
    /text{false,} /phantom{true,} /text{otherwise} //
/end{cases}
$$

### Example

The following example will mark points as outliers when there are fewer than
four neighbors within a radius of 1.0.

```json
[
    "input.las",
    {
        "type":"filters.outlier",
        "method":"radius",
        "radius":1.0,
        "min_k":4
    },
    "output.las"
]
```

## Options

class

: The classification value to apply to outliers. /[Default: 7/]

method

: The outlier removal method (either "statistical" or "radius").
  /[Default: "statistical"/]

min_k

: Minimum number of neighbors in radius (radius method only). /[Default: 2/]

radius

: Radius (radius method only). /[Default: 1.0/]

mean_k

: Mean number of neighbors (statistical method only). /[Default: 8/]

multiplier

: Standard deviation threshold (statistical method only). /[Default: 2.0/]

```{include} filter_opts.md
```

[las specification]: http://www.asprs.org/a/society/committees/standards/LAS_1_4_r13.pdf
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('filters.outlier', **args)
 
class filters_overlay(_GenericStage):
    """
(filters.overlay)=

# filters.overlay

The **overlay filter** allows you to set the values of a selected dimension
based on an OGR-readable polygon or multi-polygon.

```{eval-rst}
.. embed::
```

```{eval-rst}
.. streamable::
```

## OGR SQL support

You can limit your queries based on OGR's SQL support. If the
filter has both a [datasource] and a [query] option, those will
be used instead of the entire OGR data source. At this time it is
not possible to further filter the OGR query based on a geometry
but that may be added in the future.

```{note}
The OGR SQL support follows the rules specified in [ExecuteSQL]
documentation, and it will pass SQL down to the underlying
datasource if it can do so.
```

## Example 1

In this scenario, we are altering the attributes of the dimension
`Classification`.  Points from autzen-dd.las that lie within a feature will
have their classification to match the `CLS` field associated with that
feature.

```json
[
    "autzen-dd.las",
    {
        "type":"filters.overlay",
        "dimension":"Classification",
        "datasource":"attributes.shp",
        "layer":"attributes",
        "column":"CLS"
    },
    {
        "filename":"attributed.las",
        "scale_x":0.0000001,
        "scale_y":0.0000001
    }
]
```

## Example 2

This example sets the Intensity attribute to `CLS` values read from the
[OGR SQL] query.

```json
[
    "autzen-dd.las",
    {
        "type":"filters.overlay",
        "dimension":"Intensity",
        "datasource":"attributes.shp",
        "query":"SELECT CLS FROM attributes where cls!=6",
        "column":"CLS"
    },
    "attributed.las"
]
```

## Options

bounds

: A bounds to pre-filter the OGR datasource that is passed to
  [OGR_L_SetSpatialFilter](https://gdal.org/en/latest/doxygen/classOGRLayer.html#a0b4ab45cf97cbc470f0d60474d3e4169)
  in the form `([xmin, xmax], [ymin, ymax])`.

dimension

: Name of the dimension whose value should be altered.  /[Required/]

datasource

: OGR-readable datasource for Polygon or MultiPolygon data.  /[Required/]

column

: The OGR datasource column from which to read the attribute.
  /[Default: first column/]

query

: OGR SQL query to execute on the datasource to fetch geometry and attributes.
  The entire layer is fetched if no query is provided.  /[Default: none/]

layer

: The data source's layer to use. /[Default: first layer/]

threads

: The number of threads to use. Only valid in {ref}`standard mode <processing_modes>`. /[Default: 1/]

```{include} filter_opts.md
```

[executesql]: https://gdal.org/en/latest/doxygen/classGDALDataset.html#a5b65948b1e15fa63e96c0640eb6c5d7c
[ogr sql]: https://gdal.org/en/latest/user/ogr_sql_sqlite_dialect.html
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('filters.overlay', **args)
 
class filters_planefit(_GenericStage):
    """
(filters.planefit)=

# filters.planefit

The **Plane Fit Criterion** was introduced in {cite:p}`weyrich2004post` and computes the
deviation of a point from a manifold approximating its neighbors.  First, a
plane is fit to each point's k-neighborhood by performing an eigenvalue
decomposition. Next, the mean point to plane distance is computed by
considering all points within the neighborhood. This is compared to the point
to plane distance of the current point giving rise to the k-neighborhood. As
the mean distance of the k-neighborhood approaches 0, the Plane Fit criterion
will tend toward 1. As point to plane distance of the current point approaches
0, the Plane Fit criterion will tend toward 0.

The author suggests that the Plane Fit Criterion is well suited to outlier
detection when considering noisy reconstructions of smooth surfaces, but
produces poor results around small features and creases.

The filter creates a single new dimension, `PlaneFit`, that records the
Plane Fit criterion for the current point.

```{note}
To inspect the newly created, non-standard dimensions, be sure to write to an
output format that can support arbitrary dimensions, such as BPF.
```

```{eval-rst}
.. embed::
```

## Example

The sample pipeline below computes the Plane Fit criterion with a neighborhood
of 8 neighbors. We do not apply a fixed threshold to single out outliers based
on the Plane Fit criterion as the range of values can vary from one dataset to
another. In general, higher values indicate the likelihood of a point being an
outlier.

```json
[
    "input.las",
    {
        "type":"filters.planefit",
        "knn":8
    },
    "output.laz"
]
```

## Options

knn

: The number of k nearest neighbors. /[Default: 8/]

threads

: The number of threads to use. Only valid in {ref}`standard mode <processing_modes>`. /[Default: 1/]

```{include} filter_opts.md
```
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('filters.planefit', **args)
 
class filters_pmf(_GenericStage):
    """
(filters.pmf)=

# filters.pmf

The **Progressive Morphological Filter (PMF)** is a method of
segmenting ground and non-ground returns. This filter is an implementation
of the method described in
{cite:p}`zhang2003progressive`.

```{eval-rst}
.. embed::
```

## Example

```json
[
    "input.las",
    {
        "type":"filters.pmf"
    },
    "output.las"
]
```

## Notes

- [slope] controls the height threshold at each iteration. A slope of 1.0
  represents a 1:1 or 45º.
- [initial_distance] is /_intended/_ to be set to account for z noise, so for a
  flat surface if you have an uncertainty of around 15 cm, you set
  [initial_distance] large enough to not exclude these points from the ground.
- For a given iteration, the height threshold is determined by multiplying
  slope by [cell_size] by the difference in window size between the
  current and last iteration, plus the [initial_distance]. This height
  threshold is constant across all cells and is maxed out at the
  [max_distance] value. If the difference in elevation between a point and its
  “opened” value (from the morphological operator) exceeds the height threshold,
  it is treated as non-ground.  So, bigger slope leads to bigger height
  thresholds, and these grow with each iteration (not to exceed the max).  With
  flat terrain, keep this low, the thresholds are small, and stuff is more
  aggressively dumped into non-ground class.  In rugged terrain, open things up
  a little, but then you can start missing buildings, veg, etc.
- Very large [max_window_size] values will result in a lot of potentially
  extra iteration. This parameter can have a strongly negative impact on
  computation performance.
- [exponential] is used to control the rate of growth of morphological window
  sizes toward [max_window_size]. Linear growth preserves gradually changing
  topographic features well, but demands considerable compute time. The default
  behavior is to grow the window sizes exponentially, thus reducing the number
  of iterations.
- This filter will mark all returns deemed to be ground returns with a
  classification value of 2 (per the LAS specification). To extract only these
  returns, users can add a {ref}`range filter<filters.range>` to the pipeline.

```json
{
  "type":"filters.range",
  "limits":"Classification[2:2]"
}
```

```{note}
{cite:p}`zhang2003progressive` describes the consequences and relationships of the parameters
in more detail and is the canonical resource on the topic.
```

## Options

cell_size

: Cell Size. /[Default: 1/]

exponential

: Use exponential growth for window sizes? /[Default: true/]

ignore

: Range of values to ignore. /[Optional/]

initial_distance

: Initial distance. /[Default: 0.15/]

returns

: Comma-separated list of return types into which data should be segmented.
  Valid groups are "last", "first", "intermediate" and "only". /[Default:
  "last, only"/]

max_distance

: Maximum distance. /[Default: 2.5/]

max_window_size

: Maximum window size. /[Default: 33/]

slope

: Slope. /[Default: 1.0/]

```{include} filter_opts.md
```
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('filters.pmf', **args)
 
class filters_poisson(_GenericStage):
    """
(filters.poisson)=

# filters.poisson

The **Poisson Filter** passes data Mischa Kazhdan's poisson surface
reconstruction
algorithm. {cite:p}`kazhdan2006poisson`  It creates a watertight surface from the original
point set by creating an entirely new point set representing the imputed
isosurface.  The algorithm requires normal vectors to each point in order
to run.  If the x, y and z normal dimensions are present in the input point
set, they will be used by the algorithm.  If they don't exist, the poisson
filter will invoke the PDAL normal filter to create them before running.

The poisson algorithm will usually create a larger output point set
than the input point set.  Because the algorithm constructs new points, data
associated with the original points set will be lost, as the algorithm has
limited ability to impute associated data.  However, if color dimensions
(red, green and blue) are present in the input, colors will be reconstructed
in the output point set. This filter will also run the
{ref}`normal filter <filters.normal>` on the output point set.

This integration of the algorithm with PDAL only supports a limited set of
the options available to the implementation.  If you need support for further
options, please let us know.

```{eval-rst}
.. embed::
```

## Example

```json
[
    "dense.las",
    {
      "type":"filters.assign"
      "value": [
          "Red = Red / 256",
          "Green = Green / 256",
          "Blue = Blue / 256"
        ]
    },
    {
        "type":"filters.poisson"
    },
    {
      "type":"filters.assign"
      "value": [
          "Red = Red * 256",
          "Green = Green * 256",
          "Blue = Blue * 256"
        ]
    },
    {
        "type":"writers.ply",
        "faces":true,
        "filename":"isosurface.ply"
    }
]
```

```{note}
The algorithm is slow.  On a reasonable desktop machine, the surface
reconstruction shown below took about 15 minutes.
```


```{note}
  The filter only supports 8-bit color. It does not scale input or output at this
  time. If your input is something other than 8-bit color, you must scale it
  using filters.assign before running the filter. You may also want to scale
  the 8-bit output depending on your needs. See the example below that scales
  from and to 16-bit color.
```



```{figure} ../images/poisson_points.png
Point cloud (800,000 points)
```

```{figure} ../images/poisson_edges.png
Reconstruction (1.8 million vertices, 3.7 million faces)
```

## Options

density

: Write an estimate of neighborhood density for each point in the output
  set.

depth

: Maximum depth of the tree used for reconstruction. The output is sensitive
  to this parameter.  Increase if the results appear unsatisfactory.
  /[Default: 8/]

```{include} filter_opts.md
```

"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('filters.poisson', **args)
 
class filters_projpipeline(_GenericStage):
    """
(filters.projpipeline)=

# filters.projpipeline

The projpipeline filter applies a coordinates transformation pipeline. The pipeline could be specified as PROJ string (single step operation or multiple step string starting with +proj=pipeline), a WKT2 string describing a CoordinateOperation, or a `<urn:ogc:def:coordinateOperation:EPSG::XXXX>` URN.

```{note}
The projpipeline filter does not consider any spatial reference information.
However user could specify an output srs, but no check is done to ensure
the compliance with the provided transformation pipeline.
```

```{note}
The projpipeline filter is enabled if the version of GDAL is superior or equal to 3.0
```

```{eval-rst}
.. streamable::
```

## Example

This example shift point on the z-axis.

```json
[
    "untransformed.las",
    {
        "type":"filters.projpipeline",
        "coord_op":"+proj=affine +zoff=100"
    },
    {
        "type":"writers.las",
        "filename":"transformed.las"
    }
]
```

This example apply a shift on the z-axis then reproject from utm 10
to WGS84, using the `reverse_transfo` flag. It also set the output srs

```json
[
    "utm10.las",
    {
        "type":"filters.projpipeline",
        "coord_op":"+proj=pipeline +step +proj=unitconvert +xy_in=deg +xy_out=rad +step +proj=utm +zone=10 +step +proj=affine +zoff=100",
        "reverse_transfo": "true",
        "out_srs": "EPSG:4326"
    },
    {
        "type":"writers.las",
        "filename":"wgs84.las"
    }
]
```

```{note}
PDAL use the GDAL `OGRCoordinateTransformation` class to transform coordinates.
By default output angular unit are in radians. To change to degrees we need to
apply a unit conversion step.
```

## Options

coord_op

: The coordinate operation string.
  Could be specified as PROJ string (single step operation or
  multiple step string starting with +proj=pipeline),
  a WKT2 string describing a CoordinateOperation,
  or a “<urn:ogc:def:coordinateOperation:EPSG::XXXX>” URN.

reverse_transfo

: Boolean, Whether the coordinate operation should be evaluated
  in the reverse path /[Default: false/]

out_srs

: The spatial reference system of the file to be written.
  Can be an EPSG string (e.g. “EPSG:26910”) or a WKT string.
  No check is done to ensure the compliance with the specified coordinate
  operation /[Default: Not set/]

```{include} filter_opts.md
```
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('filters.projpipeline', **args)
 
class filters_python(_GenericStage):
    """
(filters.python)=

# filters.python

The **Python Filter** allows [Python] software to be embedded in a
{ref}`pipeline` that allows modification of PDAL points through a [NumPy]
array.  Additionally, some global {ref}`metadata` is also
available that Python functions can interact with.

The function must have two [NumPy] arrays as arguments, `ins` and `outs`.
The `ins` array represents the points before the `filters.python`
filter and the `outs` array represents the points after filtering.

````{warning}
Make sure [NumPy] is installed in your [Python] environment.

```shell
$ python3 -c "import numpy; print(numpy.__version__)"
1.18.1
```
````

```{warning}
Each array contains all the {ref}`dimensions` of the incoming `ins`
point schema.  Each array in the `outs` list matches the [NumPy]
array of the same type as provided as `ins` for shape and type.
```

```{eval-rst}
.. plugin::
```

```python
import numpy as np

def multiply_z(ins,outs):
    Z = ins['Z']
    Z = Z * 10.0
    outs['Z'] = Z
    return True
```

1. The function must always return `True` upon success. If the function
   returned `False`, an error would be thrown and the {ref}`pipeline` exited.

2. If you want write a dimension that might not be available, you can specify
   it with the [add_dimension] option:

   ```
   "add_dimension": "NewDimensionOne"
   ```

   To create more than one dimension, this option also accepts an array:

   ```
   "add_dimension": [ "NewDimensionOne", "NewDimensionTwo", "NewDimensionThree" ]
   ```

   You can also specify the {ref}`type <types>` of the dimension using an `=`.

   ```
   "add_dimension": "NewDimensionOne=uint8"
   ```

## Modification Example

```json
[
    "file-input.las",
    {
        "type":"filters.smrf"
    },
    {
        "type":"filters.python",
        "script":"multiply_z.py",
        "function":"multiply_z",
        "module":"anything"
    },
    {
        "type":"writers.las",
        "filename":"file-filtered.las"
    }
]
```

The JSON pipeline file referenced the external `multiply_z.py` [Python] script,
which scales the `Z` coordinate by a factor of 10.

```python
import numpy as np

def multiply_z(ins,outs):
    Z = ins['Z']
    Z = Z * 10.0
    outs['Z'] = Z
    return True
```

## Predicates

Points can be retained/removed from the stream by setting true/false values
into a special "Mask" dimension in the output point array.

The example above sets the "mask" to true for points that are in
classifications 1 or 2 and to false otherwise, causing points that are not
classified 1 or 2 to be dropped from the point stream.

```python
import numpy as np

def filter(ins,outs):
   cls = ins['Classification']

   keep_classes = [1, 2]

   # Use the first test for our base array.
   keep = np.equal(cls, keep_classes[0])

   # For 1:n, test each predicate and join back
   # to our existing predicate array
   for k in range(1, len(keep_classes)):
       t = np.equal(cls, keep_classes[k])
       keep = keep + t

   outs['Mask'] = keep
   return True
```

```{note}
{ref}`filters.range` is a specialized filter that implements the exact
functionality described in this Python operation. It is likely to be much
faster than Python, but not as flexible. {ref}`filters.python` is the tool
you can use for prototyping point stream processing operations.
```

```{seealso}
If you want to read a {ref}`pipeline` of operations into a numpy
array, the [PDAL Python extension](https://pypi.python.org/pypi/PDAL)
is available.
```

### Example pipeline

```json
[
    "file-input.las",
    {
        "type":"filters.smrf"
    },
    {
        "type":"filters.python",
        "script":"filter_pdal.py",
        "function":"filter",
        "module":"anything"
    },
    {
        "type":"writers.las",
        "filename":"file-filtered.las"
    }
]
```

## Module Globals

Three global variables are added to the Python module as it is run to allow
you to get {ref}`dimensions`, {ref}`metadata`, and coordinate system
information.
Additionally, the `metadata` object can be set by the function
to modify metadata
for the in-scope {ref}`filters.python` {cpp:class}`pdal::Stage`.

```python
def myfunc(ins,outs):
    print('schema: ', schema)
    print('srs: ', spatialreference)
    print('metadata: ', metadata)
    outs = ins
    return True
```

### Setting stage metadata

```{note}
The name of the output metadata variable has changed from `metadata` to `out_metadata`.
```

Stage metadata can be created by using the `out_metadata` dictionary **global** variable.
The `name` key must be set. The type of the `value` can usually be inferred, but
can be set to one of `integer`, `nonNegativeInteger`, `double`, `bounds`,
`boolean`, `spatialreference`, `uuid` or `string`.

Children may be set using the `children` key whose value is a list of dictionaries.

```python
def myfunc(ins,outs):
  global out_metadata
  out_metadata = {'name': 'root', 'value': 'a string', 'type': 'string', 'description': 'a description', 'children': [{'name': 'somekey', 'value': 52, 'type': 'integer', 'description': 'a filter description', 'children': []}, {'name': 'readers.faux', 'value': 'another string', 'type': 'string', 'description': 'a reader description', 'children': []}]}
  return True
```

### Passing Python objects

An JSON-formatted option can be passed to the filter representing a
Python dictionary containing objects you want to use in your function.
This feature is useful in situations where you
wish to call {ref}`pipeline_command` with substitutions.

If we needed to be able to provide the Z scaling factor of [Example Pipeline]
with a
Python argument, we can place that in a dictionary and pass that to the filter
as a separate argument. This feature allows us to be able easily reuse the same
basic Python function while substituting values as necessary.

```json
[
    "input.las",
    {
        "type":"filters.python",
        "module":"anything",
        "function":"filter",
        "script":"arguments.py",
        "pdalargs":"{/"factor/":0.3048,/"an_argument/":42, /"another/": /"a string/"}"
    },
    "output.las"
]
```

With that option set, you can now fetch the [pdalargs] dictionary in your
Python script and use it:

```python
import numpy as np

def multiply_z(ins,outs):
    Z = ins['Z']
    Z = Z * float(pdalargs['factor'])
    outs['Z'] = Z
    return True
```

### Standard output and error

A `redirector` module is available for scripts to output to PDAL's log stream
explicitly. The module handles redirecting `sys.stderr` and
`sys.stdout` for you
transparently, but it can be used directly by scripts. See the PDAL source
code for more details.

## Options

script

: When reading a function from a separate [Python] file, the file name to read
  from.

source

: The literal [Python] code to execute, when the script option is
  not being used.

module

: The Python module that is holding the function to run. /[Required/]

function

: The function to call. /[Required/]

add_dimension

: A dimension name or an array of dimension names to add to the pipeline that do not already exist.

pdalargs

: A JSON dictionary of items you wish to pass into the modules globals as the
  `pdalargs` object.

```{include} filter_opts.md
```

[numpy]: http://www.numpy.org/
[python]: http://python.org/
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('filters.python', **args)
 
class filters_radialdensity(_GenericStage):
    """
(filters.radialdensity)=

# filters.radialdensity

The **Radial Density filter** creates a new attribute `RadialDensity` that
contains the density of points in a sphere of given radius.

The density at each point is computed by counting the number of points falling
within a sphere of given [radius] (default is 1.0) and centered at the current
point. The number of neighbors (including the query point) is then normalized
by the volume of the sphere, defined as

$$
V = /frac{4}{3} /pi r^3
$$

The radius $r$ can be adjusted by changing the [radius] option.

```{eval-rst}
.. embed::
```

## Example

```json
[
    "input.las",
    {
        "type":"filters.radialdensity",
        "radius":2.0
    },
    {
        "type":"writers.bpf",
        "filename":"output.bpf",
        "output_dims":"X,Y,Z,RadialDensity"
    }
]
```

## Options

radius

: Radius. /[Default: 1.0/]

```{include} filter_opts.md
```
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('filters.radialdensity', **args)
 
class filters_randomize(_GenericStage):
    """
(filters.randomize)=

# filters.randomize

The randomize filter reorders the points in a point view randomly.

```{eval-rst}
.. embed::
```

## Example

```json
[
    "input.las",
    {
        "type":"filters.randomize"
    },
    {
        "type":"writers.las",
        "filename":"output.las"
    }
]
```

## Options

```{include} filter_opts.md
```
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('filters.randomize', **args)
 
class filters_range(_GenericStage):
    """
(filters.range)=

# filters.range

The **Range Filter** applies rudimentary filtering to the input point cloud
based on a set of criteria on the given dimensions.

```{eval-rst}
.. embed::
```

```{eval-rst}
.. streamable::


```

```{note}
We suggest you start using {ref}`filters.expression` for PDAL 2.5.x+.
The syntax is simpler, and it is the same syntax that is used by
the `where` option of many stages. `filters.range` will
be deprecated starting PDAL 3.0.
```

## Example

This example passes through all points whose `Z` value is in the
range /[0,100/]
and whose `Classification` equals 2 (corresponding to ground in LAS).

```json
[
    "input.las",
    {
        "type":"filters.range",
        "limits":"Z[0:100],Classification[2:2]"
    },
    {
        "type":"writers.las",
        "filename":"filtered.las"
    }
]
```

The equivalent pipeline invoked via the PDAL `translate` command would be

```bash
$ pdal translate -i input.las -o filtered.las -f range --filters.range.limits="Z[0:100],Classification[2:2]"
```

## Options

limits

: A comma-separated list of {ref}`ranges`.  If more than one range is
  specified for a dimension, the criteria are treated as being logically
  ORed together.  Ranges for different dimensions are treated as being
  logically ANDed.

  Example:

  ```
  Classification[1:2], Red[1:50], Blue[25:75], Red[75:255], Classification[6:7]
  ```

  This specification will select points that have the classification of
  1, 2, 6 or 7 and have a blue value or 25-75 and have a red value of
  1-50 or 75-255.  In this case, all values are inclusive.

```{include} filter_opts.md
```

(ranges)=

## Ranges

A range specification is a dimension name, followed by an optional negation
character ('!'), and a starting and ending value separated by a colon,
surrounded by parentheses or square brackets.  Either the starting or ending
values can be omitted.  Parentheses indicate an open endpoint that doesn't
include the adjacent value.  Square brackets indicate a closed endpoint
that includes the adjacent value.

### Example 1:

```
Z[10:]
```

Selects all points with a Z value greater than or equal to 10.

### Example 2:

```
Classification[2:2]
```

Selects all points with a classification of 2.

### Example 3:

```
Red!(20:40]
```

Selects all points with red values less than or equal to 20 and those with
values greater than 40

### Example 4:

```
Blue[:255)
```

Selects all points with a blue value less than 255.

### Example 5:

```
Intensity![25:25]
```

Selects all points with an intensity not equal to 25.
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('filters.range', **args)
 
class filters_reciprocity(_GenericStage):
    """
(filters.reciprocity)=

# filters.reciprocity

The **Nearest-Neighbor Reciprocity Criterion** was introduced in {cite:p}`weyrich2004post`
and is based on a simple assumption, that valid points may be in the
k-neighborhood of an outlier, but the outlier will most likely not be part of
the valid point's k-neighborhood.

The author suggests that the Nearest-Neighbor Reciprocity Criterion is more
robust than both the {ref}`Plane Fit <filters.planefit>` and {ref}`Miniball
<filters.miniball>` Criterion, being equally sensitive around smooth and
detailed regions. The criterion does however produce invalid results near
manifold borders.

The filter creates a single new dimension, `Reciprocity`, that records the
percentage of points(in the range 0 to 100) that are considered uni-directional
neighbors of the current point.

```{note}
To inspect the newly created, non-standard dimensions, be sure to write to an
output format that can support arbitrary dimensions, such as BPF.
```

```{eval-rst}
.. embed::
```

## Example

The sample pipeline below computes reciprocity with a neighborhood of 8
neighbors, followed by a range filter to crop out points whose `Reciprocity`
percentage is less than 98% before writing the output.

```json
[
    "input.las",
    {
        "type":"filters.reciprocity",
        "knn":8
    },
    {
        "type":"filters.range",
        "limits":"Reciprocity[:98.0]"
    },
    "output.laz"
]
```

## Options

knn

: The number of k nearest neighbors. /[Default: 8/]

threads

: The number of threads to use. Only valid in {ref}`standard mode <processing_modes>`. /[Default: 1/]

```{include} filter_opts.md
```
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('filters.reciprocity', **args)
 
class filters_relaxationdartthrowing(_GenericStage):
    """
(filters.relaxationdartthrowing)=

# filters.relaxationdartthrowing

The **Relaxation Dart Throwing Filter** is a variation on Poisson sampling. The
approach was first introduced by {cite:p}`mccool1992hierarchical`. The filter operates nearly
identically to {ref}`filters.sample`, except it will continue to shrink the
radius with each pass through the point cloud until the desired number of
output points is reached.

```{seealso}
{ref}`filters.decimation`, {ref}`filters.fps` and {ref}`filters.sample` all
perform some form of thinning or resampling.
```

```{note}
The `shuffle` option does not reorder points in the PointView, but
shuffles the order in which the points are visited while processing, which
can improve the quality of the result.
```

```{eval-rst}
.. embed::
```

## Options

decay

: Decay rate for the radius shrinkage. /[Default: 0.9/]

radius

: Starting minimum distance between samples. /[Default: 1.0/]

count

: Desired number of points in the output. /[Default: 1000/]

shuffle

: Choose whether or not to shuffle order in which points are visited. /[Default:
  true/]

seed

: Seed for random number generator, used only with shuffle.

```{include} filter_opts.md
```
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('filters.relaxationdartthrowing', **args)
 
class filters_reprojection(_GenericStage):
    """
(filters.reprojection)=

# filters.reprojection

The **reprojection filter** converts the X, Y and/or Z dimensions to a
new spatial
reference system. The old coordinates are replaced by the new ones.
If you want to preserve the old coordinates for future processing, use a
{ref}`filters.ferry` to create copies of the original dimensions before
reprojecting.

```{note}
When coordinates are reprojected, it may significantly change the precision
necessary to represent the values in some output formats.  Make sure
that you're familiar with any scaling necessary for your output format
based on the projection you've used.
```

```{eval-rst}
.. embed::
```

```{eval-rst}
.. streamable::
```

## Example 1

This pipeline reprojects terrain points with Z-values between 0 and 100 by first
applying a range filter and then specifying both the input and output spatial
reference as EPSG-codes. The X and Y dimensions are scaled to allow enough
precision in the output coordinates.

```json
[
    {
        "filename":"input.las",
        "type":"readers.las",
        "spatialreference":"EPSG:26916"
    },
    {
        "type":"filters.range",
        "limits":"Z[0:100],Classification[2:2]"
    },
    {
        "type":"filters.reprojection",
        "in_srs":"EPSG:26916",
        "out_srs":"EPSG:4326"
    },
    {
        "type":"writers.las",
        "scale_x":"0.0000001",
        "scale_y":"0.0000001",
        "scale_z":"0.01",
        "offset_x":"auto",
        "offset_y":"auto",
        "offset_z":"auto",
        "filename":"example-geog.las"
    }
]
```

## Example 2

In some cases it is not possible to use a EPSG-code as a spatial reference.
Instead {{ PROJ }} parameters can be used to define a spatial
reference.  In this example the vertical component of points in a laz file is
converted from geometric (ellipsoidal) heights to orthometric heights by using
the `geoidgrids` parameter from PROJ.  Here we change the vertical datum
from the GRS80 ellipsoid to DVR90, the vertical datum in Denmark. In the
writing stage of the pipeline the spatial reference of the file is set to
EPSG:7416. The last step is needed since PDAL will otherwise reference the
vertical datum as "Unnamed Vertical Datum" in the spatial reference VLR.

```json
[
    "./1km_6135_632.laz",
    {
        "type":"filters.reprojection",
        "in_srs":"EPSG:25832",
        "out_srs":"+init=epsg:25832 +geoidgrids=C:/data/geoids/dvr90.gtx"
    },
    {
        "type":"writers.las",
        "a_srs":"EPSG:7416",
        "filename":"1km_6135_632_DVR90.laz"
    }
]
```

## Options

in_srs

: Spatial reference system of the input data. Express as an EPSG string (eg
  "EPSG:4326" for WGS84 geographic), PROJ string or a well-known text
  string. /[Required if not part of the input data set/]

out_srs

: Spatial reference system of the output data. Express as an EPSG string (eg
  "EPSG:4326" for WGS84 geographic), PROJ string or a well-known text
  string. /[Required/]

in_axis_ordering

: An array of numbers that override the axis order for the in_srs (or if
  not specified, the inferred SRS from the previous Stage). "2, 1" for
  example would swap X and Y, which may be commonly needed for
  something like "EPSG:4326".

in_coord_epoch

: Coordinate epoch for the input coordinate system as a double. /[Default: 0/]

out_axis_ordering

: An array of numbers that override the axis order for the out_srs.
  "2, 1" for example would swap X and Y, which may be commonly needed for
  something like "EPSG:4326".

out_coord_epoch

: Coordinate epoch for the output coordinate system as a double. /[Default: 0/]

error_on_failure

: If true and reprojection of any point fails, throw an exception that terminates
  PDAL . /[Default: false/]
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('filters.reprojection', **args)
 
class filters_returns(_GenericStage):
    """
(filters.returns)=

# filters.returns

The **Returns Filter** takes a single PointView as its input and creates a
`PointView` for each of the user-specified [groups] defined below.

"first" is defined as those points whose `ReturnNumber` is 1 when the `NumberOfReturns` is greater than 1.

"intermediate" is defined as those points whose `ReturnNumber` is greater than 1 and less than `NumberOfReturns` when `NumberOfReturns` is greater than 2.

"last" is defined as those points whose `ReturnNumber` is equal to `NumberOfReturns` when `NumberOfReturns` is greater than 1.

"only" is defined as those points whose `NumberOfReturns` is 1.

```{eval-rst}
.. embed::
```

## Example

This example creates two separate output files for the "last" and "only"
returns.

```json
[
    "input.las",
    {
        "type":"filters.returns",
        "groups":"last,only"
    },
    "output_#.las"
]
```

## Options

groups

: Comma-separated list of return number groupings. Valid options are "first",
  "last", "intermediate" or "only". /[Default: "last"/]

```{include} filter_opts.md
```
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('filters.returns', **args)
 
class filters_sample(_GenericStage):
    """
(filters.sample)=

# filters.sample

The **Sample Filter** performs Poisson sampling of the input `PointView`. The
practice of performing Poisson sampling via "Dart Throwing" was introduced
in the mid-1980's by {cite:p}`cook1986stochastic` and {cite:p}`dippe1985antialiasing`, and has been applied to
point clouds in other software {cite:p}`cite_mesh2009`.

Our implementation of Poisson sampling is made streamable by voxelizing the
space and only adding points to the output `PointView` if they do not violate
the minimum distance criterion (as specified by `radius`). The voxelization
allows several optimizations, first by checking for existing points within the
same voxel as the point under consideration, which are mostly likely to
violate the minimum distance criterion. Furthermore, we can easily visit
neighboring voxels (limiting the search to those that are populated) without
the need to create a KD-tree from the entire input `PointView` first and
performing costly spatial searches.

```{seealso}
{ref}`filters.decimation`, {ref}`filters.fps`,
{ref}`filters.relaxationdartthrowing`,
{ref}`filters.voxelcenternearestneighbor`,
{ref}`filters.voxelcentroidnearestneighbor`, and {ref}`filters.voxeldownsize` also
perform decimation.
```

```{note}
Starting with PDAL v2.3, the `filters.sample` now supports streaming
mode. As a result, there is no longer an option to `shuffle` points (or
to provide a `seed` for the shuffle).
```

```{note}
Starting with PDAL v2.3, a `cell` option has been added that works with
the existing `radius`. The user must provide one or the other, but not
both. The provided option will be used to automatically compute the other.
The relationship between `cell` and `radius` is such that the
`radius` defines the radius of a sphere that circumscribes a voxel with
edge length defined by `cell`.
```

```{note}
Care must be taken with selection of the `cell`/`radius` option.
Although the filter can now operate in streaming mode, if the extents of
the point cloud are large (or conversely, if the cell size is small) the
voxel occupancy map which grows as a function of these variables can still
require a large memory footprint.
```

```{note}
To operate in streaming mode, the filter will typically retain the first
point to occupy a voxel (subject to the minimum distance criterion set
forth earlier). This means that point ordering matters, and in fact, it is
quite possible that points in the incoming stream can be ordered in such a
way as to introduce undesirable artifacts (e.g., related to previous tiling
of the data). In our experience, processing data that is still in scan
order (ordered by GpsTime, if available) does produce reliable results,
although to require this sort either internally or by inserting
{ref}`filters.sort` prior to sampling would break our ability to stream the
data.
```

```{eval-rst}
.. embed::
```

```{eval-rst}
.. streamable::
```

## Options

cell

: Voxel cell size. If `radius` is set, `cell` is automatically computed
  such that the cell is circumscribed by the sphere defined by `radius`.

dimension

: Instead of culling points, create a new `uint8_t` dimension with this name and
  write a `1` if the point was sampled and a `0` if it was not sampled.

origin_x

: X origin of the voxelization for sampling.  /[Default: X of first point/]

origin_y

: Y origin of the voxelization for sampling.  /[Default: Y of first point/]

origin_z

: Z origin of the voxelization for sampling.  /[Default: Z of first point/]

radius

: Minimum distance between samples. If `cell` is set, `radius` is
  automatically computed to defined a sphere that circumscribes the voxel cell.
  Whether specified or derived, `radius` defines the minimum allowable
  distance between points.

```{include} filter_opts.md
```
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('filters.sample', **args)
 
class filters_separatescanline(_GenericStage):
    """
(filters.separatescanline)=

# filters.separatescanline

The **Separate scan line Filter** takes a single `PointView` as its input and
creates a `PointView` for each scan line as its output. `PointView` must contain
the `EdgeOfFlightLine` dimension.

```{eval-rst}
.. embed::
```

## Example

The following pipeline will create a set of text files, where each file contains
only 10 scan lines.

```json
[
    "input.text",
    {
        "type":"filters.separatescanline",
        "groupby":10
    },
    "output_#.text"
]
```

## Options

groupby

: The number of lines to be grouped by. /[Default : 1/]

```{include} filter_opts.md
```
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('filters.separatescanline', **args)
 
class filters_shell(_GenericStage):
    """
---
orphan: true
---

(filters.shell)=

# filters.shell

The shell filter allows you to run shell operations in-line
with PDAL pipeline tasks. This can be especially useful for
follow-on items or orchestration of complex workflows.

```{eval-rst}
.. embed::
```

```{warning}
To use {ref}`filters.shell`, you must set `PDAL_ALLOW_SHELL=1`
PDAL's execution environment. Without the environment variable
set, every attempt at execution will result in the following
error:

> PDAL_ALLOW_SHELL environment variable not set, shell access is not allowed
```

## Example

GDAL processing operations applied to raster output from {ref}`writers.gdal`
are a common task. Applying these within the PDAL execution environment
can provide some convenience and allow downstream consumers to have deterministic
completion status of the task. The following task writes multiple elevation
models to disk and then uses the [gdaladdo](https://gdal.org/gdaladdo.html)
command to construct overview bands for the data using average interpolation.

```json
{
  "pipeline":[
    "autzen.las",
    {
      "type":"writers.gdal",
      "filename" : "output-1m.tif",
      "resolution" : "1.0"
    },
    {
      "type":"writers.gdal",
      "filename" : "output-2m.tif",
      "resolution" : "2.0"
    },
    {
      "type":"writers.gdal",
      "filename" : "output-5m.tif",
      "resolution" : "5.0"
    },
    {
      "type":"filters.shell",
      "command" : "gdaladdo -r average output-1m.tif 2 4 8 16"
    },
    {
      "type":"filters.shell",
      "command" : "gdaladdo -r average output-2m.tif 2 4 8 16"
    },
    {
      "type":"filters.shell",
      "command" : "gdaladdo -r average output-5m.tif 2 4 8 16"
    }
    ]
}
```

## Options

command

: The shell command to run. It is run in relation to the current
  working directory of the pipeline executing it.

```{include} filter_opts.md
```
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('filters.shell', **args)
 
class filters_skewnessbalancing(_GenericStage):
    """
(filters.skewnessbalancing)=

# filters.skewnessbalancing

**Skewness Balancing** classifies ground points based on the approach outlined
in {cite:p}`bartels2010threshold`.

```{eval-rst}
.. embed::
```

```{note}
For Skewness Balancing to work well, the scene being processed needs to be
quite flat, otherwise many above ground features will begin to be included
in the ground surface.
```

## Example

The sample pipeline below uses the Skewness Balancing filter to segment ground
and non-ground returns, using default options, and writing only the ground
returns to the output file.

```json
[
    "input.las",
    {
        "type":"filters.skewnessbalancing"
    },
    {
        "type":"filters.range",
        "limits":"Classification[2:2]"
    },
    "output.laz"
]
```

## Options

```{include} filter_opts.md
```

```{note}
The Skewness Balancing method is touted as being threshold-free. We may
still in the future add convenience parameters that are common to other
ground segmentation filters, such as `returns` or `ignore` to limit the
points under consideration for filtering.
```
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('filters.skewnessbalancing', **args)
 
class filters_smrf(_GenericStage):
    """
---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

(filters.smrf)=

# filters.smrf

The **Simple Morphological Filter (SMRF)** classifies ground points based
on the approach outlined in {cite:p}`pingel2013improved`.

```{eval-rst}
.. embed::
```

## Example #1

The sample pipeline below uses the SMRF filter to segment ground and non-ground
returns, using default options, and writing only the ground returns to the
output file.

```{code-cell}
:tags: [remove-cell]

import os
import sys

conda_env_path = os.environ.get('CONDA_PREFIX', sys.prefix)
proj_data = os.path.join(os.path.join(conda_env_path, 'share'), 'proj')
os.environ["PROJ_DATA"] = proj_data
```

```{code-cell}
json =
[
    {
        "bounds": "([-10425171.940, -10423171.940], [5164494.710, 5166494.710])",
        "filename": "https://s3-us-west-2.amazonaws.com/usgs-lidar-public/IA_FullState/ept.json",
        "type": "readers.ept"
    },
    {
        "type":"filters.smrf"
    },
    {
        "type":"filters.range",
        "limits":"Classification[2:2]"
    },
    "output.laz"
]


import pdal
pipeline = pdal.Pipeline(json)
count = pipeline.execute()
print(f"Output contains {count} points")
```

## Example #2

A more complete example, specifying some options. These match the
optimized parameters for Sample 1 given in Table 3 of {cite:p}`pingel2013improved`.

```{code-cell}
json =
[
    {
        "bounds": "([-10425171.940, -10423171.940], [5164494.710, 5166494.710])",
        "filename": "https://s3-us-west-2.amazonaws.com/usgs-lidar-public/IA_FullState/ept.json",
        "type": "readers.ept"
    },
    {
        "type":"filters.smrf",
        "scalar":1.2,
        "slope":0.2,
        "threshold":0.45,
        "window":16.0
    },
    {
        "type":"filters.range",
        "limits":"Classification[2:2]"
    },
    "output.laz"
]


import pdal
pipeline = pdal.Pipeline(json)
count = pipeline.execute()
print(f"Output contains {count} points")
```

## Options

cell

: Cell size. /[Default: 1.0/]

classbits

: Selectively ignore points marked as "synthetic", "keypoint", or "withheld".
  /[Default: empty string, use all points/]

cut

: Cut net size (`cut=0` skips the net cutting step). /[Default: 0.0/]

dir

: Optional output directory for debugging intermediate rasters.

ignore

: A {ref}`range <ranges>` of values of a dimension to ignore.

returns

: Return types to include in output.  Valid values are "first", "last",
  "intermediate" and "only". /[Default: "last, only"/]

scalar

: Elevation scalar. /[Default: **1.25**/]

slope

: Slope (rise over run). /[Default: **0.15**/]

threshold

: Elevation threshold. /[Default: **0.5**/]

window

: Max window size. /[Default: **18.0**/]

```{include} filter_opts.md
```
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('filters.smrf', **args)
 
class filters_sort(_GenericStage):
    """
(filters.sort)=

# filters.sort

The sort filter orders a point view based on the values of a {ref}`dimensions`. The
sorting can be done in increasing (ascending) or decreasing (descending) order.

```{eval-rst}
.. embed::
```

## Example

```json
[
    "unsorted.las",
    {
        "type":"filters.sort",
        "dimension":"X",
        "order":"ASC"
    },
    "sorted.las"
]
```

```{note}
See {ref}`filters.label_duplicates` for an example of using {ref}`filters.sort` to
sort multiple dimensions at once.
```

## Options

dimensions

: A list of dimensions in the order on which to sort the points. /[Required/]

order

: The order in which to sort, ASC or DESC /[Default: "ASC"/]

```{include} filter_opts.md
```
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('filters.sort', **args)
 
class filters_sparsesurface(_GenericStage):
    """
(filters.sparsesurface)=

# filters.sparsesurface

The **Sparse Surface filter** segments input points into two classes: ground or
low point. It does this by adding ground points in ascending elevation order,
and masking all neighbor points within a specified radius as low points. This
process creates a sparse sampling of the ground estimate akin to the Poisson
disk sampling available in {ref}`filters.sample` and marks all other points as
low noise. It is expected that the input point cloud will either only include
points labeled as ground or the `where` option will be employed to limit
points to those marked as ground.

```{eval-rst}
.. embed::
```

## Example #1

The sample pipeline below uses the SMRF filter to segment ground and non-ground
returns, uses the expression filter to retain only ground returns, and then the
sparse surface filter to segment ground and low noise.

```json
[
    "input.las",
    {
        "type":"filters.smrf"
    },
    {
        "type":"filters.expression",
        "expression":"Classification==2"
    },
    {
        "type":"filters.sparsesurface"
    },
    "output.laz"
]
```

## Example #2

This sample pipeline is nearly identical to the previous one, but retains all
points (including non-ground) while still only operating on ground returns when
computing the sparse surface. It also sets the only option unique to the sparse
sample filter, which is the sampling radius--no two ground points will be
closer than 3.0 meters (horizontally).

```json
[
    "input.las",
    {
        "type":"filters.smrf"
    },
    {
        "type":"filters.sparsesurface",
        "radius":3.0,
        "where":"Classification==2"
    },
    "output.laz"
]
```

## Options

radius

: Mask neighbor points as low noise. /[Default: **1.0**/]

```{include} filter_opts.md
```
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('filters.sparsesurface', **args)
 
class filters_splitter(_GenericStage):
    """
(filters.splitter)=

# filters.splitter

The **Splitter Filter** breaks a point cloud into square tiles of a
specified size.  The origin of the tiles is chosen arbitrarily unless specified
with the [origin_x] and [origin_y] option.

The splitter takes a single `PointView` as its input and creates a
`PointView` for each tile as its output.

Splitting is usually applied to data read from files (which produce one large
stream of points) before the points are written to a database (which prefer
data segmented into smaller blocks).

```{eval-rst}
.. embed::
```

## Example

```json
[
    "input.las",
    {
        "type":"filters.splitter",
        "length":"100",
        "origin_x":"638900.0",
        "origin_y":"835500.0"
    },
    {
        "type":"writers.pgpointcloud",
        "connection":"dbname='lidar' user='user'"
    }
]
```

## Options

length

: Length of the sides of the tiles that are created to hold points.
  /[Default: 1000/]

origin_x

: X Origin of the tiles.  /[Default: none (chosen arbitrarily)/]

origin_y

: Y Origin of the tiles.  /[Default: none (chosen arbitrarily)/]

buffer

: Amount of overlap to include in each tile. This buffer is added onto
  length in both the x and the y direction.  /[Default: 0/]

```{include} filter_opts.md
```
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('filters.splitter', **args)
 
class filters_stats(_GenericStage):
    """
(filters.stats)=

# filters.stats

The **Stats Filter** calculates the minimum, maximum and average (mean) values
of dimensions.  On request it will also provide an enumeration of values of
a dimension and skewness and kurtosis.

The output of the stats filter is metadata that can be stored by writers or
used through the PDAL API.  Output from the stats filter can also be
quickly obtained in JSON format by using the command "pdal info --stats".

```{note}
The filter can compute both sample and population statistics.  For kurtosis,
the filter can also compute standard and excess kurtosis.  However, only
a single value is reported for each statistic type in metadata, and that is
the sample statistic, rather than the population statistic.  For kurtosis
the sample excess kurtosis is reported.  This seems to match the behavior
of many other software packages.
```

## Example

```json
[
    "input.las",
    {
        "type":"filters.stats",
        "dimensions":"X,Y,Z,Classification",
        "enumerate":"Classification"
    },
    {
        "type":"writers.las",
        "filename":"output.las"
    }
]
```

### Options

(stats-dimensions)=

dimensions

: A comma-separated list of dimensions whose statistics should be
  processed.  If not provided, statistics for all dimensions are calculated.

enumerate

: A comma-separated list of dimensions whose values should be enumerated.
  Note that this list does not add to the list of dimensions that may be
  provided in the {ref}`dimensions <stats-dimensions>` option.

count

: Identical to the [enumerate] option, but provides a count of the number
  of points in each enumerated category.

global

: A comma-separated list of dimensions for which global statistics (median,
  mad, mode) should be calculated.

advanced

: Calculate advanced statistics (skewness, kurtosis). /[Default: false/]

```{include} filter_opts.md
```
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('filters.stats', **args)
 
class filters_straighten(_GenericStage):
    """
(filters.straighten)=

# filters.straighten

The **straighten filter** transforms the point cloud in a new parametric coordinate system,
each point in world coordinate (X,Y,Z) is being projected along closest poyline segment,
and rotated along the segment accordingly to the average m/roll value.

```{eval-rst}
.. streamable::
```

```{note}
The new coordinate system (X', Y', Z') could be understood as :
/* X' : curvilinear abcissa (or meter point)
/* Y' : orthogonal distance to segment (or orthogonal distance to line)
/* Z' : orthogonal distance from (rolling) plane
```

## Examples

```json
[
    "input.las",
    {
        "type": "filters.straighten",
        "polyline" : "LINSTRING ZM (...)"
    },
    "straighten.las"
]
```

```json
[
    "input.las",
    {
        "type": "filters.straighten",
        "polyline" : "LINSTRING ZM (...)"
    },
    "straighten.las"
]
```

## Options

polyline

: `` wkt` `` or `` json` `` definition of a 3D linestring with measurment (LINESTRING ZM in wkt) along which the cloud will be straighten.
  M is supposed to be roll expressed in radians. This is mandatory.

offset

: if you want to add an X' during straightening operation (or take an offset into account while unstraightening).
  This can be understood as a starting meter point. /[Default: 0/]

reverse

: whether to straighten or unstraighten the point cloud /[Default: `false`/]

```{include} filter_opts.md
```
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('filters.straighten', **args)
 
class filters_streamcallback(_GenericStage):
    """
(filters.streamcallback)=

# filters.streamcallback

The **Stream Callback Filter** provides a simple hook for a
user-specified action
to occur for each point.  The stream callback filter is for use by C++
programmers extending PDAL functionality and isn't useful to end users.

```{eval-rst}
.. embed::
```

```{eval-rst}
.. streamable::
```

## Options

```{include} filter_opts.md
```
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('filters.streamcallback', **args)
 
class filters_tail(_GenericStage):
    """
(filters.tail)=

# filters.tail

The **Tail Filter** returns a specified number of points from the end of the
`PointView`.

```{note}
If the requested number of points exceeds the size of the point cloud, all
points are passed with a warning.
```

```{eval-rst}
.. embed::
```

## Example

Sort and extract the 100 lowest intensity points.

```json
[
    {
        "type":"filters.sort",
        "dimension":"Intensity",
        "order":"DESC"
    },
    {
        "type":"filters.tail",
        "count":100
    }
]
```

```{seealso}
{ref}`filters.head` is the dual to {ref}`filters.tail`.
```

## Options

count

: Number of points to return. /[Default: 10/]

```{include} filter_opts.md
```
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('filters.tail', **args)
 
class filters_teaser(_GenericStage):
    """
(filters.teaser)=

# filters.teaser

The **TEASER filter** uses the Truncated least squares Estimation And
SEmidefinite Relaxation (TEASER) algorithm {cite:p}`yang2020teaser` to calculate a **rigid**
transformation that best aligns two datasets. The first input to the ICP filter
is considered the "fixed" points, and all subsequent points are "moving"
points. The output from the filter are the "moving" points after the calculated
transformation has been applied, one point view per input. The transformation
matrix is inserted into the stage's metadata.

```{seealso}
The plugin wraps the TEASER++ library, which can be found at
<https://github.com/MIT-SPARK/TEASER-plusplus>.
```

```{eval-rst}
.. plugin::
```

## Examples

```json
[
    "fixed.las",
    "moving.las",
    {
        "type": "filters.teaser"
    },
    "output.las"
]
```

To get the `transform` matrix, you'll need to use the `--metadata` option
from the pipeline command:

```
$ pdal pipeline teaser-pipeline.json --metadata teaser-metadata.json
```

The metadata output might start something like:

```json
{
    "stages":
    {
        "filters.teaser":
        {
            "centroid": "    583394  5.2831e+06   498.152",
            "composed": "           1  2.60209e-18 -1.97906e-09       -0.374999  8.9407e-08            1  5.58794e-09      -0.614662 6.98492e -10 -5.58794e-09            1   0.033234           0            0            0            1",
            "converged": true,
            "fitness": 0.01953125097,
            "transform": "           1  2.60209e-18 -1.97906e-09       -0.375  8.9407e-08            1  5.58794e-09      -0.5625 6.98492e -10 -5.58794e-09            1   0.00411987           0            0            0            1"
        }
```

To apply this transformation to other points, the `centroid` and
`transform` metadata items can by used with `filters.transformation` in
another pipeline. First, move the centroid of the points to (0,0,0), then apply
the transform, then move the points back to the original location.  For the
above metadata, the pipeline would be similar to:

```json
[
    {
        "type": "readers.las",
        "filename": "in.las"
    },
    {
        "type": "filters.transformation",
        "matrix": "1 0 0 -583394   0 1 0 -5.2831e+06   0 0 1 -498.152   0 0 0 1"
    },
    {
        "type": "filters.transformation",
        "matrix": "1  2.60209e-18 -1.97906e-09       -0.375  8.9407e-08            1  5.58794e-09      -0.5625 6.98492e -10 -5.58794e-09            1   0.00411987           0            0            0            1"
    },
    {
        "type": "filters.transformation",
        "matrix": "1 0 0 583394   0 1 0 5.2831e+06  0 0 1 498.152  0 0 0 1"
    },
    {
        "type": "writers.las",
        "filename": "out.las"
    }
]
```

```{note}
The `composed` metadata matrix is a composition of the three transformation steps outlined above, and can be used in a single call to `filters.transformation` as opposed to the three separate calls.
```

```{seealso}
{ref}`filters.transformation` to apply a transform to other points.
```

## Options

nr

: Radius to use for normal estimation. /[Default: **0.02**/]

fr

: Radius to use when computing features. /[Default: **0.04**/]

fpfh

: Use FPFH to find correspondences? /[Default: **true**/]

```{include} filter_opts.md
```
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('filters.teaser', **args)
 
class filters_trajectory(_GenericStage):
    """
(filters.trajectory)=

# filters.trajectory

The **trajectory filter** computes an estimate the the sensor location based
on the position of multiple returns and the sensor scan angle. It is primarily
useful for LAS input as it requires scan angle and return counts in order to
work.

The method is described in detail [here]. It extends the method of {cite}`Gatziolis2019`.

```{note}
This filter creates a new dataset describing the trajectory of the sensor,
replacing the input dataset.
```

## Examples

```json
[
    "input.las",
    {
        "type": "filters.trajectory"
    },
    "trajectory.las"
]
```

## Options

dtr

: Multi-return sampling interval in seconds. /[Default: .001/]

dst

: Single-return sampling interval in seconds. /[Default: .001/]

minsep

: Minimum separation of returns considered in meters. /[Default: .01/]

tblock

: Block size for cublic spline in seconds. /[Default: 1.0/]

tout

: Output data interval in seconds. /[Default: .01/]

```{include} filter_opts.md
```

[here]: ../papers/lidar-traj.pdf
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('filters.trajectory', **args)
 
class filters_transformation(_GenericStage):
    """
(filters.transformation)=

# filters.transformation

The transformation filter applies an arbitrary homography
transformation, represented as a 4x4 [matrix], to each xyz triplet.

```{note}
The transformation filter does not apply or consider any spatial
reference information.
```

```{eval-rst}
.. embed::
```

```{eval-rst}
.. streamable::
```

## Example

This example rotates the points around the z-axis while translating them.

```json
[
    "untransformed.las",
    {
        "type":"filters.transformation",
        "matrix":"0 -1  0  1  1  0  0  2  0  0  1  3  0  0  0  1"
    },
    {
        "type":"writers.las",
        "filename":"transformed.las"
    }
]
```


## Further details

A full tutorial about transformation matrices is beyond the scope of this
documentation. Instead, we will provide a few pointers to introduce core
concepts, especially as pertains to PDAL's handling of the `matrix` argument.

Transformations in a 3-dimensional coordinate system can be represented
as a homography transformation using homogeneous coordinates. This 4x4
matrix can represent affine transformations describing operations like
translation, rotation, and scaling of coordinates.  In addition it can
represent perspective transformations modeling a pinhole camera.

The transformation filter's `matrix` argument is a space delimited, 16
element string. This string is simply a row-major representation of the 4x4
matrix (i.e., first four elements correspond to the top row of the
transformation matrix and so on).

In the event that readers are accustomed to an alternate representation of the
transformation matrix, we provide some simple examples in the form of pure
translations, rotations, and scaling, and show the corresponding `matrix`
string.

### Translation

A pure translation by $t_x$, $t_y$, and $t_z$ in the X, Y,
and Z dimensions is represented by the following matrix.

$$
/begin{matrix}
    1 & 0 & 0 & t_x //
    0 & 1 & 0 & t_y //
    0 & 0 & 1 & t_z //
    0 & 0 & 0 & 1
/end{matrix}
$$

The JSON syntax required for such a translation is written as follows for $t_x=7$, $t_y=8$, and $t_z=9$.

```json
[
    {
        "type":"filters.transformation",
        "matrix":"1  0  0  7  0  1  0  8  0  0  1  9  0  0  0  1"
    }
]
```

### Scaling

Scaling of coordinates is also possible using a transformation matrix. The
matrix shown below will scale the X coordinates by $s_x$, the Y
coordinates by $s_y$, and Z by $s_z$.

$$
/begin{matrix}
    s_x &   0 &   0 & 0 //
      0 & s_y &   0 & 0 //
      0 &   0 & s_z & 0 //
      0 &   0 &   0 & 1
/end{matrix}
$$

We again provide an example JSON snippet to demonstrate the scaling
transformation. In the example, X and Y are not scaled at all (i.e.,
$s_x=s_y=1$) and Z is magnified by a factor of 2 ($s_z=2$).

```json
[
    {
        "type":"filters.transformation",
        "matrix":"1  0  0  0  0  1  0  0  0  0  2  0  0  0  0  1"
    }
]
```

### Rotation

A rotation of coordinates by $/theta$ radians counter-clockwise about
the z-axis is accomplished with the following matrix.

$$
/begin{matrix}
    /cos{/theta} & -/sin{/theta} & 0 & 0 //
    /sin{/theta} &  /cos{/theta} & 0 & 0 //
               0 &             0 & 1 & 0 //
               0 &             0 & 0 & 1
/end{matrix}
$$

In JSON, a rotation of 90 degrees ($/theta=1.57$ radians) takes the form
shown below.

```json
[
    {
        "type":"filters.transformation",
        "matrix":"0  -1  0  0  1  0  0  0  0  0  1  0  0  0  0  1"
    }
]
```

Similarly, a rotation about the x-axis by $/theta$ radians is represented
as

$$
/begin{matrix}
    1 &            0 &             0 & 0 //
    0 & /cos{/theta} & -/sin{/theta} & 0 //
    0 & /sin{/theta} &  /cos{/theta} & 0 //
    0 &            0 &             0 & 1
/end{matrix}
$$

which takes the following form in JSON for a rotation of 45 degrees ($/theta=0.785$ radians)

```json
[
    {
        "type":"filters.transformation",
        "matrix":"1  0  0  0  0  0.707  -0.707  0  0  0.707  0.707  0  0  0  0  1"
    }
]
```

Finally, a rotation by $/theta$ radians about the y-axis is accomplished
with the matrix

$$
/begin{matrix}
     /cos{/theta} & 0 & /sin{/theta} & 0 //
                0 & 1 &            0 & 0 //
    -/sin{/theta} & 0 & /cos{/theta} & 0 //
                0 & 0 &            0 & 1
/end{matrix}
$$

and the JSON string for a rotation of 10 degrees ($/theta=0.175$ radians) becomes

```json
[
    {
        "type":"filters.transformation",
        "matrix":"0.985  0  0.174  0  0  1  0  0  -0.174  0  0.985  0  0  0  0  1"
    }
]
```


## Options

invert

: If set to true, applies the inverse of the provided transformation matrix.
  /[Default: false/]

matrix

: A whitespace-delimited transformation matrix.
  The matrix is assumed to be presented in row-major order.
  Only matrices with sixteen elements are allowed.

```{include} filter_opts.md
```
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('filters.transformation', **args)
 
class filters_voxelcenternearestneighbor(_GenericStage):
    """
(filters.voxelcenternearestneighbor)=

# filters.voxelcenternearestneighbor

The **VoxelCenterNearestNeighbor filter** is a voxel-based sampling filter.
The input point
cloud is divided into 3D voxels at the given cell size. For each populated
voxel, the coordinates of the voxel center are used as the query point in a 3D
nearest neighbor search. The nearest neighbor is then added to the output point
cloud, along with any existing dimensions.

```{eval-rst}
.. embed::

```

## Example

```json
[
    "input.las",
    {
        "type":"filters.voxelcenternearestneighbor",
        "cell":10.0
    },
    "output.las"
]
```

```{seealso}
{ref}`filters.voxelcentroidnearestneighbor` offers a similar solution,
using as the query point the centroid of all points falling within the voxel as
opposed to the voxel center coordinates.  The drawback with this approach is that
all dimensional data is lost, leaving the the sampled cloud consisting of only
XYZ coordinates.
```

## Options

cell

: Cell size in the `X`, `Y`, and `Z` dimension. /[Default: 1.0/]

```{include} filter_opts.md
```
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('filters.voxelcenternearestneighbor', **args)
 
class filters_voxelcentroidnearestneighbor(_GenericStage):
    """
(filters.voxelcentroidnearestneighbor)=

# filters.voxelcentroidnearestneighbor

The **VoxelCentroidNearestNeighbor Filter** is a voxel-based sampling filter.
The input point cloud is divided into 3D voxels at the given cell size. For
each populated voxel, we apply the following ruleset. For voxels with only one
point, the point is passed through to the output. For voxels with exactly two
points, the point closest the voxel center is returned. Finally, for voxels
with more than two points, the centroid of the points within that voxel is
computed. This centroid is used as the query point in a 3D nearest neighbor
search (considering only those points lying within the voxel). The nearest
neighbor is then added to the output point cloud, along with any existing
dimensions.

```{eval-rst}
.. embed::
```

## Example

```json
[
    "input.las",
    {
        "type":"filters.voxelcentroidnearestneighbor",
        "cell":10.0
    },
    "output.las"
]
```

```{seealso}
{ref}`filters.voxelcenternearestneighbor` offers a similar solution, using
the voxel center as opposed to the voxel centroid for the query point.
```

## Options

cell

: Cell size in the `X`, `Y`, and `Z` dimension. /[Default: 1.0/]

```{include} filter_opts.md
```
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('filters.voxelcentroidnearestneighbor', **args)
 
class filters_voxeldownsize(_GenericStage):
    """
(filters.voxeldownsize)=

# filters.voxeldownsize

The **voxeldownsize filter** is a voxel-based sampling filter.
The input point cloud is divided into 3D voxels at the given cell size.
For each populated voxel, either first point entering in the voxel or
center of a voxel (depending on mode argument) is accepted and voxel is
marked as populated.  All other points entering in the same voxel are
filtered out.

## Example

```json
[
    "input.las",
    {
        "type":"filters.voxeldownsize",
        "cell":1.0,
        "mode":"center"
    },
    "output.las"
]
```

```{eval-rst}
.. streamable::
```

```{seealso}
{ref}`filters.voxelcenternearestneighbor` offers a similar solution,
using the coordinates of the voxel center as the query point in a 3D
nearest neighbor search.  The nearest neighbor is then added to the
output point cloud, along with any existing dimensions.
```

## Options

cell

: Cell size in the `X`, `Y`, and `Z` dimension. /[Default: 0.001/]

mode

: Mode for voxel based filtering. /[Default: center/]
  **center**: Coordinates of the first point found in each voxel will
  be modified to be the center of the voxel.
  **first**: Only the first point found in each voxel is retained.

```{include} filter_opts.md
```

```{warning}
If you choose **center** mode, you are overwriting the X, Y and Z
values of retained points.  This may invalidate other dimensions of
the point if they depend on this location or the location of other points
in the input.
```
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('filters.voxeldownsize', **args)
 
class filters_zsmooth(_GenericStage):
    """
(filters.zsmooth)=

# filters.zsmooth

The **Zsmooth Filter** computes a new Z value as another dimension that is based
on the Z values of neighboring points.

All points within some distance in the X-Y plane from a reference point are ordered by Z value.
The reference point's new smoothed Z value is chosen to be that of the Nth median value of
the neighboring points, where N is specified as the `` _`medianpercent` `` option.

Use {ref}`filters.assign` to assign the smoothed Z value to the actual Z dimension if
desired.

## Example

Compute the smoothed Z value as the median Z value of the neighbors within 2 units and
assign the value back to the Z dimension.

% code_block::json
%
% [
%     "input.las",
%     {
%         "type": "filters.zsmooth",
%         "radius": 2,
%         "dim": "Zadj"
%     },
%     {
%         "type": "filters.assign",
%         "value": "Z = Zadj"
%     },
%     "output.las"
% ]

## Options

radius

: All points within `radius` units from the reference point in the X-Y plane are considered
  to determine the smoothed Z value. /[Default: 1/]

medianpercent

: A value between 0 and 100 that specifies the relative position of ordered Z values of neighbors
  to use as the new smoothed Z value. 0 specifies the minimum value. 100 specifies the
  maximum value. 50 specifies the mathematical median of the values. /[Default: 50/]

dim

: The name of a dimension to use for the adjusted Z value. Cannot be 'Z'. /[Required/]

```{include} filter_opts.md
```
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('filters.zsmooth', **args)
 
class filter_opts(_GenericStage):
    """
where

: An {ref}`expression <pdal_expression>` that limits points passed to a filter.
  Points that don't pass the
  expression skip the stage but are available to subsequent stages in a pipeline.
  /[Default: no filtering/]

where_merge

: A strategy for merging points skipped by a `where` option when running in standard mode.
  If `true`, the skipped points are added to the first point view returned by the skipped
  filter or if no views are returned, placed in their own view. If `false`, skipped points are
  placed in their own point view. If `auto`,
  skipped points are merged into the returned point view provided that only one point view
  is returned and it has the same point count as it did when the filter was run, otherwise
  the skipped points are placed in their own view.

  /[Default: `auto`/]
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('filter_opts', **args)
 
class ogr_json(_GenericStage):
    """

```json
{
    "type":"ogr",
    "datasource": "File path to OGR-readable geometry",
    "drivers": ["OGR driver to use", "and OGR KEY=VALUE driver options"],
    "openoptions": ["Options to pass to the OGR open function [optional]"],
    "layer": "OGR layer from which to fetch polygons [optional]",
    "sql": "SQL query to use to filter the polygons in the layer [optional]",
    "options":
    {
        "geometry": "WKT or GeoJSON geomtry used to filter query [optional]",
        "dialect": "SQL dialect to use (default: OGR SQL) [optional]"
    }
}
```
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('ogr_json', **args)
 
class readers_arrow(_GenericStage):
    """
(readers.arrow)=

# readers.arrow

```{eval-rst}
.. plugin::
```

```{eval-rst}
.. streamable::
```

The Arrow reader supports reading Arrow and Parquet -formatted data as written by
{ref}`writers.arrow`, although it should support point clouds written by other
writers too if they follow either the [GeoArrow](https://github.com/geoarrow/geoarrow/)
or [GeoParquet](https://github.com/opengeospatial/geoparquet/) specification.

Caveats:

- Which schema is read is chosen by the file name extension, but can be
  overridden with the `format` option set to `geoarrow` or `geoparquet`

## Options

filename

: Arrow GeoArrow or GeoParquet file to read /[Required/]

format

: `geoarrow` or `geoparquet` option to override any filename extension
  hinting of data type /[Optional/]

```{include} reader_opts.md
```
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('readers.arrow', **args)
 
class readers_bpf(_GenericStage):
    """
(readers.bpf)=

# readers.bpf

BPF is an NGA [specification](https://nsgreg.nga.mil/doc/view?i=4220&month=8&day=30&year=2016) for point cloud data.  The BPF reader supports
reading from BPF files that are encoded as version 1, 2 or 3.

This BPF reader only supports Zlib compression.  It does NOT support the
deprecated compression types QuickLZ and FastLZ.  The reader will consume files
containing ULEM frame data and polarimetric data, although these data are not
made accessible to PDAL; they are essentially ignored.

Data that follows the standard header but precedes point data is taken to
be metadata and is UTF-encoded and added to the reader's metadata.

```{eval-rst}
.. embed::
```

```{eval-rst}
.. streamable::
```

## Example

```json
[
    "inputfile.bpf",
    {
      "type":"writers.text",
      "filename":"outputfile.txt"
    }
]
```

## Options

filename

: BPF file to read /[Required/]

fix_dims

: BPF files may contain dimension names that aren't allowed by PDAL. When this
  option is 'true', invalid characters in dimension names are replaced by '/_' in
  order to make the names valid.
  /[Default: true/]

```{include} reader_opts.md
```
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('readers.bpf', **args)
 
class readers_buffer(_GenericStage):
    """
(readers.buffer)=

# readers.buffer

The {ref}`readers.buffer` stage is a special stage that allows
you to read data from your own PointView rather than
fetching the data from a specific reader. In the {ref}`writing` example,
it is used to take a simple listing of points and turn them into an
LAS file.

```{eval-rst}
.. embed::
```

## Example

See {ref}`writing` for an example usage scenario for {ref}`readers.buffer`.

## Options

```{include} reader_opts.md
```
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('readers.buffer', **args)
 
class readers_copc(_GenericStage):
    """
(readers.copc)=

# readers.copc

The **COPC Reader** supports reading from [COPC format] files. A COPC file is
a [LASzip] (compressed LAS) file that organizes its data spatially, allowing for
incremental loading and spatial filtering.

```{note}
LAS stores X, Y and Z dimensions as scaled integers.  Users converting an
input LAS file to an output LAS file will frequently want to use the same
scale factors and offsets in the output file as existed in the input
file in order to
maintain the precision of the data.  Use the `forward` option of
{ref}`writers.las` to facilitate transfer of header information from
source COPC files to destination LAS/LAZ files.
```

```{note}
COPC files can contain datatypes that are actually arrays rather than
individual dimensions.  Since PDAL doesn't support these datatypes, it
must map them into datatypes it supports.  This is done by appending the
array index to the name of the datatype.  For example, datatypes 11 - 20
are two dimensional array types and if a field had the name Foo for
datatype 11, PDAL would create the dimensions Foo0 and Foo1 to hold the
values associated with LAS field Foo.  Similarly, datatypes 21 - 30 are
three dimensional arrays and a field of type 21 with the name Bar would
cause PDAL to create dimensions Bar0, Bar1 and Bar2.  See the information
on the extra bytes VLR in the [LAS Specification] for more information
on the extra bytes VLR and array datatypes.
```

```{warning}
COPC files that use the extra bytes VLR and datatype 0 will be accepted,
but the data associated with a dimension of datatype 0 will be ignored
(no PDAL dimension will be created).
```

```{eval-rst}
.. embed::
```

```{eval-rst}
.. streamable::

```

## Example

```json
[
    {
        "type":"readers.copc",
        "filename":"inputfile.copc.laz"
    },
    {
        "type":"writers.text",
        "filename":"outputfile.txt"
    }
]
```

## Options

filename

: COPC file to read. Remote file specifications (http, AWS, Google, Azure, Dropbox) are supported.
  /[Required/]

```{include} reader_opts.md
```

bounds

: The extent of the data to select in 2 or 3 dimensions, expressed as a string,
  e.g.: `([xmin, xmax], [ymin, ymax], [zmin, zmax])`.  If omitted, the entire dataset
  will be selected. The bounds specification can be followed by a slash ('/') and a
  spatial reference specification to apply to the bounds specification.

polygon

: A clipping polygon, expressed in a well-known text string,
  e.g.: `POLYGON((0 0, 5000 10000, 10000 0, 0 0))`.  This option can be
  specified more than once. Multiple polygons will will be treated
  as a single multipolygon. The polygon specification can be followed by a slash ('/') and a
  spatial reference specification to apply to the polygon.

ogr

: A JSON object representing an OGR query to fetch polygons to use for filtering. The polygons
  fetched from the query are treated exactly like those specified in the `polygon` option.
  The JSON object is specified as follows:

```{include} ogr_json.md
```

requests

: The number of worker threads processing data. The optimal number depends on your system
  and your network connection, but more is not necessarily better.  A reasonably fast
  network connection can often fetch data faster than it can be processed, leading to
  memory consumption and slower performance. /[Default: 15/]

resolution

: Limit the pyramid levels of data to fetch based on the expected resolution of the data.
  Units match that of the data. /[Default: no resolution limit/]

header

: HTTP headers to forward for remote endpoints. Specify as a JSON
  object of key/value string pairs.

query

: HTTP query parameters to forward for remote endpoints. Specify as a JSON
  object of key/value string pairs.

vlr

: Read LAS VLRs and import as metadata. /[Default: false/]

keep_alive

: The number of chunks to keep active in memory while reading /[Default: 10/]

fix_dims

: Make invalid dimension names valid by converting disallowed characters to '/_'. Only
  applies to names specified in an extra-bytes VLR. /[Default: true/]

srs_vlr_order

: Preference order to read SRS VLRs (list of 'wkt1', 'wkt2', or 'projjson').
  /[Default: 'wkt1, wkt2, projjson'/]

nosrs

: Don't read the SRS VLRs. The data will not be assigned an SRS. This option is
  for use only in special cases where processing the SRS could cause performance
  issues. /[Default: false/]

[copc format]: https://copc.io/
[las specification]: https://www.asprs.org/wp-content/uploads/2019/03/LAS_1_4_r14.pdf
[laszip]: http://laszip.org
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('readers.copc', **args)
 
class readers_draco(_GenericStage):
    """
(readers.draco)=

# readers.draco

[Draco] is a library for compressing and decompressing 3D geometric meshes and
point clouds and was designed and built for compression efficiency and speed.
The code supports compressing points, connectivity information, texture coordinates,
color information, normals, and any other generic attributes associated with geometry.

## Example

```json
[
    {
        "type": "readers.draco",
        "filename": "color.las"
    }
]
```

## Options

filename

: Input file name. /[Required/]

```{include} reader_opts.md
```

[draco]: https://github.com/google/draco
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('readers.draco', **args)
 
class readers_e57(_GenericStage):
    """
(readers.e57)=

# readers.e57

The **E57 Reader** supports reading from E57 files.

The reader supports E57 files with Cartesian point clouds.

```{note}
E57 files can contain multiple point clouds stored in a single
file.  If that is the case, the reader will read all the points
from all of the internal point clouds as one.

Only dimensions present in all of the point clouds will be read.
```

```{note}
Point clouds stored in spherical format are not supported.
```

```{note}
The E57 `cartesianInvalidState` dimension is mapped to the Omit
PDAL dimension.  A range filter can be used to filter out the
invalid points.
```

```{eval-rst}
.. plugin::
```

```{eval-rst}
.. streamable::

```

## Example 1

```json
[
    {
        "type":"readers.e57",
        "filename":"inputfile.e57"
    },
    {
        "type":"writers.text",
        "filename":"outputfile.txt"
    }
]
```

## Example 2

```json
[
    {
        "type":"readers.e57",
        "filename":"inputfile.e57"
    },
    {
        "type":"filters.range",
        "limits":"Omit[0:0]"
    },
    {
        "type":"writers.text",
        "filename":"outputfile.txt"
    }
]
```

## Options

`` _`filename` ``

: E57 file to read /[Required/]

```{include} reader_opts.md
```
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('readers.e57', **args)
 
class readers_ept(_GenericStage):
    """
(readers.ept)=

# readers.ept

[Entwine Point Tile] (EPT) is a hierarchical octree-based point cloud format
suitable for real-time rendering and lossless archival.  [Entwine] is a
producer of this format.  The EPT Reader supports reading data from the
EPT format, including spatially accelerated queries and file reconstruction
queries.

Sample EPT datasets of hundreds of billions of points in size may be viewed
with [Potree].

```{eval-rst}
.. embed::
```

```{eval-rst}
.. streamable::
```

## Example

This example downloads a small area around the the Statue of Liberty from the New York City data set (4.7 billion points) which can be viewed in its entirety in [Potree].

```json
[
   {
      "type": "readers.ept",
      "filename": "http://na.entwine.io/nyc/ept.json",
      "bounds": "([-8242669, -8242529], [4966549, 4966674])"
   },
   "statue-of-liberty.las"
]
```

Additional attributes created by the
{ref}`EPT addon writer <writers.ept_addon>` can be referenced with the `addon` option.  Here is an example that overrides the `Classification` dimension with an addon dimension derived from the original dataset:

```json
[
    {
        "type": "readers.ept",
        "filename": "http://na.entwine.io/autzen/ept.json",
        "addons": { "Classification": "~/entwine/addons/autzen/smrf" }
    },
    {
        "type": "writers.las",
        "filename": "autzen-ept-smrf.las"
    }
]
```

For more details about addon dimensions and how to produce them, see {ref}`writers.ept_addon`.

```{note}
The `forward` option of {ref}`writers.copc` or {ref}`writers.las` cannot work
with EPT due to how EPT can mix content and files. There is no single unified metadata
value to forward. You will have to explicitly set any output options that you
would expect to come from EPT on any writers.
```

## Options

filename

: Path to the EPT resource from which to read, ending with `ept.json`.
  For example, `/Users/connor/entwine/autzen/ept.json` or
  `http://na.entwine.io/autzen/ept.json`. /[Required/]

spatialreference

: Spatial reference to apply to the data.  Overrides any SRS in the input
  itself.  Can be specified as a WKT, proj.4 or EPSG string. /[Default: none/]

bounds

: The extents of the resource to select in 2 or 3 dimensions, expressed as a string,
  e.g.: `([xmin, xmax], [ymin, ymax], [zmin, zmax])`.  If omitted, the entire dataset
  will be selected. The bounds can be followed by a slash ('/') and a spatial reference
  specification to apply to the bounds.

resolution

: A point resolution limit to select, expressed as a grid cell edge length.  Units
  correspond to resource coordinate system units.  For example, for a coordinate system
  expressed in meters, a `resolution` value of `0.1` will select points up to a
  ground resolution of 100 points per square meter.

  The resulting resolution may not be exactly this value: the minimum possible resolution
  that is at *least* as precise as the requested resolution will be selected.  Therefore
  the result may be a bit more precise than requested.

addons

: A mapping of assignments of the form `DimensionName: AddonPath`, which
  assigns dimensions from the specified paths to the named dimensions.
  These addon dimensions are created by the
  {ref}`EPT addon writer <writers.ept_addon>`.  If the dimension names
  already exist in the EPT [Schema] for the given resource, then their
  values will be overwritten with those from the appropriate addon.

  Addons may used to override well-known {ref}`dimension <dimensions>`.  For example,
  an addon assignment of `"Classification": "~/addons/autzen/MyGroundDimension/"`
  will override an existing EPT `Classification` dimension with the custom dimension.

origin

: EPT datasets are lossless aggregations of potentially multiple source
  files.  The *origin* option can be used to select all points from a
  single source file.  This option may be specified as a string or an
  integral ID.

  The string form of this option selects a source file by its original
  file path.  This may be a substring instead of the entire path, but
  the string must uniquely select only one source file (via substring
  search).  For example, for an EPT dataset created from source files
  *one.las*, *two.las*, and *two.bpf*, "one" is a sufficient selector,
  but "two" is not.

  The integral form of this option selects a source file by its `OriginId`
  dimension, which can be determined from  the file's position in EPT
  metadata file `entwine-files.json`.

```{note}
When using `pdal info --summary`, using the `origin` option will cause the
resulting bounds to be clipped to those of the selected origin, and the resulting
number of points to be an upper bound for this selection.
```

polygon

: The clipping polygon, expressed in a well-known text string,
  e.g.: `POLYGON((0 0, 5000 10000, 10000 0, 0 0))`.  This option can be
  specified more than once by placing values in an array, in which case all of
  them will be unioned together, acting as a single multipolygon. The polygon definition
  can be followed by a slash ('/') and a spatial reference specification to apply to
  the polygon.

```{note}
When using `pdal info --summary`, using the `polygon` option will cause the
resulting bounds to be clipped to the maximal extents of all provided polygons,
and the resulting number of points to be an upper bound for this polygon selection.
```

```{note}
When both the `bounds` and `polygon` options are specified, only
the points that fall within *both* the bounds and the polygon(s) will be
returned.
```

ogr

: A JSON object representing an OGR query to fetch polygons to use for filtering. The polygons
  fetched from the query are treated exactly like those specified in the `polygon` option.
  The JSON object is specified as follows:

```{include} ogr_json.md
```

requests

: Maximum number of simultaneous requests for EPT data. /[Minimum: 4/] /[Default: 15/]

header

: HTTP headers to forward for remote EPT endpoints, specified as a JSON
  object of key/value string pairs.

query

: HTTP query parameters to forward for remote EPT endpoints, specified as a
  JSON object of key/value string pairs.

ignore_unreadable

: If set to true, ignore errors for missing or unreadable point data nodes.

[entwine]: https://entwine.io/
[entwine point tile]: https://entwine.io/entwine-point-tile.html
[potree]: http://potree.entwine.io/data/nyc.html
[schema]: https://entwine.io/entwine-point-tile.html#schema
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('readers.ept', **args)
 
class readers_faux(_GenericStage):
    """
(readers.faux)=

# readers.faux

The faux reader is used for testing pipelines. It does not read from a
file or database, but generates synthetic data to feed into the pipeline.

The faux reader requires a mode argument to define the method in which points
should be generated.  Valid modes are as follows:

constant

: The values provided as the minimums to the bounds argument are
  used for the X, Y and Z value, respectively, for every point.

random

: Random values are chosen within the provided bounds.

ramp

: Value increase uniformly from the minimum values to the maximum values.

uniform

: Random values of each dimension are uniformly distributed in the
  provided ranges.

normal

: Random values of each dimension are normally distributed in the
  provided ranges.

grid

: Creates points with integer-valued coordinates in the range provided
  (excluding the upper bound).

```{eval-rst}
.. embed::
```

```{eval-rst}
.. streamable::
```

## Example

```json
[
    {
        "type":"readers.faux",
        "bounds":"([0,1000000],[0,1000000],[0,100])",
        "count":"10000",
        "mode":"random"
    },
    {
        "type":"writers.text",
        "filename":"outputfile.txt"
    }
]
```

## Options

bounds

: The spatial extent within which points should be generated.
  Specified as a string in the form "(/[xmin,xmax/],/[ymin,ymax/],/[zmin,zmax/])".
  /[Default: unit cube/]

count

: The number of points to generate. /[Required, except when mode is 'grid'/]

override_srs

: Spatial reference to apply to data. /[Optional/]

mean_x|y|z

: Mean value in the x, y, or z dimension respectively. (Normal mode only)
  /[Default: 0/]

stdev_x|y|z

: Standard deviation in the x, y, or z dimension respectively. (Normal mode
  only) /[Default: 1/]

mode

: "constant", "random", "ramp", "uniform", "normal" or "grid" /[Required/]
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('readers.faux', **args)
 
class readers_fbi(_GenericStage):
    """
(readers.fbi)=

# readers.fbi

The **FBI Reader** supports reading from `FastBinary format` files. FastBinary
is the internal format for TerraScan. This driver allows to read FBI files in
version 1 of the FBI specification.

```{note}
Support for all point attributes in LAS 1.2 format so data can be converted between LAS 1.2
and Fast Binary formats without any loss of point attribute information.
```

```{eval-rst}
.. embed::
```

```{eval-rst}
.. streamable::

```

## Example

```json
[
    {
        "type":"readers.fbi",
        "filename":"inputfile.fbi"
    },
    {
        "type":"writers.text",
        "filename":"outputfile.txt"
    }
]
```

## Options

filename

: FBI file to read /[Required/]
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('readers.fbi', **args)
 
class readers_gdal(_GenericStage):
    """
(readers.gdal)=

# readers.gdal

The [GDAL] reader reads [GDAL readable raster] data sources as point clouds.

Each pixel is given an X and Y coordinate (and corresponding PDAL dimensions)
that are center pixel, and each band is represented by "band-1", "band-2", or
"band-n".  Using the 'header' option allows naming the band data to standard
PDAL dimensions.

```{eval-rst}
.. embed::
```

## Basic Example

Simply writing every pixel of a JPEG to a text file is not very useful.

```json
[
    {
        "type":"readers.gdal",
        "filename":"./pdal/test/data/autzen/autzen.jpg"
    },
    {
        "type":"writers.text",
        "filename":"outputfile.txt"
    }
]
```

## LAS Example

The following example assigns the bands from a JPG to the
RGB values of an [ASPRS LAS] file using {ref}`writers.las`.

```json
[
    {
        "type":"readers.gdal",
        "filename":"./pdal/test/data/autzen/autzen.jpg",
        "header": "Red, Green, Blue"
    },
    {
        "type":"writers.las",
        "filename":"outputfile.las"
    }
]
```

```{note}
{ref}`readers.gdal` is quite sensitive to GDAL's cache settings. See the
`GDAL_CACHEMAX` value at <https://gdal.org/user/configoptions.html> for
more information.
```

## Options

filename

: [GDALOpen] 'able raster file to read /[Required/]

```{include} reader_opts.md
```

header

: A comma-separated list of {ref}`dimension <dimensions>` IDs to map
  bands to. The length of the list must match the number
  of bands in the raster.

memorycopy

: Use the [GDAL MEM driver](https://gdal.org/drivers/raster/mem.html)
  to copy the entire raster into memory before converting to points. This
  is useful if the raster driver has a lot of per-block overhead or you
  are willing to trade memory for performance.

gdalopts

: A list of key/value options to pass directly to the GDAL driver.  The
  format is name=value,name=value,...  The option may be specified
  any number of times.

[asprs las]: http://www.asprs.org/Committee-General/LASer-LAS-File-Format-Exchange-Activities.html
[gdal]: http://gdal.org
[gdal readable raster]: http://www.gdal.org/formats_list.html
[gdalopen]: https://gdal.org/en/latest/api/raster_c_api.html#gdal_8h_1a9cb8585d0b3c16726b08e25bcc94274a
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('readers.gdal', **args)
 
class readers_hdf(_GenericStage):
    """
(readers.hdf)=

# readers.hdf

The **HDF reader** reads data from files in the
[HDF5 format.](https://www.hdfgroup.org/solutions/hdf5/)
You must explicitly specify a mapping of HDF datasets to PDAL
dimensions using the dimensions parameter. ALL dimensions must
be scalars and be of the same length. Compound types are not
supported at this time.

```{eval-rst}
.. plugin::
```

```{eval-rst}
.. streamable::
```

## Example

This example reads from the Autzen HDF example with all dimension
properly mapped and then outputs a LAS file.

```json
[
    {
        "type": "readers.hdf",
        "filename": "test/data/hdf/autzen.h5",
        "dimensions":
        {
            "X" : "autzen/X",
            "Y" : "autzen/Y",
            "Z" : "autzen/Z",
            "Red" : "autzen/Red",
            "Blue" : "autzen/Blue",
            "Green" : "autzen/Green",
            "Classification" : "autzen/Classification",
            "EdgeOfFlightLine" : "autzen/EdgeOfFlightLine",
            "GpsTime" : "autzen/GpsTime",
            "Intensity" : "autzen/Intensity",
            "NumberOfReturns" : "autzen/NumberOfReturns",
            "PointSourceId" : "autzen/PointSourceId",
            "ReturnNumber" : "autzen/ReturnNumber",
            "ScanAngleRank" : "autzen/ScanAngleRank",
            "ScanDirectionFlag" : "autzen/ScanDirectionFlag",
            "UserData" : "autzen/UserData"
        }
    },
    {
        "type" : "writers.las",
        "filename": "output.las",
        "scale_x": 1.0e-5,
        "scale_y": 1.0e-5,
        "scale_z": 1.0e-5,
        "offset_x": "auto",
        "offset_y": "auto",
        "offset_z": "auto"
    }
]
```

```{note}
All dimensions must be simple numeric HDF datasets with
equal lengths. Compound types, enum types, string types,
etc. are not supported.
```

```{warning}
The HDF reader does not set an SRS.
```

## Common Use Cases

A possible use case for this driver is reading NASA's [ICESat-2](https://icesat-2.gsfc.nasa.gov/) data.
This example reads the X, Y, and Z coordinates from the ICESat-2
[ATL03](https://icesat-2.gsfc.nasa.gov/sites/default/files/page_files/ICESat2_ATL03_ATBD_r002.pdf) format and converts them into a LAS file.

```{note}
ICESat-2 data use [EPSG:7912](https://epsg.io/7912). ICESat-2 Data products documentation can be found [here](https://icesat-2.gsfc.nasa.gov/science/data-products)
```

```json
[
    {
        "type": "readers.hdf",
        "filename": "ATL03_20190906201911_10800413_002_01.h5",
        "dimensions":
        {
            "X" : "gt1l/heights/lon_ph",
            "Y" : "gt1l/heights/lat_ph",
            "Z" : "gt1l/heights/h_ph"
        }
    },
    {
        "type" : "writers.las",
        "filename": "output.las"
    }
]
```

## Options

```{include} reader_opts.md
```

dimensions

: A JSON map with PDAL dimension names as the keys and HDF dataset paths as the values.
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('readers.hdf', **args)
 
class readers_i3s(_GenericStage):
    """
(readers.i3s)=

# readers.i3s

[Indexed 3d Scene Layer (I3S)] is a specification created by Esri as a format for their
3D Scene Layer and scene services. The I3S reader handles RESTful webservices in an I3S
file structure/format.

```{eval-rst}
.. embed::
```

```{eval-rst}
.. streamable::

```

## Example

This example will download the Autzen dataset from the ArcGIS scene server and output it to a las file. This is done through PDAL's command line interface or through the pipeline.

```json
[
    {
        "type": "readers.i3s",
        "filename": "https://tiles.arcgis.com/tiles/8cv2FuXuWSfF0nbL/arcgis/rest/services/AUTZEN_LiDAR/SceneServer",
        "obb": {
            "center": [
                636590,
                849216,
                460
            ],
            "halfSize": [
                590,
                281,
                60
            ],
            "quaternion":
            [
                0,
                0,
                0,
                1
            ]
        }
    }
]
```

```
pdal translate i3s://https://tiles.arcgis.com/tiles/8cv2FuXuWSfF0nbL/arcgis/rest/services/AUTZEN_LiDAR/SceneServer /
    autzen.las /
    --readers.i3s.threads=64
```

## Options

```{include} reader_opts.md
```

filename

: I3S file stored remotely. These must be prefaced with an "i3s://".

  Example remote file: `pdal translate i3s://https://tiles.arcgis.com/tiles/arcgis/rest/services/AUTZEN_LiDAR/SceneServer autzen.las`

threads

: This specifies the number of threads that you would like to use while
  reading. The default number of threads to be used is 8. This affects
  the speed at which files are fetched and added to the PDAL view.

  Example: `--readers.i3s.threads=64`

obb

: An oriented bounding box used to filter the data being retrieved.  The obb
  is specified as JSON exactly as described by the [I3S specification].

dimensions

: Comma-separated list of dimensions that should be read.  Specify the
  Esri name, rather than the PDAL dimension name.

  > | Esri         | PDAL            |
  > | ------------ | --------------- |
  > | INTENSITY    | Intensity       |
  > | CLASS_CODE   | ClassFlags      |
  > | FLAGS        | Flag            |
  > | RETURNS      | NumberOfReturns |
  > | USER_DATA    | UserData        |
  > | POINT_SRC_ID | PointSourceId   |
  > | GPS_TIME     | GpsTime         |
  > | SCAN_ANGLE   | ScanAngleRank   |
  > | RGB          | Red             |

  Example: `--readers.i3s.dimensions="returns, rgb"`

min_density and max_density

: This is the range of density of the points in the nodes that will be selected during the read. The density of a node is calculated by the vertex count divided by the effective area of the node. Nodes do not have a uniform density across depths in the tree, so some sections may be more or less dense than others. The default values for these parameters will pull all the leaf nodes (the highest resolution).

  Example: `--readers.i3s.min_density=2 --readers.i3s.max_density=2.5`

[i3s specification]: https://github.com/Esri/i3s-spec/blob/master/docs/2.0/obb.cmn.md
[indexed 3d scene layer (i3s)]: https://github.com/Esri/i3s-spec/blob/master/format/Indexed%203d%20Scene%20Layer%20Format%20Specification.md
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('readers.i3s', **args)
 
class readers_ilvis2(_GenericStage):
    """
(readers.ilvis2)=

# readers.ilvis2

The **ILVIS2 reader** read from files in the ILVIS2 format. See the
[product spec](https://nsidc.org/data/ilvis2) for more information.

```{figure} readers.ilvis2.metadata.png
Dimensions provided by the ILVIS2 reader
```

```{eval-rst}
.. embed::
```

```{eval-rst}
.. streamable::
```

## Example

```json
[
    {
        "type":"readers.ilvis2",
        "filename":"ILVIS2_GL2009_0414_R1401_042504.TXT",
        "metadata":"ILVIS2_GL2009_0414_R1401_042504.xml"
    },
    {
        "type":"writers.las",
        "filename":"outputfile.las"
    }
]
```

## Options

filename

: File to read from /[Required/]

```{include} reader_opts.md
```

mapping

: Which ILVIS2 field type to map to X, Y, Z dimensions
  'LOW', 'CENTROID', or 'HIGH' /[Default: 'CENTROID'/]

metadata

: XML metadata file to coincidentally read /[Optional/]
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('readers.ilvis2', **args)
 
class readers_las(_GenericStage):
    """
(readers.las)=

# readers.las

The **LAS Reader** supports reading from [LAS format] files, the standard
interchange format for LIDAR data.  The reader does NOT support point formats
containing waveform data (4, 5, 9 and 10).

The reader also supports compressed LAS files, known as LAZ files or
[LASzip] files.

```{note}
LAS stores X, Y and Z dimensions as scaled integers.  Users converting an
input LAS file to an output LAS file will frequently want to use the same
scale factors and offsets in the output file as existed in the input
file in order to
maintain the precision of the data.  Use the `forward` option on the
{ref}`writers.las` to facilitate transfer of header information from
source to destination LAS/LAZ files.
```

```{note}
LAS 1.4 files can contain datatypes that are actually arrays rather than
individual dimensions.  Since PDAL doesn't support these datatypes, it
must map them into datatypes it supports.  This is done by appending the
array index to the name of the datatype.  For example, datatypes 11 - 20
are two dimensional array types and if a field had the name Foo for
datatype 11, PDAL would create the dimensions Foo0 and Foo1 to hold the
values associated with LAS field Foo.  Similarly, datatypes 21 - 30 are
three dimensional arrays and a field of type 21 with the name Bar would
cause PDAL to create dimensions Bar0, Bar1 and Bar2.  See the information
on the extra bytes VLR in the [LAS Specification] for more information
on the extra bytes VLR and array datatypes.
```

```{warning}
LAS 1.4 files that use the extra bytes VLR and datatype 0 will be accepted,
but the data associated with a dimension of datatype 0 will be ignored
(no PDAL dimension will be created).
```

```{eval-rst}
.. embed::
```

```{eval-rst}
.. streamable::

```

## Example

```json
[
    {
        "type":"readers.las",
        "filename":"inputfile.las"
    },
    {
        "type":"writers.text",
        "filename":"outputfile.txt"
    }
]
```

## Options

`` _`filename` ``

: LAS file to read /[Required/]

```{include} reader_opts.md
```

`` _`start` ``

: Point at which reading should start (0-indexed). Useful in combination
  with 'count' option to read a subset of points. /[Default: 0/]

`` _`extra_dims` ``

: Extra dimensions to be read as part of each point beyond those specified by
  the LAS point format.  The format of the option is
  `<dimension_name>=<type>[, ...]`.  Any valid PDAL {ref}`type <types>` can be
  specified.

  ```{note}
  The presence of an extra bytes VLR when reading a version
  1.4 file or a version 1.0 - 1.3 file with **use_eb_vlr** set
  causes this option to be ignored.
  ```

`` _`use_eb_vlr` ``

: If an extra bytes VLR is found in a version 1.0 - 1.3 file, use it as if it
  were in a 1.4 file. This option has no effect when reading a version 1.4 file.
  /[Default: false/]

compression

: /[Deprecated/]

ignore_vlr

: A comma-separated list of "userid/record_id" pairs specifying VLR records that should
  not be loaded.

fix_dims

: Make invalid dimension names valid by converting disallowed characters to '/_'. Only
  applies to names specified in an extra-bytes VLR. /[Default: true/]

nosrs

: Don't read the SRS VLRs. The data will not be assigned an SRS. This option is
  for use only in special cases where processing the SRS could cause performance
  issues. /[Default: false/]

threads

: Thread pool size. Number of threads used to decode laz chunk tables (Default: 7)

[las format]: http://asprs.org/Committee-General/LASer-LAS-File-Format-Exchange-Activities.html
[las specification]: http://www.asprs.org/a/society/committees/standards/LAS_1_4_r13.pdf
[laszip]: http://laszip.org
[lazperf]: https://github.com/verma/laz-perf
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('readers.las', **args)
 
class readers_matlab(_GenericStage):
    """
(readers.matlab)=

# readers.matlab

The **Matlab Reader** supports readers Matlab `.mat` files. Data
must be in a [Matlab struct], with field names that correspond to
{ref}`dimension <dimensions>` names. No ability to provide a name map is yet
provided.

Additionally, each array in the struct should ideally have the
same number of points. The reader takes its number of points
from the first array in the struct. If the array has fewer
elements than the first array in the struct, the point's field
beyond that number is set to zero.

```{note}
The Matlab reader requires the Mat-File API from MathWorks, and it must be
explicitly enabled at compile time with the `BUILD_PLUGIN_MATLAB=ON`
variable
```

```{eval-rst}
.. plugin::
```

```{eval-rst}
.. streamable::
```

## Example

```json
[
    {
        "type":"readers.matlab",
        "struct":"PDAL",
        "filename":"autzen.mat"
    },
    {
        "type":"writers.las",
        "filename":"output.las"
    }
]
```

## Options

filename

: Input file name. /[Required/]

```{include} reader_opts.md
```

struct

: Array structure name to read. /[Default: 'PDAL'/]

[matlab struct]: https://www.mathworks.com/help/matlab/ref/struct.html
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('readers.matlab', **args)
 
class readers_mbio(_GenericStage):
    """
(readers.mbio)=

# readers.mbio

The mbio reader allows sonar bathymetry data to be read into PDAL and
treated as data collected using LIDAR sources.  PDAL uses the [MB-System]
library to read the data and therefore supports [all formats] supported by
that library.  Some common sonar systems are NOT supported by MB-System,
notably Kongsberg, Reson and Norbit.  The mbio reader reads each "beam"
of data after averaging and processing by the MB-System software and stores
the values for the dimensions 'X', 'Y', 'Z' and 'Amplitude'.  X and Y use
longitude and latitude for units and the Z values are in meters (negative,
being below the surface).  Units for 'Amplitude' is not specified and may
vary.

```{eval-rst}
.. plugin::
```

```{eval-rst}
.. streamable::

```

## Example

This reads beams from a sonar data file and writes points to a LAS file.

```json
[
    {
        "type" : "readers.mbio",
        "filename" : "shipdata.m57",
        "format" : "MBF_EM3000RAW"
    },
    {
        "type":"writers.las",
        "filename":"outputfile.las"
    }
]
```

## Options

filename

: Filename to read from /[Required/]

```{include} reader_opts.md
```

format

: Name of number of format of file being read.  See MB-System documentation
  for a list of [all formats]. /[Required/]

datatype

: Type of data to read.  Either 'multibeam' or 'sidescan'.
  /[Default: 'multibeam'/]

timegap

: The maximum number of seconds that can elapse between pings before the
  end of the data stream is assumed. /[Default: 1.0/]

speedmin

: The minimum speed that the ship can be moving to before the end of the
  data stream is assumed. /[Default: 0/]

[all formats]: http://www3.mbari.org/products/mbsystem/html/mbsystem_formats.html
[mb-system]: https://www.mbari.org/products/research-software/mb-system/
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('readers.mbio', **args)
 
class readers(_GenericStage):
    """
(readers)=

# Readers

Readers provide {ref}`dimensions` to {ref}`pipeline`. PDAL attempts to
normalize common dimension types, like X, Y, Z, or Intensity, which are often
found in LiDAR point clouds. Not all dimension types need to be fixed, however.
Database drivers typically return unstructured lists of dimensions.  A reader
might provide a simple file type, like {ref}`readers.text`, a complex database
like {ref}`readers.pgpointcloud`, or a network service like {ref}`readers.ept`.

<!-- ```{toctree}
:glob: true
:hidden: true
:maxdepth: 1

readers.arrow
readers.bpf
readers.buffer
readers.copc
readers.draco
readers.ept
readers.e57
readers.faux
readers.fbi
readers.gdal
readers.hdf
readers.i3s
readers.ilvis2
readers.las
readers.matlab
readers.memoryview
readers.mbio
readers.nitf
readers.numpy
readers.obj
readers.optech
readers.pcd
readers.pgpointcloud
readers.ply
readers.pts
readers.ptx
readers.qfit
readers.rdb
readers.rxp
readers.sbet
readers.smrmsg
readers.slpk
readers.stac
readers.terrasolid
readers.text
readers.tiledb
readers.tindex
``` -->

{ref}`readers.arrow`

: Read GeoArrow/GeoParquet formatted data.

{ref}`readers.bpf`

: Read BPF files encoded as version 1, 2, or 3. BPF is an NGA specification
  for point cloud data.

{ref}`readers.copc`

: COPC, or Cloud Optimized Point Cloud is an LAZ 1.4 file stored as a
  clustered octree.

{ref}`readers.buffer`

: Special stage that allows you to read data from your own PointView rather
  than fetching data from a specific reader.

{ref}`readers.draco`

: Read a buffer in Google Draco format

{ref}`readers.ept`

: Used for reading [Entwine Point Tile](https://entwine.io) format.

{ref}`readers.e57`

: Read point clouds in the E57 format.

{ref}`readers.faux`

: Used for testing pipelines. It does not read from a file or database, but
  generates synthetic data to feed into the pipeline.

{ref}`readers.fbi`

: Read TerraSolid FBI format

{ref}`readers.gdal`

: Read GDAL readable raster data sources as point clouds.

{ref}`readers.hdf`

: Read data from files in the HDF5 format.

{ref}`readers.i3s`

: Read data stored in the Esri I3S format.  The data is read from an
  appropriate server.

{ref}`readers.ilvis2`

: Read from files in the ILVIS2 format.

{ref}`readers.las`

: Read ASPRS LAS versions 1.0 - 1.4. Does not support point formats
  containing waveform data. LASzip support is also enabled through this
  driver if LASzip  or LAZperf are found during compilation.

{ref}`readers.matlab`

: Read point cloud data from MATLAB .mat files where dimensions are stored as
  arrays in a MATLAB struct.

{ref}`readers.mbio`

: Read sonar bathymetry data from formats supported by the MB-System library.

{ref}`readers.memoryview`

: Read data from memory where dimension data is arranged in rows.  For
  use only with the PDAL API.

{ref}`readers.nitf`

: Read point cloud data (LAS or LAZ) wrapped in NITF 2.1 files.

{ref}`readers.numpy`

: Read point cloud data from Numpy `.npy` files.

{ref}`readers.obj`

: Read points and a mesh from Wavefront OBJ files.

{ref}`readers.optech`

: Read Optech Corrected Sensor Data (.csd) files.

{ref}`readers.pcd`

: Read files in the PCD format.

{ref}`readers.pgpointcloud`

: Read point cloud data from a PostgreSQL database with the PostgreSQL
  Pointcloud extension enabled.

{ref}`readers.ply`

: Read points and vertices from either ASCII or binary PLY files.

{ref}`readers.pts`

: Read data from Leica Cyclone PTS files.

{ref}`readers.ptx`

: Read data from Leica Cyclone PTX files.

{ref}`readers.qfit`

: Read data in the QFIT format originated for NASA's Airborne Topographic
  Mapper project.

{ref}`readers.rxp`

: Read data in the RXP format, the in-house streaming format used by RIEGL.
  The reader requires a copy of RiVLib during compilation.

{ref}`readers.rdb`

: Read data in the RDB format, the in-house database format used by RIEGL.
  The reader requires a copy of rdblib during compilation and usage.

{ref}`readers.sbet`

: Read the SBET format.

{ref}`readers.slpk`

: Read data stored in an Esri SLPK file.

{ref}`readers.smrmsg`

: Read from POSPac MMS post-processed accuracy files.

{ref}`readers.stac`

: Read STAC JSON Catalogs and Items with the Pointcloud extension.

{ref}`readers.terrasolid`

: TerraSolid Reader

{ref}`readers.text`

: Read point clouds from ASCII text files.

{ref}`readers.tiledb`

: Read point cloud data from a TileDB instance.

{ref}`readers.tindex`

: The tindex (tile index) reader allows you to automatically merge and query
  data described in tile index files that have been generated using the PDAL
  tindex command.
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('readers', **args)
 
class readers_memoryview(_GenericStage):
    """
(readers.memoryview)=

# readers.memoryview

The memoryview reader is a special stage that allows
the reading of point data arranged in rows directly from memory --
each point needs to have dimension data arranged at a fixed offset
from a base address of the point.
Before each point is read, the memoryview reader calls a function that
should return the point's base address, or a null pointer if there are no
points to be read.

Note that the memoryview reader does not currently work with columnar
data (data where individual dimensions are packed into arrays).

## Usage

The memoryview reader cannot be used from the command-line.  It is for use
by software using the PDAL API.

After creating an instance of the memoryview reader, the user should
call pushField() for every dimension that should be read from memory.
pushField() takes a single argument, a MemoryViewReader::Field, that consists
of a dimension name, a type and an offset from the point base address:

```c++
struct Field
{
    std::string m_name;
    Dimension::Type m_type;
    size_t m_offset;
};

void pushField(const Field&);
```

The user should also call setIncrementer(), a function that takes a
single argument, a std::function that receives the ID of the point to
be added and should return the base address of the point data, or a
null pointer if there are no more points to be read.

```c++
using PointIncrementer = std::function<char *(PointId)>;

void setIncrementer(PointIncrementer inc);
```

## Options

None.
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('readers.memoryview', **args)
 
class readers_nitf(_GenericStage):
    """
(readers.nitf)=

# readers.nitf

The [NITF] format is used primarily by the US Department of Defense and
supports many kinds of data inside a generic wrapper. The [NITF 2.1] version
added support for LIDAR point cloud data, and the **NITF file reader** supports
reading that data, if the NITF file supports it.

- The file must be NITF 2.1
- There must be at least one Image segment ("IM").
- There must be at least one [DES segment] ("DE") named "LIDARA".
- Only LAS or LAZ data may be stored in the LIDARA segment

The dimensions produced by the reader match exactly to the LAS dimension names
and types for convenience in file format transformation.

```{note}
Only LAS or LAZ data may be stored in the LIDARA segment. PDAL uses
the {ref}`readers.las` and {ref}`writers.las`
to actually read and write the data.
```

```{note}
PDAL uses a fork of the [NITF Nitro] library available at
<https://github.com/hobu/nitro> for NITF read and write support.
```

```{eval-rst}
.. embed::
```

```{eval-rst}
.. streamable::

```

## Example

```json
[
    {
        "type":"readers.nitf",
        "filename":"mynitf.nitf"
    },
    {
        "type":"writers.las",
        "filename":"outputfile.las"
    }
]
```

## Options

filename

: Filename to read from /[Required/]

```{include} reader_opts.md
```

extra_dims

: Extra dimensions to be read as part of each point beyond those specified by
  the LAS point format.  The format of the option is
  `<dimension_name>=<type>[, ...]`.  Any PDAL {ref}`type <types>` can
  be specified.

  ```{note}
  The presence of an extra bytes VLR when reading a version
  1.4 file or a version 1.0 - 1.3 file with **use_eb_vlr** set
  causes this option to be ignored.
  ```

use_eb_vlr

: If an extra bytes VLR is found in a version 1.0 - 1.3 file, use it as if it
  were in a 1.4 file. This option has no effect when reading a version 1.4 file.
  /[Default: false/]

compression

: May be set to "lazperf" or "laszip" to choose either the LazPerf decompressor
  or the LASzip decompressor for LAZ files.  PDAL must have been built with
  support for the decompressor being requested.  The LazPerf decompressor
  doesn't support version 1 LAZ files or version 1.4 of LAS.
  /[Default: "none"/]

[des segment]: https://nsgreg.nga.mil/doc/view?i=5402
[nitf]: http://en.wikipedia.org/wiki/National_Imagery_Transmission_Format
[nitf 2.1]: https://gwg.nga.mil/gwg/focus-groups/NITFS_NTB_Documentation.html
[nitf nitro]: https://github.com/mdaus/nitro
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('readers.nitf', **args)
 
class readers_numpy(_GenericStage):
    """
(readers.numpy)=

# readers.numpy

PDAL has support for processing data using {ref}`filters.python`, but it is also
convenient to read data from [Numpy] for processing in PDAL.

[Numpy] supports saving files with the `save` method, usually with the
extension `.npy`. As of PDAL 1.7.0, `.npz` files were not yet supported.

```{warning}
It is untested whether problems may occur if the versions of Python used
in writing the file and for reading the file don't match.
```

## Array Types

readers.numpy supports reading data in two forms:

- As a [structured array] with specified field names (from [laspy] for
  example)
- As a standard array that contains data of a single type.

### Structured Arrays

Numpy arrays can be created as structured data, where each entry is a set
of fields.  Each field has a name.  As an example, [laspy] provides its
`.points` as an array of named fields:

```
import laspy
f = laspy.file.File('test/data/autzen/autzen.las')
print (f.points[0:1])
```

```
array([ ((63608330, 84939865, 40735, 65, 73, 1, -11, 126, 7326,  245385.60820904),)],
dtype=[('point', [('X', '<i4'), ('Y', '<i4'), ('Z', '<i4'), ('intensity', '<u2'), ('flag_byte', 'u1'), ('raw_classification', 'u1'), ('scan_angle_rank', 'i1'), ('user_data', 'u1'), ('pt_src_id', '<u2'), ('gps_time', '<f8')])])
```

The numpy reader supports reading these Numpy arrays and mapping
field names to standard PDAL {ref}`dimension <dimensions>` names.
If that fails, the reader retries by removing `_`, `-`, or `space`
in turn.  If that also fails, the array field names are used to create
custom PDAL dimensions.

### Standard (non-structured) Arrays

Arrays without field information contain a single datatype.  This datatype is
mapped to a dimension specified by the `dimension` option.

```
f = open('./perlin.npy', 'rb')
data = np.load(f,)

data.shape
(100, 100)

data.dtype
dtype('float64')
```

```
pdal info perlin.npy --readers.numpy.dimension=Intensity --readers.numpy.assign_z=4
```

```
{
  "filename": "..//test//data//plang//perlin.npy",
  "pdal_version": "1.7.1 (git-version: 399e19)",
  "stats":
  {
    "statistic":
    [
      {
        "average": 49.5,
        "count": 10000,
        "maximum": 99,
        "minimum": 0,
        "name": "X",
        "position": 0,
        "stddev": 28.86967866,
        "variance": 833.4583458
      },
      {
        "average": 49.5,
        "count": 10000,
        "maximum": 99,
        "minimum": 0,
        "name": "Y",
        "position": 1,
        "stddev": 28.87633116,
        "variance": 833.8425015
      },
      {
        "average": 0.01112664759,
        "count": 10000,
        "maximum": 0.5189296418,
        "minimum": -0.5189296418,
        "name": "Intensity",
        "position": 2,
        "stddev": 0.2024120437,
        "variance": 0.04097063545
      }
    ]
  }
}
```

### X, Y and Z Mapping

Unless the X, Y or Z dimension is specified as a field in a structured array,
the reader will create dimensions X, Y and Z as necessary and populate them
based on the position of each item of the array.  Although Numpy arrays always
contain contiguous, linear data, that data can be seen to be arranged in more
than one dimension.  A two-dimensional array will cause dimensions X and Y
to be populated.  A three dimensional array will cause X, Y and Z to be
populated.  An array of more than three dimensions will reuse the X, Y and Z
indices for each dimension over three.

When reading data, X Y and Z can be assigned using row-major (C) order or
column-major (Fortran) order by using the `order` option.

```{eval-rst}
.. plugin::
```

```{eval-rst}
.. streamable::
```

## Loading Options

{ref}`readers.numpy` supports two modes of operation - the first is to pass a
reference to a `.npy` file to the `filename` argument. It will simply load
it and read.

The second is to provide a reference to a `.py` script to the `filename` argument.
It will then invoke the Python function specified in `module` and `function` with
the `fargs` that you provide.

### Loading from a Python script

A reference to a Python function that returns a Numpy array can also be used
to tell {ref}`readers.numpy` what to load. The following example itself loads
a Numpy array from a Python script

#### Python Script

```python
import numpy as np

def load(filename):
    array = np.load(filename)
    return array
```

#### Command Line Invocation

Using the above Python file with its `load` function, the following
{ref}`pdal info<info_command>` invocation passes in the reference to the filename to load.

```
pdal info threedim.py  /
    --readers.numpy.function=load /
    --readers.numpy.fargs=threedim.npy /
    --driver readers.numpy
```

#### Pipeline

An example {ref}`pipeline` definition would follow:

```
[
    {
        "function": "load",
        "filename": "threedim.py",
        "fargs": "threedim.npy",
        "type": "readers.numpy"
    },
    ...
]
```

## Options

filename

: npy file to read or optionally, a .py file that defines
  a function that returns a Numpy array using the
  `module`, `function`, and `fargs` options. /[Required/]

```{include} reader_opts.md
```

dimension

: {ref}`Dimension <dimensions>` name to map raster values

order

: Either 'row' or 'column' to specify assigning the X,Y and Z values
  in a row-major or column-major order. /[Default: matches the natural
  order of the array./]

module

: The Python module name that is holding the function to run.

function

: The function name in the module to call.

fargs

: The function args to pass to the function

```{note}
The functionality of the 'assign_z' option in previous versions is
provided with {ref}`filters.assign`

The functionality of the 'x', 'y', and 'z' options in previous versions
are generally handled with the current 'order' option.
```

[formatted]: http://en.cppreference.com/w/cpp/string/basic_string/stof
[laspy]: https://github.com/laspy/laspy
[numpy]: http://www.numpy.org/
[structured array]: https://docs.scipy.org/doc/numpy/user/basics.rec.html
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('readers.numpy', **args)
 
class readers_obj(_GenericStage):
    """
(readers.obj)=

# readers.obj

The **OBJ reader** reads data from files in the OBJ format.
This reader constructs a mesh from the faces specified in the OBJ file, ignoring
vertices that are not associated with any face. Faces, vertices, vertex normals and vertex
textures are read, while all other obj elements (such as lines and curves) are ignored.

```{eval-rst}
.. plugin::
```

## Example

This pipeline reads from an example OBJ file outputs
the vertices as a point to a LAS file.

```json
[
    {
        "type": "readers.obj",
        "filename": "test/data/obj/1.2-with-color.obj"
    },
    {
        "type" : "writers.las",
        "filename": "output.las",
        "scale_x": 1.0e-5,
        "scale_y": 1.0e-5,
        "scale_z": 1.0e-5,
        "offset_x": "auto",
        "offset_y": "auto",
        "offset_z": "auto"
    }
]
```

## Options

```{include} reader_opts.md
```

filename

: File to read. /[Required/]
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('readers.obj', **args)
 
class readers_optech(_GenericStage):
    """
(readers.optech)=

# readers.optech

The **Optech reader** reads Corrected Sensor Data (.csd) files.  These files
contain scan angles, ranges, IMU and GNSS information, and boresight
calibration values, all of which are combined in the reader into XYZ points
using the WGS84 reference frame.

```{eval-rst}
.. embed::
```

## Example

```json
[
    {
        "type":"readers.optech",
        "filename":"input.csd"
    },
    {
        "type":"writers.text",
        "filename":"outputfile.txt"
    }
]
```

## Options

filename

: csd file to read /[Required/]

```{include} reader_opts.md
```
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('readers.optech', **args)
 
class readers_pcd(_GenericStage):
    """
(readers.pcd)=

# readers.pcd

The **PCD Reader** supports reading from [Point Cloud Data (PCD)] formatted
files, which are used by the [Point Cloud Library (PCL)].

```{eval-rst}
.. embed::
```

```{eval-rst}
.. streamable::

```

## Example

```json
[
    {
        "type":"readers.pcd",
        "filename":"inputfile.pcd"
    },
    {
        "type":"writers.text",
        "filename":"outputfile.txt"
    }
]
```

## Options

filename

: PCD file to read /[Required/]

```{include} reader_opts.md
```

[point cloud data (pcd)]: https://pcl-tutorials.readthedocs.io/en/latest/pcd_file_format.html
[point cloud library (pcl)]: http://pointclouds.org
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('readers.pcd', **args)
 
class readers_pgpointcloud(_GenericStage):
    """
(readers.pgpointcloud)=

# readers.pgpointcloud

The **PostgreSQL Pointcloud Reader** allows you to read points from a PostgreSQL
database with [PostgreSQL Pointcloud] extension enabled. The Pointcloud
extension stores point cloud data in tables that contain rows of patches. Each
patch in turn contains a large number of spatially nearby points.

The reader pulls patches from a table, potentially sub-setting the query
with a "where" clause.

```{eval-rst}
.. plugin::
```

## Example

```json
[
    {
        "type":"readers.pgpointcloud",
        "connection":"dbname='lidar' user='user'",
        "table":"lidar",
        "column":"pa",
        "spatialreference":"EPSG:26910",
        "where":"PC_Intersects(pa, ST_MakeEnvelope(560037.36, 5114846.45, 562667.31, 5118943.24, 26910))"
    },
    {
        "type":"writers.text",
        "filename":"output.txt"
    }
]
```

## Options

```{include} reader_opts.md
```

connection

: PostgreSQL connection string. In the form *"host=hostname dbname=database user=username password=pw port=5432"* /[Required/]

table

: Database table to read from. /[Required/]

schema

: Database schema to read from. /[Default: **public**/]

column

: Table column to read patches from. /[Default: **pa**/]

[postgresql pointcloud]: https://github.com/pramsey/pointcloud
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('readers.pgpointcloud', **args)
 
class readers_ply(_GenericStage):
    """
(readers.ply)=

# readers.ply

The **ply reader** reads points and vertices from the [polygon file format], a
common file format for storing three dimensional models.  The ply reader
can read ASCII and binary ply files.

```{eval-rst}
.. embed::
```

```{eval-rst}
.. streamable::
```

## Example

```json
[
    {
        "type":"readers.ply",
        "filename":"inputfile.ply"
    },
    {
        "type":"writers.text",
        "filename":"outputfile.txt"
    }
]
```

## Options

filename

: ply file to read /[Required/]

```{include} reader_opts.md
```

[polygon file format]: http://paulbourke.net/dataformats/ply/
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('readers.ply', **args)
 
class readers_pts(_GenericStage):
    """
(readers.pts)=

# readers.pts

The **PTS reader** reads data from Leica Cyclone PTS files.  It infers
dimensions from points stored in a text file.

```{eval-rst}
.. embed::

```

## Example Pipeline

```json
[
    {
        "type":"readers.pts",
        "filename":"test.pts"
    },
    {
        "type":"writers.text",
        "filename":"outputfile.txt"
    }
]
```

## Options

filename

: File to read. /[Required/]

```{include} reader_opts.md
```
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('readers.pts', **args)
 
class readers_ptx(_GenericStage):
    """
(readers.ptx)=

# readers.ptx

The **PTX reader** reads data from [Leica Cyclone PTX] files. It infers
dimensions from points stored in a text file.

```{note}
PTX files can contain multiple point clouds stored in a single
file.  If that is the case, the reader will read all the points
from all of the internal point clouds as one.
:::

```{eval-rst}
.. embed::

```

## Example Pipeline

```json
[
    {
        "type":"readers.ptx",
        "filename":"test.ptx"
    },
    {
        "type":"writers.text",
        "filename":"outputfile.txt"
    }
]
```

## Options

filename

: File to read. /[Required/]

```{include} reader_opts.md
```

discard_missing_points

: Each point cloud in a PTX file is "fully populated", in that the point cloud
  will contain missing points with XYZ values of "0 0 0". When this option is
  enabled, we will skip over any missing input points.
  /[Default: true/]

[leica cyclone ptx]: http://paulbourke.net/dataformats/ptx/
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('readers.ptx', **args)
 
class readers_qfit(_GenericStage):
    """
(readers.qfit)=

# readers.qfit

The **QFIT reader** read from files in the [QFIT format] originated for the
Airborne Topographic Mapper (ATM) project at NASA Goddard Space Flight Center.

```{eval-rst}
.. embed::

```

## Example

```json
[
    {
        "type":"readers.qfit",
        "filename":"inputfile.qi",
        "flip_coordinates":"false",
        "scale_z":"1.0"
    },
    {
        "type":"writers.las",
        "filename":"outputfile.las"
    }
]
```

## Options

filename

: File to read from /[Required/]

```{include} reader_opts.md
```

flip_coordinates

: Flip coordinates from 0-360 to -180-180 /[Default: **true**/]

scale_z

: Z scale. Use 0.001 to go from mm to m. /[Default: **1**/]

little_endian

: Are data in little endian format? This should be automatically detected
  by the driver. /[Optional/]

[qfit format]: http://nsidc.org/data/docs/daac/icebridge/ilatm1b/docs/ReadMe.qfit.txt
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('readers.qfit', **args)
 
class readers_rdb(_GenericStage):
    """
(readers.rdb)=

# readers.rdb

The **RDB reader** reads from files in the RDB format, the in-house format
used by [RIEGL Laser Measurement Systems GmbH].

```{eval-rst}
.. plugin::
```

```{eval-rst}
.. streamable::
```

## Installation

To build PDAL with rdb support, `set rdb_DIR` to the path of your local
rdblib installation. rdblib can be obtained from the [RIEGL download pages]
with a properly enabled user account. The rdblib files do not need to be
in a system-level directory, though they could be (e.g. they could be in
`/usr/local`, or just in your home directory somewhere). For help building
PDAL with optional libraries, see [the optional library documentation].

```{note}
- Minimum rdblib version required to build the driver and run
  the tests: 2.1.6
- This driver was developed and tested on Ubuntu 17.10 using GCC 7.2.0.
```

## Example

This example pipeline reads points from a RDB file and stores them in LAS
format. Only points classified as "ground points" are read since option
`filter` is set to "riegl.class == 2" (see line 5).

```{code-block} json
:emphasize-lines: 5
:linenos: true

[
    {
        "type": "readers.rdb",
        "filename": "autzen-thin-srs.rdbx",
        "filter": "riegl.class == 2"
    },
    {
        "type": "writers.las",
        "filename": "autzen-thin-srs.las"
    }
]
```

## Options

filename

: Name of file to read
  /[Required/]

```{include} reader_opts.md
```

filter

: Point filter expression string (see RDB SDK documentation for details)
  /[Optional/]
  /[Default: empty string (= no filter)/]

extras

: Read all available dimensions (`true`) or known PDAL dimensions only (`false`)
  /[Optional/]
  /[Default: false/]

## Dimensions

The reader maps following default RDB point attributes to PDAL dimensions
(if they exist in the RDB file):

| RDB attribute              | PDAL dimension(s)                     |
| -------------------------- | ------------------------------------- |
| riegl.id                   | Id::PointId                           |
| riegl.source_cloud_id      | Id::OriginId                          |
| riegl.timestamp            | Id::InternalTime                      |
| riegl.xyz                  | Id::X, Id::Y, Id::Z                   |
| riegl.intensity            | Id::Intensity                         |
| riegl.amplitude            | Id::Amplitude                         |
| riegl.reflectance          | Id::Reflectance                       |
| riegl.deviation            | Id::Deviation                         |
| riegl.pulse_width          | Id::PulseWidth                        |
| riegl.background_radiation | Id::BackgroundRadiation               |
| riegl.target_index         | Id::ReturnNumber                      |
| riegl.target_count         | Id::NumberOfReturns                   |
| riegl.scan_direction       | Id::ScanDirectionFlag                 |
| riegl.scan_angle           | Id::ScanAngleRank                     |
| riegl.class                | Id::Classification                    |
| riegl.rgba                 | Id::Red, Id::Green, Id::Blue          |
| riegl.surface_normal       | Id::NormalX, Id::NormalY, Id::NormalZ |

All other point attributes that may exist in the RDB file are ignored unless
the option `extras` is set to `true`. If so, a custom dimension is defined
for each additional point attribute, whereas the dimension name is equal to
the point attribute name.

```{note}
Point attributes are read "as-is", no scaling or unit conversion is done
by the reader. The only exceptions are point coordinates (`riegl.xyz`)
and surface normals (`riegl.surface_normal`) which are transformed to
the RDB file's SRS by applying the matrix defined in the (optional) RDB
file metadata object `riegl.geo_tag`.
```

## Metadata

The reader adds following objects to the stage's metadata node:

### Object "database"

Contains basic information about the RDB file such as the bounding box,
number of points and the file ID.

```{code-block} json
:caption: 'Example:'
:linenos: true

 {
   "bounds": {
     "maximum": {
       "X": -2504493.762,
       "Y": -3846841.252,
       "Z":  4413210.394
     },
     "minimum": {
       "X": -2505882.459,
       "Y": -3848231.393,
       "Z":  4412172.548
     }
   },
   "points": 10653,
   "uuid": "637de54d-7e6b-4004-b6ab-b6bc588ec9ea"
 }
```

### List "dimensions"

List of point attribute description objects.

```{code-block} json
:caption: 'Example:'
:linenos: true

 [{
   "compression_options": "shuffle",
   "default_value": 0,
   "description": "Cartesian point coordinates wrt. application coordinate system (0: X, 1: Y, 2: Z)",
   "invalid_value": "",
   "length": 3,
   "maximum_value": 535000,
   "minimum_value": -535000,
   "name": "riegl.xyz",
   "resolution": 0.00025,
   "scale_factor": 1,
   "storage_class": "variable",
   "title": "XYZ",
   "unit_symbol": "m"
 },
 {
   "compression_options": "shuffle",
   "default_value": 0,
   "description": "Target surface reflectance",
   "invalid_value": "",
   "length": 1,
   "maximum_value": 327.67,
   "minimum_value": -327.68,
   "name": "riegl.reflectance",
   "resolution": 0.01,
   "scale_factor": 1,
   "storage_class": "variable",
   "title": "Reflectance",
   "unit_symbol": "dB"
 }]
```

Details about the point attribute properties see RDB SDK documentation.

### Object "metadata"

Contains one sub-object for each metadata object stored in the RDB file.

```{code-block} json
:caption: 'Example:'
:linenos: true

 {
   "riegl.scan_pattern": {
     "rectangular": {
       "phi_start": 45.0,
       "phi_stop": 270.0,
       "phi_increment": 0.040,
       "theta_start": 30.0,
       "theta_stop": 130.0,
       "theta_increment": 0.040,
       "program": {
         "name": "High Speed"
       }
     }
   },
   "riegl.geo_tag": {
     "crs": {
       "epsg": 4956,
       "wkt": "GEOCCS[/"NAD83(HARN) // Geocentric/",DATUM[/"NAD83(HARN)/",SPHEROID[/"GRS 1980/",6378137.000,298.257222101,AUTHORITY[/"EPSG/",/"7019/"]],AUTHORITY[/"EPSG/",/"6152/"]],PRIMEM[/"Greenwich/",0.0000000000000000,AUTHORITY[/"EPSG/",/"8901/"]],UNIT[/"Meter/",1.00000000000000000000,AUTHORITY[/"EPSG/",/"9001/"]],AXIS[/"X/",OTHER],AXIS[/"Y/",EAST],AXIS[/"Z/",NORTH],AUTHORITY[/"EPSG/",/"4956/"]]"
     },
     "pose": [
        0.837957447, 0.379440385, -0.392240121, -2505819.156,
       -0.545735575, 0.582617132, -0.602270669, -3847595.645,
        0.000000000, 0.718736580,  0.695282481,  4412064.882,
        0.000000000, 0.000000000,  0.000000000,        1.000
     ]
   }
 }
```

The `riegl.geo_tag` object defines the Spatial Reference System (SRS) of the
file. The point coordinates are actually stored in a local coordinate system
(usually horizontally leveled) which is based on the SRS. The transformation
from the local system to the SRS is defined by the 4x4 matrix `pose` which
is stored in row-wise order. Point coordinates (`riegl.xyz`) and surface
normals (`riegl.surface_normal`) are automatically transformed to the SRS
by the reader.

Details about the metadata objects see RDB SDK documentation.

### List "transactions"

List of transaction objects describing the history of the file.

```{code-block} json
:caption: 'Example:'
:linenos: true

 [{
   "agent": "RDB Library 2.1.6-1677 (x86_64-windows, Apr  5 2018, 10:58:39)",
   "comments": "",
   "id": 1,
   "rdb": "RDB Library 2.1.6-1677 (x86_64-windows, Apr  5 2018, 10:58:39)",
   "settings": {
     "cache_size": 524288000,
     "chunk_size": 65536,
     "chunk_size_lod": 20,
     "compression_level": 10,
     "primary_attribute": {
       "compression_options": "shuffle",
       "default_value": 0,
       "description": "Cartesian point coordinates wrt. application coordinate system (0: X, 1: Y, 2: Z)",
       "invalid_value": "",
       "length": 3,
       "maximum_value": 535000,
       "minimum_value": -535000,
       "name": "riegl.xyz",
       "resolution": 0.00025,
       "scale_factor": 1,
       "storage_class": "variable",
       "title": "XYZ",
       "unit_symbol": "m"
     }
   },
   "start": "2018-04-06 10:10:39.336",
   "stop": "2018-04-06 10:10:39.336",
   "title": "Database creation"
 },
 {
   "agent": "rdbconvert",
   "comments": "",
   "id": 2,
   "rdb": "RDB Library 2.1.6-1677 (x86_64-windows, Apr  5 2018, 10:58:39)",
   "settings": "",
   "start": "2018-04-06 10:10:39.339",
   "stop": "2018-04-06 10:10:39.380",
   "title": "Import"
 },
 {
   "agent": "RiSCAN PRO 64 bit v2.6.3",
   "comments": "",
   "id": 3,
   "rdb": "RDB Library 2.1.6-1677 (x86_64-windows, Apr  5 2018, 10:58:39)",
   "settings": "",
   "start": "2018-04-06 10:10:41.666",
   "stop": "2018-04-06 10:10:41.666",
   "title": "Meta data saved"
 }]
```

Details about the transaction objects see RDB SDK documentation.

[riegl download pages]: http://www.riegl.com/members-area/software-downloads/libraries/
[riegl laser measurement systems gmbh]: http://www.riegl.com
[the optional library documentation]: http://pdal.io/compilation/unix.html#configure-your-optional-libraries
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('readers.rdb', **args)
 
class readers_rxp(_GenericStage):
    """
(readers.rxp)=

# readers.rxp

The **RXP reader** read from files in the RXP format, the in-house streaming format used by [RIEGL Laser Measurement Systems GmbH].

```{warning}
This software has not been developed by RIEGL, and RIEGL will not provide
any support for this driver.  Please do not contact RIEGL with any
questions or issues regarding this driver.  RIEGL is not responsible
for damages or other issues that arise from use of this driver.
This driver has been tested against RiVLib version 1.39 on a Ubuntu
14.04 using gcc43.
```

```{eval-rst}
.. plugin::
```

```{eval-rst}
.. streamable::
```

## Installation

To build PDAL with rxp support, set RiVLib_DIR to the path of your local
RiVLib installation.  RiVLib can be obtained from the [RIEGL download pages]
with a properly enabled user account.  The RiVLib files do not need to be
in a system-level directory, though they could be (e.g. they could be
in `/usr/local`, or just in your home directory somewhere).

## Example

This example rescales the points, given in the scanner's own coordinate
system, to values that can be written to a las file.  Only points with a
valid gps time, as determined by a pps pulse, are read from the rxp, since
the `sync_to_pps` option is "true".  Reflectance values are mapped to
intensity values using sensible defaults.

```json
[
    {
        "type": "readers.rxp",
        "filename": "120304_204030.rxp",
        "sync_to_pps": "true",
        "reflectance_as_intensity": "true"
    },
    {
        "type": "writers.las",
        "filename": "outputfile.las",
        "discard_high_return_numbers": "true"
    }
]
```

We set the `discard_high_return_numbers` option to `true` on the
{ref}`writers.las`.  RXP files can contain more returns per shot than is
supported by las, and so we need to explicitly tell the las writer to ignore
those high return number points.  You could also use {ref}`filters.python`
to filter those points earlier in the pipeline.

## Options

filename

: File to read from, or rdtp URI for network-accessible scanner. /[Required/]

```{include} reader_opts.md
```

rdtp

: Boolean to switch from file-based reading to RDTP-based. /[Default: false/]

sync_to_pps

: If "true", ensure all incoming points have a valid pps timestamp, usually
  provided by some sort of GPS clock.  If "false", use the scanner's internal
  time.  /[Default: true/]

reflectance_as_intensity

: If "true", in addition to storing reflectance values directly, also
  stores the values as Intensity by mapping the reflectance values in the
  range from `min_reflectance` to `max_reflectance` to the range 0-65535.
  Values less than `min_reflectance` are assigned the value 0.
  Values greater `max_reflectance` are assigned the value 65535.
  /[Default: true/]

min_reflectance

: The low end of the reflectance-to-intensity map.  /[Default: -25.0/]

max_reflectance

: The high end of the reflectance-to-intensity map.  /[Default: 5.0/]

[riegl download pages]: http://www.riegl.com/members-area/software-downloads/libraries/
[riegl laser measurement systems gmbh]: http://www.riegl.com
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('readers.rxp', **args)
 
class readers_sbet(_GenericStage):
    """
(readers.sbet)=

# readers.sbet

The **SBET reader** read from files in the SBET format, used for exchange data from inertial measurement units (IMUs).
SBET files store angles as radians, but by default this reader converts all angle-based measurements to degrees.
Set `angles_as_degrees` to `false` to disable this conversion.

```{eval-rst}
.. embed::
```

```{eval-rst}
.. streamable::
```

## Example

```json
[
    "sbetfile.sbet",
    "output.las"
]
```

## Options

filename

: File to read from /[Required/]

```{include} reader_opts.md
```

angles_as_degrees

: Convert all angles to degrees. If false, angles are read as radians. /[Default: true/]
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('readers.sbet', **args)
 
class readers_slpk(_GenericStage):
    """
(readers.slpk)=

# readers.slpk

[Scene Layer Packages (SLPK)] is a specification created by Esri as a format
for their 3D Scene Layer and scene services. SLPK is a format that allows you
to package all the necessary {ref}`I3S <readers.i3s>` files together and store them locally rather
than find information through REST.

```{eval-rst}
.. embed::
```

```{eval-rst}
.. streamable::

```

## Example

This example will unarchive the slpk file, store it in a temp directory,
and traverse it. The data will be output to a las file. This is done
through PDAL's command line interface or through the pipeline.

```json
[
    {
        "type": "readers.slpk",
        "filename": "PDAL/test/data/i3s/SMALL_AUTZEN_LAS_All.slpk",
        "obb": {
            "center": [
                636590,
                849216,
                460
            ],
            "halfSize": [
                590,
                281,
                60
            ],
            "quaternion":
            [
                0,
                0,
                0,
                1
            ]
        }
    }
]
```

```
pdal traslate  PDAL/test/data/i3s/SMALL_AUTZEN_LAS_All.slpk autzen.las
```

## Options

filename

: SLPK file must have a file extension of .slpk.
  Example: `pdal translate /PDAL/test/data/i3s/SMALL_AUTZEN_LAS_ALL.slpk output.las`

```{include} reader_opts.md
```

obb

: An oriented bounding box used to filter the data being retrieved.  The obb
  is specified as JSON exactly as described by the [I3S specification].

dimensions

: Comma-separated list of dimensions that should be read.  Specify the
  Esri name, rather than the PDAL dimension name.

  > | Esri         | PDAL            |
  > | ------------ | --------------- |
  > | INTENSITY    | Intensity       |
  > | CLASS_CODE   | ClassFlags      |
  > | FLAGS        | Flag            |
  > | RETURNS      | NumberOfReturns |
  > | USER_DATA    | UserData        |
  > | POINT_SRC_ID | PointSourceId   |
  > | GPS_TIME     | GpsTime         |
  > | SCAN_ANGLE   | ScanAngleRank   |
  > | RGB          | Red             |

  Example: `--readers.slpk.dimensions="rgb, intensity"`

min_density and max_density

: This is the range of density of the points in the nodes that will
  be selected during the read. The density of a node is calculated by
  the vertex count divided by the effective area of the node. Nodes do
  not have a uniform density across depths in the tree, so some sections
  may be more or less dense than others. Default values for these
  parameters will select all leaf nodes (the highest resolution).

  Example: `--readers.slpk.min_density=2 --readers.slpk.max_density=2.5`

[i3s specification]: https://github.com/Esri/i3s-spec/blob/master/docs/2.0/obb.cmn.md
[scene layer packages (slpk)]: https://github.com/Esri/i3s-spec/blob/master/format/Indexed%203d%20Scene%20Layer%20Format%20Specification.md#_8_1
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('readers.slpk', **args)
 
class readers_smrmsg(_GenericStage):
    """
(readers.smrmsg)=

# readers.smrmsg

The **SMRMSG reader** read from POSPac MMS post-processed accuracy files, used to describes the accuracy of the post-processed solution (SBET file) and
contains the position, orientation and velocity RMS after smoothing. See {ref}`writers.sbet`.

```{eval-rst}
.. embed::
```

```{eval-rst}
.. streamable::
```

## Example

```json
[
    "smrmsg_xxx.out",
    "output.txt"
]
```

## Options

filename

: File to read from /[Required/]

```{include} reader_opts.md
```
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('readers.smrmsg', **args)
 
class readers_stac(_GenericStage):
    """
(readers.stac)=

# readers.stac

[Spatio Temporal Access Catalog (STAC)] is a common language to describe geospatial
information, so it can more easily be worked with, indexed, and discovered. The STAC
reader will read Catalogs and Features. For Catalogs, the reader will iterate through
items available in the Links key, creating a list of reads to accomplish.

```{eval-rst}
.. embed::
```

## Example

```json
[
    {
        "type": "readers.stac",
        "filename": "https://s3-us-west-2.amazonaws.com/usgs-lidar-stac/ept/catalog.json",
        "reader_args": [{"type": "readers.ept", "resolution": 100}],
        "items": ["MD_GoldenBeach_2012"],
        "catalogs": ["3dep"],
        "properties": { "pc:type": ["lidar", "sonar"], "pc:encoding": "ept" },
        "asset_name": "ept.json",
        "date_ranges": [
            [
                "2022-11-11T0:00:0Z",
                "2022-11-30T0:00:0Z"
            ]
        ],
        "validate_schema": true
    }
]
```

```bash
pdal info --input https://s3-us-west-2.amazonaws.com/usgs-lidar-stac/ept/MD_GoldenBeach_2012.json /
    --driver readers.stac --asset_name ept.json --summary
```

## Options

filename

: STAC endpoint, local or remote, that corresponds to a Catalog, Feature or ItemCollection.

asset_names

: The list of asset names that should be looked at to find the source data.
  The default is 'data'.

date_ranges

: A list of date ranges to prune Features by.
  Example: `--readers.stac.date_ranges '[["2022-11-11T0:00:0Z","2022-11-30T0:00:0Z"],...]'`

bounds

: Bounds to prune Features by.
  Form: `([minx,maxx],[miny,maxy],[minz,maxz])`
  Example: `--readers.stac.bounds '([-79.0,-74.0],[38.0,39.0])'`

ogr
: JSON object describing an OGR query, selecting a polygon to prune Features by. Filters for STAC
  Items that overlap any point of the specified polygon.
  Form:
```{include} ogr_json.md
```

items

: List of [Regular Expression] strings to prune STAC Item IDs by.
  Example: `--readers.stac.items '["MD_GoldenBeach_2012", "USGS_LPC//w{0,}"]'`

catalogs

: List of [Regular Expression] strings to prune STAC Catalog IDs by.
  Root catalog IDs are always included in the list.
  Example: `--readers.stac.catalogs '["3dep-test", "USGS"]'`

collections

: List of [Regular Expression] strings to prune STAC Collection IDs by.
  This will filter by the `collections` key in a STAC Item and the `id` key
  of the STAC Collection.
  Example: `--readers.stac.collections '["3dep-test", "USGS"]'`

validate_schema

: Boolean value determining if the reader should validate the supplied STAC as
  it's being read using JSON schema and the publicly available STAC schemas and
  list of STAC extension schemas.

properties

: A key value mapping (JSON) of properties and the desired values to prune
  Features by. Different keys will be AND'd together, and list of values will
  OR'd together.
  Example: `--readers.stac.properties '{"pc:type":["lidar","sonar"],"pc:encoding":"ept"}'`
  In this example, a Feature must have a `pc:type` key with values of either
  `lidar` or `sonar`, and a `pc:encoding` key with a value of `ept`.

reader_args

: A list of JSON objects with keys of reader options and the values to pass through.
  These will be in the exact same form as a Pipeline Stage object minus the filename.

  Exmaple:

```bash
--readers.stac.reader_args /
'[{"type": "readers.ept", "resolution": 100}, {"type": "readers.las", "nosrs": true}]'
```

catalog_schema_url

: URL of JSON schema you'd like to use for JSON schema validation of STAC Catalogs.

collection_schema_url

: URL of JSON schema you'd like to use for JSON schema validation of STAC Collections.

feature_schema_url

: URL of JSON schema you'd like to use for JSON schema validation of STAC Items/Features.

## Metadata

Metadata outputs will include `ids` and `item_ids` for representings STAC Feature Ids,
as well as `catalog_ids` and `collection_ids` representing STAC Catalogs and Collections,
respectively.

```bash
pdal info --summary --driver readers.stac /
--readers.stac.asset_names 'ept.json' /
--readers.stac.asset_names 'data' /
${PDAL_DIR}/test/data/stac/local_catalog/catalog.json
```

```json
{
    "file_size": 1177,
    "filename": "/PDAL_DIR/test/data/stac/local_catalog/catalog.json",
    "now": "2023-08-07T15:48:59-0500",
    "pdal_version": "2.6.0 (git-version: 54be24)",
    "reader": "readers.stac",
    "summary":
    {
        "bounds":
        {
            "maxx": 637179.22,
            "maxy": 5740737,
            "maxz": 1069,
            "minx": -10543360,
            "miny": 848935.2,
            "minz": -22
        },
        "dimensions": "ClassFlags, Classification, EdgeOfFlightLine, GpsTime, Intensity, NumberOfReturns, PointSourceId, ReturnNumber, ScanAngleRank, ScanChannel, ScanDirectionFlag, UserData, X, Y, Z, OriginId, Red, Green, Blue",
        "metadata":
        {
            "catalog_ids":
            [
                "3dep"
            ],
            "collection_ids":
            [
                "usgs-test"
            ],
            "ids":
            [
                "IA_SouthCentral_1_2020",
                "MI_Charlevoix_Islands_TL_2018",
                "MD_GoldenBeach_2012",
                "Autzen Trim"
            ],
            "item_ids":
            [
                "IA_SouthCentral_1_2020",
                "MI_Charlevoix_Islands_TL_2018",
                "MD_GoldenBeach_2012",
                "Autzen Trim"
            ]
        },
        "num_points": 44851411750
    }
}
```

## Curl Timeouts

STAC reader, and PDAL as a whole, rely on curl for external requests. The curl
requests default to a timeout of 5s. If your requests are failing, it could be
because the timeout is too short. You can set `CURL_TIMEOUT` in your environment
to get around this.

To debug your requests to make sure that the timeout is the problem, set `VERBOSE=1`
in your environment before running your PDAL task.

```bash
VERBOSE=1 CURL_TIMEOUT=30 /
    pdal info --summary --driver readers.stac /
    --readers.stac.asset_names 'ept.json' /
    --readers.stac.asset_names 'data' /
    ${PDAL_DIR}/test/data/stac/local_catalog/catalog.json
```

[regular expression]: https://en.cppreference.com/w/cpp/regex
[spatio temporal access catalog (stac)]: https://stacspec.org/en
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('readers.stac', **args)
 
class readers_terrasolid(_GenericStage):
    """
(readers.terrasolid)=

# readers.terrasolid

The **Terrasolid Reader** loads points from [Terrasolid] files (.bin).
It supports both Terrasolid format 1 and format 2.

## Example

```json
[
    {
        "type":"readers.terrasolid",
        "filename":"autzen.bin"
    },
    {
        "type":"writers.las",
        "filename":"output.las"
    }
]
```

## Options

filename

: Input file name /[Required/]

```{include} reader_opts.md
```

[terrasolid]: https://terrasolid.com/products/terrascan/
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('readers.terrasolid', **args)
 
class readers_text(_GenericStage):
    """
(readers.text)=

# readers.text

The **text reader** reads data from ASCII text files.  Each point is
represented in the file as a single line.  Each line is expected to be divided
into a number of fields by a separator.  Each field represents a value for
a point's dimension.  Each value needs to be [formatted] properly for
C++ language double-precision values.

The text reader expects a header line to indicate the dimensions are
in each subsequent line.  There are two types of header lines.

## Quoted dimension names

When the first character of the header is a double quote, each dimension name
is assumed to be surrounded by double quotes.  A single separator character
is expected between the dimension names (spaces are stripped).  If no separator
character is found, a space is assumed.  You can set the [separator] character
if it differs from that in the header.  Note that PDAL requires dimension
names that consist only of alphabetic characters and underscores.  Edit
the header line or use the [header] option to set the dimension names to
ones that PDAL understands.

## Unquoted dimension names

The first non alpha-numeric character encountered is treated as a separator
between dimension names.  The separator in the header line can be overridden
by the [separator] option.

Each line in the
file must contain the same number of fields as indicated by
dimension names in the header.  Spaces are generally ignored in the input
unless used as a separator.  When a space character is used as a separator,
any number of consecutive spaces are treated as single space and
leading/trailing spaces are ignored.

Blank lines are ignored after the header line is read.

```{eval-rst}
.. embed::
```

```{eval-rst}
.. streamable::
```

## Example Input File

This input file contains X, Y and Z value for 10 points.

```
X,Y,Z
289814.15,4320978.61,170.76
289814.64,4320978.84,170.76
289815.12,4320979.06,170.75
289815.60,4320979.28,170.74
289816.08,4320979.50,170.68
289816.56,4320979.71,170.66
289817.03,4320979.92,170.63
289817.53,4320980.16,170.62
289818.01,4320980.38,170.61
289818.50,4320980.59,170.58
```

## Example #1

```json
[
    {
        "type":"readers.text",
        "filename":"inputfile.txt"
    },
    {
        "type":"writers.text",
        "filename":"outputfile.txt"
    }
]
```

## Example #2

This reads the data in the input file as Red, Green and Blue instead of
as X, Y and Z.

```json
[
    {
        "type":"readers.text",
        "filename":"inputfile.txt",
        "header":"Red, Green, Blue",
        "skip":1
    },
    {
        "type":"writers.text",
        "filename":"outputfile.txt"
    }
]
```

## Options

filename

: text file to read, or “STDIN” to read from standard in /[Required/]

```{include} reader_opts.md
```

header

: String to use as the file header.  All lines in the file are assumed to be
  records containing point data unless skipped with the [skip] option.
  /[Default: None/]

separator

: Separator character to override that found in header line. /[Default: None/]

skip

: Number of lines to ignore at the beginning of the file. /[Default: 0/]

[formatted]: http://en.cppreference.com/w/cpp/string/basic_string/stof
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('readers.text', **args)
 
class readers_tiledb(_GenericStage):
    """
(readers.tiledb)=

# readers.tiledb

Implements [TileDB] 2.3.0+ storage.

```{eval-rst}
.. plugin::
```

```{eval-rst}
.. streamable::
```

## Example

```json
[
    {
      "type":"readers.tiledb",
      "array_name":"my_array"
    },
    {
      "type":"writers.las",
      "filename":"outputfile.las"
    }
]
```

## Options

array_name

: [TileDB] array to read from. Synonymous with `filename`. /[Required/]

config_file

: [TileDB] configuration file /[Optional/]

chunk_size

: Size of chunks to read from TileDB array /[Optional/]

stats

: Dump query stats to stdout /[Optional/]

bbox3d

: TileDB subarray to read in format (/[minx, maxx/], /[miny, maxy/], /[minz, maxz/]) /[Optional/]

start_timestamp

: Opens the array between a timestamp range of start_timestamp and end_timestamp. Default is 0. /[Optional/]

end_timestamp

: Opens the array between a timestamp range of start_timestamp and end_timestamp. Default is UINT64_MAX. /[Optional/]

timestamp

: Synonymous with start_timestamp. /[Optional/]

strict

: Raise an error if the array contains a TileDB attribute not supported by PDAL, the default is set to true to raise an error for unsupported attribute types /[Optional/]

```{include} reader_opts.md
```

[tiledb]: https://tiledb.com
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('readers.tiledb', **args)
 
class readers_tindex(_GenericStage):
    """
(readers.tindex)=

# readers.tindex

A [GDAL tile index] is an [OGR]-readable data source of boundary information.
PDAL provides a similar concept for PDAL-readable point cloud data. You can use
the {ref}`tindex_command` application to generate tile index files in any
format that [OGR] supports writing. Once you have the tile index, you can then
use the tindex reader to automatically merge and query the data described by
the tiles.

```{eval-rst}
.. embed::

```

## Basic Example

Given a tile index that was generated with the following scenario:

```
pdal tindex index.sqlite /
    "/Users/hobu/dev/git/pdal/test/data/las/interesting.las" /
    -f "SQLite" /
    --lyr_name "pdal" /
    --t_srs "EPSG:4326"
```

Use the following {ref}`pipeline <pipeline>` example to read and automatically
merge the data.

```json
[
    {
        "type":"readers.tindex",
        "filter_srs":"+proj=lcc +lat_1=43 +lat_2=45.5 +lat_0=41.75 +lon_0=-120.5 +x_0=399999.9999999999 +y_0=0 +ellps=GRS80 +units=ft +no_defs",
        "filename":"index.sqlite",
        "where":"location LIKE /'%nteresting.las%/'",
        "wkt":"POLYGON ((635629.85000000 848999.70000000, 635629.85000000 853535.43000000, 638982.55000000 853535.43000000, 638982.55000000 848999.70000000, 635629.85000000 848999.70000000))"
    },
    {
        "type":"writers.las",
        "filename":"outputfile.las"
    }
]
```

## Options

filename

: OGROpen'able raster file to read /[Required/]

```{include} reader_opts.md
```

lyr_name

: The OGR layer name for the data source to use to
  fetch the tile index information.

reader_args

: A list of JSON objects with keys of reader options and the values to pass through.
  These will be in the exact same form as a Pipeline Stage object minus the filename.

  Exmaple:

```bash
--readers.stac.reader_args /
'[{"type": "readers.ept", "resolution": 100}, {"type": "readers.las", "nosrs": true}]'
```

srs_column

: The column in the layer that provides the SRS
  information for the file. Use this if you wish to
  override or set coordinate system information for
  files.

tindex_name

: The column name that defines the file location for
  the tile index file.
  /[Default: **location**/]

sql

: [OGR SQL] to use to define the tile index layer.

bounds

: A 2D box to pre-filter the tile index. If it is set,
  it will override any [wkt] option.

wkt

: A geometry to pre-filter the tile index using
  OGR.

ogr

: A JSON object representing an OGR query to fetch a polygon for pre-filtering
  the tile index. This will also override any [wkt] option if set. 
  The JSON object is specified as follows:

```{include} ogr_json.md
```


t_srs

: Reproject the layer SRS, otherwise default to the
  tile index layer's SRS. /[Default: "EPSG:4326"/]

filter_srs

: Transforms any [wkt] or [bounds] option to this
  coordinate system before filtering or reading data.
  /[Default: "EPSG:4326"/]

where

: [OGR SQL] filter clause to use on the layer. It only
  works in combination with tile index layers that are
  defined with [lyr_name]

dialect

: [OGR SQL] dialect to use when querying tile index layer
  /[Default: OGRSQL/]

[gdal]: https://gdal.org
[gdal tile index]: https://gdal.org/en/latest/programs/gdaltindex.html
[ogr]: https://gdal.org/ogr/
[ogr sql]: https://gdal.org/en/latest/user/ogr_sql_dialect.html
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('readers.tindex', **args)
 
class reader_opts(_GenericStage):
    """
count

: Maximum number of points to read. /[Default: unlimited/]

override_srs

: Spatial reference to apply to the data.  Overrides any SRS in the input
  itself. Can be specified as a [WKT](https://www.ogc.org/standard/wkt-crs/),
  [PROJ](https://proj.org) or [EPSG](https://spatialreference.org) string.
  Can't use with 'default_srs'. /[Default: none/]

default_srs

: Spatial reference to apply to the data if the input does not specify
  one. Can be specified as a [WKT](https://www.ogc.org/standard/wkt-crs/),
  [PROJ](https://proj.org) or [EPSG](https://spatialreference.org) string.
  Can't use with 'override_srs'. /[Default: none/]
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('reader_opts', **args)
 
class stages(_GenericStage):
    """
(stages)=

# Stages

The stages of a PDAL {ref}`pipeline` are divided into {ref}`readers`, {ref}`filters`
and {ref}`writers`. Stages may support {ref}`streaming mode <processing_modes>` or
not, depending on
their functionality or particular implementation.  Many stages are built into the
base PDAL library (the file pdalcpp.so on Unix, pdalcpp.dylib on OSX and pdalcpp.dll
on Windows).  PDAL can also load stages that have been built separately. These stages
are called plugins.

Stages are usually created as plugins for one of several reasons. First, a user may wish
to create a stage for their own purposes. In this case a user has no need to build
their stage into the PDAL library itself. Second, a stage may depend on some third-party
library that cannot be distributed with PDAL.  Providing the stage as a plugin eliminates
the direct dependency on a library and can simplify licensing issues.  Third, a stage may
be little used and its addition would unnecessarily increase the size of the PDAL library.

PDAL will automatically load plugins when necessary. PDAL plugins have a specific naming
pattern:

```
libpdal_plugin_<plugin type>_<plugin name>.<shared library extension>
```

Where /<plugin type> is "reader", "writer" or "filter" and /<shared library extension> is
".dll" on Windows, ".dylib" on OSX and ".so" on UNIX systems.

The /<plugin name> must start with a letter or number, which can be followed by letters,
numbers, or an underscore ('/_').

PDAL looks for plugins in the directory that contains the PDAL library itself, as well
as the directories `.`, `./lib`, `../lib`, `./bin`, `../bin`. Those paths
are relative to the current working directory.  These locations can be overridden by
setting the environment variable `PDAL_DRIVER_PATH` to a list of directories delimited
by `;` on Windows and `:` on other platforms.

You can use `pdal --drivers` to show stages that PDAL is able to load.  Verify the above
if you are having trouble loading specific plugins.
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('stages', **args)
 
class writers_arrow(_GenericStage):
    """
(writers.arrow)=

# writers.arrow

The **Arrow Writer** supports writing to [Apache Arrow] [Feather]
and [Parquet] file types.

```{eval-rst}
.. plugin::
```

```{eval-rst}
.. streamable::


```

## Example

```json
[
    {
        "type":"readers.las",
        "filename":"inputfile.las"
    },
    {
        "type":"writers.arrow",
        "format":"feather",
        "filename":"outputfile.feather"
    }
]
```

```json
[
    {
        "type":"readers.las",
        "filename":"inputfile.las"
    },
    {
        "type":"writers.arrow",
        "format":"parquet",
        "geoparquet":"true",
        "filename":"outputfile.parquet"
    }
]
```

## Options

batch_size

: Number of rows to write as a batch /[Default: 65536/*4 /]

filename

: Output file to write /[Required/]

format

: File type to write (feather, parquet) /[Default: "feather"/]

geoarrow_dimension_name

: Dimension name to write GeoArrow struct /[Default: xyz/]

geoparquet

: Write WKB column and GeoParquet metadata when writing parquet output

write_pipeline_metadata

: Write PDAL pipeline metadata into `PDAL:pipeline:metadata` of
  `geoarrow_dimension_name`

```{include} writer_opts.md
```

[apache arrow]: https://arrow.apache.org/
[feather]: https://arrow.apache.org/docs/python/feather.html
[parquet]: https://arrow.apache.org/docs/cpp/parquet.html
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('writers.arrow', **args)
 
class writers_bpf(_GenericStage):
    """
(writers.bpf)=

# writers.bpf

BPF is an [NGA specification] for point cloud data.  The PDAL **BPF Writer**
only supports writing of version 3 BPF format files.

```{eval-rst}
.. embed::
```

```{eval-rst}
.. streamable::
```

## Example

```json
[
    {
        "type":"readers.bpf",
        "filename":"inputfile.las"
    },
    {
        "type":"writers.bpf",
        "filename":"outputfile.bpf"
    }
]
```

## Options

filename

: BPF file to write.  The writer will accept a filename containing
  a single placeholder character ('#').  If input to the writer consists
  of multiple PointViews, each will be written to a separate file, where
  the placeholder will be replaced with an incrementing integer.  If no
  placeholder is found, all PointViews provided to the writer are
  aggregated into a single file for output.  Multiple PointViews are usually
  the result of using {ref}`filters.splitter`, {ref}`filters.chipper` or
  {ref}`filters.divider`.
  /[Required/]

compression

: This option can be set to true to cause the file to be written with Zlib
  compression as described in the BPF specification.  /[Default: false/]

format

: Specifies the format for storing points in the file. /[Default: dim/]

  - dim: Dimension-major (non-interleaved).  All data for a single dimension
    are stored contiguously.
  - point: Point-major (interleaved).  All data for a single point
    are stored contiguously.
  - byte: Byte-major (byte-segregated).  All data for a single dimension are
    stored contiguously, but bytes are arranged such that the first bytes for
    all points are stored contiguously, followed by the second bytes of all
    points, etc.  See the BPF specification for further information.

bundledfile

: Path of file to be written as a bundled file (see specification).  The path
  part of the filespec is removed and the filename is stored as part of the
  data.  This option can be specified as many times as desired.

header_data

: Base64-encoded data that will be decoded and written following the
  standard BPF header.

coord_id

: The coordinate ID (UTM zone) of the data.  Southern zones take negative
  values.  A value of 0 indicates cartesian instead of UTM coordinates.  A
  value of 'auto' will attempt to set the UTM zone from a suitable spatial
  reference, or set to 0 if no such SRS is set.  /[Default: 0/]

scale_x, scale_y, scale_z

: Scale to be divided from the X, Y and Z nominal values, respectively, after
  the offset has been applied.  The special value "auto" can be specified,
  which causes the writer to select a scale to set the stored values of the
  dimensions to range from /[0, 2147483647/].  /[Default: .01/]

  Note: written value = (nominal value - offset) / scale.

offset_x, offset_y, offset_z

: Offset to be subtracted from the X, Y and Z nominal values, respectively,
  before the value is scaled.  The special value "auto" can be specified,
  which causes the writer to set the offset to the minimum value of the
  dimension.  /[Default: auto/]

  Note: written value = (nominal value - offset) / scale.

  ```{note}
  Because BPF data is always stored in UTM, the XYZ offsets are set to
  "auto" by default. This is to avoid truncation of the decimal digits
  (which may occur with offsets left at 0).
  ```

output_dims

: If specified, limits the dimensions written for each point.  Dimensions
  are listed by name and separated by commas.  X, Y and Z are required and
  must be explicitly listed.

```{include} writer_opts.md
```

[nga specification]: https://nsgreg.nga.mil/doc/view?i=4202
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('writers.bpf', **args)
 
class writers_copc(_GenericStage):
    """
(writers.copc)=

# writers.copc

The **COPC Writer** supports writing to [COPC format] files. COPC
is *Cloud Optimized Point Clouds*, and it is a LAZ 1.4 file that is
organized stored as a clustered octree.

```{eval-rst}
.. embed::

```

```{note}
Visit <https://viewer.copc.io> to view COPC files in your browser.
Simply drag-n-drop the file from your desktop onto the page,
or use
```

## VLRs

VLRs can be created by providing a JSON node called `vlrs` with objects
as shown:

```json
[
    {
        "type":"readers.las",
        "filename":"inputfile.las"
    },
    {
        "type":"writers.las",
        "vlrs": [{
            "description": "A description under 32 bytes",
            "record_id": 42,
            "user_id": "hobu",
            "data": "dGhpcyBpcyBzb21lIHRleHQ="
            },
            {
            "description": "A description under 32 bytes",
            "record_id": 43,
            "user_id": "hobu",
            "filename": "path-to-my-file.input"
            },
            {
            "description": "A description under 32 bytes",
            "record_id": 44,
            "user_id": "hobu",
            "metadata": "metadata_keyname"
            }],
        "filename":"outputfile.las"
    }
]
```

```{note}
One of `data`, `filename` or `metadata` must be specified. Data must be
specified as base64 encoded strings. The content of a file is inserted as
binary. The metadata key specified must refer to a string or base64 encoded data.
```

## Example

```json
[
    "inputfile1.las",
    "inputfile2.laz",
    {
        "type":"writers.copc",
        "filename":"outputfile.copc.laz"
    }
]
```

## Options

filename

: Output filename.  /[Required/]

forward

: List of header fields whose values should be preserved from a source
  LAS file.  The option can be specified multiple times, which has the same effect as
  listing values separated by a comma.  The following values are valid:
  `filesource_id`, `global_encoding`, `project_id`, `system_id`, `software_id`,
  `creation_doy`, `creation_year`, `scale_x`, `scale_y`, `scale_z`,
  `offset_x`, `offset_y`, `offset_z`.  In addition, the special value `header`
  can be specified, which is equivalent to specifying all the values EXCEPT the scale and
  offset values.  Scale and offset values can be forwarded as a group by
  using the special values `scale` and `offset` respectively.  The special
  value `all` is equivalent to specifying `header`, `scale`, `offset` and
  `vlr` (see below).  If a header option is specified explicitly, it will override
  any forwarded header value.
  If a LAS file is the result of multiple LAS input files, the header values
  to be forwarded must match or they will be ignored and a default will
  be used instead.

  VLRs can be forwarded by using the special value `vlr`.  VLRs containing
  the following User IDs are NOT forwarded: `LASF_Projection`,
  `liblas`, `laszip encoded`.  VLRs with the User ID `LASF_Spec` and
  a record ID other than 0 or 3 are also not forwarded.  These VLRs are known
  to contain information regarding the formatting of the data and will be rebuilt
  properly in the output file as necessary.  Unlike header values, VLRs from multiple
  input files are accumulated and each is written to the output file.  Forwarded
  VLRs may contain duplicate User ID/Record ID pairs.

software_id

: String identifying the software that created this LAS file.
  /[Default: PDAL version num (build num)/]"

creation_doy

: Number of the day of the year (January 1 == 1) this file is being created.

creation_year

: Year (Gregorian) this file is being created.

system_id

: String identifying the system that created this LAS file. /[Default: "PDAL"/]

global_encoding

: Various indicators to describe the data.  See the LAS documentation.  Note
  that PDAL will always set bit four when creating LAS version 1.4 output.
  /[Default: 0/]

project_id

: UID reserved for the user /[Default: Nil UID/]

scale_x, scale_y, scale_z

: Scale to be divided from the X, Y and Z nominal values, respectively, after
  the offset has been applied.  The special value `auto` can be specified,
  which causes the writer to select a scale to set the stored values of the
  dimensions to range from /[0, 2147483647/].  /[Default: .01/]

  Note: written value = (nominal value - offset) / scale.

offset_x, offset_y, offset_z

: Offset to be subtracted from the X, Y and Z nominal values, respectively,
  before the value is scaled.  The special value `auto` can be specified,
  which causes the writer to set the offset to the minimum value of the
  dimension.  /[Default: 0/]

  Note: written value = (nominal value - offset) / scale.

filesource_id

: The file source id number to use for this file (a value between
  0 and 65535 - 0 implies "unassigned") /[Default: 0/]

pipeline

: Write a JSON representation of the running pipeline as a VLR.

vlrs

: Add VLRS specified as json. See [VLRs] above for details.

a_srs

: Spatial reference to use to write output.

threads

: Number of threads to use when writing /[Default: 10/]

extra_dims

: Extra dimensions to be written as part of each point beyond those specified
  by the LAS point format.  The format of the option is
  `<dimension_name>=<type> [, ...]`.  Any valid PDAL {ref}`type <types>`
  can be specified.

  The special value `all` can be used in place of a dimension/type list
  to request that all dimensions that can't be stored in the predefined
  LAS point record get added as extra data at the end of each point record.

enhanced_srs_vlrs

: Write WKT2 and PROJJSON as VLR /[Default: false/]

```{include} writer_opts.md
```

[copc format]: https://copc.io/
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('writers.copc', **args)
 
class writers_draco(_GenericStage):
    """
(writers.draco)=

# writers.draco

[Draco] is a library for compressing and decompressing 3D geometric meshes and
point clouds and was designed and built for compression efficiency and speed.
The code supports compressing points, connectivity information, texture coordinates,
color information, normals, and any other generic attributes associated with geometry.

This writer aims to use the encoding feature of the Draco library to compress and
output Draco files.

## Example

This example will read in a las file and output a Draco encoded file, with options
to include PDAL dimensions X, Y, and Z as double, and explicitly setting quantization
levels of some of the Draco attributes.

```json
[
    {
        "type": "readers.las",
        "filename": "color.las"
    },
    {
        "type": "writers.draco",
        "filename": "draco.drc",
        "dimensions": {
            "X": "float",
            "Y": "float",
            "Z": "float"
        },
        "quantization": {
            "NORMAL": 8,
            "TEX_COORD": 7,
            "GENERIC": 6
        }
    }
]
```

## Options

filename

: Output file name. /[Required/]

dimensions

: A json map of PDAL dimensions to desired data types. Data types must be string
  and must be available in [PDAL's Type specification]. Any dimension that
  combine to make one Draco dimension must all have the same type (eg. POSITION is
  made up of X, Y, and Z. X cannot by float while Y and Z are specified as double)

  This argument will filter the dimensions being written to only the dimensions
  that have been specified. If that dimension is part of a multi-dimensional
  draco attribute (POSITION=/[X,Y,Z/]), then any dimension not specified will be
  filled in with zeros.

quantization

: A json map of Draco attributes to desired quantization levels. These levels
  must be integers. Default quantization levels are below, and will be
  overridden by any values placed in the options.

```json
{
    "POSITION": 11,
    "NORMAL": 7,
    "TEX_COORD": 10,
    "COLOR": 8,
    "GENERIC": 8
}
```

```{include} writer_opts.md
```

[draco]: https://github.com/google/draco
[pdal's type specification]: https://github.com/PDAL/PDAL/blob/master/pdal/DimUtil.hpp
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('writers.draco', **args)
 
class writers_e57(_GenericStage):
    """
(writers.e57)=

# writers.e57

The **E57 Writer** supports writing to E57 files.

The writer supports E57 files with Cartesian point clouds.

```{note}
E57 files can contain multiple point clouds stored in a single
file.  The writer will only write a single cloud per file.
```

```{note}
Spherical format points are not supported.
```

```{note}
The E57 `cartesianInvalidState` dimension is mapped to the Omit
PDAL dimension.  A range filter can be used to filter out the
invalid points.
```

```{eval-rst}
.. plugin::
```

```{eval-rst}
.. streamable::

```

## Example

```json
[
    {
        "type":"readers.las",
        "filename":"inputfile.las"
    },
    {
        "type":"writers.e57",
        "filename":"outputfile.e57",
          "double_precision":false
    }
]
```

## Options

filename

: E57 file to write /[Required/]

double_precision

: Use double precision for storage (false by default).

```{include} writer_opts.md
```
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('writers.e57', **args)
 
class writers_ept_addon(_GenericStage):
    """
(writers.ept_addon)=

# writers.ept_addon

The **EPT Addon Writer** supports writing additional dimensions to
[Entwine Point Tile] datasets.  The EPT addon writer may only
be used in a pipeline with an {ref}`EPT reader <readers.ept>`, and it
creates additional attributes for an existing dataset rather than
creating a brand new one.

The addon dimensions created by this writer are stored independently from the corresponding EPT dataset, therefore write-access to the EPT resource itself is not required to create and use addon dimensions.

```{eval-rst}
.. embed::
```

## Example

This example downloads the Autzen dataset (10M points) and runs the
{ref}`SMRF filter <filters.smrf>`, which populates the `Classification`
dimension with ground values, and writes the resulting attribute to an EPT
addon dataset on the local filesystem.

```json
[
    {
        "type": "readers.ept",
         "filename": "http://na.entwine.io/autzen/ept.json"
    },
    {
        "type": "filters.assign",
        "assignment": "Classification[:]=0"
    },
    {
        "type": "filters.smrf"
    },
    {
        "type": "writers.ept_addon",
        "addons": { "~/entwine/addons/autzen/smrf": "Classification" }
    }
]
```

And here is a follow-up example of reading this dataset with the
{ref}`EPT reader <readers.ept>` with the created addon overwriting the
`Classification` value.  The output is then written to a single file
with the {ref}`LAS writer <writers.las>`.

```json
[
    {
        "type": "readers.ept",
        "filename": "http://na.entwine.io/autzen/ept.json",
        "addons": { "Classification": "~/entwine/addons/autzen/smrf" }
    },
    {
        "type": "writers.las",
        "filename": "autzen-ept-smrf.las"
    }
]
```

This is an example of using multiple mappings in the `addons` option to
apply a new color scheme with {ref}`filters.colorinterp` mapping the
Red, Green, and Blue dimensions to new values.

```json
[
    {
        "type": "readers.ept",
        "filename": "http://na.entwine.io/autzen/ept.json"
    },
    {
        "type": "filters.colorinterp"
    },
    {
        "type": "writers.ept_addon",
        "addons": {
            "~/entwine/addons/autzen/interp/Red":   "Red",
            "~/entwine/addons/autzen/interp/Green": "Green",
            "~/entwine/addons/autzen/interp/Blue":  "Blue"
        }
    }
]
```

The following pipeline will read the data with the new colors:

```json
[
    {
        "type": "readers.ept",
        "filename": "http://na.entwine.io/autzen/ept.json",
        "addons": {
            "Red":   "~/entwine/addons/autzen/interp/Red",
            "Green": "~/entwine/addons/autzen/interp/Green",
            "Blue":  "~/entwine/addons/autzen/interp/Blue"
        }
    },
    {
        "type": "writers.las",
        "filename": "autzen-ept-interp.las"
    }
]
```

## Options

addons

: A JSON object whose keys represent output paths for each addon dimension,
  and whose corresponding values represent the attributes to be written to
  these addon dimensions. /[Required/]

```{note}
The `addons` option is reversed between the EPT reader and addon-writer: in each case, the right-hand side represents an assignment to the left-hand side.  In the writer, the dimension value is assigned to an addon path.  In the reader, the addon path is assigned to a dimension.
```

threads

: Number of worker threads used to write EPT addon data.  A minimum of 4 will be used no matter what value is specified.

```{include} writer_opts.md
```

[entwine point tile]: https://entwine.io/entwine-point-tile.html
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('writers.ept_addon', **args)
 
class writers_fbi(_GenericStage):
    """
(writers.fbi)=

# writers.fbi

The **fbi writer** writes the `FastBinary file format`. FastBinary is the
internal format for [TerraScan](https://terrasolid.com/products/terrascan/).
This driver allows to write FBI files in version 1 of the FBI specification.

```{note}
Support for all point attributes in LAS 1.2 format so data can be converted between LAS 1.2
and Fast Binary formats without any loss of point attribute information.
```

Point attributes are stored as attribute streams instead of point records. This makes it
possible for reading software to read only those attributes it is interested in.

```{eval-rst}
.. embed::
```

## Example

```json
[
    {
        "type":"readers.las",
        "filename":"inputfile.las"
    },
    {
        "type":"writers.fbi",
        "filename":"outputfile.fbi"
    }
]
```

## Options

filename

: FBI file to write /[Required/]
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('writers.fbi', **args)
 
class writers_fbx(_GenericStage):
    """
(writers.fbx)=

# writers.fbx

Output to the Autodesk FBX format. You must use a filter that
creates a mesh, such as {ref}`filters.poisson` or `filters.greedyprojection`,
in order to use this writer.

```{eval-rst}
.. plugin::
```

## Compilation

You must download and install the Autodesk SDK
and then compile the PDAL FBX plugin against it. Visit
<https://aps.autodesk.com/developer/overview/fbx-sdk>
to obtain a current copy of the SDK.

Example Windows CMake configuration

```
-DFBX_ROOT_DIR:FILEPATH="C:fbx2019.0" -DBUILD_PLUGIN_FBX=ON
```

## Example

```json
[
    {
        "type":"readers.las",
        "filename":"inputfile.las"
    },
    {
        "type":"filters.poisson"
    },
    {
        "type":"writers.fbox",
        "filename":"outputfile.fbx"
    }
]
```

```
pdal translate autzen.las autzen.fbx -f poisson
```

## Options

filename

: FBX filename to write.  /[Required/]

ascii

: Write ASCII FBX format.  /[Default: false/]

```{include} writer_opts.md
```
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('writers.fbx', **args)
 
class writers_gdal(_GenericStage):
    """
(writers.gdal)=

# writers.gdal

The **GDAL writer** creates a raster from a point cloud using an interpolation
algorithm.  Output is produced using [GDAL] and can use any [driver
that supports creation of rasters][driver that supports creation of rasters].  A [data_type] can be specified for the
raster (double, float, int32, etc.).  If no data type is specified, the
data type with the largest range supported by the driver is used.

The technique used to create the raster is a simple interpolation where
each point that falls within a given [radius] of a raster cell center
potentially contributes to the raster's value.  If no radius is provided,
it is set to the product of the [resolution] and the square root of two.
If a circle with the provided radius
doesn't encompass the entire cell, it is possible that some points will
not be considered at all, including those that may be within the bounds
of the raster cell.

The GDAL writer creates rasters using the data specified in the [dimension]
option (defaults to `Z`). The writer creates up to six rasters based on
different statistics in the output dataset.  The order of the layers in the
dataset is as follows:

min

: Give the cell the minimum value of all points within the given radius.

max

: Give the cell the maximum value of all points within the given radius.

mean

: Give the cell the mean value of all points within the given radius.

idw

: Cells are assigned a value based on [Shepard's inverse distance weighting]
  algorithm, considering all points within the given radius.

count

: Give the cell the number of points that lie within the given radius.

stdev

: Give the cell the population standard deviation of the points that lie
  within the given radius.

If no points fall within the circle about a raster cell, a secondary
algorithm can be used to attempt to provide a value after the standard
interpolation is complete.  If the [window_size] option is non-zero, the
values of a square of rasters surrounding an empty cell is applied
using inverse distance weighting of any non-empty cells.
The value provided for window_size is the
maximum horizontal or vertical distance that a donor cell may be in order to
contribute to the subject cell (A window_size of 1 essentially creates a 3x3
array around the subject cell.  A window_size of 2 creates a 5x5 array, and
so on.)

Cells that have no value after interpolation are given a value specified by
the [nodata] option.

```{eval-rst}
.. embed::
```

```{eval-rst}
.. streamable::

```

## Basic Example

This  pipeline reads the file autzen_trim.las and creates a Geotiff dataset
called outputfile.tif.  Since output_type isn't specified, it creates six
raster bands ("min", "max", "mean", "idx", "count" and "stdev") in the output
dataset.  The raster cells are 10x10 and the radius used to locate points
whose values contribute to the cell value is 14.14.

```json
[
    "pdal/test/data/las/autzen_trim.las",
    {
        "resolution": 10,
        "radius": 14.14,
        "filename":"outputfile.tif"
    }
]
```

## Options

filename

: Name of output file. The writer will accept a filename containing
  a single placeholder character (`#`).  If input to the writer consists
  of multiple PointViews, each will be written to a separate file, where
  the placeholder will be replaced with an incrementing integer.  If no
  placeholder is found, all PointViews provided to the writer are
  aggregated into a single file for output.  Multiple PointViews are usually
  the result of using {ref}`filters.splitter`, {ref}`filters.chipper` or
  {ref}`filters.divider`./[Required/]

binmode:

: If 'true', only points **inside** the raster pixel will be considered
  for statistics, and no distance-based summary or interpolation will
  be applied /[Default: false/]

(resolution)=

resolution

: Length of raster cell edges in X/Y units.  /[Required/]

(radius)=

radius

: Radius about cell center bounding points to use to calculate a cell value.
  /[Default: [resolution] * sqrt(2)/]

power

: Exponent of the distance when computing IDW. Close points have higher
  significance than far points. /[Default: 1.0/]

gdaldriver

: GDAL code of the [GDAL driver] to use to write the output.
  /[Default: "GTiff"/]

gdalopts

: A list of key/value options to pass directly to the GDAL driver.  The
  format is name=value,name=value,...  The option may be specified
  any number of times.

  ```{note}
  The INTERLEAVE GDAL driver option is not supported.  writers.gdal
  always uses BAND interleaving.
  ```

(data-type)=

data_type

: The {ref}`data type <types>` to use for the output raster.
  Many GDAL drivers only
  support a limited set of output data types.
  /[Default: depends on the driver/]

(nodata)=

nodata

: The value to use for a raster cell if no data exists in the input data
  with which to compute an output cell value. /[Default: depends on the
  [data_type].  -9999 for double, float, int and short, 9999 for
  unsigned int and unsigned short, 255 for unsigned char and -128 for char/]

(output-type)=

output_type

: A comma separated list of statistics for which to produce raster layers.
  The supported values are "min", "max", "mean", "idw", "count", "stdev"
  and "all".  The option may be specified more than once. /[Default: "all"/]

(window-size)=

window_size

: The maximum distance from a donor cell to a target cell when applying
  the fallback interpolation method.  See the stage description for more
  information. /[Default: 0/]

(dimension)=

dimension

: A dimension name to use for the interpolation. /[Default: "Z"/]

bounds

: The bounds of the data to be written.  Points not in bounds are discarded.
  The format is (/[minx, maxx/],/[miny,maxy/]). /[Optional/]

origin_x

: X origin (lower left corner) of the grid. /[Default: None/]

origin_y

: Y origin (lower left corner) of the grid. /[Default: None/]

width

: Number of cells in the X direction. /[Default: None/]

height

: Number of cells in the Y direction. /[Default: None/]

override_srs

: Write the raster with the provided SRS. /[Default: None/]

default_srs

: Write the raster with the provided SRS if none exists. /[Default: None/]

metadata:

: Add or set GDAL metadata to set on the raster, in the form
  `NAME=VALUE,NAME2=VALUE2,NAME3=VALUE3` /[Default: None/]

pdal_metadata:

: Write PDAL's pipeline and metadata as base64 to the GDAL PAM metadata /[Default: False/]

```{include} writer_opts.md
```

```{note}
You may use the 'bounds' option, or 'origin_x', 'origin_y', 'width'
and 'height', but not both.
```

```{note}
Unless the raster being written is empty, the spatial reference will automatically
come from the data and does not need to be set with 'override_srs' or 'default_srs'.
```

[driver that supports creation of rasters]: http://www.gdal.org/formats_list.html
[gdal]: http://gdal.org
[gdal driver]: http://www.gdal.org/formats_list.html
[shepard's inverse distance weighting]: https://en.wikipedia.org/wiki/Inverse_distance_weighting
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('writers.gdal', **args)
 
class writers_gltf(_GenericStage):
    """
(writers.gltf)=

# writers.gltf

GLTF is a file format [specification] for 3D graphics data.
If a mesh has been generated
for a PDAL point view, the **GLTF Writer** will produce simple output in
the GLTF format.  PDAL does not currently support many of the attributes
that can be found in a GLTF file.  This writer creates a *binary* GLTF (extension '.glb').

```{eval-rst}
.. embed::
```

## Example

```json
[
    "infile.las",
    {
        "type": "filters.poisson",
        "depth": 12
    },
    {
        "type":"writers.gltf",
        "filename":"output.glb",
        "red": 0.8,
        "metallic": 0.5
    }
]
```

## Options

filename

: Name of the GLTF (.glb) file to be written. /[Required/]

metallic

: The metallic factor of the faces. /[Default: 0/]

roughness

: The roughness factor of the faces. /[Default: 0/]

red

: The base red component of the color applied to the faces. /[Default: 0/]

green

: The base green component of the color applied to the faces. /[Default: 0/]

blue

: The base blue component of the color applied to the faces. /[Default: 0/]

alpha

: The alpha component to be applied to the faces. /[Default: 1.0/]

double_sided

: Whether the faces are colored on both sides, or just the side
  visible from the initial observation point (positive normal vector).
  /[Default: false/]

colors

: Write color data for each vertex.  Red, Green and Blue dimensions must exist.
  Note that most renderers will "interpolate the
  color of each vertex across a face, so this may look odd." /[Default: false/]

normals

: Write vertex normals. NormalX, NormalY and NormalZ dimensions must exist. /[Default: false/]

```{include} writer_opts.md
```

[specification]: https://www.khronos.org/gltf/
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('writers.gltf', **args)
 
class writers_las(_GenericStage):
    """
(writers.las)=

# writers.las

The **LAS Writer** supports writing to [LAS format] files, the standard
interchange file format for LIDAR data.

```{warning}
Scale/offset are not preserved from an input LAS file.  See below for
information on the scale/offset options and the [forward] option.
```

```{eval-rst}
.. embed::
```

```{eval-rst}
.. streamable::
```

## VLRs

VLRs can be created by providing a JSON node called `vlrs` with objects
as shown:

```json
[
    {
        "type":"readers.las",
        "filename":"inputfile.las"
    },
    {
        "type":"writers.las",
        "vlrs": [{
            "description": "A description under 32 bytes",
            "record_id": 42,
            "user_id": "hobu",
            "data": "dGhpcyBpcyBzb21lIHRleHQ="
            },
            {
            "description": "A description under 32 bytes",
            "record_id": 43,
            "user_id": "hobu",
            "filename": "path-to-my-file.input"
            },
            {
            "description": "Write metadata as EVLR",
            "record_id": 44,
            "user_id": "hobu",
            "evlr": true,
            "metadata": "metadata_keyname"
            }],
        "filename":"outputfile.las"
    }
]
```

```{note}
One of `data`, `filename` or `metadata` must be specified. Data must be
specified as base64 encoded strings. The content of a file is inserted as
binary. The metadata key specified must refer to a string or base64 encoded data.
```

## Example

```json
[
    {
        "type":"readers.las",
        "filename":"inputfile.las"
    },
    {
        "type":"writers.las",
        "filename":"outputfile.las"
    }
]
```

## Options

filename

: Output filename. The writer will accept a filename containing
  a single placeholder character (`#`).  If input to the writer consists
  of multiple PointViews, each will be written to a separate file, where
  the placeholder will be replaced with an incrementing integer.  If no
  placeholder is found, all PointViews provided to the writer are
  aggregated into a single file for output.  Multiple PointViews are usually
  the result of using {ref}`filters.splitter`, {ref}`filters.chipper` or
  {ref}`filters.divider`.
  /[Required/]

forward

: List of header fields whose values should be preserved from a source
  LAS file.  The
  option can be specified multiple times, which has the same effect as
  listing values separated by a comma.  The following values are valid:
  `major_version`, `minor_version`, `dataformat_id`, `filesource_id`,
  `global_encoding`, `project_id`, `system_id`, `software_id`, `creation_doy`,
  `creation_year`, `scale_x`, `scale_y`, `scale_z`, `offset_x`, `offset_y`,
  `offset_z`.  In addition, the special value `header` can be specified,
  which is equivalent to specifying all the values EXCEPT the scale and
  offset values.  Scale and offset values can be forwarded as a group by
  using the special values `scale` and `offset` respectively.  The special
  value `all` is equivalent to specifying `header`, `scale`, `offset` and
  `vlr` (see below).
  If a header option is specified explicitly, it will override any forwarded
  header value.
  If a LAS file is the result of multiple LAS input files, the header values
  to be forwarded must match or they will be ignored and a default will
  be used instead.

  VLRs can be forwarded by using the special value `vlr`.  VLRs containing
  the following User IDs are NOT forwarded: `LASF_Projection`,
  `liblas`, `laszip encoded`.  VLRs with the User ID `LASF_Spec` and
  a record ID other than 0 or 3 are also not forwarded.  These VLRs are known
  to contain information
  regarding the formatting of the data and will be rebuilt properly in the
  output file as necessary.  Unlike header values, VLRs from multiple input
  files are accumulated and each is written to the output file.  Forwarded
  VLRs may contain duplicate User ID/Record ID pairs.

minor_version

: All LAS files are version 1, but the minor version (0 - 4) can be specified
  with this option. /[Default: 4 (was 2 for PDAL 1.0 - 2.7)/]

software_id

: String identifying the software that created this LAS file.
  /[Default: PDAL version num (build num)/]"

creation_doy

: Number of the day of the year (January 1 == 1) this file is being created.

creation_year

: Year (Gregorian) this file is being created.

dataformat_id

: Controls whether information about color and time are stored with the point
  information in the LAS file. /[Default: 3/]

  - 0 == no color or time stored
  - 1 == time is stored
  - 2 == color is stored
  - 3 == color and time are stored
  - 4 /[Not Currently Supported/]
  - 5 /[Not Currently Supported/]
  - 6 == time is stored (LAS version 1.4+ only)
  - 7 == time and color are stored (LAS version 1.4+ only)
  - 8 == time, color and near infrared are stored (LAS version 1.4+ only)
  - 9 /[Not Currently Supported/]
  - 10 /[Not Currently Supported/]

system_id

: String identifying the system that created this LAS file. /[Default: "PDAL"/]

a_srs

: The spatial reference system of the file to be written. Can be an EPSG string
  (e.g. "EPSG:26910") or a WKT string. /[Default: Not set/]

global_encoding

: Various indicators to describe the data.  See the LAS documentation.  Note
  that PDAL will always set bit four when creating LAS version 1.4 output.
  /[Default: 0/]

project_id

: UID reserved for the user /[Default: Nil UID/]

compression

: Set to "true" to apply compression to the output, creating a LAZ file (using
  the LazPerf compressor) instead of a LAS file.
  For backwards compatibility, "lazperf" or "laszip" are still accepted, but
  those values are treated as "true". /[Default: "false"/]

scale_x, scale_y, scale_z

: Scale to be divided from the X, Y and Z nominal values, respectively, after
  the offset has been applied.  The special value `auto` can be specified,
  which causes the writer to select a scale to set the stored values of the
  dimensions to range from /[0, 2147483647/].  /[Default: .01/]

  Note: written value = (nominal value - offset) / scale.

offset_x, offset_y, offset_z

: Offset to be subtracted from the X, Y and Z nominal values, respectively,
  before the value is scaled.  The special value `auto` can be specified,
  which causes the writer to set the offset to the minimum value of the
  dimension.  /[Default: 0/]

  Note: written value = (nominal value - offset) / scale.

filesource_id

: The file source id number to use for this file (a value between
  0 and 65535 - 0 implies "unassigned") /[Default: 0/]

discard_high_return_numbers

: If true, discard all points with a return number greater than the maximum
  supported by the point format (5 for formats 0-5, 15 for formats 6-10).
  /[Default: false/]

extra_dims

: Extra dimensions to be written as part of each point beyond those specified
  by the LAS point format.  The format of the option is
  `<dimension_name>=<type> [, ...]`.  Any valid PDAL {ref}`type <types>`
  can be specified.

  The special value `all` can be used in place of a dimension/type list
  to request that all dimensions that can't be stored in the predefined
  LAS point record get added as extra data at the end of each point record.

  PDAL writes an extra bytes VLR (User ID: LASF_Spec, Record ID: 4) when
  extra dims are written.  The VLR describes the extra dimensions specified by
  this option.  Note that reading of this VLR is only specified for LAS
  version 1.4, though some systems will honor it for earlier file formats.
  The {ref}`LAS reader <readers.las>` requires the option
  use_eb_vlr in order to
  read the extra bytes VLR for files written with 1.1 - 1.3 LAS format.

  Setting --verbose=Info will provide output on the names, types and order
  of dimensions being written as part of the LAS extra bytes.

pdal_metadata

: Write two VLRs containing [JSON] output with both the {ref}`metadata` and
  {ref}`pipeline` serialization. /[Default: false/]

vlrs

: Add VLRS specified as json. See [VLRs] above for details.

```{include} writer_opts.md
```

[json]: http://www.json.org/
[las format]: http://asprs.org/Committee-General/LASer-LAS-File-Format-Exchange-Activities.html
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('writers.las', **args)
 
class writers_matlab(_GenericStage):
    """
(writers.matlab)=

# writers.matlab

The **Matlab Writer** supports writing Matlab `.mat` files.

The produced files has a single variable, `PDAL`, an array struct.

```{image} ./writers.matlab.png
```

```{note}
The Matlab writer requires the Mat-File API from MathWorks, and
it must be explicitly enabled at compile time with the
`BUILD_PLUGIN_MATLAB=ON` variable
```

```{eval-rst}
.. plugin::
```

## Example

```json
[
    {
        "type":"readers.las",
        "filename":"inputfile.las"
    },
    {
        "type":"writers.matlab",
        "output_dims":"X,Y,Z,Intensity",
        "filename":"outputfile.mat"
    }
]
```

## Options

filename

: Output file name /[Required/]

output_dims

: A comma-separated list of dimensions to include in the output file.
  May also be specified as an array of strings. /[Default: all available
  dimensions/]

struct

: Array structure name to read /[Default: "PDAL"/]

```{include} writer_opts.md
```
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('writers.matlab', **args)
 
class writers(_GenericStage):
    """
(writers)=

# Writers

Writers consume data provided by {ref}`readers`. Some writers can consume any
dimension type, while others only understand fixed dimension names.

```{note}
PDAL predefined dimension names can be found in the dimension registry:
{ref}`dimensions`
```

<!-- ```{toctree}
:glob: true
:hidden: true
:maxdepth: 1

writers.arrow
writers.bpf
writers.copc
writers.draco
writers.ept_addon
writers.e57
writers.fbi
writers.fbx
writers.gdal
writers.gltf
writers.las
writers.matlab
writers.nitf
writers.null
writers.ogr
writers.pcd
writers.pgpointcloud
writers.ply
writers.raster
writers.sbet
writers.text
writers.tiledb
``` -->

{ref}`writers.arrow`

: write Apache Arrow Feather- or Parquet-formatted files

{ref}`writers.bpf`

: write BPF version 3 files. BPF is an NGA specification for point cloud data.

{ref}`writers.copc`

: COPC, or Cloud Optimized Point Cloud, is an LAZ 1.4 file stored as a
  clustered octree.

{ref}`writers.draco`

: Write a buffer in Google Draco format

{ref}`writers.ept_addon`

: Append additional dimensions to Entwine resources.

{ref}`writers.e57`

: Write data in the E57 format.

{ref}`writers.fbi`

: Write TerraSolid FBI format

{ref}`writers.fbx`

: Write mesh output in the Adobe FBX format.

{ref}`writers.gdal`

: Create a raster from a point cloud using an interpolation algorithm.

{ref}`writers.gltf`

: Write mesh data in GLTF format.  Point clouds without meshes cannot be
  written.

{ref}`writers.las`

: Write ASPRS LAS and LAZ versions 1.0 - 1.4 formatted data.

{ref}`writers.matlab`

: Write MATLAB .mat files. The output has a single array struct.

{ref}`writers.nitf`

: Write LAS and LAZ point cloud data, wrapped in a NITF 2.1 file.

{ref}`writers.null`

: Provides a sink for points in a pipeline. It's the same as sending pipeline
  output to /dev/null.

{ref}`writers.ogr`

: Write a point cloud as a set of OGR points/multipoints

{ref}`writers.pcd`

: Write PCD-formatted files in the ASCII, binary, or compressed format.

{ref}`writers.pgpointcloud`

: Write to a PostgreSQL database that has the PostgreSQL Pointcloud extension
  enabled.

{ref}`writers.ply`

: Write points as PLY vertices. Can also emit a mesh as a set of faces.

{ref}`writers.raster`

: Writes rasters using GDAL. Rasters must be created using a PDAL filter.

{ref}`writers.sbet`

: Write data in the SBET format.

{ref}`writers.text`

: Write points in a text file. GeoJSON and CSV formats are supported.

{ref}`writers.tiledb`

: Write points into a TileDB database.
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('writers', **args)
 
class writers_nitf(_GenericStage):
    """
(writers.nitf)=

# writers.nitf

The [NITF] format is a US Department of Defense format for the transmission
of imagery.  It supports various formats inside a generic wrapper.

```{note}
LAS inside of NITF is widely supported by software that uses NITF
for point cloud storage, and LAZ is supported by some softwares.
No other content type beyond those two is widely supported as
of January of 2016.
```

```{eval-rst}
.. embed::
```

```{eval-rst}
.. streamable::
```

## Example

**Example One**

```json
[
    {
        "type":"readers.las",
        "filename":"inputfile.las"
    },
    {
        "type":"writers.nitf",
        "compression":"laszip",
        "idatim":"20160102220000",
        "forward":"all",
        "acftb":"SENSOR_ID:LIDAR,SENSOR_ID_TYPE:LILN",
        "filename":"outputfile.ntf"
    }
]
```

**Example Two**

```json
[
    {
        "type":"readers.las",
        "filename":"inputfile.las"
    },
    {
        "type":"writers.nitf",
        "compression":"laszip",
        "idatim":"20160102220000",
        "forward":"all",
        "acftb":"SENSOR_ID:LIDAR,SENSOR_ID_TYPE:LILN",
        "aimidb":"ACQUISITION_DATE:20160102235900",
        "filename":"outputfile.ntf"
    }
]
```

## Options

filename

: NITF file to write.  The writer will accept a filename containing
  a single placeholder character ('#').  If input to the writer consists
  of multiple PointViews, each will be written to a separate file, where
  the placeholder will be replaced with an incrementing integer.  If no
  placeholder is found, all PointViews provided to the writer are
  aggregated into a single file for output.  Multiple PointViews are usually
  the result of using {ref}`filters.splitter`, {ref}`filters.chipper` or
  {ref}`filters.divider`.

clevel

: File complexity level (2 characters) /[Default: **03**/]

stype

: Standard type (4 characters) /[Default: **BF01**/]

ostaid

: Originating station ID (10 characters) /[Default: **PDAL**/]

ftitle

: File title (80 characters) /[Default: /<spaces>/]

fsclas

: File security classification ('T', 'S', 'C', 'R' or 'U') /[Default: **U**/]

oname

: Originator name (24 characters) /[Default: /<spaces>/]

ophone

: Originator phone (18 characters) /[Default: /<spaces>/]

fsctlh

: File control and handling (2 characters) /[Default: /<spaces>/]

fsclsy

: File classification system (2 characters) /[Default: /<spaces>/]

idatim

: Image date and time (format: 'CCYYMMDDhhmmss'). Required.
  /[Default: AIMIDB.ACQUISITION_DATE if set or /<spaces>/]

iid2

: Image identifier 2 (80 characters) /[Default: /<spaces>/]

fscltx

: File classification text (43 characters) /[Default: /<spaces>/]

aimidb

: Comma separated list of name/value pairs to complete the AIMIDB
  (Additional Image ID) TRE record (format name:value).
  Required: ACQUISITION_DATE, will default to IDATIM value.
  /[Default: NITF defaults/]

acftb

: Comma separated list of name/value pairs to complete the ACFTB
  (Aircraft Information) TRE record (format name:value). Required:
  SENSOR_ID, SENSOR_ID_TYPE /[Default: NITF defaults/]

```{include} writer_opts.md
```

[nitf]: http://en.wikipedia.org/wiki/National_Imagery_Transmission_Format
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('writers.nitf', **args)
 
class writers_null(_GenericStage):
    """
(writers.null)=

# writers.null

The **null writer** discards its input.  No point output is produced when using
a null writer.

```{eval-rst}
.. embed::
```

```{eval-rst}
.. streamable::
```

## Example

```json
[
    {
        "type":"readers.las",
        "filename":"inputfile.las"
    },
    {
        "type":"filters.hexbin"
    },
    {
        "type":"writers.null"
    }
]
```

When used with an option that forces metadata output, like
--pipeline-serialization, this pipeline will create a hex boundary for
the input file, but no output point data file will be produced.

## Options

The null writer discards all passed options.
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('writers.null', **args)
 
class writers_ogr(_GenericStage):
    """
(writers.ogr)=

# writers.ogr

The **OGR Writer** will create files of various [vector formats] as supported
by the OGR library.  PDAL points are generally stored as point geometries in the
output format, though PDAL will create multipoint geometries instead if the
[multicount] option is set to a value greater than 1.
Points can be written with a additional measure value (POINTZM) if [measure_dim]
specifies a valid PDAL dimension, and dimensions can be set as feature
attributes using the [attr_dims] option.

By default, the OGR writer will create ESRI shapefiles.  The particular OGR
driver can be specified with the `ogrdriver` option.

## Example

```json
[
    "inputfile.las",
    {
        "type": "writers.ogr",
        "filename": "outfile.geojson",
        "measure_dim": "Intensity",
        "attr_dims": "Classification"
    }
]
```

## Options

filename

: Output file to write.  The writer will accept a filename containing
  a single placeholder character (`#`).  If input to the writer consists
  of multiple PointViews, each will be written to a separate file, where
  the placeholder will be replaced with an incrementing integer.  If no
  placeholder is found, all PointViews provided to the writer are
  aggregated into a single file for output.  Multiple PointViews are usually
  the result of multiple input files, or using {ref}`filters.splitter`,
  {ref}`filters.chipper` or {ref}`filters.divider`.

  The driver will use the OGR GeoJSON driver if the output filename
  extension is `.geojson`, and the ESRI Shapefile driver if the output
  filename extension is `.shp`.
  If neither extension is recognized, the filename is taken
  to represent a directory in which ESRI Shapefiles are written.  The
  driver can be explicitly specified by using the [ogrdriver] option.

multicount

: If 1, point features will be written.  If greater than 1, specifies the
  number of points to group into a feature with a multipoint geometry.  Not all
  OGR drivers support multipoint geometries. /[Default: 1/]

measure_dim

: If specified, points will be written with an extra data field, the dimension
  of which is specified by this option. Not all output formats support
  measure data. /[Default: None/]

attr_dims

: List of dimensions to write as feature attributes. Separate multiple values
  with `,` or repeat the option. Use `all` to write all dimensions.
  `X`, `Y`, `Z`, and any [measure_dim] are never written as attributes.
  This option is incompatible with the [multicount] option. /[Default: None/]

ogrdriver

: The OGR driver to use for output.  This option overrides any inference made
  about output drivers from [filename].

ogr_options

: List of OGR driver-specific layer creation options, formatted as an
  `OPTION=VALUE` string. Separate multiple values with `,` or repeat the
  option. /[Default: None/]

```{include} writer_opts.md
```

[vector formats]: https://gdal.org/drivers/vector/index.html
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('writers.ogr', **args)
 
class writers_pcd(_GenericStage):
    """
(writers.pcd)=

# writers.pcd

The **PCD Writer** supports writing to [Point Cloud Data (PCD)] formatted
files, which are used by the [Point Cloud Library (PCL)].

By default, compression is not enabled, and the PCD writer will output ASCII
formatted data.

```{eval-rst}
.. embed::
```

```{eval-rst}
.. streamable::
```

```{note}
X, Y, and Z dimensions will be written as single-precision floats by
default to be compatible with most of the existing PCL point types. These
dimensions can be forced to double-precision using the `order` option, but
the PCL code reading this data must be capable of reading double-precision
fields (i.e., it is not the responsibility of PDAL to ensure this
compatibility).
```

```{note}
When working with large coordinate values it is recommended that users
first translate the coordinate values using {ref}`filters.transformation`
to avoid loss of precision when writing single-precision XYZ data.
```

## Example

```json
[
    {
        "type":"readers.pcd",
        "filename":"inputfile.pcd"
    },
    {
        "type":"writers.pcd",
        "filename":"outputfile.pcd"
    }
]
```

## Options

filename

: PCD file to write /[Required/]

compression

: Level of PCD compression to use (ascii, binary, compressed) /[Default:
  "ascii"/]

precision

: Decimal Precision for output of values. This can be overridden for individual
  dimensions using the order option. /[Default: 2/]

order

: Comma-separated list of dimension names in the desired output order. For
  example "X,Y,Z,Red,Green,Blue". Dimension names can optionally be followed
  by a PDAL type (e.g., Unsigned32) and dimension-specific precision (used only
  with "ascii" compression).  Ex: "X=Float:2, Y=Float:2, Z=Float:3,
  Intensity=Unsigned32" If no precision is specified the value provided with
  the [precision] option is used.  The default dimension type is double
  precision float. /[Default: none/]

keep_unspecified

: If true, writes all dimensions. Dimensions specified with the [order] option
  precede those not specified. /[Default: **true**/]

```{include} writer_opts.md
```

[point cloud data (pcd)]: https://pcl-tutorials.readthedocs.io/en/latest/pcd_file_format.html
[point cloud library (pcl)]: http://pointclouds.org
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('writers.pcd', **args)
 
class writers_pgpointcloud(_GenericStage):
    """
(writers.pgpointcloud)=

# writers.pgpointcloud

The **PostgreSQL Pointcloud Writer** allows you to write to PostgreSQL database
that have the [PostgreSQL Pointcloud] extension enabled. The Pointcloud
extension stores point cloud data in tables that contain rows of patches. Each
patch in turn contains a large number of spatially nearby points.

While you can theoretically store the contents of a whole file of points in a
single patch, it is more practical to store a table full of smaller patches,
where the patches are under the PostgreSQL page size (8KB). For most LIDAR
data, this practically means a patch size of between 400 and 600 points.

In order to create patches of the right size, the Pointcloud writer should be
preceded in the pipeline file by {ref}`filters.chipper`.

The pgpointcloud format does not support WKT spatial reference specifications.  A subset of spatial references can be stored by using the 'srid' option, which
allows storage of an [EPSG code] that covers many common spatial references.
PDAL makes no attempt to reproject data to your specified srid.  Use
{ref}`filters.reprojection` for this purpose.

```{eval-rst}
.. plugin::
```

## Example

```json
[
    {
        "type":"readers.las",
        "filename":"inputfile.las",
        "spatialreference":"EPSG:26916"
    },
    {
        "type":"filters.chipper",
        "capacity":400
    },
    {
        "type":"writers.pgpointcloud",
        "connection":"host='localhost' dbname='lidar' user='pramsey'",
        "table":"example",
        "compression":"dimensional",
        "srid":"26916"
    }
]
```

## Options

connection

: PostgreSQL connection string. In the form *"host=hostname dbname=database user=username password=pw port=5432"* /[Required/]

table

: Database table to write to. /[Required/]

schema

: Database schema to write to. /[Default: "public"/]

column

: Table column to put patches into. /[Default: "pa"/]

compression

: Patch compression type to use. /[Default: ""dimensional""/]

  - **none** applies no compression
  - **dimensional** applies dynamic compression to each dimension separately
  - **lazperf** applies a "laz" compression (using the [laz-perf] library in PostgreSQL Pointcloud)

overwrite

: To drop the table before writing set to 'true'. To append to the table
  set to 'false'. /[Default: false/]

srid

: Spatial reference ID (relative to the `spatial_ref_sys` table in PostGIS)
  to store with the point cloud schema. /[Default: 4326/]

pcid

: An optional existing PCID to use for the point cloud schema. If specified,
  the schema must be present. If not specified, a match will still be
  looked for, or a new schema will be inserted. /[Default: 0/]

pre_sql

: SQL to execute *before* running the translation. If the value
  references a file, the file is read and any SQL inside is executed.
  Otherwise the value is executed as SQL itself. /[Optional/]

post_sql

: SQL to execute *after* running the translation. If the value references
  a file, the file is read and any SQL inside is executed. Otherwise the
  value is executed as SQL itself. /[Optional/]

scale_x, scale_y, scale_z / offset_x, offset_y, offset_z

: If ANY of these options are specified the X, Y and Z dimensions are adjusted
  by subtracting the offset and then dividing the values by the specified
  scaling factor before being written as 32-bit integers (as opposed to double
  precision values).  If any of these options is specified, unspecified
  scale/_/<x,y,x> options are given the value of 1.0 and unspecified
  offset/_/<x,y,z> are given the value of 0.0.

output_dims

: If specified, limits the dimensions written for each point.  Dimensions
  are listed by name and separated by commas.

```{include} writer_opts.md
```

[epsg code]: https://www.iogp.org/bookstore/product/epsg-geodetic-parameter-relational-database-developers-guide/
[laz-perf]: https://github.com/hobu/laz-perf
[postgresql pointcloud]: http://github.com/pramsey/pointcloud
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('writers.pgpointcloud', **args)
 
class writers_ply(_GenericStage):
    """
(writers.ply)=

# writers.ply

The **ply writer** writes the [polygon file format], a common file format
for storing three dimensional models.  The writer emits points as PLY vertices.
The writer can also emit a mesh as a set of faces.
{ref}`filters.greedyprojection` and {ref}`filters.poisson` create a
mesh suitable for output as faces.

```{eval-rst}
.. embed::
```

## Example

```json
[
    {
        "type":"readers.pcd",
        "filename":"inputfile.pcd"
    },
    {
        "type":"writers.ply",
        "storage_mode":"little endian",
        "filename":"outputfile.ply"
    }
]
```

## Options

filename

: ply file to write /[Required/]

storage_mode

: Type of ply file to write. Valid values are 'ascii', 'little endian',
  'big endian'.  /[Default: "ascii"/]

dims

: List of dimensions (and {ref}`types`) in the format
  `<dimension_name>[=<type>] [,...]` to write as output.
  (e.g., "Y=int32_t, X,Red=char")
  /[Default: All dimensions with stored types/]

faces

: Write a mesh as faces in addition to writing points as vertices.
  /[Default: false/]

sized_types

: PLY has variously been written with explicitly sized type strings
  ('int8', 'float32", 'uint32', etc.) and implied sized type strings
  ('char', 'float', 'int', etc.).  If true, explicitly sized type strings
  are used.  If false, implicitly sized type strings are used.
  /[Default: true/]

precision

: If specified, the number of digits to the right of the decimal place
  using f-style formatting.  Only permitted when 'storage_mode' is 'ascii'.
  See the [printf] reference for more information.
  /[Default: g-style formatting (variable precision)/]

```{include} writer_opts.md
```

[polygon file format]: http://paulbourke.net/dataformats/ply/
[printf]: https://en.cppreference.com/w/cpp/io/c/fprintf
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('writers.ply', **args)
 
class writers_raster(_GenericStage):
    """
(writers.raster)=

# writers.raster

The **Raster Writer** writes an existing raster to a file.
Output is produced using [GDAL] and can use any [driver
that supports creation of rasters][driver that supports creation of rasters].  A `data_type` can be specified for the
raster (double, float, int32, etc.).  If no data type is specified, the
data type with the largest range supported by the driver is used.

Cells that have no value are given a value specified by the `nodata` option.

```{eval-rst}
.. embed::
```

```{eval-rst}
.. streamable::

```

## Basic Example

This  pipeline reads the file autzen_trim.las, triangulates the data, creates a raster
based on the `Z` dimension as determined by interpolation of the location and values
of 'Z' of the vertices of a containing triangle, if any exists.  The resulting raster
is written to "outputfile.tif".

```json
[
    "pdal/test/data/las/autzen_trim.las",
    {
        "type": "filters.delaunay"
    }
    {
        "type": "filters.faceraster",
        "resolution": 1
    }
    {
        "type": "writers.raster"
        "filename":"outputfile.tif"
    }
]
```

## Options

filename

: Name of output file. /[Required/]

gdaldriver

: GDAL code of the [GDAL driver] to use to write the output.
  /[Default: "GTiff"/]

gdalopts

: A list of key/value options to pass directly to the GDAL driver.  The
  format is name=value,name=value,...  The option may be specified
  any number of times.

  ```{note}
  The INTERLEAVE GDAL driver option is not supported.  writers.gdal
  always uses BAND interleaving.
  ```

rasters

: A comma-separated list of raster names to be written as bands of the raster.
  All rasters must have the same limits (origin/width/height). Rasters following the first
  that don't have the same limits will be dropped. If no raster names are provided,
  only the first raster found will be placed into a single band for output.

data_type

: The {ref}`data type <types>` to use for the output raster.  Many GDAL drivers only
  support a limited set of output data types.  /[Default: depends on the driver/]

nodata

: The value to use for a raster cell if the raster contains no data in a cell.
  Note that the nodata written to the output may be different from that of the
  raster being written.
  /[Default: depends on the `data_type`.  -9999 for double, float, int and short, 9999 for
  unsigned int and unsigned short, 255 for unsigned char and -128 for char/]

```{include} writer_opts.md
```

[driver that supports creation of rasters]: http://www.gdal.org/formats_list.html
[gdal]: http://gdal.org
[gdal driver]: http://www.gdal.org/formats_list.html
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('writers.raster', **args)
 
class writers_sbet(_GenericStage):
    """
(writers.sbet)=

# writers.sbet

The **SBET writer** writes files in the SBET format, used for exchange data from inertial measurement units (IMUs).

```{eval-rst}
.. embed::
```

## Example

```json
[
    "input.sbet",
    "output.sbet"
]
```

## Options

filename

: File to write. /[Required/]

angles_are_degrees

: Convert all angular values from degrees to radians before write.
  /[Default: true/]

```{include} writer_opts.md
```
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('writers.sbet', **args)
 
class writers_text(_GenericStage):
    """
(writers.text)=

# writers.text

The **text writer** writes out to a text file. This is useful for debugging or
getting smaller files into an easily parseable format.  The text writer
supports both [GeoJSON] and [CSV] output.

```{eval-rst}
.. embed::
```

```{eval-rst}
.. streamable::
```

## Example

```json
[
    {
        "type":"readers.las",
        "filename":"inputfile.las"
    },
    {
        "type":"writers.text",
        "format":"geojson",
        "order":"X,Y,Z",
        "keep_unspecified":"false",
        "filename":"outputfile.txt"
    }
]
```

## Options

filename

: File to write to, or "STDOUT" to write to standard out /[Required/]

format

: Output format to use. One of `geojson` or `csv`. /[Default: "csv"/]

precision

: Decimal Precision for output of values. This can be overridden for
  individual dimensions using the order option. /[Default: 3/]

order

: Comma-separated list of dimension names in the desired output order.
  For example "X,Y,Z,Red,Green,Blue". Dimension names
  can optionally be followed with a colon (':') and an integer to indicate the
  precision to use for output. Ex: "X:3, Y:5,Z:0" If no precision is specified
  the value provided with the [precision] option is used. /[Default: none/]

keep_unspecified

: If true, writes all dimensions.  Dimensions specified with the [order]
  option precede those not specified. /[Default: **true**/]

jscallback

: When producing GeoJSON, the callback allows you to wrap the data in
  a function, so the output can be evaluated in a /<script> tag.

quote_header

: When producing CSV, should the column header named by quoted?
  /[Default: true/]

write_header

: Whether a header should be written. /[Default: true/]

newline

: When producing CSV, what newline character should be used? (For Windows,
  `//r//n` is common.) /[Default: "//n"/]

delimiter

: When producing CSV, what character to use as a delimiter? /[Default: ","/]

```{include} writer_opts.md
```

[csv]: http://en.wikipedia.org/wiki/Comma-separated_values
[geojson]: http://geojson.org
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('writers.text', **args)
 
class writers_tiledb(_GenericStage):
    """
(writers.tiledb)=

# writers.tiledb

Implements [TileDB] 2.3.0+ reads from an array.

```{eval-rst}
.. plugin::
```

```{eval-rst}
.. streamable::
```

## Example

```json
[
    {
        "type":"readers.las",
        "filename":"input.las"
    },
    {
        "type":"filters.stats"
    },
    {
        "type":"writers.tiledb",
        "array_name":"output_array"
    }
]
```

## Options

array_name

: [TileDB] array to write to. Synonymous with `filename`. /[Required/]

config_file

: [TileDB] configuration file. /[Optional/]

data_tile_capacity

: Number of points per tile. Not used when `append=true`. /[Default: 100,000/]

cell_order

: The layout to use for TileDB cells. May be `auto`, `row-major`, `col-major`, or `hilbert`. Not used when `append=true`. /[Default: auto/]

tile_order

: The layout to use for TileDB tiles. May be `row-major` or `col-major`. Not used when `append=true`. /[Default: row-major/]

x_tile_size

: Tile size (x). Floating point value used for determining on-disk data order. Not used when `append=true`. /[Optional/]

y_tile_size

: Tile size (y). Floating point value used for determining on-disk data order. Not used when `append=true`. /[Optional/]

z_tile_size

: Tile size (z). Floating point value used for determining on-disk data order. Not used when `append=true`. /[Optional/]

time_tile_size

: Tile size (time). Not used when `append=true`. /[Optional/]

x_domain_st

: Domain minimum for x. Not used when `append=true`. /[Optional/]

x_domain_end

: Domain maximum for x. Not used when `append=true`. /[Optional/]

y_domain_st

: Domain minimum for y. Not used when `append=true`. /[Optional/]

y_domain_end

: Domain maximum for y. Not used when `append=true`. /[Optional/]

z_domain_st

: Domain minimum for z. Not used when `append=true`. /[Optional/]

z_domain_end

: Domain maximum for z. Not used when `append=true`. /[Optional/]

time_domain_st

: Domain minimum for GpsTime. Not used when `append=true`. /[Optional/]

time_domain_end

: Domain maximum for GpsTime. Not used when `append=true`. /[Optional/]

use_time_dim

: Use GpsTime coordinate data as an array dimension instead of an array attribute. Not used when `append=true`. /[Default: false/]

time_first

: Put the GpsTime dimension first instead of last. Only used when `use_time_dim=true`. Not used when `append=true`. /[Default: false/]

combine_bit_fields

: Store all sub-byte fields together in an attribute named `BitFields`. Not used when `append=true`. /[Default: true/]

chunk_size

: Point cache size for chunked writes. /[Default: 1,000,000/]

append

: Instead of creating a new array, append to an existing array that has the dimensions stored as a TileDB dimension or TileDB attribute. /[Default: false/]

stats

: Dump query stats to stdout. /[Default: false/]

filters

: JSON array or object of compression filters for either dimenions or attributes of the form {dimension/attribute name : {"compression": name, compression_options: value, ...}}.  Not used when `append=true`. /[Optional/]

filter_profile

: Profile of compression filters to use for dimensions and attributes not provided in `filters`. Options include `balanced`, `aggressive`, and `none`. Not used when `append=true`. /[Default: balanced/]

scale_x, scale_y, scale_z

: Scale factor used for the float-scale filter for the X, Y, and Z dimensions, respectively, when using the `balanced` or `aggressive` filter profile. Not used when `append=true`. /[Default: 0.01/]

  Note: written value = (nominal value - offset) / scale.

offset_x, offset_y, offset_z

: Offset used for the float-scale filter for the  X, Y and Z dimenisons, respectively, when using the `balanced` or `aggressive` filter profile. Not used when `append=true`. /[Default: 0.0/]

  Note: written value = (nominal value - offset) / scale.

compression

: The default TileDB compression filter to use. Only used if the dimension or attribute name is not included in `filters`. Not used when `append=true`. /[Default: none/]

compression_level

: The TileDB compression level to use for the default compression. Option is ignored if set to `-1`. Not used when `append=true`. /[Default: -1/]

timestamp

: Sets the TileDB timestamp for this write. /[Optional/]

allow_dups

: Allow duplicate points. /[Default: true/]

```{include} writer_opts.md
```

TileDB provides default filter profiles. The filters can be over-written by the `filters` option. If a TileDB attribute is not set by the filter profile or the `filter` option, the compression filter set by the compression option is used.

Filters set by the `balanced` (default) filter profile (the delta filter is skipped if using TileDB version less than 2.16.0):

- X

  1. Float-scale filter (factor=/`scale_x/`, offset=/`offset_x/`, scale_float_bytewidth=4)
  2. Delta filter (reinterpret_datatype=/`INT32/`)
  3. Bit shuffle filter
  4. Zstd filter (level=7)

- Y

  1. Float-scale filter (factor=/`scale_y/`, offset=/`offset_y/`, scale_float_bytewidth=4)
  2. Delta filter (reinterpret_datatype=/`INT32/`)
  3. Bit shuffle filter
  4. Zstd filter (level=7)

- Z

  1. Float-scale filter (factor=/`scale_z/`, offset=/`offset_z/`, scale_float_bytewidth=4)
  2. Delta filter (reinterpret_datatype=/`INT32/`)
  3. Bit shuffle filter
  4. Zstd filter (level=7)

- GPSTime

  1. Delta filter (reinterpret_datatype="INT64")
  2. Bit width reduction filter
  3. Zstd filter (level=7)

- Intensity

  1. Delta filter
  2. Zstd filter (level=5)

- BitFields

  1. Zstd filter (level=5)

- ReturnNumber

  1. Zstd filter (level=5)

- NumberOfReturns

  1. Zstd filter (level=5)

- ScanDirectionFlag

  1. Zstd filter (level=5)

- EdgeOfFlightLine

  1. Zstd filter (level=5)

- Classification

  1. Zstd filter (level=5)

- UserData

  1. Zstd filter (level=5)

- PointSourceId

  1. Zstd filter (level=5)

- Red

  1. Delta filter
  2. Bit width reduction filter
  3. Zstd filter (level=7)

- Green

  1. Delta filter
  2. Bit width reduction filter
  3. Zstd filter (level=7)

- Blue

  1. Delta filter
  2. Bit width reduction filter
  3. Zstd filter (level=7)

Filters set by the `aggressive` filter profile (the delta filter is skipped if using TileDB version less than 2.16.0):

- X

  1. Float-scale filter (factor=/`scale_x/`, offset=/`offset_x/`, scale_float_bytewidth=4)
  2. Delta filter (reinterpret_datatype=/`INT32/`)
  3. Bit width reduction filter
  4. BZIP2 filter (level=9)

- Y

  1. Float-scale filter (factor=/`scale_y/`, offset=/`offset_y/`, scale_float_bytewidth=4)
  2. Delta filter (reinterpret_datatype=/`INT32/`)
  3. Bit width reduction filter
  4. BZIP2 filter (level=9)

- Z

  1. Float-scale filter (factor=/`scale_z/`, offset=/`offset_z/`, scale_float_bytewidth=4)
  2. Delta filter (reinterpret_datatype=/`INT32/`)
  3. Bit width reduction filter
  4. BZIP2 filter (level=9)

- GPSTime

  1. Delta filter (reinterpret_datatype="INT64")
  2. Bit width reduction filter
  3. BZIP2 filter (level=9)

- Intensity

  1. Delta filter
  2. Bit width reduction
  3. BZIP2 filter (level=5)

- BitFields

  1. BZIP2 filter (level=9)

- ReturnNumber

  1. BZIP2 filter (level=9)

- NumberOfReturns

  1. BZIP2 filter (level=9)

- ScanDirectionFlag

  1. BZIP2 filter (level=9)

- EdgeOfFlightLine

  1. BZIP2 filter (level=9)

- Classification

  1. BZIP2 filter (level=9)

- UserData

  1. BZIP2 filter (level=9)

- PointSourceId

  1. BZIP2 filter (level=9)

- Red

  1. Delta filter
  2. Bit width reduction filter
  3. BZIP2 filter (level=9)

- Green

  1. Delta filter
  2. Bit width reduction filter
  3. BZIP2 filter (level=9)

- Blue

  1. Delta filter
  2. Bit width reduction filter
  3. BZIP2 filter (level=9)

The filter profile `none` does not set any default filters.

[tiledb]: https://tiledb.io
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('writers.tiledb', **args)
 
class writer_opts(_GenericStage):
    """
where

: An {ref}`expression <pdal_expression>` that limits points passed to a writer.
  Points that don't pass the
  expression skip the stage but are available to subsequent stages in a pipeline.
  /[Default: no filtering/]

where_merge

: A strategy for merging points skipped by a '`where'` option when running in standard mode.
  If `true`, the skipped points are added to the first point view returned by the skipped
  filter or if no views are returned, placed in their own view. If `false`, skipped points are
  placed in their own point view. If `auto`,
  skipped points are merged into the returned point view provided that only one point view
  is returned and it has the same point count as it did when the filter was run, otherwise
  the skipped points are placed in their own view.
  /[Default: `auto`/]
"""

    def __init__(self, inputs = None, tag = None, **kwargs):
        args = {'inputs':inputs,'tag':tag}
        args.update(kwargs)
        super().__init__('writer_opts', **args)
 
