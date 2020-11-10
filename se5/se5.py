import numpy as np


def compute_matching(x, y):
    """
    Returns a new array which is "true" everywhere x == y and 
    false otherwise. 

    Note this is simply the Numpy version of the same function
    in SE2 but should be substantially simpler. 

    Input:
        x: n-dimensional array
        y: n-dimensional array

    Returns: Boolean-valued n-dimensional array with the same shape as 
             x and y
    """

    pass


def compute_matching_indices(x, y):
    """
    Returns a new array consisting of the indices where
    x == y. 

    Note this is simply the Numpy version of the same function
    in SE2 but should be substantially simpler. 

    Input: 
        x: 1-dimensional array
        y: 1-dimensional array

    Returns: a sorted array of the indices where x[i] == y[i]

    Note that the returned array must be one-dimensional! 

    """

    pass


def powers(N, p):
    """
    Return the first N powers of p. For example:
    powers(5, 2) --> [1, 2, 4, 8, 16]
    powers(5, 4) --> [1, 4, 16, 64, 256]

    Input:
       N: number of powers to return 
       p: base that we are raising to the given powers
    
    Returns: an array consisting of powers of p
    """

    pass


def clip_values(x, min_val=None, max_val=None):
    """
    Return a new array with the values clipped. 

    If min_val is set, all values < min_val will be set to min_val
    If max_val is set, all values > max_val will be set to max_val

    Remember to return a new array, NOT to modify the input array. 

    Inputs: 
        x: the n-dimensional array to be clipped
        min_val : the minimum value in the returned array (if not None)
        max_val : the maximum value in the returned array (if not None)

    returns: an array with the same dimensions of X with values clipped
             to (min_val, max-val)

    """

    pass


def find_closest_value(x, tgt_value):
    """
    Returns the value in the one-dimensional array x
    that is closest to target_value. 

    Examples:
    find_closest_value(np.array([1.0, 1.5, 2.0]), 1.7) -> 1.5
    find_closest_value(np.array([1.0, 1.5, 2.0]), 1.8) -> 2.0

    Inputs: 
        x: 1-dimensional array of values

    Returns: scalar value in x closest to tgt_value

    """

    pass


def select_row_col(x, is_row, tgt):
    """
    Select a subset of rows or columns in the 
    two-dimensional array x. 

    Inputs:
        x: input two-dimensional array 
        is_row: boolean which is true if we are selecting rows
                and false if we are selecting columns. 
        tgt: a list of integers indicating which rows or columns
             we are selecting

    Returns: a two-dimensional array where we have selected either
         the rows or columns as requested
    """

    pass

