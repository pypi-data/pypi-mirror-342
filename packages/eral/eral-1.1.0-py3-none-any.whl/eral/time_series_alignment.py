import numpy as np
from .time_series_helpers import _check_nan_padding, _remove_nan_padding
from .eral_score import eral_score
from scipy.signal import correlate, correlation_lags


def get_score_and_shift(in1: np.ndarray, in2: np.ndarray, apply_zero_mean: bool = True, exclusion_zone: float = 0.0) -> tuple[float, int]:
    """ Helper function returning the eral score and calculated lag for two time series

    :param in1: first time series (passed to `scipy.signal.correlate` as first argument). May include NaNs.
    :param in2: second time series (passed to `scipy.signal.correlate` as second argument). May include NaNs.
    :param apply_zero_mean: If `True`, zero mean will be applied to both time series
    :param exclusion_zone: Proportion of forbidden shifts. Eg. 0.1 means that the optimal shift can not be in the first or last 10% of the time series.
    :return: First output: eral score (the highest value accross all lags); Second argument: optimal lag (at highest eral score)
    """

    if not 0 <= exclusion_zone < 0.5:
        raise ValueError("exclusion_zone must be between 0 and 0.5")


    in1_diff = in2_diff = None
    corr_diff = lags_diff = None

    # region Handle NaNs
    _check_nan_padding(in1, in2)
    in1_nan_left_padding_count = in2_nan_left_padding_count = 0
    for x in in1:
        if np.isnan(x):
            in1_nan_left_padding_count += 1
        else:
            break
    for x in in2:
        if np.isnan(x):
            in2_nan_left_padding_count += 1
        else:
            break
    in1, in2 = _remove_nan_padding(in1, in2)
    # endregion

    # Apply zero mean
    if apply_zero_mean:
        # check if in1 has nans
        if np.isnan(in1).any():
            in1 = in1 - np.nanmean(in1)
        else:
            in1 = in1 - np.mean(in1)

        # check if in2 has nans
        if np.isnan(in2).any():
            in2 = in2 - np.nanmean(in2)
        else:
            in2 = in2 - np.mean(in2)

    _eral = eral_score(in1, in2)
    old_settings = None
    if np.min(_eral) == 0:
        old_settings = np.seterr(divide='ignore')  # _eral can be 0 if the two signals are identical.
        # This would cause a division by zero warning, which is not necessary.
    corr = 1 / _eral
    if old_settings is not None:
        np.seterr(**old_settings)

    lags = correlation_lags(len(in1), len(in2), 'full')  # eral uses the same lags as 'full'
    assert len(corr) == len(lags)

    if exclusion_zone > 0:
        # Exclude the forbidden shifts
        exclusion_zone = int(len(corr) * exclusion_zone)
        corr[:exclusion_zone] = 0
        corr[-exclusion_zone:] = 0

    # We must account for the left padding of NaN values when returning the lag
    argmax = np.argmax(corr)
    return corr[argmax], lags[argmax] + in1_nan_left_padding_count - in2_nan_left_padding_count
    # return np.max(corr), lags[np.argmax(corr)] # + in1_nan_left_padding_count - in2_nan_left_padding_count


def _get_optimal_shift_for_two_series(in1: np.ndarray, in2: np.ndarray):
    """ Helper function returning the optimal shift for two time series

    Does not use circular padding, and does not use diff for lag calculation

    :param in1: first time series (passed to `scipy.signal.correlate` as first argument)
    :param in2: second time series (passed to `scipy.signal.correlate` as second argument)
    :param mode: mode of signal alignment (`full`, `valid`, `eral`)
    :return: optimal shift
    """
    return get_score_and_shift(in1, in2)[1]


def sync_2_series(in1: np.ndarray, in2: np.ndarray, shift: int | None = None) -> tuple[
    np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """ Helper function to synchronize two time series by shifting the second one

    :param in1: The 'background' time series - is stationary
    :param in2: The 'foreground' time series - is shifted according to the `shift` parameter
    :param shift: The number of samples `in2` should be shifted. Positive = shift 'right'; Negative = shift 'left'. If `None`, the optimal shift will be calculated.
    :param mode: `mode` used in aligning the time series (`full`, `valid`, `eral`)
    :return: [0] -> new indices for in1;
             [1] -> shifted in1;
             [2] -> new indices for in2;
             [3] -> shifter in2
    """

    if shift is None:
        shift = _get_optimal_shift_for_two_series(in1, in2)

    signal_2_shifted = np.ones(np.abs(shift) + len(in2)) * np.nan
    signal_1_shifted = np.ones(np.abs(shift) + len(in1)) * np.nan
    if shift < 0:
        shifted_indices_1 = range(-np.abs(shift), len(in1))
        shifted_indices_2 = range(-np.abs(shift), len(in2))
        signal_2_shifted[0:len(in2)] = in2
        signal_1_shifted[np.abs(shift):] = in1
    else:
        shifted_indices_1 = range(0, len(signal_1_shifted))
        shifted_indices_2 = range(0, len(signal_2_shifted))
        signal_2_shifted[np.abs(shift):] = in2
        signal_1_shifted[0:len(in1)] = in1

    return shifted_indices_1, signal_1_shifted, shifted_indices_2, signal_2_shifted


def sync_n_series(series: list[np.ndarray], shifts: list[int]) -> tuple[np.ndarray, list[np.ndarray]]:
    """ Shift all series in `series` by `shifts` samples

    :param series: A list of time series to be shifted
    :param shifts: The shifts (a list of integers)
    :return: [0] -> new common indices for all series;
             [1] -> list shifted series. np.nan where series has no value.
    """
    output_series: list[np.ndarray] = []

    time_start: int = np.min(shifts)
    time_end: int = np.max(np.array(shifts) + np.array(list(map(lambda x: len(x), series)))).__int__()
    output_time: np.ndarray = np.array(list(range(time_start, time_end)))

    for i in range(len(shifts)):
        ser: np.ndarray = series[i]
        shift: int = shifts[i]
        shifted: np.ndarray = np.ones(len(output_time)) * np.nan
        shifted[shift - time_start:shift - time_start + len(ser)] = ser
        output_series.append(shifted)

    return output_time, output_series


def sync_n_series_to_prototype(prototype: np.ndarray, series: list[np.ndarray], shifts: list[int] = None, exclusion_zone: float = 0.0) -> tuple[
    np.ndarray, list[np.ndarray], np.ndarray]:
    """ Shift all series in `series` by `shifts` samples and align them to the prototype

    :param prototype: The prototype to which all series should be aligned
    :param series: A list of time series to be shifted
    :param shifts: The shifts (a list of integers). If `None`, the optimal shifts will be calculated.
    :return: [0] -> new common indices for all series;
             [1] -> list shifted series. np.nan where series has no value.
             [2] -> shifted prototype
    """

    if shifts is None:
        shifts = [get_score_and_shift(prototype, ser, exclusion_zone=exclusion_zone)[1] for ser in series]

    # We will use sync_n_series which takes a list of time series and allignes them according to the shifts.
    # We pass the prototype as the first series in the list, and add it the shift of 0.
    temp_data = [prototype]
    temp_data.extend(series)
    temp_shifts = [0]
    temp_shifts.extend(shifts)

    synced_time, synced_data = sync_n_series(series=temp_data, shifts=temp_shifts)

    # First synced_data is the prototype
    return synced_time, synced_data[1:], synced_data[0]
