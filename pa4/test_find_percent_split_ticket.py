'''
Polling places: test code for find_percent_split_ticket
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

from simulate import find_percent_split_ticket

DATA_DIR = "./data/"

# DO NOT MODIFY THIS FILE
# pylint: disable-msg= invalid-name, missing-docstring, too-many-arguments, line-too-long

with open(DATA_DIR + "best_percent_split_ticket.csv") as f:
    reader = csv.DictReader(f)

    configs = []
    for row in reader:
        config = (row["config_file"],
                  int(row["num_trials"]),
                  float(row["target_wait_time"]),
                  float(row["percent_split_ticket"]),
                  None if row["avg_wait_time"] == "" else float(row["avg_wait_time"])
                 )
        configs.append(config)

def run_test(precincts_file, num_trials, target_wait_time,
             percent_split_ticket, avg_wait_time):
    precincts, seed = util.load_precincts(precincts_file)
    p = precincts[0]

    actual_pst, actual_wt = find_percent_split_ticket(p, target_wait_time, num_trials, seed)
    expected_pst = percent_split_ticket
    expected_wt = avg_wait_time

    recreate_msg = "\nTo recreate this test run:\n"
    recreate_msg += "    precincts, seed = util.load_precincts(\"{}\")\n".format(precincts_file[2:])
    recreate_msg += "    p = precincts[0]\n"
    recreate_msg += "    simulate.find_percent_split_ticket(p, {}, {}, {})".format(target_wait_time, num_trials, seed)

    if expected_wt == None:
      expected_wt = None
    else:
      expected_wt = pytest.approx(expected_wt)

    # Account for floating point issues
    actual_pst = pytest.approx(actual_pst)

    ut.check_equals(actual_pst, expected_pst, recreate_msg)
    ut.check_equals(actual_wt, expected_wt, recreate_msg)

@pytest.mark.parametrize("config_file,num_trials,target_wait_time,percent_split_ticket,avg_wait_time", configs)
def test_simulate(config_file, num_trials, target_wait_time,
                  percent_split_ticket, avg_wait_time):
    run_test(DATA_DIR + config_file, num_trials, target_wait_time,
             percent_split_ticket, avg_wait_time)

