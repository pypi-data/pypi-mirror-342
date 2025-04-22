import numpy as np
from .time_series_helpers import _var_nan_sum


def get_new_prototype_full_clipping(previous_prototype: np.ndarray, synced_series: list[np.ndarray],
                                    similarities: np.ndarray = None, learning_rate: float = 0.1) -> np.ndarray:
    """ This function calculates a new prototype

    The new prototype is calculated from the previous prototype, the other time series in the class and a vector of similarities (existing prototype -> all series in class)
    The new prototype will only be defined for indices where all the series in `synced_series` are defined.

    :param previous_prototype: Previous prototype to be updated and to which the scores were computed
    :param synced_series: List of all series in the dataset being 'averaged'
    :param similarities: Similarity scores (e.g. max value of ERAL) between each series in `synced_series` and `previous_prototype`
    :param learning_rate: rate of movement
    :return: new_prototype
    """

    return get_new_prototype_variable_clipping(previous_prototype, synced_series, similarities, learning_rate, alpha=0)


def get_new_prototype_variable_clipping(previous_prototype: np.ndarray, synced_series: list[np.ndarray],
                                        similarities: np.ndarray = None, learning_rate: float = 0.1,
                                        alpha=0.1) -> np.ndarray:
    """ This function calculates a new prototype

    The new prototype is calculated from the previous prototype, the other time series in the class and a vector of similarities (existing prototype -> all series in class)
    The new prototype will be defined for indices where `alpha` proportion of series in `synced_series` are defined.

    :param previous_prototype: Previous prototype to be updated and to which the scores were computed
    :param synced_series: List of all series in the dataset being 'averaged'
    :param similarities: Similarity scores (e.g. max value of eral) between each series in `synced_series` and `previous_prototype`
    :param learning_rate: rate of movement
    :param alpha: proportion of NaN values allowed
    :return: new_prototype
    """

    # Transform synced_series into a matrix
    synced_series: np.ndarray = np.vstack(synced_series)

    # Rename similarities to memberships
    memberships: np.ndarray = similarities

    assert synced_series.shape[0] == memberships.size
    assert synced_series.shape[1] == previous_prototype.size
    previous_prototype = previous_prototype.reshape(1, -1)
    memberships = memberships.reshape(-1)

    # Calculate the errors of each series to the previous prototype
    # N-by-M matrix, where N is the number of series and M is the length time series
    # NaN values wherever previous_prototype or synced_series are NaN
    errors: np.ndarray = synced_series - previous_prototype

    # Based on the memberships, calculate the weights of each series
    # N-by-1 vector
    # Should not contain NaN values, because memberships should not contain NaN values
    weights: np.ndarray = np.divide(memberships, np.sum(memberships)).reshape(-1, 1)

    # region moving the prototype where both it, and the synced series are defined
    # Multiply the errors by the weights
    # N-by-M matrix
    weighted_errors = np.multiply(errors, weights)

    # Aggregate the weighted errors for each index
    # M-by-1 vector
    weighted_errors_sum = _var_nan_sum(weighted_errors, axis=0, alpha=alpha)

    # Calculate the move (correction of the prototype)
    move: np.ndarray = weighted_errors_sum * learning_rate

    # Move the prototype
    new_prototype: np.ndarray = previous_prototype + move

    # endregion

    # region defining the prototype were the previous prototype is not defined, but the synced series are
    # Calculate the weighted average of the synced time series
    # M-by-1 vector
    # NaN values wherever more than `alpha` proportion of series in `synced_series` are NaN

    def _var_avg_with_weights(a: np.ndarray, weights: np.ndarray, alpha: float = 0.0) -> np.ndarray:
        """ Calculate the sum of a matrix along an axis, but allow alpha percentage of NaN values.

        At indices where the proportion is NaN values is less than alpha, perform the sum as usual.
        At indices where the proportion of NaN values is greater than alpha, return NaN.

        :param a: input matrix
        :param alpha: proportion of NaN values allowed
        :return: sum of `a` along `axis`
        """

        assert 0.0 <= alpha <= 1.0

        # We must recalculate the weights for each index, because for some indices, the input matrix (a) includes NaN
        # values and the weights of those rows which do not contain NaN values must be recalculated for that index

        weights = np.repeat(weights.reshape(-1, 1), a.shape[1], axis=1)
        assert weights.shape == a.shape
        weights[np.isnan(a)] = np.nan
        weights /= np.nansum(weights, axis=0)
        assert weights.shape == a.shape

        assert np.count_nonzero(np.isnan(weights)) == np.count_nonzero(np.isnan(a))

        # Calculate the weighted average
        # M-by-1 vector
        weighted_average = _var_nan_sum(np.multiply(a, weights), axis=0, alpha=alpha)

        return weighted_average

    weighted_average_of_synced_series: np.ndarray = _var_avg_with_weights(a=synced_series,
                                                                          weights=weights,
                                                                          alpha=alpha)

    # Apply the weighted average to the new prototype where the previous prototype is NaN
    # M-by-1 vector
    new_prototype[np.isnan(new_prototype)] = weighted_average_of_synced_series[np.isnan(new_prototype.reshape(-1))]
    # endregion

    return new_prototype


