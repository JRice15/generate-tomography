#-----------------------------------------------------------------------
#Copyright 2019 Centrum Wiskunde & Informatica, Amsterdam
#
#Author: Daniel M. Pelt
#Contact: D.M.Pelt@cwi.nl
#Website: http://dmpelt.github.io/foam_ct_phantom/
#License: MIT
#
#This file is part of foam_ct_phantom, a Python package for generating
#foam-like phantoms for CT.
#-----------------------------------------------------------------------

"""
Example 03: Generate parallel-beam projections
==============================================
"""

import foam_ct_phantom
import numpy as np
import h5py
import astra
import matplotlib.pylab as pl
import argparse
import os
pl.gray()

os.makedirs("data", exist_ok=True)

### 01 generate phantom

print("Generating...")
random_seed = np.random.randint(0, 100000)
print("seed:", random_seed)

seedstr = str(random_seed)

# Note that nspheres_per_unit is set to a low value to reduce the computation time here.
# The default value is 100000.
foam_ct_phantom.FoamPhantom.generate('data/'+seedstr+'phantom.h5',random_seed,nspheres_per_unit=25)

### 03 create parallel projection

print("Projecting...")
phantom = foam_ct_phantom.FoamPhantom('data/'+seedstr+'phantom.h5')

geom = foam_ct_phantom.ParallelGeometry(256,256,np.linspace(0,np.pi,128,False),3/256)

phantom.generate_projections('data/'+seedstr+'proj_par.h5',geom)

projs = foam_ct_phantom.load_projections('data/'+seedstr+'proj_par.h5')

print(len(projs), "projections, shape", projs.shape)
pl.imshow(projs[0])
pl.savefig("projected.png")
pl.imshow(projs[3])
pl.savefig("projected3.png")

### 08 add poisson noise
print("Adding Noise...")
fac = foam_ct_phantom.estimate_absorption_factor('data/'+seedstr+'proj_par.h5',0.5)

foam_ct_phantom.apply_poisson_noise(input_file='data/'+seedstr+'proj_par.h5',
                                    output_file='data/'+seedstr+'proj_noisy.h5',
                                    seed=1234,
                                    flux=100,
                                    absorption_factor=fac)

projs = foam_ct_phantom.load_projections('data/'+seedstr+'proj_noisy.h5')

pl.imshow(projs[0])
pl.savefig("noisy.png")
pl.imshow(projs[3])
pl.savefig("noisy3.png")


