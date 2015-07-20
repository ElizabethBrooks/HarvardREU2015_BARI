# Imports for the program (Original program by Josh Lozjim and edited by Hayden Fuss, this version by Jeremy McKenzie)

import matplotlib
import time                      # time/date parsing
import csv                       # data parsing
import numpy as np               # arrays for plotting
import matplotlib.pyplot as plt  # Plotting
import math                      # ceiling for y-max in plots
import sys

import os
sys.path.append(os.path.realpath('../census'))
import bostonmap as bm


# time_fmt declares the format for the time data

time_fmt = "%m/%d/%Y %H:%M"

filename = raw_input("Enter the file name to read data from: ")
#filename = sys.stdin.readline()
print filename
filename = filename.rstrip("\n")
prefix = raw_input("Enter prefix for maps: ")
prefix = prefix.rstrip("\n")

# This portion of the program builds the data list, organized by month, in a list called emergency. It runs through the list, pulling dates from the csv file, and then counts the number of times any particular month (and thereby the amount of calls in that month) comes up. If a month has not previously been encountered, it is added to the list and given a count of one. Otherwise, it's incremented by one.

reports = []
data = {}

with open(filename) as csvfile:
    nineOne = csv.DictReader(csvfile)
        # for all the 911 calls the reader finds
    for e in nineOne:
        date = time.strptime(e['ENTRY_DT'], time_fmt) # converts string version of date into a date object
        y = date.tm_year
        d = date.tm_mday
        if y == 2013 and date.tm_mon == 4 and d in range (12,23):
            if not d in data.keys():
                data[d] = []
            data[d].append(e)
            
for d in sorted(data):                              
    boston = bm.BostonDensityCT(data[d])
    boston.plotMap(outname=prefix + '_bombday_density_911_' + str(d),
        title='Density of 911 dispatches, 4-' + str(d) + '-13')
    f = open(prefix + "_most_dense_911_4-" + str(d) + "-13.csv", "w")
    f.write(boston.highest)
    f.close()

