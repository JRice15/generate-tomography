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

parser = argparse.ArgumentParser()
parser.add_argument("--spheres",required=True,type=int)
parser.add_argument("--seed")
args = parser.parse_args()

os.makedirs("data", exist_ok=True)

### 01 generate phantom

if args.seed is None:
    print("Generating...")
    random_seed = np.random.randint(0, 100000)
    print("seed:", random_seed)
else:
    random_seed = int(args.seed)

prefix = "data/" + str(random_seed) + "_"
suffix = "_" + str(args.spheres) + "spheres.h5"

# Note that nspheres_per_unit is set to a low value to reduce the computation time here.
# The default value is 100000.
foam_ct_phantom.FoamPhantom.generate(prefix+'phantom'+suffix,random_seed,nspheres_per_unit=args.spheres)

### 03 create parallel projection

print("Projecting...")
phantom = foam_ct_phantom.FoamPhantom(prefix+'phantom'+suffix)

geom = foam_ct_phantom.ParallelGeometry(256,256,np.linspace(0,np.pi,128,False),3/256)

phantom.generate_projections(prefix+'proj_par'+suffix,geom)

projs = foam_ct_phantom.load_projections(prefix+'proj_par'+suffix)

print(len(projs), "projections, shape", projs.shape)
pl.imshow(projs[0])
pl.savefig("projected.png")
pl.imshow(projs[3])
pl.savefig("projected3.png")

### 08 add poisson noise
print("Adding Noise...")
fac = foam_ct_phantom.estimate_absorption_factor(prefix+'proj_par'+suffix,0.5)

foam_ct_phantom.apply_poisson_noise(input_file=prefix+'proj_par'+suffix,
                                    output_file=prefix+'proj_noisy'+suffix,
                                    seed=1234,
                                    flux=100,
                                    absorption_factor=fac)

projs = foam_ct_phantom.load_projections(prefix+'proj_noisy'+suffix)

pl.imshow(projs[0])
pl.savefig("noisy.png")
pl.imshow(projs[3])
pl.savefig("noisy3.png")


