from openeo.local import LocalConnection
from openeo.internal.graph_building import PGNode
import json
#from rioxarray import to_raster
import rioxarray

local_conn = LocalConnection("./")

url = "https://earth-search.aws.element84.com/v1/collections/sentinel-2-l2a"
spatial_extent = {"west": 11, "east": 12, "south": 46, "north": 47}
temporal_extent = ["2019-01-01", "2019-06-15"]
bands = ["red", "nir"]
properties = {"eo:cloud_cover": dict(lt=50)}
s2_cube = local_conn.load_stac(url=url,
    spatial_extent=spatial_extent,
    temporal_extent=temporal_extent,
    bands=bands,
    properties=properties,
)

datacube = s2_cube

job_1 = s2_cube.execute()

print("job_1 output is")
print(job_1)

## url of stac item (this will need to be passed in from the EOEPCA)
## this example has been taken from snuggs.http. Here only a single time is captured
#url = "https://earth-search.aws.element84.com/v0/collections/sentinel-s2-l2a-cogs/items/S2A_38VNM_20221124_0_L2A"
#url = "https://raw.githubusercontent.com/EOEPCA/convert/main/stac/catalog.json"

b04 = datacube.band("red")
print(b04)
b08 = datacube.band("nir")
print(b08)

ndvi = (b04-b08) / (b04+b08)

#datacube = datacube.reduce_dimension(dimension="t", reducer="min")

job_2 = ndvi.execute()

print("job_2 output is")
print(job_2)

## open a raster file
print("writing to tif")
#job.isel(time=0).rio.to_raster("test.tif")
#print("writing completed")

job_2.isel(time=0).rio.to_raster(
    "output_job_2.tif",
    tiled=True,  # GDAL: By default striped TIFF files are created. This option can be used to force creation of tiled TIFF files.
    windowed=True,  # rioxarray: read & write one window at a time
)

try:
    job_2.attrs['spec'] = str(job_2.attrs['spec'])
except:
    None
job_2_nc = job_2.to_netcdf()

with open("output_job_2.nc", "wb") as file:
    file.write(job_2_nc)
file.close()


## NIR-RED / NIR+RED
# b08 = datacube.band("NIR")

# ndviCube = (b04-b08)/(b04+b08)


# job = ndviCube.execute()

#json_object = json.dumps(job, indent=2)
#with open("local_proc_out.json", "w") as outfile:
#    outfile.write(json_object)

#print(job.data)


## expect we need to update the json files separately, as done for the previous convert python example
