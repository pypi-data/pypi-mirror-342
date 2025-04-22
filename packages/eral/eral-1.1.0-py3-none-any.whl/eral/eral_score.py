import numpy as np
from numba import jit


@jit(nopython=True)
def eral_score_with_normalization(x_original: np.ndarray, y_original: np.ndarray) -> tuple[
    np.ndarray, np.ndarray]:
    """ Compute ERAL but allow shifts thar result in only partial overlap of x and y. Normalize result by length of
    overlap.

    :param x: first time series
    :param y: second time series
    :return: error of alignment, normalization
    """
    # Make sure x and y are 1D arrays
    x = x_original.reshape(-1)
    y = y_original.reshape(-1)
    assert x.ndim == 1
    assert y.ndim == 1

    # Make sure x is longer than y
    flipped = False
    if len(x) < len(y):
        x, y = y, x
        flipped = True # If the inputs were flipped, the result must be flipped back.
        # We will be sliding the shorter series (now y) along x.
        # In the end, the result must be flipped back to match the original inputs.

    # Compute eral
    _eral = np.empty(len(x) + (len(y)-1)) # (len(y)-1) to account for the shifts that result in partial overlap

    l_overlap_len = len(y) - 1
    r_overlap_len = len(y) - 1
    central_len = len(x) - len(y) + 1

    x = np.concatenate((np.ones(l_overlap_len)*np.nan, x, np.ones(r_overlap_len)*np.nan))

    overlap_len_y = len(y)
    x_fragments = np.lib.stride_tricks.sliding_window_view(x, (overlap_len_y,))
    normalization = np.concatenate(
        (np.sqrt(np.arange(1,l_overlap_len+1, 1)), # start, stop, step arguments. For some reason they must not be keywords!
         np.ones(central_len)*np.sqrt(len(y)),
         np.sqrt(np.arange(r_overlap_len, 0, -1)))) # start, stop, step arguments. For some reason they must not be keywords!

    # This implementation is much slower than the one below:
    # diffs =  x_fragments - y # ta vrstica je počasna
    # _eral = np.sqrt(np.array([np.nansum(row**2) for row in diffs]))
    # Experimental results (v1 above, v2 below):
    # ------ v1 ------
    # 1x: 10pctl: 0.012s, 50pctl:0.012s, 90pctl: 0.719s, slowdown: 0.0x
    # 2x: 10pctl: 0.014s, 50pctl:0.015s, 90pctl: 0.016s, slowdown: 0.1x
    # 4x: 10pctl: 0.047s, 50pctl:0.048s, 90pctl: 0.051s, slowdown: 3.2x
    # 8x: 10pctl: 0.098s, 50pctl:0.106s, 90pctl: 0.123s, slowdown: 2.3x
    # 16x: 10pctl: 0.297s, 50pctl:0.301s, 90pctl: 0.306s, slowdown: 2.8x
    # 32x: 10pctl: 1.988s, 50pctl:2.011s, 90pctl: 2.036s, slowdown: 6.7x
    # ------ v2 ------
    # 1x: 10pctl: 0.018s, 50pctl:0.018s, 90pctl: 0.697s, slowdown: 0.0x
    # 2x: 10pctl: 0.023s, 50pctl:0.024s, 90pctl: 0.024s, slowdown: 0.1x
    # 4x: 10pctl: 0.051s, 50pctl:0.054s, 90pctl: 0.060s, slowdown: 2.4x
    # 8x: 10pctl: 0.107s, 50pctl:0.108s, 90pctl: 0.122s, slowdown: 2.0x
    # 16x: 10pctl: 0.289s, 50pctl:0.294s, 90pctl: 0.333s, slowdown: 2.7x
    # 32x: 10pctl: 0.927s, 50pctl:0.961s, 90pctl: 0.970s, slowdown: 3.1x

    _eral = np.sqrt(np.array([np.nansum((row-y)**2) for row in x_fragments])) # This is slower than the above two lines! But using this enables us to use numba, and therefore the overall function is faster.
    _eral = np.divide(_eral, normalization)

    if flipped:
        _eral = np.flip(_eral)

    return _eral, normalization


def eral_score(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    """ Compute ERAL but allow shifts thar result in only partial overlap of x and y. Normalize result by length of
    overlap.

    :param x: first time series
    :param y: second time series
    :return: error of alignment
    """
    return eral_score_with_normalization(x, y)[0]


def eral_lags(x_len: int, y_len: int) -> np.ndarray:
    """ Compute the lags for the ERAL function

    :param x_len: length of the first time series
    :param y_len: length of the second time series
    :return: lags
    """
    lags = np.arange(-y_len + 1, x_len, 1)

    return lags


def eral_score_min_with_exclusion_zone(eral: np.ndarray, exclusion_zone: float) -> int:
    """ Compute the minimum of the ERAL function with an exclusion zone

    :param eral: error of alignment
    :param exclusion_zone: exclusion zone
    :return: minimum of the ERAL function
    """
    if exclusion_zone > 0:
        # Exclude the forbidden shifts
        exclusion_zone = int(len(eral) * exclusion_zone)
        eral[:exclusion_zone] = np.inf
        eral[-exclusion_zone:] = np.inf

    return np.min(eral)
