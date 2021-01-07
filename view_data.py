
import foam_ct_phantom
import numpy as np
import h5py
import astra
import matplotlib.pylab as pl
import argparse
import os
pl.gray()

parser = argparse.ArgumentParser()
parser.add_argument("--file",required=True)
args = parser.parse_args()

projs = foam_ct_phantom.load_projections(args.file)

print(len(projs), "projections, shape", projs.shape)
pl.imshow(projs[0])
pl.title("0")
pl.show()
pl.imshow(projs[10])
pl.title("10")
pl.show()
pl.imshow(projs[20])
pl.title("20")
pl.show()
