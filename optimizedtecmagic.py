import os
import csv
import re
import time

CWD = os.getcwd()

IGNORE_ROUTE = ["(LAXE)", "(LAXNA)", "(SANE)", "(SNAN)", "(RWY11)", "LAX EAST"]
UNIGNORE_ROUTE = ["LAX WEST AND EAST"]

def checkConfig(info):

    configs = []
    FLAG = False

    for testCase1 in IGNORE_ROUTE:

        if testCase1 in info:

            configs.append(testCase1)
            FLAG = True

    for testCase2 in UNIGNORE_ROUTE:

        if testCase2 in info:

            configs.append(testCase2)

    return [FLAG, configs]


def generateRouteCommand(line: list, config):

    code = line[10]
    altitude = line[8]

    builder = f".{code.lower()} .am rte {line[1][4:-4]}"

    if config[0]:

        parsed = ' '.join(config[1])

        actualCfg = parsed.replace("LAX EAST", "(LAXE)").replace(
            "LAX WEST AND EAST", "(LAXW, LAXE)"
        )

        if "(LAXE)" in actualCfg and "(LAXW, LAXE)" in actualCfg:

            actualCfg = actualCfg.replace('(LAXE)', '')

        builder += f" [{code} {actualCfg} {altitude}]"

    else:

        builder += f" [{code} {altitude}]"

    return builder


def generateImpliedCommands(line: list, config):

    output = []

    altitude = line[8]
    allowTypes = re.sub(r"\d+", "", altitude)

    for typ in allowTypes:

        builder = ""

        builder += f".{(line[0]+line[2]+typ).lower()}"

        if line[10][-1] == "R":

            builder += "r"

        builder += f" .am rte {line[1][4:-4]}"

        if len(config[1]) > 0:

            parsed = ' '.join(config[1])
            actualCfg = parsed.replace("LAX WEST AND EAST", "(LAXW, LAXE)")

            builder += f" [{line[10]} {actualCfg} {altitude}]"

        else:

            builder += f" [{line[10]} {altitude}]"

        output.append(builder)

    return output


def parseDBtoCommands():

    output = {
        "cityPair": {"commands": []},
        "routeCode": {"knownRoutes": [], "commands": [], "routeCodeAndLineValue": []},
    }

    with open(CWD + "\\prefroutes_db.csv", "r") as df:

        spr = csv.reader(df)

        for line in spr:

            rType = line[6]
            isZLA = line[12] == "ZLA" or line[13] == "ZLA"

            if rType == "TEC" and isZLA:

                code = line[10]
                information = line[7]
                uncommonConfiguration = checkConfig(information)

                if not uncommonConfiguration[0]:

                    commands = generateImpliedCommands(line, uncommonConfiguration)

                    for command in commands:

                        output["cityPair"]["commands"].append(command)

                if code not in output["routeCode"]["knownRoutes"]:

                    information = line[7]
                    uncommonConfiguration = checkConfig(information)

                    command = generateRouteCommand(line, uncommonConfiguration)
                    output["routeCode"]["commands"].append(command)
                    output["routeCode"]["knownRoutes"].append(code)
                    output["routeCode"]["routeCodeAndLineValue"].append([code, line])

    return output


def buildAliasFile(commands: dict):

    with open("tecoutput.tec", "w") as of:

        of.write("*****TEC ROUTES BY DESIGNATOR*****\n\n")

        for codeCommand in commands["routeCode"]["commands"]:

            of.write(codeCommand + "\n")

        of.write("\n*****TEC ROUTES BY AIRPORT PAIR AND AIRCRAFT TYPE*****\n\n")

        for cityPairCommand in commands["cityPair"]["commands"]:

            of.write(cityPairCommand + "\n")

    of.close()

    print(
        f"Built {len(commands['routeCode']['commands'])} route code commands and {len(commands['cityPair']['commands'])} city pair commands!"
    )


def exportToCsv(routes: list):

    with open("tcompare.csv", "w") as cf:

        cf.write(
            "TCODE,Orig,Route String,Dest,Hours1,Hours2,Hours3,Type,Area,Altitude,Aircraft,Direction,Seq,DCNTR,ACNTR"
        )

        for routeLinePair in routes:

            cf.write(f"\n{routeLinePair[0]},{','.join(routeLinePair[1])}")


def main():

    start = time.time()

    commandList = parseDBtoCommands()
    buildAliasFile(commandList)
    exportToCsv(commandList["routeCode"]["routeCodeAndLineValue"])

    end = time.time()

    print(f"Task complete in {end - start} seconds!")


if __name__ == "__main__":

    main()
