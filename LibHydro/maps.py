import matplotlib.pyplot as plt
from matplotlib import rcParams
from scipy.interpolate import griddata
import cartopy.crs as ccrs
import cartopy.feature as ft
from owslib.wmts import WebMapTileService
import folium
from pykml import parser
import pandas as pd
import cartopy.io.img_tiles as cimgt
# import osrm
import json
import glob
import numpy as np

from sqlalchemy import create_engine

###############################################################################
#
# Simple and useful mapping routines, especially for sampling locations
#
###############################################################################

def global_loc(cl = -180 , loc_point=(-15.103,-147.68)):
    """Simple location map using cartopy. Location on globe using orthographic projection
    Default location corrresponds to Rangiroa atoll in French Polynesia

    Parameters
    ----------
    cl : int, optional
        central longitude, by default -180
    loc_point : tuple, optional
        Location position (lat,lon), by default (-15.103,-147.68)
    """
    fig = plt.figure(figsize=(10, 10))

    pr = ccrs.Orthographic(central_longitude=cl)
    ax = fig.add_subplot(111, projection=pr)
    # ~ ax=fig.add_subplot(111,projection=ccrs.Orthographic(central_longitude=47,central_latitude=-19))
    # in the case of world maps you can use the predefined datasets of NaturalEarth

    ax.stock_img()
    # ~ ax.add_feature(ft.LAND)
    # ~ ax.add_feature(ft.OCEAN)
    ax.add_feature(ft.LAKES)
    ax.add_feature(ft.RIVERS)
    ax.add_feature(ft.BORDERS, linestyle="--", edgecolor="gray", linewidth=0.5)
    ax.coastlines()

    ex = ax.get_extent(crs=ccrs.Geodetic())

    ax.plot(loc_point[1], loc_point[0], marker='o', ms=12, color="C3", transform=ccrs.Geodetic())

    ax.gridlines(
        draw_labels=True,
        dms=True,
        x_inline=False,
        y_inline=False,
        color="blue",
        linestyle="dashed",
    )

    # ~ ax.set_extent((-50,100,-80,80))
    # ax.set_extent((-10, 55, -40, 60))

    plt.savefig("./travel.png", bbox_inches="tight")

if __name__ == "__main__":
    global_loc()