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
pl.gray()

### 01 generate phantom

print("Generating...")
random_seed = 12345

# Note that nspheres_per_unit is set to a low value to reduce the computation time here.
# The default value is 100000.
foam_ct_phantom.FoamPhantom.generate('test_phantom.h5',random_seed,nspheres_per_unit=4)

### 02 plot

phantom = foam_ct_phantom.FoamPhantom('test_phantom.h5')

geom = foam_ct_phantom.VolumeGeometry(256,256,1,3/256)

phantom.generate_volume('test_midslice.h5', geom)

vol = foam_ct_phantom.load_volume('test_midslice.h5')

print(len(vol), "volumes, shape", vol.shape)
pl.imshow(vol[0])
pl.savefig("phantom.png")

### 03 create parallel projection

print("Projecting...")
phantom = foam_ct_phantom.FoamPhantom('test_phantom.h5')

geom = foam_ct_phantom.ParallelGeometry(256,256,np.linspace(0,np.pi,128,False),3/256)

phantom.generate_projections('test_projs_par.h5',geom)

projs = foam_ct_phantom.load_projections('test_projs_par.h5')

print(len(projs), "projections, shape", projs.shape)
pl.imshow(projs[0])
pl.savefig("projected.png")
pl.imshow(projs[3])
pl.savefig("projected3.png")

### 08 add poisson noise
print("Adding Noise...")
fac = foam_ct_phantom.estimate_absorption_factor('test_projs_par.h5',0.5)

foam_ct_phantom.apply_poisson_noise(input_file='test_projs_par.h5',
                                    output_file='test_projs_noisy.h5',
                                    seed=1234,
                                    flux=100,
                                    absorption_factor=fac)

projs = foam_ct_phantom.load_projections('test_projs_noisy.h5')

pl.imshow(projs[0])
pl.savefig("noisy.png")
pl.imshow(projs[3])
pl.savefig("noisy3.png")

### 09 astra reconstruction
print("Reconstructing...")

projs = foam_ct_phantom.load_projections('test_projs_par.h5')

vol_geom = foam_ct_phantom.VolumeGeometry(256, 256, 256, 3/256)

proj_geom = foam_ct_phantom.ParallelGeometry.from_file('test_projs_par.h5')

pg = proj_geom.to_astra(single_slice=True)
vg = vol_geom.to_astra(single_slice=True)

pid = astra.create_projector('cuda', pg, vg)
w = astra.OpTomo(pid)

mid_slice = w.reconstruct('FBP_CUDA', projs[:,projs.shape[1]//2])

pl.imshow(mid_slice)
pl.savefig("reconstructed.png")


projs = foam_ct_phantom.load_projections('test_projs_noisy.h5')

pg = proj_geom.to_astra(single_slice=True)
vg = vol_geom.to_astra(single_slice=True)

pid = astra.create_projector('cuda', pg, vg)
w = astra.OpTomo(pid)

mid_slice = w.reconstruct('FBP_CUDA', projs[:,projs.shape[1]//2])

pl.imshow(mid_slice)
pl.savefig("reconstructed_noisy.png")


