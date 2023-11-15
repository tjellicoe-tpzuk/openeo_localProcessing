from openeo.local import LocalConnection
from openeo.internal.graph_building import PGNode
import json
#from rioxarray import to_raster
import rioxarray

## the job must have been executed before being passed in here
def output_to_tif(job, fileName):
    print("writing to tif")
    job.rio.to_raster(f"/output/{fileName}")
    print(f"writing completed, output available at /output/{fileName}")

