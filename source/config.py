import os.path as osp
import yaml

class YAMLobj(dict):
    """
    Maps a YAML parsed nested dictionary to python attributes.
    This solution is a variation on http://stackoverflow.com/a/32107024/805357
    """
    def __init__(self, args):
        super(YAMLobj, self).__init__(args)
        if isinstance(args, dict):
            for k, v in args.iteritems():
                if not isinstance(v, dict):
                    self[k] = v
                else:
                    self.__setattr__(k, YAMLobj(v))


    def __getattr__(self, attr):
        # return self.get(attr)
        return getattr(self, attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __setitem__(self, key, value):
        super(YAMLobj, self).__setitem__(key, value)
        self.__dict__.update({key: value})

    def __delattr__(self, item):
        self.__delitem__(item)

    def __delitem__(self, key):
        super(YAMLobj, self).__delitem__(key)
        del self.__dict__[key]


class SCRIPConfigError(Exception):
    pass

class PySCRIPConfig(YAMLobj):
    defaultconfigfile = osp.join(osp.expanduser("~"), ".pyscrip.yaml")
    def __init__(self, configfile=None):
        if configfile is None:
            if osp.isfile(PySCRIPConfig.defaultconfigfile):
                ff = open(PySCRIPConfig.defaultconfigfile, 'r')
            else:
                raise RuntimeError("No config file given and no default file for PySCRIPConfig object")
        else:
            ff = open(configfile, 'r')
        
        super(PySCRIPConfig, self).__init__( yaml.load(ff, Loader=yaml.Loader) )
        ff.close()


    def mapfile(self, gfrom, gto, maptype="conservative"):
        """
        Constructs and returns the name of the SCRIP netcdf mapping file corresponding
        to the map type "maptype" from grid "grom" to grid "gto".
        """
        if (hasattr(self.maptype, maptype)):
            maps = getattr(self.maptype, maptype)
            for mapconf in maps:
                if (mapconf["from"] == gfrom) and (mapconf["to"] == gto):
                    return osp.join(self.datadir[0], mapconf["fname"])
            raise SCRIPConfigError("No information for selected mapping in PySCRIP config file")
        else:
            raise SCRIPConfigError("No information for selected mapping in PySCRIP config file")


    def mapname(self, gfrom, gto, maptype="conservative"):
        """
        Constructs and returns the name of the SCRIP netcdf mapping file corresponding
        to the map type "maptype" from grid "grom" to grid "gto".
        """
        if (hasattr(self.maptype, maptype)):
            maps = getattr(self.maptype, maptype)
            for mapconf in maps:
                if (mapconf["from"] == gfrom) and (mapconf["to"] == gto):
                    return mapconf["name"]
            raise SCRIPConfigError("No information for selected mapping in PySCRIP config file")
        else:
            raise SCRIPConfigError("No information for selected mapping in PySCRIP config file")



a = PySCRIPConfig()
# print a.maptype.conservative.fdsfs
# print hasattr(a.maptype, "dfd")