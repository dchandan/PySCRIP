
import sys, os
import PySCRIP.source as scrip
from PySCRIP.source.config import PySCRIPConfig
from netCDF4 import Dataset
import numpy as np
from matplotlib import pylab as plt


a = PySCRIPConfig()

# for maptype in a.maptype:
#     print maptype
#     for map_ in getattr(a.maptype, maptype):
#         print a.mapfile(map_["from"], map_["to"], maptype=maptype)
#         # print map_

g1  = "gx1"
g2  = "ll1"
maptype = "conservative"
# scrip.compute_remap_weights("/Users/dchandan/Development/PySCRIP/test/ptest_gx1.nc",
#                             "/Users/dchandan/Development/PySCRIP/grids/ll1deg_grid.nc",
#                             a.mapfile(g1, g2),
#                             a.mapfile(g2, g1),
#                             a.mapname(g1, g2),
#                             a.mapname(g2, g1),
#                             2,
#                             maptype,
#                             normalize_opt="destarea",
#                             luse_grid1_area='.false.', luse_grid2_area='.false.',)


# Testing part
scrip.test_remap_weights(2, a.mapfile(g1, g2), "out.nc")
