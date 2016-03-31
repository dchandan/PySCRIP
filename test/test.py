
import sys, os
import PySCRIP.source as scrip
from PySCRIP.source.config import PySCRIPConfig
from netCDF4 import Dataset
import numpy as np
from matplotlib import pylab as plt


a = PySCRIPConfig()


# Mapping part
ncfile = Dataset("testdata/cesmpifv1mts_cam_mapping_testdata.nc", "r")
src_array = ncfile.variables["TS"][:,:]
print src_array.shape
dest = scrip.remap(src_array, "/Users/dchandan/Research/CESM/bc/cesmpifv1mts/cpl_s2/wrkdir/map_fv1-gx1_a_cesmpifv1_130513.nc",
                   fformat="ncar-csm")
print dest.shape

print src_array.min(), src_array.max()
print dest.min(), dest.max()

plt.figure()
plt.imshow(np.flipud(src_array[0,:]))
plt.colorbar()


plt.figure()
plt.imshow(np.flipud(dest))
plt.colorbar()


# plt.figure()
# plt.imshow(np.flipud(dest), vmin=src_array.min(), vmax=src_array.max())
# # plt.imshow(np.flipud(dest))
# plt.colorbar()
plt.show()
