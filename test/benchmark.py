from datetime import datetime


from etlController import ETLController
import argparse


def main():
    etl = ETLController()

    start=datetime.now()
    etl.runRules("benchmark.json", 0, 100)
    time = str(datetime.now()-start).lstrip("0:00:")
    print("---------------------")
    print("Time to validate a hundred entries: %s seconds" % time)
    print("---------------------")

    start=datetime.now()
    etl.runRules("benchmark.json", 0, 1000)
    time = str(datetime.now()-start).lstrip("0:00:")
    print("---------------------")
    print("Time to validate a thousand entries: %s seconds" % time)
    print("---------------------")

if __name__ == '__main__':
    main()
