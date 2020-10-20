import csv
import json
import os
import sys

def read_CSV_file(filename):
    '''
    Load the data from a CSV file.

    Inputs:
      filename (string): the name of the file

    Returns: list
    '''

    try:
        with open(filename) as f:
            return [row for row in csv.DictReader(f)]
    except FileNotFoundError:
        msg = ("Cannot open file: {}.")
        assert False, msg.format(filename)


def read_JSON_file(filename):
    '''
    Load data from a JSON file.

    Inputs:
      filename (string): the file name

    Returns: whatever is in the json file
    '''

    try:
        with open(filename) as f:
            return json.load(f)
    except FileNotFoundError:
        msg = ("Cannot open file: {}.")
        assert False, msg.format(filename)

        
