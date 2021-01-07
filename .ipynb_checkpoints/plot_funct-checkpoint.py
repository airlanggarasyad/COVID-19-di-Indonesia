import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import matplotlib.colors as mcolors
import matplotlib.font_manager as fm
import warnings
from IPython.display import display, HTML
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

init_notebook_mode(connected=True)

display(HTML("""
<style>
.output {
    display: flex;
    align-items: center;
    text-align: center;
}
</style>
"""))

warnings.filterwarnings('ignore')
sf_med = fm.FontProperties(fname='sf_medium.otf')

def make_colormap(seq):
    """Return a LinearSegmentedColormap
    seq: a sequence of floats and RGB-tuples. The floats should be increasing
    and in the interval (0,1).
    """
    seq = [(None,) * 3, 0.0] + list(seq) + [1.0, (None,) * 3]
    cdict = {'red': [], 'green': [], 'blue': []}
    for i, item in enumerate(seq):
        if isinstance(item, float):
            r1, g1, b1 = seq[i - 1]
            r2, g2, b2 = seq[i + 1]
            cdict['red'].append([item, r1, r2])
            cdict['green'].append([item, g1, g2])
            cdict['blue'].append([item, b1, b2])
    return mcolors.LinearSegmentedColormap('CustomMap', cdict)

def chloropleth(to_plot, COLOR, title, var):
    fig = plt.figure()
    vmin, vmax = to_plot[var].min(), to_plot[var].max()
    
    # plt.suptitle(title, fontsize = 25, fontproperties = sf_med)
    
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis('off')
    fig.set_facecolor("#ffffff")
    fig.patch.set_facecolor("#ffffff")
    
    ax.axis('off')
    ax.margins(0)
    ax.apply_aspect()
    
    bbox = ax.get_window_extent().inverse_transformed(fig.transFigure)
    w,h = fig.get_size_inches()
    fig.set_size_inches(w * bbox.width, h * bbox.height)
    
    to_plot.plot(column = var, cmap = COLOR, linewidth = 0.3, ax = ax, edgecolor = '0.8')
    
def top10_plot(parameter_to_plot, YLABEL, COLOR):
    ax = (parameter_to_plot[0:10].plot.bar(color = COLOR, figsize = (8,5)))
    
    # y-axis' setting
    ax.set_ylabel(YLABEL)
    ax.set_xlabel("")

    # x-axis' setting
    ax.set_axisbelow(True)
    ax.set_xticklabels(parameter_to_plot.index[:10], rotation=60)
    
    ax.grid()
    
    return ax

def top10_plot(df, param_to_plot, COLOR):
    
    fig, ax = plt.subplots()
    ax.set_axisbelow(True)
    ax.grid()
    ax.tick_params(axis=u'both', which=u'both',length=0)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_visible(True)
    ax.get_xaxis().set_major_formatter(mtick.FuncFormatter(lambda x, p: format(int(x)/1000)))
    ax.set_xlabel('Jumlah (Dalam Ribuan)')
    
    plt.barh(df.index, df[param_to_plot], color = COLOR)
    plt.setp( ax.xaxis.get_majorticklabels(), ha="right" )

    r = ax.set_yticklabels(df.index, ha = 'left')
    fig.set_size_inches(6, 4, forward=True)

    plt.draw()
    yax = ax.get_yaxis()
    yax.set_tick_params(pad=123)

c = mcolors.ColorConverter().to_rgb