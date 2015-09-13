
# coding: utf-8

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
import poisson311 as pts

probTol = 0.05

latents = ['pubd', 'public', 'private', 'other']

# time_fmt declares the format for the time data
# year_data declares an empty hash, and the for loop creates further hashes (think: vectors) assigned to the keys of '2012' and '2013'

time_fmt = "%m/%d/%Y"


# This portion of the program builds the data list, organized by month, in a list called emergency. It runs through the list, pulling dates from the csv file, and then counts the number of times any particular month (and thereby the amount of calls in that month) comes up. If a month has not previously been encountered, it is added to the list and given a count of one. Otherwise, it's incremented by one.

for l in latents:

    reports = {}

    with open('311_' + l + '_2012_2013.csv') as csvfile:
        threeOne = csv.DictReader(csvfile)
            # for all the 311 calls the reader finds
        for e in threeOne:
            date = time.strptime(e['OPEN_DT'], time_fmt) # converts string version of date into a date object
            y = date.tm_year
            d = date.tm_mday
            if y == 2013 and date.tm_mon == 4 and d in range (12,23):
                e['lon'] = e['X']
                e['lat'] = e['Y']
                if e['lat'] != 'NA':
                    if not d in reports.keys():
                        reports[d] = []
                    reports[d].append(e)
                     
    # boston = bm.BostonScatter(reports)
    # boston.plotMap(outname=l + '_bombday_scatter_311_' + str(currentDay),
    #     title='Locations of 311 Reports on 4-' + str(currentDay) + '-13')
    for d in sorted(reports):
        #if l != 'pubd' and d != '22':
            boston = bm.BostonDensity(reports[d])
            boston.plotMap(outname=l + '_bombday_density_311_' + str(d),
                title='Locations of ' + l.title() + ' 311 Reports in 4-' + str(d) + '-13')
            # f = open(l + "_most_dense_311_4-" + str(d) + "-13.csv", "w")
            # f.write(boston.highest)
            # f.close()

            # with open(l + "_response_tracts_311_4-" + str(d) + "-13.csv", "w") as f:
            #     ct_counts = []
            #     for i, row in boston.df_map.iterrows():
            #         prob = pts.poissonProb(row['count'], row['CT_ID_10'], l)
            #         if (prob <= probTol):
            #             ct_counts.append(str(row['CT_ID_10']) + "," + str(row['count']) + "," + str(prob))

            #     f.write('ct_id,numReports,probability\n')
            #     f.write('\n'.join(ct_counts))

            plt.close('all')
