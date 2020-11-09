'''
Helper functions for the test code
'''

import os
import json
import pytest

from util import sort_count_pairs

# keep lint quiet on test code.
#pylint: disable-msg=consider-using-ternary

BASE_DIR = os.path.dirname(__file__)
TEST_DIR = os.path.join(BASE_DIR, "tests")

def read_config_file(filename):
    '''
    Load the test cases from a JSON file.

    Inputs:
      filename (string): the name of the test configuration file.

    Returns: (list) test cases
    '''

    full_path = os.path.join(TEST_DIR, filename)
    try:
        with open(full_path) as f:
            return json.load(f)
    except FileNotFoundError:
        msg = ("Cannot open file: {}.\n"
               "Did you remember to run the script to get"
               " the data and the test files?")
        pytest.fail(msg.format(full_path))

def gen_none_error(recreate_msg):
    '''
    Generate the error message for an unexpected return value of None.

    Inputs:
      recreate_msg (string): a string with the informatino needed to
        rerun the test in ipython.

    Returns (string): error message
    '''

    msg = "The function returned None."
    msg += " Did you forget to include a return statement?\n"
    return msg + recreate_msg + "\n"


def gen_type_error(recreate_msg, expected, actual):
    '''
    Generate the error message for an return value of the wrong type

    Inputs:
      recreate_msg (string): a string with the informatino needed to
        rerun the test in ipython.

    Returns (string): error message
    '''

    msg = "The function returned a value of the wrong type.\n"
    msg += "  Expected return type: {}.\n"
    msg += "  Actual return type: {}.\n"
    msg += recreate_msg  + "\n"
    return msg.format(type(expected), type(actual))

def gen_mismatch_error(recreate_msg, expected, actual):
    '''
    Generate the error message for the case whether the expected and
    actual values do not match.

    Inputs:
      recreate_msg (string): a string with the informatino needed to
        rerun the test in ipython.

    Returns (string): error message
    '''

    msg = "\nActual ({}) and expected ({}) values do not match.\n"
    msg += recreate_msg  + "\n"
    return msg.format(actual, expected)


def is_sequence(arg):
    '''
    Take this code as a black box, it checks whether an object is a
    list or tuple but not a string.

    Ref. stackoverflow.com/questions/
      1835018/python-check-if-an-object-is-a-list-or-tuple-but-not-string
    '''
    return (not hasattr(arg, "strip") and
            hasattr(arg, "__getitem__") or
            hasattr(arg, "__iter__"))

def check_tuple_list(actual, recreate_msg):
    '''
    doc string
    '''

    assert actual is not None, gen_none_error(recreate_msg)

    msg = "Expected a sorted list of pairs. Got {}.\n{}"

    assert is_sequence(actual), \
        msg.format(type(actual), recreate_msg)

    for val in actual:
        msg = ("Expected a sorted list of pairs."
               " Got list with at least one {}.\n{}")
        assert isinstance(val, tuple), \
            msg.format(type(val), recreate_msg)



def compare_lists(actual, params, recreate_msg):
    '''
    Do a test, check the result, report an error, if necessary.
    '''
    expected = params["expected"]

    if actual != expected:
        if len(actual) != len(expected):
            msg = ("Length of actual result ({}) does not match "
                   "the length of the expected result ({}).\n{}")
            pytest.fail(msg.format(len(actual), len(expected), recreate_msg))

        for i, actual_val in enumerate(actual):
            if actual_val != expected[i]:
                msg = ("At index {}:"
                       "  Actual result ({}) does not match"
                       "  Expected result ({}).\n{}")
                pytest.fail(msg.format(i,
                                       actual_val,
                                       expected[i],
                                       recreate_msg))
    # Test succeeded if you get to here
    return

def compare_sets(actual, params, recreate_msg):
    '''
    Do a test, check the result, report an error, if necessary.
    '''
    expected = params["expected"]

    assert isinstance(actual, set), \
        "Wrong return type.  Expected a set.  Got {}".format(type(actual))

    if actual != expected:
        if len(actual) != len(expected):
            msg = ("Length of actual result ({}) does not match "
                   "the length of the expected result ({}).\n{}")
            pytest.fail(msg.format(len(actual), len(expected), recreate_msg))

        if actual - expected:
            msg = ("Actual includes unexpected values: {}")
            pytest.fail(msg.format(actual - expected))

        if expected - actual:
            msg = ("Actual missing expected values: {}")
            pytest.fail(msg.format(expected - actual))

    # Test succeeded if you get to here
    return


def compare_tuple_lists(actual, params, recreate_msg):
    '''
    Do a test, check the result, report an error, if necessary.
    '''

    print("Actual:", actual)
    print()
    print("Expected:", params["expected"])

    # check the type
    check_tuple_list(actual, recreate_msg)

    expected = params["expected"]

    if actual != expected:
        if len(actual) != len(expected):
            msg = ("Length of actual result ({}) does not match "
                   "the length of the expected result ({}).\n{}")
            pytest.fail(msg.format(len(actual), len(expected), recreate_msg))

        if sort_count_pairs(actual) == expected:
            msg = "Actual result is not sorted properly.\n{}"
            pytest.fail(msg.format(recreate_msg))

        for i, actual_val in enumerate(actual):
            if actual_val != expected[i]:
                msg = ("At index {}:"
                       "  Actual result ({}) does not match"
                       "  Expected result ({}).\n{}")
                pytest.fail(msg.format(i,
                                       actual_val,
                                       expected[i],
                                       recreate_msg))
    # Test succeeded if you get to here
    return


def compare_list_of_lists(actual, params, recreate_msg):
    '''
    Check the result, report an error, if necessary.
    '''

    # check the type
    assert actual is not None, gen_none_error(recreate_msg)

    msg = "Expected list of lists. Got {}.\n{}"
    assert is_sequence(actual), \
        msg.format(type(actual), recreate_msg)

    expected = params["expected"]

    if actual != expected:
        if len(actual) != len(expected):
            msg = ("Length of actual result ({}) does not match "
                   "the length of the expected result ({}).\n{}")
            pytest.fail(msg.format(len(actual), len(expected), recreate_msg))

        for i, actual_val in enumerate(actual):
            msg = ("Expected list of lists of {}."
                   " Got list with at least one {}.\n{}")
            assert is_sequence(actual_val), \
                msg.format(type(actual_val), recreate_msg)

            if actual_val != expected[i]:
                msg = ("At index {}:"
                       "  Actual result ({}) does not match"
                       "  Expected result ({}).\n{}")
                pytest.fail(msg.format(i,
                                       actual_val,
                                       expected[i],
                                       recreate_msg))

    # Test succeeded if you get to here
    return
