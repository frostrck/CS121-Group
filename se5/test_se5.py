import sys
import os
import math

# Handle the fact that the test code may not
# be in the same directory as the solution code
sys.path.insert(0, os.getcwd())

import se5
import numpy as np

MODULE = "se5"

# # #
#
# HELPER FUNCTIONS
#
# # #

def pretty_print_repr(x):
    """
    A version of repr with some special casing.
    """
    if isinstance(x, np.ndarray):
        return "np." + repr(x)
    return repr(x)

def gen_recreate_msg(module, function, *params, **kwparams):


        
    params_str = ", ".join([pretty_print_repr(p) for p in params])
    if len(kwparams) > 0:
        params_str += ", ".join(["{} = {}".format(k, repr(v)) for k, v in kwparams.items()])


    recreate_msg = "To recreate this test in ipython3 run:\n"
    recreate_msg += "  {}.{}({})".format(module, function, params_str)

    return recreate_msg


def check_none(actual, recreate_msg=None):
    msg = "The function returned None."
    msg += " Did you forget to replace the placeholder value we provide?"
    if recreate_msg is not None:
        msg += "\n" + recreate_msg

    assert actual is not None, msg

def check_type(actual, expected, recreate_msg=None):
    actual_type = type(actual)
    expected_type = type(expected)

    msg = "The function returned a value of the wrong type.\n"
    msg += "  Expected return type: {}.\n".format(expected_type.__name__)
    msg += "  Actual return type: {}.".format(actual_type.__name__)
    if recreate_msg is not None:
        msg += "\n" + recreate_msg

    assert isinstance(actual, expected_type), msg

def check_dtype(array, expected, recreate_msg=None):
    actual_dtype = array.dtype
    expected_dtype = expected

    msg = "The function returned an array of the wrong dtype.\n"
    msg += "  Expected return dtype: {}.\n".format(expected_dtype)
    msg += "  Actual return dtype: {}.".format(actual_dtype)
    if recreate_msg is not None:
        msg += "\n" + recreate_msg

    assert actual_dtype == expected_dtype, msg

def check_array_equal(actual, expected, recreate_msg):
    msg = "The function returned the wrong array"
    msg += " Expected array: {}\n".format(expected)
    msg += " Actual returned array: {}\n".format(expected)

    if recreate_msg is not None:
        msg += "\n" + recreate_msg
    
    np.testing.assert_allclose(actual, expected,
                               err_msg = msg, verbose=False)
    
    
    # # #
#
# TEST HELPERS
#
# # #
def check_is_ndarray(actual, recreate_msg=None):
    check_type(actual, np.zeros(1), recreate_msg)
    


def test_compute_matching_values():

    x = np.array([1, 2, 3, 4])
    y = np.array([1, 5, 3, 2])

    recreate_msg = gen_recreate_msg(MODULE, 'compute_matching',
                                    x, y)
    
    result = se5.compute_matching(x, y)

    check_none(result, recreate_msg)
    check_is_ndarray(result, recreate_msg)
    check_dtype(result, np.bool, recreate_msg)
        
    
    check_array_equal(result, np.array([True, False, True, False]),
                      recreate_msg)

def test_compute_matching_indices():

    x = np.array([1, 2, 3, 4])
    y = np.array([1, 5, 3, 2])

    recreate_msg = gen_recreate_msg(MODULE, 'compute_matching_indices',
                                    x, y)
    
    result = se5.compute_matching_indices(x, y)

    check_none(result, recreate_msg)
    check_is_ndarray(result, recreate_msg)
    check_dtype(result, np.int, recreate_msg)
        
    
    check_array_equal(result, np.array([0, 2]),
                      recreate_msg)
    
def test_powers():

    for p in [1, 2, 4]:
        for N in [1, 2, 5, 10]:
            recreate_msg = gen_recreate_msg(MODULE, 'powers',
                                            N, p)
            
    
            result = se5.powers(N, p)

            check_none(result, recreate_msg)
            check_is_ndarray(result, recreate_msg)

            check_array_equal(result,
                              np.array([p**i for i in range(N)]),
                              recreate_msg)

