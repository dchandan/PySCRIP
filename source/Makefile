#!/bin/csh
#
# Makefile for interpolation code
#
# CVS:$Id: makefile,v 1.7 2000/04/19 21:46:44 pwjones Exp $
#
#===============================================================================
# SVN $Id$
# SVN $URL$
#===============================================================================

NC_CONFIG = $(HOME)/local/gcc/netcdf/430_hdf5_serial_gcc48/bin/nc-config
LIBDIR    = $(shell $(NC_CONFIG) --prefix)/lib
INCDIR    = $(shell $(NC_CONFIG) --prefix)/include
SRCDIR    = .
PREFIX    = /usr/local

LIBNAME   = _scrip
COMPILE   = gfortran
FLAGS     = -fdefault-real-8 -ffixed-form -O2 -fPIC
LIB       =  $(shell $(NC_CONFIG) --flibs)
INCLUDE   = -I$(INCDIR)
F2PY      = f2py
F2PY_LIB  = -L${LIBDIR} -L$(HDF5SERIAL_LIB_DIR_GCC) -lnetcdf -lnetcdff -lhdf5 -lhdf5_hl
F2PY_INCLUDE  = -I${INCDIR}
F2PY_F90_FLAG = '-fdefault-real-8 -ffixed-form -O2 -fPIC'

OBJF2PY  = \
	kinds_mod.o \
	constants.o \
	iounits.o \
	netcdf.o \
	grids.o \
	remap_vars.o \
	remap_distwgt.o \
	remap_conserv.o \
	remap_bilinear.o \
	remap_bicubic.o \
	remap_read.o \
	remap.o \
	timers.o \
	remap_write.o


all: f2py

f2py: $(SRCDIR)/$(LIBNAME)

$(SRCDIR)/$(LIBNAME): $(SRCDIR)/pyscrip.f90 $(OBJF2PY)
	$(F2PY) --f90flags=$(F2PY_F90_FLAG) \
	$(F2PY_LIB) $(F2PY_INCLUDE) -m $(LIBNAME) \
	-c $(OBJF2PY) pyscrip.f90


kinds_mod.o: $(SRCDIR)/kinds_mod.f
	$(COMPILE) $(FLAGS) $(INCLUDE) -c $(SRCDIR)/kinds_mod.f

constants.o: $(SRCDIR)/constants.f kinds_mod.o
	$(COMPILE) $(FLAGS) $(INCLUDE) -c $(SRCDIR)/constants.f

iounits.o: $(SRCDIR)/iounits.f kinds_mod.o
	$(COMPILE) $(FLAGS) $(INCLUDE) -c $(SRCDIR)/iounits.f

netcdf.o: $(SRCDIR)/netcdf.f kinds_mod.o constants.o
	$(COMPILE) $(FLAGS) $(INCLUDE) -c $(SRCDIR)/netcdf.f

grids.o: $(SRCDIR)/grids.f kinds_mod.o constants.o iounits.o netcdf.o
	$(COMPILE) $(FLAGS) $(INCLUDE) -c $(SRCDIR)/grids.f

remap_vars.o: $(SRCDIR)/remap_vars.f kinds_mod.o constants.o grids.o
	$(COMPILE) $(FLAGS) $(INCLUDE) -c $(SRCDIR)/remap_vars.f

remap_conserv.o: $(SRCDIR)/remap_conserv.f kinds_mod.o constants.o \
		timers.o remap_vars.o grids.o
	$(COMPILE) $(FLAGS) $(INCLUDE) -c $(SRCDIR)/remap_conserv.f

remap_distwgt.o: $(SRCDIR)/remap_distwgt.f kinds_mod.o constants.o \
		remap_vars.o grids.o
	$(COMPILE) $(FLAGS) $(INCLUDE) -c $(SRCDIR)/remap_distwgt.f

remap_bilinear.o: $(SRCDIR)/remap_bilinear.f kinds_mod.o constants.o \
		remap_vars.o grids.o timers.o
	$(COMPILE) $(FLAGS) $(INCLUDE) -c $(SRCDIR)/remap_bilinear.f

remap_bicubic.o: $(SRCDIR)/remap_bicubic.f kinds_mod.o constants.o \
		remap_vars.o grids.o
	$(COMPILE) $(FLAGS) $(INCLUDE) -c $(SRCDIR)/remap_bicubic.f

timers.o: $(SRCDIR)/timers.f kinds_mod.o constants.o
	$(COMPILE) $(FLAGS) $(INCLUDE) -c $(SRCDIR)/timers.f

remap_write.o: $(SRCDIR)/remap_write.f kinds_mod.o constants.o \
		netcdf.o remap_vars.o grids.o
	$(COMPILE) $(FLAGS) $(INCLUDE) -c $(SRCDIR)/remap_write.f

remap_read.o: $(SRCDIR)/remap_read.f kinds_mod.o constants.o netcdf.o \
		remap_vars.o grids.o
	$(COMPILE) $(FLAGS) $(INCLUDE) -c $(SRCDIR)/remap_read.f

remap.o: $(SRCDIR)/remap.f kinds_mod.o constants.o 
	$(COMPILE) $(FLAGS) -c $(SRCDIR)/remap.f


tidy:
	/bin/rm -f *.o *.mod

clean: 
	/bin/rm -f *.o *.mod *.so
