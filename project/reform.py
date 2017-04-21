""""
This program reform badness data which would be then used in R to draw heat map.
Author: Haoyou Liu
"""
import csv
import collections
import math

with open('badness.csv') as f:
    incsv = csv.reader(f, delimiter=',')
    next(f)

    dic = {}
    for line in f:
        line = line.strip().replace('"', '').split(',')
        if line[2] in dic.keys():
            try:
                dic[line[2]][int(line[1])] = math.log(float(line[3]), 10) + 2
            except:
                dic[line[2]][int(line[1])] = line[3]
        else:
            dic[line[2]] = {}
            try:
                dic[line[2]][int(line[1])] = math.log(float(line[3]), 10) + 2
            except:
                dic[line[2]][int(line[1])] = line[3]

for key, value in dic.items():
    for year in range(1960, 2015):
        if year not in value:
            dic[key][year] = 0

sorted_dic = {}
for key, value in dic.items():
    sorted_dic[key] = collections.OrderedDict(sorted(dic[key].items()))

with open('avg_badness.csv', 'wb') as ouf:
    writer = csv.writer(ouf)
    writer.writerow([''] + (range(1960, 2015)))
    for key, value in dic.items():
        writer.writerow([key] + value.values())
