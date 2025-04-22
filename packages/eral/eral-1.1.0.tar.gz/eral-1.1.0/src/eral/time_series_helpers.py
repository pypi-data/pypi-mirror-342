import numpy as np

def _check_nan_padding(a: np.ndarray, b: np.ndarray) -> bool:
    # assert time series are only NaN-padded at the beginning and the end, there are no NaN values in between
    test = lambda ts, start_nan, end_nan: np.count_nonzero(np.diff(np.isnan(ts))) == int(start_nan) + int(end_nan)
    assert len(a) > 0, "Input array is empty"
    assert len(b) > 0, "Input array is empty"
    return test(a, np.isnan(a[0]), np.isnan(a[-1])) and test(b, np.isnan(b[0]), np.isnan(b[-1]))


def _remove_nan_padding_single(a: np.ndarray) -> np.ndarray:
    """ Remove all NaN values from series"""
    a = a[np.logical_not(np.isnan(a))]
    return a

def _remove_nan_padding(a: np.ndarray, b: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """ Remove NaN values from two time series"""
    a = _remove_nan_padding_single(a)
    b = _remove_nan_padding_single(b)
    return a, b


def _var_nan_sum(a: np.ndarray, axis: int = 0, alpha: float = 0.0) -> np.ndarray:
    """ Calculate the sum of a matrix along an axis, but allow alpha percentage of NaN values.

    At indices where the proportion is NaN values is less than alpha, perform the sum as usual.
    At indices where the proportion is NaN values is greater than alpha, return NaN.

    :param a: input matrix
    :param axis: axis along which to sum
    :param alpha: proportion of NaN values allowed
    :return: sum of `a` along `axis`
    """

    assert 0.0 <= alpha <= 1.0
    assert 0 <= axis < len(a.shape)

    # Calculate the number of NaN values along the axis
    nans = np.isnan(a)
    nans = np.sum(nans, axis=axis)

    # Calculate the proportion of NaN values along the axis
    nans = np.divide(nans, a.shape[axis])

    # Calculate the sum of `a` along `axis`
    s = np.nansum(a, axis=axis)

    # Replace the sum with NaN where the proportion of NaN values is greater than alpha
    s[nans > alpha] = np.nan

    return s