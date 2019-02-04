import argparse
import importPkg.generate as generate
true = True
false = False

parser = argparse.ArgumentParser()

parser.add_argument("-json", "--writejson", help="use this option to generate a JSON file in resources/data", action='store_true')

parser.add_argument("-csv", "--writecsv", help="use this option to generate a CSV file in resources/data", action='store_true')

parser.add_argument("-l", "--lines",
                    help="Sets the amount of lines generated",
                    type=int, required=False, default=-1, nargs='?', const=True)

parser.add_argument("-csvn", "--csvname",
                    help="Sets the name and location of the generated csv file",
                    type=str, required=False, default="../resources/data/result.csv", nargs='?', const=True)

parser.add_argument("-jsonn", "--jsonname",
                    help="Sets the name and location of the generated json file",
                    type=str, required=False, default="../resources/data/result.csv", nargs='?', const=True)

args = parser.parse_args()


if __name__ == '__main__':
    generate.lel(args)
