import json
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
import folium
from shapely.geometry import Point, Polygon
import geopandas

def merger(f: pd.DataFrame, p: pd.DataFrame, h, l="None") -> pd.DataFrame:
    master_table = f.merge(p, on = l, how="h")
    return master_table

def selection(f: pd.DataFrame, L) -> pd.DataFrame:
    return f.dropna(subset = L)

def drop_duplica(f: pd.DataFrame, L) -> pd.DataFrame:
    return f[L].drop_duplicates()

def geo(f: pd.DataFrame) -> pd.DataFrame:
    f["geometry"] = f.apply(lambda x: Point(x["Long"], x["Lat"]), axis=1)
    f = geopandas.GeoDataFrame(f, geometry="geometry")
    return f