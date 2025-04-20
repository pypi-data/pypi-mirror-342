from mpl_toolkits.axes_grid1 import make_axes_locatable, inset_locator


def ufuk_cax(div, horizontal_size="7%",pad="2%", vertical_size="30%"):
    axins = div.append_axes("right",horizontal_size,
                           pad=pad)
    axins.set_visible(False)
    cax = inset_locator.inset_axes(axins, 
                               width="100%", 
                               height=vertical_size, 
                               loc="lower left",
                              borderpad=0)
    return cax


def ufuk_cbar_format(cbar, adjust_label=True):
    if adjust_label:
        cbar.ax.yaxis.label.set_horizontalalignment("center")
        cbar.ax.yaxis.label.set_verticalalignment("bottom")
        cbar.ax.yaxis.label.set_rotation(0)
        cbar.ax.yaxis.set_label_coords(.5,1, transform=cbar.ax.transAxes)
    cbar.set_ticks([cbar.vmin, cbar.vmax])

