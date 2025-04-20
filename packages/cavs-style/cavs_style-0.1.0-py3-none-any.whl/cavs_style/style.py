from importlib.resources import files, as_file, read_binary
from pathlib import Path
import os
import cycler

from matplotlib import font_manager

from .colors import CAVS_cycle, CAVS_cycle_dark, CAVS_cubehelix, CAVS_colors



_font_paths = {os.path.splitext(os.path.basename(path))[0]:
         path for path in files("cavs_style.fonts").iterdir() 
         if os.path.splitext(path)[-1].lower() == ".ttf"}

for _fpath in _font_paths.values():
    font_manager.fontManager.addfont(os.fspath(_fpath))
         
         
CAVS_style = {"axes.prop_cycle":CAVS_cycle,
              "font.sans-serif":"Chivo",
              "mathtext.default":"regular",
              "figure.dpi":200, 
              "savefig.dpi":200,
              "savefig.transparent": True,
              "savefig.pad_inches": 0,
              "legend.fancybox": False,
              "image.cmap":"CAVS_blend"
              }

paper = {"font.size":10, "axes.linewidth":1}


dark = {"axes.prop_cycle":CAVS_cycle_dark,
           "text.color": CAVS_colors[3], 
           "savefig.transparent": False,
           "axes.facecolor":     CAVS_colors[1],
           "axes.edgecolor":     CAVS_colors[3],
           "axes.labelcolor":    CAVS_colors[3],
           "xtick.color": CAVS_colors[3],
           "ytick.color": CAVS_colors[3],
           "figure.facecolor":   CAVS_colors[1]}
                

single_column = {'figure.figsize':[3.5, 3.5*2/3]}

poster = {"font.size": 16,
         "axes.linewidth":     2}
