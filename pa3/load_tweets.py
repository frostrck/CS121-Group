"""
Load the tweets for the Analyze Candidate Tweets assignment.
"""

import util

Conservatives = util.get_json_from_file("data/Conservatives.json")
UKLabour = util.get_json_from_file("data/UKLabour.json")
theSNP = util.get_json_from_file("data/theSNP.json")
LibDems = util.get_json_from_file("data/LibDems.json")

# sample tweet from the "Data" section
tweet0 = UKLabour[651]

# sample tweet from the "Pre-processing step" and "Representing
# N-grams" sections.
tweet1 = UKLabour[55]
