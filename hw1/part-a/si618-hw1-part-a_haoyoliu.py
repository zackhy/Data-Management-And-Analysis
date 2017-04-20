from __future__ import division
from math import log
import csv

result = []
name_list = []
with open('world_bank_indicators.txt') as f:
    k = 0
    for line in f:
        raw_list = line.replace('\n', '').replace('"', '').split('\t')
        # Keep only rows with date = 2000 or date = 2010
        if k != 0 and raw_list[1].find("2010") == -1 and raw_list[1].find("2000") == -1:
            continue

        # Create a list to store all required columns
        new_list = [raw_list[0]] + [raw_list[1][raw_list[1].rfind('/')+1:]] + [raw_list[9]] + \
                   [raw_list[4]] + [raw_list[6]] + [raw_list[5]] + [raw_list[19]]
        # Get rid of rows with missing values
        if '' in new_list:
            continue

        if k == 0:
            new_list.append('Mobile subscribers per capita')
            new_list.append('log(GDP per capita)')
            new_list.append('log(Health: mortality under 5)')
            new_list.append('region')
        # Compute and add new columns
        else:
            x = '{:.5f}'.format(int(new_list[3].replace(',', '')) / int(new_list[2].replace(',', '')))
            new_list.append(str(x))
            y = '{:.5f}'.format(log(int(new_list[6].replace(',', ''))))
            new_list.append(str(y))
            z = '{:.5f}'.format(log(int(new_list[4].replace(',', ''))))
            new_list.append(str(z))
            # Add regions
            with open('world_bank_regions.txt') as f1:
                flag = 0
                for row in f1:
                    region_list = row.replace('\n', '').split('\t')
                    if new_list[0] == region_list[2].replace('"', ''):
                        new_list.append(region_list[0])
                        flag = 1
                # For countries like 'West Bank and Gaza' that could not match any region
                # Set the region to 'None'
                if flag == 0:
                    new_list.append('None')
        if k > 0:
            result.append(new_list)
        else:
            name_list = new_list
        k += 1

# Sorting
sorted_result = sorted(result, key=lambda i: (int(i[1]), i[10], int(i[6].replace(',', ''))))

# Write the CSV file
outfile = file('worldbank_output_haoyoliu.csv', 'wb')
writer = csv.writer(outfile)
writer.writerow(name_list)
for data in sorted_result:
    writer.writerow(data)
