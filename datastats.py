import numpy as np

from matplotlib import pyplot as plt


with open("X:/OneDrive/TU Delft/_Thesis/data/sats.txt", "r") as f:
    data_string = f.readlines()

line1_cols = [1, 7, 8, 17, 32, 43, 52, 61, 63, 68, 69]
line2_cols = [1, 7, 16, 25, 33, 42, 51, 63, 68, 69]

# data1 = np.empty((len(data_string)//2, len(line1_cols)))
data2 = np.empty((len(data_string)//2, len(line2_cols)))

for i in range(0, len(data_string), 2):
    # line1 = data_string[i]
    line2 = data_string[i + 1]

    # c0 = 0
    # for j, c1 in enumerate(line1_cols):
    #     data1[i//2, j] = line1[c0:c1].strip()
    #     c0 = c1

    c0 = 0
    for j, c1, in enumerate(line2_cols):
        data2[i//2, j] = line2[c0:c1].strip()
        c0 = c1

data2[:, 4] = data2[: ,4]*1e-7

# string = ""
# for line in data2:
#     string += f"{int(line[1])},{line[7]},{line[2]},{line[4]},{line[3]},{line[5]},{line[6]}\n"

data = np.column_stack((data2[:, 1], data2[:, 7], data2[:, 2], data2[:, 4], data2[:, 3], data2[:, 5], data2[:, 6]))

geo_fltr = (0.95 < data[:, 1]) * (data[:, 1] < 1.05) * (data[:, 3] < 0.1)
geos = data[geo_fltr]

gto_fltr = data[:, 3] > 0.7
gtos = data[gto_fltr]

rest_fltr = np.logical_not(geo_fltr) * np.logical_not(gto_fltr)
rest = data[rest_fltr]

string = ""
for line in geos:
    string += f"{int(line[0])} & ${round(line[1], 3)}$ & ${round(line[2], 3)}$ & ${line[3]}$ & ${round(line[4], 3)}$ & ${round(line[5], 3)}$ & ${round(line[6], 3)}$ \\\\\n"

string += "\n"
print(string)

string = ""
for line in gtos:
    string += f"{int(line[0])} & ${round(line[1], 3)}$ & ${round(line[2], 3)}$ & ${round(line[3], 3)}$ & ${round(line[4], 3)}$ & ${round(line[5], 3)}$ & ${round(line[6], 3)}$ \\\\\n"

string += "\n"
print(string)

string = ""
for line in rest:
    string += f"{int(line[0])} & ${round(line[1], 3)}$ & ${round(line[2], 3)}$ & ${round(line[3], 3)}$ & ${round(line[4], 3)}$ & ${round(line[5], 3)}$ & ${round(line[6], 3)}$ \\\\\n"

string += "\n"
print(string)