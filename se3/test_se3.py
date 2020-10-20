import sys
import os
import csv
import json
import pytest

# Handle the fact that the test code may not
# be in the same directory as the solution code
sys.path.insert(0, os.getcwd())
BASE_DIR = os.path.dirname(__file__)
TEST_DIR = os.path.join(BASE_DIR, "tests")

import se3
import test_helpers

MODULE = "se3"

### Helper
def read_config_file(filename):
    '''
    Load the test cases from a JSON file.

    Inputs:
      filename (string): the name of the test configuration file.

    Returns: (list) test cases
    '''

    full_path = os.path.join(TEST_DIR, filename)
    return test_helpers.read_JSON_file(full_path)

def test_construct_dict_from_lists_1():
    do_test_construct_dict_from_lists(keys=["a"], values=[1], expected={"a": 1})

def test_construct_dict_from_lists_2():
    do_test_construct_dict_from_lists(keys=["x", "y", "z"], values=[10, 20, 30],
                                      expected={"x": 10, "y": 20, "z": 30})

def test_construct_dict_from_lists_3():
    do_test_construct_dict_from_lists(keys=[], values=[], expected={})
    

@pytest.mark.parametrize(
    "params",
    read_config_file("find_candidates_from_city.json"))
def test_find_candidates_from_city(params):
    do_test_find_candidates_from_city(params)

@pytest.mark.parametrize(
    "params",
    read_config_file("find_unsuccessful_fund_raisers.json"))
def test_find_unsuccessful_fund_raisers(params):
    do_test_find_unsuccessful_fund_raisers(params)
    

@pytest.mark.parametrize(
    "params",
    read_config_file("construct_homestate_dict.json"))
def test_construct_homestate_dict(params):
    do_test_construct_homestate_dict(params)

@pytest.mark.parametrize(
    "params",
    read_config_file("construct_cands_by_state.json"))
def test_construct_cands_by_state(params):
    do_test_construct_cands_by_state(params)
    


# # #
#
# HELPER FUNCTIONS
#
# # #

def gen_recreate_msg(module, function, load_strs, *params):
    params_str = ", ".join([str(p) for p in params])

    recreate_msg = "To recreate this test in ipython3 run:\n"
    if load_strs:
        for s in load_strs:
            recreate_msg += "  {}\n".format(s)
    recreate_msg += "  {}.{}({})".format(module, function, params_str)
    return recreate_msg

def read_file_or_val(params, file_key, val_key):
    if file_key in params:
        filename = params[file_key]
        if filename.endswith(".csv"):
            load_str = "test_helpers.read_CSV_file('{}')".format(filename)
            return load_str, test_helpers.read_CSV_file(filename)
        elif filename.endswith(".json"):
            load_str = "test_helpers.read_JSON_file('{}')".format(filename)
            return load_str, test_helpers.read_JSON_file(filename)
        else:
            assert False, "Test code is broken in read_file_or_val"
    elif val_key in params:
        load_str = "{}".format(str(params[val_key]))
        return load_str, params[val_key]
    else:
        assert False, "Test code is broken in read_file_or_val"        


def check_none(actual, recreate_msg=None):
    msg = "The function returned None."
    msg += " Did you forget to replace the placeholder value we provide?"
    if recreate_msg is not None:
        msg += "\n" + recreate_msg

    assert actual is not None, msg

def check_expected_none(actual, recreate_msg=None):
    msg = "The function is expected to return None."
    msg += " Your function returns: {}".format(actual)
    if recreate_msg is not None:
        msg += "\n" + recreate_msg

    assert actual is None, msg


def check_type(actual, expected, recreate_msg=None):
    actual_type = type(actual)
    expected_type = type(expected)

    msg = "The function returned a value of the wrong type.\n"
    msg += "  Expected return type: {}.\n".format(expected_type.__name__)
    msg += "  Actual return type: {}.".format(actual_type.__name__)
    if recreate_msg is not None:
        msg += "\n" + recreate_msg

    assert isinstance(actual, expected_type), msg


def check_equals(actual, expected, recreate_msg=None):
    msg = "Actual ({}) and expected ({}) values do not match.".format(actual, expected)
    if recreate_msg is not None:
        msg += "\n" + recreate_msg

    assert actual == expected, msg


def check_list_unmodified(param_name, before, after, recreate_msg=None):
    msg = "You modified the contents of {} (this is not allowed).\n".format(param_name)
    msg += "  Value before your code: {}\n".format(before)
    msg += "  Value after your code:  {}".format(after)
    if recreate_msg is not None:
        msg += "\n" + recreate_msg

    assert before == after, msg



# # #
#
# TEST HELPERS
#
# # #


def do_test_construct_dict_from_lists(keys, values, expected):
    recreate_msg = gen_recreate_msg(MODULE, "construct_dict_from_lists", [], *(keys, values))

    actual = se3.construct_dict_from_lists(keys, values)

    check_none(actual, recreate_msg)
    check_type(actual, expected, recreate_msg)
    check_equals(actual, expected, recreate_msg)


def do_test_find_candidates_from_city(params):
    # read the candidate data for this task
    cands_str, cands = read_file_or_val(params, "cand_filename", "cands")
    load_strs = ["cands = {}".format(cands_str)]
    loc = tuple(params["location"])
    recreate_msg = gen_recreate_msg(MODULE, "find_candidates_from_city",
                                    load_strs, *("cands", loc))

    actual = se3.find_candidates_from_city(cands, loc)
    expected = params["expected"]

    print("actual length:", len(actual))
    print("expected length:", len(expected))

    check_none(actual, recreate_msg)
    check_type(actual, expected, recreate_msg)
    check_equals(actual, expected, recreate_msg)    

    
def do_test_find_unsuccessful_fund_raisers(params):
    dc_str, dc = read_file_or_val(params, "dc_filename", "dc")
    load_strs = ["dc = {}".format(dc_str)]
    recreate_msg = gen_recreate_msg(MODULE, "find_unsuccessful_fund_raisers",
                                    load_strs, *("dc", params["threshold"]))

    print(dc)
    print(params["threshold"])
    actual = se3.find_unsuccessful_fund_raisers(dc, params["threshold"])
    expected = params["expected"]

    check_none(actual, recreate_msg)
    check_type(actual, expected, recreate_msg)
    check_equals(set(actual), set(expected), recreate_msg)    

    
def do_test_construct_homestate_dict(params):
    cands_str, cands = read_file_or_val(params, "cand_filename", "cands")
    load_strs = ["cands = {}".format(cands_str)]
    recreate_msg = gen_recreate_msg(MODULE, "construct_homestate_dict",
                                    load_strs, *(["cands"]))

    actual = se3.construct_homestate_dict(cands)
    expected = params["expected"]

    check_none(actual, recreate_msg)
    check_type(actual, expected, recreate_msg)
    check_equals(actual, expected, recreate_msg)    

def do_test_construct_cands_by_state(params):
    cands_str, cands = read_file_or_val(params, "cand_filename", "cands")
    load_strs = ["cands = {}".format(cands_str)]
    recreate_msg = gen_recreate_msg(MODULE, "construct_cands_by_state",
                                    load_strs, *(["cands"]))

    actual = se3.construct_cands_by_state(cands)
    expected = params["expected"]

    check_none(actual, recreate_msg)
    check_type(actual, expected, recreate_msg)
    check_equals(actual, expected, recreate_msg)    
    
