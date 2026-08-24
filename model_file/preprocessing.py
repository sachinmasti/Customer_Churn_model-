from scipy.stats.mstats import  winsorize


def capping(x):
    cap = winsorize(x,limits=(0.05,0.05))
    return cap