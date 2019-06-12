import sys, os
import PySCRIP as scrip
from PySCRIP.config import PySCRIPConfig
from netCDF4 import Dataset
from matplotlib import pylab as plt



a = PySCRIPConfig()

case = "LGM6GC"
maptype = "conservative"

# print(a.getmap("BurlsFedorov", maptype, 'T31', 'll1').fname)
# print(a.getmap_by_mapset(case, maptype, 'T31', 'll1').fname)

# g1  = "fv1"
# g2  = "ll1"
# scrip.compute_remap_weights("/Users/dchandan/Research/PMIP4/bc/PMIP4_21ka_dc/cpl_s2/grids/fv0.9x1.25_070727.nc",
#                             "/Users/dchandan/Development/PySCRIP/grids/ll1deg_grid.nc",
#                             a.getmap_by_mapset(case, maptype, g1, g2).fname,
#                             a.getmap_by_mapset(case, maptype, g2, g1).fname,
#                             a.getmap_by_mapset(case, maptype, g1, g2).name,
#                             a.getmap_by_mapset(case, maptype, g2, g1).name,
#                             2,
#                             maptype,
#                             normalize_opt="fracarea")


g1  = "gx1"
g2  = "ll1"
scrip.compute_remap_weights("/Users/dchandan/Research/PMIP4/bc/LGM6GC/cpl_s2/grids/LGM6GC_gx1.nc",
                            "/Users/dchandan/Development/PySCRIP/grids/ll1deg_grid.nc",
                            a.getmap_by_mapset(case, maptype, g1, g2).fname,
                            a.getmap_by_mapset(case, maptype, g2, g1).fname,
                            a.getmap_by_mapset(case, maptype, g1, g2).name,
                            a.getmap_by_mapset(case, maptype, g2, g1).name,
                            2,
                            maptype,
                            normalize_opt="fracarea")


# # Testing part
scrip.test_remap_weights(2, a.getmap_by_mapset(case, maptype, g1, g2).fname, "out1.nc")
scrip.test_remap_weights(2, a.getmap_by_mapset(case, maptype, g2, g1).fname, "out2.nc")
