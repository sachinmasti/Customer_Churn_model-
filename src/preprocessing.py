from scipy.stats.mstats import winsorize


def capping(x):
    """
    Apply Winsorization to cap extreme outlier values in a numerical feature.
    
    Winsorization limits the extreme values of the input array to mitigate
    the effect of outliers during model training or prediction.
    
    Args:
        x (array-like): The input numerical data containing potential outliers.
        
    Returns:
        array-like: The Winsorized array with extreme values capped at the 5th and 95th percentiles.
    """
    # Cap values at the 5th and 95th percentiles (5% limits on both ends)
    cap = winsorize(x, limits=(0.05, 0.05))
    return cap