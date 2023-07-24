import os
import csv
import re

CWD = os.getcwd()

ALL_APTS = []

IGNORE_ROUTE = ["(LAXE)", "(LAXNA)", "(SANE)", "(SNAN)", "(RWY11)", "LAX EAST"]
UNIGNORE_ROUTE = ['LAX WEST AND EAST']
LARGE_LIST = []
TEC_ROUTE_LIST = []
EXPORT_TEC_ROUTE_LIST = []
COMPARE_LIST = []


def loadAirports():

    global ALL_APTS

    path = input("Enter airport load file: ")

    with open(path, "r") as f:

        for line in f:

            if line != '':

                ALL_APTS.append(line.replace('\n', ''))

    f.close()


def parseLine(line):

    out = ""

    for z in line:

        out += z + ","

    return out[:-1]


def lookupAirportPair(departure, destination):

    with open(CWD + "\\prefroutes_db.csv", "r") as csvfile:

        spamreader = csv.reader(csvfile)

        output = []

        for line in spamreader:

            if line[0] == departure:

                if destination in line[2]:

                    aircraft = re.sub(r"\d+", "", line[8])
                    aircraftaltitude = line[8]

                    for n in aircraft:

                        area = line[7]
                        FLAG_IGNORE = False
                        for test in IGNORE_ROUTE:

                            if test in area:

                                FLAG_IGNORE = True

                            for test2 in UNIGNORE_ROUTE:

                                if test2 not in line[8] and test in line[8]:

                                    FLAG_IGNORE = True

                        if not FLAG_IGNORE:

                            if line[10][-1] == "R":
                                command = f".{(departure+destination+n).lower()}r .am rte {line[1][4:-4]} [{line[10]} {aircraftaltitude}]"

                            else:

                                command = f".{(departure+destination+n).lower()} .am rte {line[1][4:-4]} [{line[10]} {aircraftaltitude}]"

                            output.append(command)

    return output


def findTecRoutes(departure, destination):

    with open(CWD + "\\prefroutes_db.csv", "r") as csvfile:

        spamreader = csv.reader(csvfile)

        output = []

        for line in spamreader:

            if line[0] == departure:

                if destination in line[2]:

                    aircraftaltitude = line[8]
                    area = line[7]

                    FLAG = [False, ""]

                    for test in IGNORE_ROUTE:

                        if test in area:

                            FLAG[0] = True
                            FLAG[1] += f"{test} "

                        for test2 in UNIGNORE_ROUTE:

                                if test2 not in line[8] and test in line[8]:

                                    FLAG[0] = True
                                    FLAG[1] += f"({test}) "

                    FLAG[1] = FLAG[1].strip()

                    if not FLAG[0]:

                        command = [
                            f".{(line[10]).lower()} .am rte {line[1][4:-4]} [{line[10]} {aircraftaltitude}]",
                            line[10],
                            parseLine(line),
                        ]

                    else:

                        command = [
                            f".{(line[10]).lower()} .am rte {line[1][4:-4]} [{line[10]} {FLAG[1]} {aircraftaltitude}]",
                            line[10],
                            parseLine(line),
                        ]

                    output.append(command)

        return output


def buildCommands():

    print("Building TEC Route City Pair commands!")
    for departure in ALL_APTS:

        for destination in ALL_APTS:

            z = lookupAirportPair(departure, destination)

            if len(z) > 0:

                for q in z:

                    LARGE_LIST.append(q)

    print(f"Built TEC Route City Pair commands! ({len(LARGE_LIST)})")
    print("Building TEC Route Code commands...")

    for departure in ALL_APTS:

        for destination in ALL_APTS:

            z = findTecRoutes(departure, destination)

            for p_route in z:

                if p_route[1] not in TEC_ROUTE_LIST:

                    TEC_ROUTE_LIST.append(p_route[1])
                    COMPARE_LIST.append([p_route[1], p_route[2]])
                    EXPORT_TEC_ROUTE_LIST.append(p_route[0])

    print(f"Built TEC Route Code commands! ({len(TEC_ROUTE_LIST)})")


def exportFiles():

    with open("tecoutput.tec", "w") as f:

        f.write("*****TEC ROUTES BY DESIGNATOR*****\n\n")

        for export in EXPORT_TEC_ROUTE_LIST:

            f.write(export + "\n")

        f.write("\n*****TEC ROUTES BY AIRPORT PAIR AND AIRCRAFT TYPE*****\n\n")

        for item in LARGE_LIST:

            f.write(item + "\n")

    f.close()

    with open("tecroutecompare.csv", "w") as cf:

        cf.write(
            "TCODE,Orig,Route String,Dest,Hours1,Hours2,Hours3,Type,Area,Altitude,Aircraft,Direction,Seq,DCNTR,ACNTR"
        )
        for route in COMPARE_LIST:

            cf.write(f"\n{route[0]},{route[1]}")

    cf.close()

    print("Task done!")


def main():

    loadAirports()
    buildCommands()
    exportFiles()


if __name__ == "__main__":

    main()
