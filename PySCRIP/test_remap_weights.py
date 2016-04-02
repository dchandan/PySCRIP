import os
import tempfile
import _scrip


def test_remap_weights(field_choice, interp_file, output_file): 
    '''
    test addresses and weights computed in a setup phase
    '''

    # write test namelist file
    nmlfile = os.path.join(tempfile.gettempdir(), 'test_remap_weights_in')
    f = open(nmlfile,'w')

    f.write('&remap_inputs' + '\n')
    f.write('    field_choice = ' + str(field_choice) + '\n')
    f.write('    interp_file = \'' + str(interp_file) + '\'\n')
    f.write('    output_file = \'' + str(output_file) + '\'\n')
    f.write('/\n')

    f.close()

    # run test weights
    _scrip.test_remap_weights(nmlfile)

    # clean
    os.remove(nmlfile) 
