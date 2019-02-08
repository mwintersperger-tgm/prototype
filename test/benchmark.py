from datetime import datetime


from etlController import ETLController
from shutil import copyfile


def main():
    etl = ETLController()

    copyfile("benchmark_ori.json", "benchmark.json")
    start=datetime.now()
    etl.runRules("benchmark.json", 0, 100)
    time = str(datetime.now()-start).lstrip("0:00:")
    print("---------------------")
    print("Time to validate a hundred lines: %s seconds" % time)
    print("---------------------")

    copyfile("benchmark_ori.json", "benchmark.json")
    start=datetime.now()
    etl.runRules("benchmark.json", 0, 1000)
    time = str(datetime.now()-start).lstrip("0:00:")
    print("---------------------")
    print("Time to validate a thousand lines: %s seconds" % time)
    print("---------------------")


    copyfile("benchmark_ori.json", "benchmark.json")
    start=datetime.now()
    etl.runRules("benchmark.json", 0, 10000)
    time = str(datetime.now()-start).lstrip("0:")

    print("---------------------")
    print("Time to validate ten thousand lines: %s seconds" % time)
    print("---------------------")

if __name__ == '__main__':
    main()
