import csv
import library

def read_csv(filename):
    libs = []
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            libs.append(library.Library(row["Island"], 
                                        row["LIBRARY"], 
                                        int(row["REFERENCE"]), 
                                        int(row["BOOK"]),
                                        int(row["MICROFORM"])))
    return libs

HI_LCS_2011 = read_csv("data/libraries-collection-statistics-2011-csv.csv")