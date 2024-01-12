# Import required packages
import openeo
from openeo.processes import process

# Connect to the back-end
connection = openeo.connect("https://openeo.cloud")
# ToDo: Here you need to authenticate with authenticate_basic() or authenticate_oidc()


# Set the metadata for the process
# id: "ndwi_manual"

load1 = connection.load_collection(collection_id = "TERRASCOPE_S2_RHOW_V1", bands = ["B03", "B08"], spatial_extent = {"east": 5.850499911580535, "north": 52.036289351361205, "south": 50.031899260916134, "west": 3.0755066427889015}, temporal_extent = ["2020-01-01T00:00:00Z", "2023-09-01T00:00:00Z"])

def reducer1(data, context = None):
    array1 = process("array_element", data = data, label = "B03")
    array2 = process("array_element", data = data, label = "B08")
    add3 = process("add", x = array1, y = array2)
    subtract4 = process("subtract", x = array1, y = array2)
    divide5 = process("divide", x = subtract4, y = add3)
    return divide5

reduce2 = load1.reduce_dimension(dimension = "bands", reducer = reducer1)
save3 = reduce2.save_result(format = "NETCDF")

# The process can be executed synchronously (see below), as batch job or as web service now
result = connection.execute(save3)
