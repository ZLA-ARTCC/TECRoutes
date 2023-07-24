import os
import csv

CWD = os.getcwd()

AIRPORTS = []

with open(CWD+'\\prefroutes_db.csv', 'r') as csvfile:

    spamreader = csv.reader(csvfile)

    for line in spamreader:

        departcc = line[12]
        arrartcc = line[13]
        typecode = line[6]
        departure = line[0]
        destination = line[2]

        if departcc == 'ZLA' and departcc == 'ZLA' and typecode =='TEC':

            if departure not in AIRPORTS:

                AIRPORTS.append(departure)

            if destination not in AIRPORTS:

                AIRPORTS.append(destination)

csvfile.close()

with open(CWD+'\\tecports.tec', 'w') as tf:

    for line in AIRPORTS:

        tf.write(line+'\n')