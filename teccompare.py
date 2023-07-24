import os
import csv

CWD = os.getcwd()

NEW = []
NEW_CODES = []
OLD = []
OLD_CODES = []

def parseNewFile():

    path1 = input("Enter newest 'tecroutecompare.csv' type file: ")
    with open(path1, 'r') as p1:

        spr1 = csv.reader(p1)
        for l1 in spr1:

            NEW.append([l1[0], l1[1:]])
            NEW_CODES.append(l1[0])

    p1.close()

def parseOldFile():

    path2 = input("Enter older 'tecroutecompare.csv' type file: ")
    with open(path2, 'r') as p2:

        spr2 = csv.reader(p2)
        for l2 in spr2:

            OLD.append([l2[0], l2[1:]])
            OLD_CODES.append(l2[0])

    p2.close()

def compare(nu, old):

    CHANGES = []
    NEW_ROUTES = []
    EXPORTS = []

    for pair1 in nu:

        nucode = pair1[0]
        nuroute = pair1[1]

        if nucode not in OLD_CODES:

            CHANGES.append(f"New TEC route found: {nucode}")

        for pair2 in old:

            oldcode = pair2[0]
            oldroute = pair2[1]

            FLAG = False
            UPDATES = []

            if nucode == oldcode:

                if nuroute[0] != oldroute[0]:

                    FLAG = True
                    UPDATES.append(f'Origin changed from {oldroute[0]} to {nuroute[0]}')

                if nuroute[1] != oldroute[1]:

                    FLAG = True
                    UPDATES.append(f'Route changed from {oldroute[1]} to {nuroute[1]}')

                if nuroute[2] != oldroute[2]:

                    FLAG = True
                    UPDATES.append(f'Destination changed from {oldroute[2]} to {nuroute[2]}')

                if nuroute[3] != oldroute[3]:

                    FLAG = True
                    UPDATES.append(f'Hours1 changed from {oldroute[3]} to {nuroute[3]}')

                if nuroute[4] != oldroute[4]:

                    FLAG = True
                    UPDATES.append(f'Hours2 changed from {oldroute[4]} to {nuroute[4]}')

                if nuroute[5] != oldroute[5]:

                    FLAG = True
                    UPDATES.append(f'Hours3 changed from {oldroute[5]} to {nuroute[5]}')

                if nuroute[6] != oldroute[6]:

                    FLAG = True
                    UPDATES.append(f'Type changed from {oldroute[6]} to {nuroute[6]}')

                if nuroute[7] != oldroute[7]:

                    FLAG = True
                    UPDATES.append(f'Area changed from {oldroute[7]} to {nuroute[7]}')
                    
                if nuroute[8] != oldroute[8]:

                    FLAG = True
                    UPDATES.append(f'Altitude changed from {oldroute[8]} to {nuroute[8]}')

                if nuroute[9] != oldroute[9]:

                    FLAG = True
                    UPDATES.append(f'Aircraft changed from {oldroute[9]} to {nuroute[9]}')

                if nuroute[11] != oldroute[11]:

                    FLAG = True
                    UPDATES.append(f'Sequence changed from {oldroute[11]} to {nuroute[11]}')

            if FLAG:

                format_str = f"Changes for route code {nucode} [{len(UPDATES)}]: "

                for line in UPDATES:

                    format_str += line + ' | '

                CHANGES.append(format_str)
    
    for item1 in NEW_ROUTES:

        EXPORTS.append(item1+'\n')

    for item2 in CHANGES:

        EXPORTS.append(item2+'\n')

    return EXPORTS

def exportChanges(li: list):

    with open('changefile.tec', 'w') as xf:

        for line in li:

            xf.write(line)

def main():

    parseNewFile()
    parseOldFile()
    changes = compare(NEW, OLD)
    exportChanges(changes)

if __name__ == '__main__':

    main()