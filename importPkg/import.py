import csv
import json
import os
import argparse
from builtins import staticmethod
from importPkg.importCls import ImportCls

parser = argparse.ArgumentParser()

parser.add_argument("-d", "--delimiter",
					help="Sets the delimiter used for importing the CSV file",
                    type=str, required=False, default="", nargs='?', const=True)

parser.add_argument("-file", "--fileinput",
					help="Sets the location of the file that should be imported",
                    type=str, required=False, default="", nargs='?', const=True)

parser.add_argument("-out", "--fileoutput",
					help="Sets the location, the converted JSON file will be saved at",
                    type=str, required=False, default="", nargs='?', const=True)

args = parser.parse_args()

if __name__ == '__main__':
    ImportCls.importcsv(args)
