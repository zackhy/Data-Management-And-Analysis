import sqlite3
import csv

conn = sqlite3.connect('vehicles.db')
cur = conn.cursor()
cur.execute("DROP TABLE IF EXISTS vehicles")

statement = "CREATE TABLE vehicles (year INT," \
            "make TEXT, " \
            "model TEXT, " \
            "vclass TEXT, " \
            "cylinders INT, " \
            "displ REAL, " \
            "trany TEXT, " \
            "city08 INT, " \
            "highway08 INT, " \
            "combo08 INT)"
cur.execute(statement)

with open('vehicles.csv', 'rU') as f:
    incsv = csv.reader(f)

    next(incsv)

    for line in incsv:
        try:
            if float(line[23]) == 0.0:
                continue
        except:
            continue

        try:
            record = (int(line[63]),  # year
                      line[46],  # make
                      line[47],  # model
                      line[62],  # VClass
                      int(line[22]),  # cylinders
                      float(line[23]),  # displ
                      line[57],  # trany
                      int(line[4]),  # city08
                      int(line[34]),  # highway08
                      int(line[15]))  # combo08
        except:
            continue

        statement = "INSERT INTO vehicles VALUES (?,?,?,?,?,?,?,?,?,?)"
        cur.execute(statement, record)

conn.commit()
conn.close()
