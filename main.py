#import pyproj
#print(pyproj.datadir.get_data_dir())





from pyproj import CRS
crs = CRS.from_epsg(4326)
print(crs)