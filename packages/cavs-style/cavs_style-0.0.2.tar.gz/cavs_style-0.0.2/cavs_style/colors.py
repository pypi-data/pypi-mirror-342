from seaborn import blend_palette, color_palette, diverging_palette, light_palette, dark_palette
from colorsys import rgb_to_hls
from matplotlib.colors import hex2color

import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib import colormaps

register = colormaps.register

from cycler import cycler

import os
import glob

from configparser import ConfigParser


from importlib.resources import files, as_file, read_binary


CAVS_colors = {1:"#00164E", 2:"#33CB9C", 3:"#F9F9F9"}


def get_CAVS_cmap(palette_type="blend", n_colors=6, as_cmap=True):
    """
    create a CAVS color styled colormap or color series
    
    """
    
    if palette_type=="blend":
        return blend_palette(colors=[CAVS_colors[1], CAVS_colors[2]], 
                n_colors=n_colors, 
                as_cmap=as_cmap)
    if palette_type=="diverging":
        return blend_palette(colors=[CAVS_colors[1],
                                     CAVS_colors[3], 
                                     CAVS_colors[2]], 
                                     n_colors=n_colors, 
                                     as_cmap=as_cmap)

    if palette_type=="main":
        return light_palette(CAVS_colors[1],
                             n_colors=n_colors, 
                             as_cmap=as_cmap)
    
    if palette_type=="secondary":
        return light_palette(CAVS_colors[2],
                             n_colors=n_colors, 
                             as_cmap=as_cmap)





bitmap_cmap_conf = ConfigParser()
bitmap_cmap_conf.read(files("cavs_style").joinpath("bitmap_cmaps.conf"))


def get_Bitmap_cmap(name):
    vals = [[float(e.strip()) for e in row.split(",")] for row in bitmap_cmap_conf["BITMAP_CMAP"][name].split("\n")]
    return LinearSegmentedColormap.from_list(name, vals)


for name  in bitmap_cmap_conf["BITMAP_CMAP"].keys():
    cmap = get_Bitmap_cmap(name)
    cmap_name = "CAVS_"+name

    register(cmap, name=cmap_name)
    locals()[cmap_name] = cmap


CAVS_blend = get_CAVS_cmap("blend")
register(CAVS_blend, name="CAVS_blend")

CAVS_diverging = get_CAVS_cmap("diverging")
register(CAVS_diverging, name="CAVS_diverging")

CAVS_main = get_CAVS_cmap("main")
register(CAVS_main, name="CAVS_main")


CAVS_secondary = get_CAVS_cmap("secondary")
register(CAVS_secondary, name="CAVS_secondary")


CAVS_cubehelix = LinearSegmentedColormap.from_list("CAVS_cubehelix", ['#11263A', '#12263B', '#13263C', '#14263D', '#14263E', '#15263F', '#16263F', '#162640', '#172641', '#182642', '#192743', '#1A2743', '#1A2744', '#1B2745', '#1C2746', '#1D2746', '#1E2747', '#1F2748', '#1F2748', '#202749', '#21274A', '#22274A', '#23274B', '#24274C', '#25274C', '#26274D', '#27274D', '#28274E', '#29274E', '#2A274F', '#2B274F', '#2C2750', '#2D2750', '#2E2751', '#2F2751', '#302752', '#312752', '#322753', '#332753', '#342753', '#352754', '#362754', '#372754', '#382755', '#392755', '#3A2755', '#3B2755', '#3C2756', '#3D2756', '#3E2756', '#3F2756', '#402856', '#412856', '#422856', '#432857', '#442857', '#452857', '#462857', '#472857', '#482857', '#492857', '#4A2857', '#4B2857', '#4C2857', '#4D2857', '#4E2957', '#4F2956', '#502956', '#512956', '#522956', '#532956', '#542956', '#552A55', '#562A55', '#572A55', '#582A55', '#592A55', '#5A2B54', '#5B2B54', '#5B2B54', '#5C2B53', '#5D2B53', '#5E2C53', '#5F2C52', '#602C52', '#602C52', '#612D51', '#622D51', '#632D51', '#632E50', '#642E50', '#652E4F', '#662E4F', '#662F4F', '#672F4E', '#682F4E', '#68304D', '#69304D', '#6A314C', '#6A314C', '#6B314B', '#6B324B', '#6C324A', '#6C334A', '#6D3349', '#6D3349', '#6E3448', '#6E3448', '#6F3547', '#6F3547', '#703646', '#703646', '#703745', '#713745', '#713844', '#713844', '#723943', '#723943', '#723A42', '#733B42', '#733B41', '#733C41', '#733C40', '#743D40', '#743D40', '#743E3F', '#743F3F', '#743F3E', '#74403E', '#74413D', '#74413D', '#75423C', '#75423C', '#75433C', '#75443B', '#75443B', '#75453A', '#75463A', '#75463A', '#754739', '#744839', '#744939', '#744938', '#744A38', '#744B38', '#744B37', '#744C37', '#744D37', '#734E37', '#734E36', '#734F36', '#735036', '#735136', '#725136', '#725235', '#725335', '#725435', '#715435', '#715535', '#715635', '#705735', '#705735', '#705835', '#6F5935', '#6F5A35', '#6F5B35', '#6E5B35', '#6E5C35', '#6E5D35', '#6D5E35', '#6D5E35', '#6D5F35', '#6C6036', '#6C6136', '#6B6236', '#6B6236', '#6B6336', '#6A6437', '#6A6537', '#696537', '#696637', '#696738', '#686838', '#686838', '#676939', '#676A39', '#666B3A', '#666B3A', '#666C3A', '#656D3B', '#656E3B', '#646E3C', '#646F3C', '#64703D', '#63703D', '#63713E', '#62723F', '#62723F', '#627340', '#617440', '#617541', '#607542', '#607642', '#607643', '#5F7744', '#5F7844', '#5F7845', '#5E7946', '#5E7A47', '#5E7A48', '#5D7B48', '#5D7C49', '#5D7C4A', '#5C7D4B', '#5C7D4C', '#5C7E4D', '#5C7E4D', '#5B7F4E', '#5B804F', '#5B8050', '#5B8151', '#5B8152', '#5A8253', '#5A8254', '#5A8355', '#5A8356', '#5A8457', '#5A8458', '#598559', '#59855A', '#59865B', '#59865C', '#59865D', '#59875E', '#59875F', '#598860', '#598861', '#598962', '#598963', '#598965', '#598A66', '#598A67', '#598A68', '#598B69', '#598B6A', '#598B6B', '#5A8C6C', '#5A8C6D', '#5A8C6E', '#5A8D70', '#5A8D71', '#5A8D72', '#5B8E73', '#5B8E74', '#5B8E75', '#5B8E76'])
register(CAVS_cubehelix, name="CAVS_cubehelix")




CAVS_cycle_list =[CAVS_colors[1], 
                  '#5a009c', 
                  '#9c0059', 
                  '#9c2d00', 
                  '#859c00', 
                  '#009c01', 
                  '#009c86']
 

CAVS_cycle_list_dark = CAVS_cycle_list[1:] + [  CAVS_colors[3]]                     

CAVS_cycle = cycler("color",CAVS_cycle_list)
CAVS_cycle_dark = cycler("color",CAVS_cycle_list_dark)
                               
                               


