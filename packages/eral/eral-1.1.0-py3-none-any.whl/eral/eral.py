import numpy as np
import warnings
from matplotlib import pyplot as plt

from .time_series_alignment import sync_n_series, get_score_and_shift


def single_iteration(prototype: np.ndarray, class_segments: list[np.ndarray], learning_rate: float,
                     previous_t: np.ndarray, prototyping_function=None,
                     exclusion_zone: float = 0.0) -> tuple[
    np.ndarray, np.ndarray]:
    """ Perform a single iteration of prototype generation

    Given the previous prototype, the class segments and the learning rate, calculate the new prototype and the new
    time indices for the prototype.

    The new prototype is calculated using the prototyping_function, which must be specified. The prototyping_function
    must have the following signature:
    previous_prototype: np.ndarray, synced_series: list[np.ndarray], similarities: np.ndarray, learning_rate: float -> np.ndarray

    :param prototype: Previous prototype
    :param class_segments: List of time series in the class
    :param learning_rate: Learning rate
    :param previous_t: Previous time indices for the prototype
    :param use_diff_for_lags: If True, diff(signal) will be used to determine the lag
    :param prototyping_function: Function to be used to generate the new prototype
    :return: [0] -> new prototype; [1] -> new time indices for the prototype

    """
    scores_and_shifts: list[tuple[float, int]] = [
        get_score_and_shift(prototype, segment,
                            exclusion_zone=exclusion_zone, apply_zero_mean=False) for segment in class_segments]
    scores: list[float] = [x[0] for x in scores_and_shifts]
    shifts: list[int] = [x[1] for x in scores_and_shifts]

    temp = [prototype]
    temp.extend(class_segments)
    ts = [0]
    ts.extend(shifts)
    t_synced, synced_series = sync_n_series(temp, ts)

    # Check for validity of the sync
    # Synced series are stacked into a matrix, and then the sum of each column is calculated.
    # If all columns sum up to NaN, this means thath the next prototype will be all NaN, and the algorithm should stop.
    if np.count_nonzero(np.isnan(np.sum(np.vstack(synced_series), axis=0))) == len(t_synced):
        return prototype, previous_t

    # Transform scores into similarities
    # If any scorr score is infinite (can occur when using eral mode), it is replaced with a large value
    similarities = np.ones(len(scores)).reshape(-1, 1)
    # similarities = np.array(scores).reshape(-1, 1)
    # max_not_inf = np.max(similarities[np.isfinite(similarities)])
    # if max_not_inf <= 0:
    #     max_not_inf = 1
    # similarities = np.nan_to_num(similarities, posinf=max_not_inf * 3)

    # Call to prototyping function to obtain the new prototype
    new_prototype: np.ndarray = prototyping_function(previous_prototype=synced_series[0],
                                                     synced_series=synced_series[1:],
                                                     similarities=similarities,
                                                     learning_rate=learning_rate).reshape(-1)
    return new_prototype, t_synced


def obtain_prototype(class_segments: list[np.ndarray],
                     initial_prototype: np.ndarray | int | None = None,
                     max_iterations: int = 10,
                     learning_rate: float = 0.3,
                     min_length: int = -1,
                     prototyping_function=None,
                     exclusion_zone: float = 0.0,
                     min_rmse: float|None = 0.0) -> np.ndarray | None:
    """ Generate prototype from class segments

    Perform several iterations of prototype generation. In each iteration, the prototype is generated using the
    prototyping_function, which must be specified. The prototyping_function must have the following signature:
    previous_prototype: np.ndarray, synced_series: list[np.ndarray], similarities: np.ndarray, learning_rate: float -> np.ndarray

    The learning rate is constant across all iterations. It defines the rate at which the prototype is updated and moved
    towards the training samples.

    This function supports plotting, if ax_series and ax_final are specified.

    :param class_segments: List of time series in the class
    :param initial_prototype: Initial prototype. If None, a random segment will be selected from the class segments
    :param max_iterations: Maximum number of iterations
    :param learning_rate: Learning rate
    :param use_diff_for_lags: If True, diff(signal) will be used to determine the lag
    :param min_length: Minimum length of the prototype. If the prototype is shorter than this, the algorithm will stop
    :param prototyping_function: Function to be used to generate the new prototype. See `alignment_prototyping_functions.py` for examples`
    :param use_eral: If True, the eral mode will be used
    :param exclusion_zone: Exclusion zone
    :param min_rmse: Minimum RMSE. If the RMSE of prototype change is lower than this, the algorithm will stop. If None, will use 1% of data range.
    :return: The final prototype
    """

    assert type(class_segments) is list
    if len(class_segments) == 0:
        raise Exception("No class segments provided")
    if len(class_segments) == 1:
        return class_segments[0]

    if initial_prototype is None:
        all_sample_indices = list(range(len(class_segments)))
        while len(all_sample_indices) > 0:
            initial_prototype_idx = all_sample_indices[0]
            all_sample_indices.pop(0)
            prototype = obtain_prototype(class_segments, initial_prototype=initial_prototype_idx,
                                         max_iterations=max_iterations, learning_rate=learning_rate,
                                         min_length=min_length,
                                         prototyping_function=prototyping_function,
                                         exclusion_zone=exclusion_zone,
                                         min_rmse=min_rmse)
            if prototype is not None:
                return prototype
        warnings.warn("Could not find a prototype, returning the first segment")
        return class_segments[0]

    elif type(initial_prototype) is int:
        prototype = class_segments[initial_prototype]
    else:
        prototype = initial_prototype


    if prototyping_function is None:
        raise Exception("prototyping_function must be specified, it must be a function with the following signature: "
                        "previous_prototype: np.ndarray, synced_series: list[np.ndarray], similarities: np.ndarray, "
                        "learning_rate: float -> np.ndarray. "
                        "See `alignment_prototyping_functions.py` "
                        "for examples")


    if min_rmse is None:
        data_range = np.max([np.max(segment) for segment in class_segments]) - np.min([np.min(segment) for segment in class_segments])
        min_rmse = 0.01 * data_range

    t_synced = np.arange(0, len(prototype))
    for i in range(max_iterations):
        new_prototype, t_synced = single_iteration(prototype, class_segments, learning_rate, t_synced,
                                                   prototyping_function=prototyping_function,
                                                   exclusion_zone=exclusion_zone)

        if np.count_nonzero(np.isnan(new_prototype)) == len(new_prototype):
            raise Exception("Prototype is all nan!")

        if min_length > 0 and np.count_nonzero(np.logical_not(np.isnan(new_prototype))) < min_length:
            if i == 0:
                return None
            else:
                break

        # Todo: Add a stopping criterion based on the change in the prototype
        if len(prototype) == len(new_prototype):
            if np.all(prototype == new_prototype):
                break

        if len(prototype) == len(new_prototype):
            rmse = np.sqrt(np.nanmean((prototype - new_prototype) ** 2))
            if rmse < min_rmse:
                break
        else:
            pass


        prototype = new_prototype
    return prototype

