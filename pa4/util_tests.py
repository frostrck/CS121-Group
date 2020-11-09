'''
Polling places

Utilities
'''

import csv
import sys
import os
import pytest

from util import load_precincts

# Handle the fact that the grading code may not
# be in the same directory as implementation
sys.path.insert(0, os.getcwd())

from simulate import Precinct

# DO NOT MODIFY THIS FILE
# pylint: disable-msg= invalid-name, too-many-arguments, line-too-long
# pylint: disable-msg= too-many-branches

# # #
#
# HELPER FUNCTIONS
#
# # #

def check_none(actual, recreate_msg=None):
    msg = "The function returned None."
    msg += " Did you forget a return statement?"
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

def check_equals(actual, expected, recreate_msg=None):
    msg = "Actual ({}) and expected ({}) values do not match.".format(actual, expected)
    if recreate_msg is not None:
        msg += "\n" + recreate_msg

    assert actual == expected, msg

def fcompare(pname, nvoter, field, actual, expected, recreate_msg):

    recreate_msg += "\n    voters[{}].{}_{}".format(nvoter, *field.split())

    msg = "\nThe {} of voter #{} in precint '{}' is incorrect (actual {}, expected {})\n".format(field, nvoter, pname, actual, expected)
    msg += recreate_msg

    assert actual == pytest.approx(expected), msg

# # #
#
# RUN TESTS
#
# # #

def run_test(precincts_file, check_start):
    precincts, seed = load_precincts(precincts_file)
    results_file = precincts_file.replace(".json", ".csv")

    voters = {}
    for p in precincts:
        precinct = Precinct(p["name"],
                            p["hours_open"],
                            p["num_voters"],
                            p["num_booths"],
                            p["arrival_rate"],
                            p["voting_duration_rate"])
        voters[p["name"]] = precinct.simulate(p["percent_straight_ticket"], p["straight_ticket_duration"], seed)

        recreate_msg = "To recreate this test run:\n"
        recreate_msg += "    precinct = Precinct(\"{}\", {}, {}, {}, {}, {})\n".format(p["name"],
                                                                                       p["hours_open"],
                                                                                       p["num_voters"],
                                                                                       p["num_booths"],
                                                                                       p["arrival_rate"],
                                                                                       p["voting_duration_rate"])
        recreate_msg += "    voters = precinct.simulate({}, {}, {})".format(p["percent_straight_ticket"],
                                                                            p["straight_ticket_duration"],
                                                                            seed)

    with open(results_file) as f:
        reader = csv.DictReader(f)

        results = {}
        for row in reader:
            results.setdefault(row["precinct"], []).append(row)

        for p in precincts:
            pname = p["name"]

            pvoters = voters[pname]
            rvoters = results.get(pname, [])

            actual = len(pvoters)
            expected = len(rvoters)

            msg = "Incorrect number of voters for precinct '{}' (actual {}, expected {})\n".format(pname, actual, expected)
            msg += recreate_msg

            assert actual == expected, msg

            i = 0
            for returned_voter, expected_voter in zip(pvoters, rvoters):
                fcompare(pname, i, "arrival time", returned_voter.arrival_time, float(expected_voter["arrival_time"]), recreate_msg)
                fcompare(pname, i, "voting duration", returned_voter.voting_duration, float(expected_voter["voting_duration"]), recreate_msg)
                if check_start:
                    fcompare(pname, i, "start time", returned_voter.start_time, float(expected_voter["start_time"]), recreate_msg)
                i += 1
