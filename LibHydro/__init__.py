#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LibHydro
"""

__author__ = "François Métivier"
__copyright__ = "Copyright 2025"
__license__ = "CC-By-4.0"
__version__ = "1.0"

__all__ = [
    "LibHydro",
    "meteo_piezo",
    "maps",
    "flownets",
    "lib_book",
    "wells"
]

#############################
#
# Librairies
#
#############################

import pyFreeFem as pyff

import numpy as np
import time
import geopandas
import pandas

# from osgeo import gdal
# from osgeo import ogr
import cartopy.crs as ccrs
import cartopy.io.shapereader as shapereader

import glob
import shapely as shp

import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.patches import Rectangle
from mpl_toolkits.axes_grid1 import make_axes_locatable
from mpl_toolkits.mplot3d import Axes3D

import triangle as tr

from scipy.interpolate import griddata
from scipy.interpolate import RegularGridInterpolator
from scipy.sparse.linalg import spsolve

from copy import deepcopy

from meteo_piezo import *
from maps import *
from lib_book import *
from flownets import *
from wells import *


if __name__ == '__main__':
    pass
