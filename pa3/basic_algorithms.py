"""
CS121: Analyzing Election Tweets (Solutions)

Algorithms for efficiently counting and sorting distinct `entities`,
or unique values, are widely used in data analysis.

Functions to implement:

- count_tokens
- find_top_k
- find_min_count
- find_most_salient

You may add helper functions.
"""

import math
from util import sort_count_pairs

def count_tokens(tokens):
    '''
    Counts each distinct token (entity) in a list of tokens

    Inputs:
        tokens: list of tokens (must be immutable)

    Returns: dictionary that maps tokens to counts
    '''

    # YOUR CODE HERE

    # REPLACE {} WITH A SUITABLE RETURN VALUE
    return {}


def find_top_k(tokens, k):
    '''
    Find the k most frequently occuring tokens

    Inputs:
        tokens: list of tokens (must be immutable)
        k: a non-negative integer

    Returns: list of the top k tokens ordered by count.
    '''

    #Error checking (DO NOT MODIFY)
    if k < 0:
        raise ValueError("In find_top_k, k must be a non-negative integer")

    # YOUR CODE HERE

    # REPLACE [] WITH A SUITABLE RETURN VALUE
    return []


def find_min_count(tokens, min_count):
    '''
    Find the tokens that occur *at least* min_count times

    Inputs:
        tokens: a list of tokens  (must be immutable)
        min_count: a non-negative integer

    Returns: set of tokens
    '''

    #Error checking (DO NOT MODIFY)
    if min_count < 0:
        raise ValueError("min_count must be a non-negative integer")

    # YOUR CODE HERE

    # REPLACE set() WITH A SUITABLE RETURN VALUE
    return set()


def find_salient(docs, threshold):
    '''
    Compute the salient words for each document.  A word is salient if
    its tf-idf score is strictly above a given threshold.

    Inputs:
      docs: list of list of tokens
      threshold: float

    Returns: list of sets of salient words
    '''

    # YOUR CODE HERE

    # REPLACE [] WITH A SUITABLE RETURN VALUE
    return []
