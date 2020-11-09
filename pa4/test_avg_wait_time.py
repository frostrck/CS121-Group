'''
Polling places: test code for avg_wait_time
'''

import csv
import pytest
import util
import sys
import os
import util_tests as ut

# Handle the fact that the grading code may not
# be in the same directory as implementation
sys.path.insert(0, os.getcwd())

from simulate import find_avg_wait_time

# DO NOT MODIFY THIS FILE
# pylint: disable-msg= invalid-name, missing-docstring


DATA_DIR = "./data/"

with open(DATA_DIR + "avg_wait_time.csv") as f:
    reader = csv.DictReader(f)

    configs = []
    for row in reader:
        config = (row["config_file"],
                  int(row["num_trials"]),
                  float(row["percent_straight_ticket"]),
                  float(row["avg_wait_time"])
                 )
        configs.append(config)

def run_test(precincts_file, num_trials, percent_straight_ticket, avg_wait_time):
    precincts, seed = util.load_precincts(precincts_file)
    p = precincts[0]

    actual_wt = find_avg_wait_time(p, percent_straight_ticket, num_trials, initial_seed=seed)
    expected_wt = avg_wait_time

    recreate_msg = "\nTo recreate this test run:\n"
    recreate_msg += "    precincts, seed = util.load_precincts(\"{}\")\n".format(precincts_file[2:])
    recreate_msg += "    p = precincts[0]\n"
    recreate_msg += "    simulate.find_avg_wait_time(p, {}, {}, initial_seed={})".format(percent_straight_ticket, num_trials, seed)

    ut.check_none(actual_wt, recreate_msg)
    ut.check_type(actual_wt, expected_wt, recreate_msg)
    ut.check_equals(actual_wt, pytest.approx(expected_wt), recreate_msg)

@pytest.mark.parametrize("precincts_file,num_trials,percent_straight_ticket,avg_wait_time", configs)
def test_simulate(precincts_file, num_trials, percent_straight_ticket, avg_wait_time):
    run_test(DATA_DIR + precincts_file, num_trials, percent_straight_ticket, avg_wait_time)