def test_clip_values():

    x = np.linspace(0, 2, 10)
    x_orig = x.copy()

    ### Check for modification of input array
    recreate_msg = gen_recreate_msg(MODULE, 'clip_values',
                                    min_val=1, max_val=1.8)
    
    result = se5.clip_values(x, min_val=1, max_val=1.8)
    
    check_none(result, recreate_msg)
    check_is_ndarray(result, recreate_msg)

    assert np.allclose(x, x_orig), \
        "\n Input array was modified.\n\n" + recreate_msg

    
    ### Check what happens with no specification
    recreate_msg = gen_recreate_msg(MODULE, 'clip_values')

    result = se5.clip_values(x)
    
    check_none(result, recreate_msg)
    check_is_ndarray(result, recreate_msg)

    assert np.max(result) == np.max(x), \
    "\n The max value of the array was modified when max_val=None\n\n" \
        + recreate_msg
    
    assert np.min(result) == np.min(x), \
        "\n The min value of the array was modified when min_val=None\n\n" \
        + recreate_msg

    

    
    ### Check minimum value
    recreate_msg = gen_recreate_msg(MODULE, 'clip_values', min_val =1)

    result = se5.clip_values(x, min_val=1)
    
    check_none(result, recreate_msg)
    check_is_ndarray(result, recreate_msg)

    assert np.min(result) == 1.0,\
        "\n The minimum value of the array is not 1.0\n\n" \
        + recreate_msg

    


    ### Check maximum value
    recreate_msg = gen_recreate_msg(MODULE, 'clip_values', max_val =1)

    result = se5.clip_values(x, max_val=1)
    
    check_none(result, recreate_msg)
    check_is_ndarray(result, recreate_msg)

    assert np.max(result) == 1.0, \
        "\n The maximum value of the array is not 1.0\n\n" \
        + recreate_msg
    
    ### Check Both
    recreate_msg = gen_recreate_msg(MODULE, 'clip_values', min_val =1.0, max_val=1.5)

    result = se5.clip_values(x, min_val=1.0, max_val=1.5)
    
    check_none(result, recreate_msg)
    check_is_ndarray(result, recreate_msg)

    assert np.max(result) == 1.5, \
    "\n The maximum value of the array is not 1.5\n\n"\
        + recreate_msg

    assert np.min(result) == 1.0, \
    "\n The minimum value of the array is not 1.0\n\n"\
        + recreate_msg
        

def test_find_closest_value():

    def manual_closest_value(x, cv):
        closest_delta = 1e9
        closest_val = None
        for x_item in x:
            delta = abs(x_item - cv)

            if delta < closest_delta:
                closest_delta = delta
                closest_val = x_item
        assert closest_val is not None
        
        return closest_val
        
    
    x = np.array([1.0, 1.1, 1.2, 1.3, 1.4, 1.5])


    for cv in [1.1, 1.22, 1.28]:
        
        recreate_msg = gen_recreate_msg(MODULE, 'find_closest_value', 
                                        x, cv)

        result = se5.find_closest_value(x, cv)

        check_none(result, recreate_msg)

        expected_closest_val = manual_closest_value(x, cv)

        assert expected_closest_val == result, \
            "\n function returned {} as closest val ".format(result) \
            + "but we expected {}\n\n".format(expected_closest_val) \
            + recreate_msg


def test_select_row_col():
    x = np.arange(20).reshape(4, 5)

    def custom_get_cols(x, cols):
        out = np.stack([x[:, r] for r in cols], -1)
        return out
    
    def custom_get_rows(x, rows):
        out = np.stack([x[r] for r in rows])
        return out
    
        
    for tgt_cols in [[0], [1, 2, 3], [3, 2, 1], [2, 1, 3, 4, 0]]:

        recreate_msg = gen_recreate_msg(MODULE, 'select_row_col', x, False, tgt_cols)
        
        result = se5.select_row_col(x, False, tgt_cols)
    
        check_none(result, recreate_msg)
        check_is_ndarray(result, recreate_msg)

        expected_shape = (4, len(tgt_cols))
        assert result.shape == expected_shape, \
            "The shape of the returned array was {}, but".format(result.shape) \
            + " we expected {}\n\n".format(expected_shape) + recreate_msg

        expected_value = custom_get_cols(x, tgt_cols)

        check_array_equal(result, expected_value, 
                          recreate_msg)

        
    for tgt_rows in [[0], [1, 2, 3], [3, 2, 1], [2, 1, 3, 0]]:

        recreate_msg = gen_recreate_msg(MODULE, 'select_row_col', x, True, tgt_rows)
        
        result = se5.select_row_col(x, True, tgt_rows)
    
        check_none(result, recreate_msg)
        check_is_ndarray(result, recreate_msg)

        expected_shape = (len(tgt_rows), 5)
        assert result.shape == expected_shape, \
            "The shape of the returned array was {}, but".format(result.shape) \
            + " we expected {}\n\n".format(expected_shape) + recreate_msg

        expected_value = custom_get_rows(x, tgt_rows)

        check_array_equal(result, expected_value, 
                          recreate_msg)

        

    
