import os
import tempfile
import _scrip


def compute_remap_weights(grid1_file, grid2_file, interp_file1, interp_file2, \
       map1_name, map2_name, num_maps, map_method, \
       luse_grid1_area='.false.', luse_grid2_area='.false.', \
       normalize_opt='fracarea', output_opt='scrip', \
       restrict_type='latitude', num_srch_bins='90', \
       grid1_periodic='.false.', grid2_periodic='.false.',
       ncformat='netcdf4'):
    '''
    compute remap weights and addresses
    '''

    # write namelist file
    nmlfile = os.path.join(tempfile.gettempdir(), 'compute_remap_weights_in')
    f = open(nmlfile,'w')

    f.write('&remap_inputs' + '\n')
    f.write('    num_maps = ' + str(num_maps) + '\n')
    f.write('    grid1_file = \'' + str(grid1_file) + '\'\n')
    f.write('    grid2_file = \'' + str(grid2_file) + '\'\n')
    f.write('    interp_file1 = \'' + str(interp_file1) + '\'\n')
    f.write('    interp_file2 = \'' + str(interp_file2) + '\'\n')
    f.write('    map1_name = \'' + str(map1_name) + '\'\n')
    f.write('    map2_name = \'' + str(map2_name) + '\'\n')
    f.write('    map_method = \'' + str(map_method) + '\'\n')
    f.write('    normalize_opt = \'' + str(normalize_opt) + '\'\n')
    f.write('    output_opt = \'' + str(output_opt) + '\'\n')
    f.write('    restrict_type = \'' + str(restrict_type) + '\'\n')
    f.write('    num_srch_bins = ' + str(num_srch_bins) + '\n')
    f.write('    luse_grid1_area = ' + str(luse_grid1_area) + '\n')
    f.write('    luse_grid2_area = ' + str(luse_grid2_area) + '\n')
    f.write('    grid1_periodic = ' + str(grid1_periodic) + '\n')
    f.write('    grid2_periodic = ' + str(grid2_periodic) + '\n')
    f.write('    ncformat       = \'' + str(ncformat) + '\'\n')
    f.write('/\n')

    f.close()

    # compute weights
    _scrip.compute_remap_weights(nmlfile)

    # clean
    os.remove(nmlfile) 