def get_new_prototype_no_clipping(previous_prototype: np.ndarray, synced_series: list[np.ndarray],
                                  similarities: np.ndarray = None, learning_rate: float = 0.1) -> np.ndarray:
    return get_new_prototype_variable_clipping(previous_prototype, synced_series, similarities, learning_rate,
                                               alpha=1.0)


def get_new_prototype_with_pruning(previous_prototype: np.ndarray, synced_series: list[np.ndarray],
                                   similarities: np.ndarray = None, learning_rate: float = 0.1,
                                   pruning_rate: float = 0.7) -> np.ndarray:
    """ Obtain a new prototype by pruning series which would shorten the resulting prototype

    The new prototype is calculated from the previous prototype, the other time series in the class and a vector of similarities (existing prototype -> all series in class)

    Since the new prototype is only defined at indices where all series in `synced_series` are defined, the new
     prototype will be shorter than the previous prototype. However, this shortening is recuded by pruning series in
     `synced_series` which would result in the biggest shortening of the prototype. As a restuls, the new prototype
     will be longer than the number of indices where all series in `synced_series` are defined.

    :param previous_prototype: Previous prototype to be updated and to which the scores were computed
    :param synced_series: List of all series in the dataset being 'averaged'
    :param similarities: Similarity scores (e.g. max value of eral) between each series in `synced_series` and `previous_prototype`
    :param learning_rate: rate of movement
    :param pruning_rate: Proportion of series to be pruned prior to calculating the new prototype
    :return: new_prototype
    """

    def resulting_length(a: np.ndarray, b: np.ndarray) -> int:
        """ Return the number of indices where both a and b are defined

        :param a: first input
        :param b: second input
        :return: length
        """
        return np.count_nonzero(np.logical_not(np.logical_or(np.isnan(a), np.isnan(b))))

    resulting_lengths = [resulting_length(previous_prototype, synced_series[i]) for i in range(len(synced_series))]

    # Sort the series by the resulting length
    sorted_synced_series: list[np.ndarray] = [x for _, x in
                                              sorted(zip(resulting_lengths, synced_series), key=lambda pair: pair[0],
                                                     reverse=True)]
    sorted_similarities: np.ndarray = np.array(
        [float(x) for _, x in sorted(zip(resulting_lengths, similarities), key=lambda pair: pair[0], reverse=True)])

    # Prune the series
    sorted_synced_series = sorted_synced_series[:int(len(sorted_synced_series) * pruning_rate)]
    sorted_similarities = sorted_similarities[:int(len(sorted_similarities) * pruning_rate)]

    # Calculate the new prototype
    new_prototype: np.ndarray = get_new_prototype_full_clipping(previous_prototype, sorted_synced_series,
                                                                sorted_similarities, learning_rate)

    return new_prototype
