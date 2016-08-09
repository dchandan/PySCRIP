#!/usr/bin/env python

from setuptools.command.install import install as setuptoolsinstall
from distutils.command.build import build as distbuild

from distutils.command.clean import clean as distclean

import os
import errno
import sys
from subprocess import call

# https://github.com/Turbo87/py-xcsoar/blob/master/setup.py


class PySCRIP_Build(distbuild):
    """
    A class that

    """
    def run(self):
        if sys.version_info >= (3, 0):
            F2PY = "f2py3"
        else:
            F2PY = "f2py"

        build_path = os.path.abspath(self.build_temp)
        # os.makedirs(build_path)
        try:
            os.makedirs(build_path)
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir(build_path):
                pass

        # Construct the make command call
        cmd = ['make', '-C', 'PySCRIP', 'F2PY='+F2PY, 'BUILDIR='+build_path]

        def callmake():
            call(cmd)

        # Execute the make call
        self.execute(callmake, [], 'Compiling SCRIP')

        # copy resulting tool to library build folder
        self.mkpath(self.build_lib)

        if sys.version_info >= (3, 0):
            target_files = [os.path.join(build_path, '_scrip.cpython-35m-darwin.so')]
            pyscriplib = "PySCRIP/_scrip.cpython-35m-darwin.so"
        else:
            target_files = [os.path.join(build_path, '_scrip.so')]
            pyscriplib = "PySCRIP/_scrip.so"

        # run original build code
        distbuild.run(self)

        # Copy the shared library to the lib folder
        self.copy_file(pyscriplib, os.path.join(self.build_lib, 'PySCRIP'))
        os.remove(pyscriplib)


class PySCRIP_Install(setuptoolsinstall):
    def run(self):
        # do pre install stuff:

        setuptoolsinstall.run(self)

        # do post install stuff:
        print("\nPySCRIP installed successfully\n")


class PySCRIP_Clean(distclean):
    def run(self):
        # Construct the make command call
        cmd = ['make', 'clean', '-C', 'PySCRIP']

        def callclean():
            call(cmd)

        # Execute the make call
        self.execute(callclean, [], 'Cleaning SCRIP compilation')

        distclean.run(self)


if __name__ == "__main__":
    from numpy.distutils.core import setup

    exec(open("PySCRIP/version.py").read())

    setup(name='PySCRIP',
          version=__version__,
          description="Python wrapper around SCRIP",
          author="Deepak Chandan",
          author_email="dchandan@atmosp.physics.utoronto.ca",

          license="MIT",

          classifiers=[
              'Development Status :: 5 - Production/Stable',

              'License :: OSI Approved :: MIT License',

              'Intended Audience :: Scientists',

              'Programming Language :: Python :: 2.7',
              'Programming Language :: Python :: 3',
              'Programming Language :: Python :: 3.2',
              'Programming Language :: Python :: 3.3',
              'Programming Language :: Python :: 3.4',
              'Programming Language :: Python :: 3.5',
          ],

          keywords='scrip cesm',
          packages=['PySCRIP'],

          cmdclass={
              'build': PySCRIP_Build,
              'install': PySCRIP_Install,
              'clean': PySCRIP_Clean},

          )
