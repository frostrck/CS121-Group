# -*- coding: utf-8 -*-
"""Test code for basic analysis algorithms

This module defines the test functions for
the basic analysis algorithms.
"""

import os
import sys
import pytest

import test_helpers
import basic_algorithms

# Want to catch any exception thrown by student code.
#pylint: disable-msg=broad-except

# Handle the fact that the grading code may not
# be in the same directory as basic_algorithms.py
sys.path.append(os.getcwd())

# Get the test files from the same directory as
# this file.
BASE_DIR = os.path.dirname(__file__)
TEST_DIR = os.path.join(BASE_DIR, "tests")

def run_test(fn, params, arg0_name, arg1_name):
    '''
    add a doc string
    '''

    recreate_msg = "To recreate this test in ipython3 run:\n"
    recreate_msg += "  basic_algorithms.{}({}, {})"
    recreate_msg = recreate_msg.format(fn.__name__,
                                       params[arg0_name],
                                       params[arg1_name])
    try:
        actual = fn(params[arg0_name], params[arg1_name])
    except Exception as e:
        s = "Caught exception: {}\n{}"
        pytest.fail(s.format(e, recreate_msg))

    assert actual is not None, \
        test_helpers.gen_none_error(recreate_msg)

    expected = params["expected"]
    assert isinstance(actual, type(expected)), \
        test_helpers.gen_type_error(recreate_msg, expected, actual)

    assert actual == expected, \
        test_helpers.gen_mismatch_error(recreate_msg, expected, actual)

@pytest.mark.parametrize(
    "params",
    test_helpers.read_config_file("find_top_k.json"))
def test_top_k(params):
    '''
    Test find_top_k
    '''
    run_test(basic_algorithms.find_top_k, params, "items", "k")


@pytest.mark.parametrize(
    "params",
    test_helpers.read_config_file("find_min_count.json"))
def test_find_min_count(params):
    '''
    Test find_min_count
    '''
    # Fix the rexpected type.
    params["expected"] = set(params["expected"])

    run_test(basic_algorithms.find_min_count, params, "items", "min_count")


@pytest.mark.parametrize(
    "params",
    test_helpers.read_config_file("find_salient.json"))
def test_find_salient(params):
    '''
    Test find most salient
    '''

    # convert expected result from a list of lists to a list of sets
    params["expected"] = [set(words) for words in params["expected"]]

    run_test(basic_algorithms.find_salient, params, "items", "threshold")
