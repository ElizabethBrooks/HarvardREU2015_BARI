#!/usr/bin/python2.7

# author: Hayden Fuss

#################### LIBRARIES ########################################################################

import time                         # time/date parser
import csv                          # data parser
import re                           # regex
import numpy as np                  # arrays for plotting
import matplotlib.pyplot as plt     # plotting
import math                         # ceiling for y-max in plots


#################### CRITERIA ########################################################################

tweet_time_fmt = "%Y-%m-%d %H:%M:%S"

keywords_list = ['#bostonmarathon', 
                 '#marathonmonday',
                 '#patriotsday',
                 'marathon',
                 'boylston',
                 'finish line',
                 '#bostonstrong',
                 '#bostonpride',
                 '#prayforboston',
                 '#pray4bos',
                 'bomb',
                 'explosion',
                 'explode',
                 'wounded',
                 'hostage',
                 'watertown',
                 'lockdown',
                 'manhunt',
                 'collier']

# build regex for searching for all the keywords
keywords = re.compile('|'.join(keywords_list))

# initialze hash/dictionary for counting keyword occurances
keyword_counts = {}

for word in keywords_list:
  keyword_counts[word] = 0


#################### FUNCTIONS #######################################################################

def tweetContainsKeyWords(tweet):
  # searches tweet for keywords, if none were found, findall returns empty list
  found_words = keywords.findall(tweet)
  if found_words:
    for word in found_words:
      keyword_counts[word] += 1
    return True
  else:
    return False

# Sentiment analysis functions, will require a lot more code
def angryTweet(tweet):
  return

def peacefulTweet(tweet):
  return

def scaredTweet(tweet):
  return

def excitedTweet(tweet):
  return


##################### MAIN ###########################################################################
# uses the csv.DictReader class to parse the data
# time.strptime to parse date/time
# regex to analyze tweet text
# matplotlib and numpy to make barchart

## main function
def main():

  ### get data

  dates = {}

  with open('cleaned_geo_tweets_Apr_12_to_22.csv') as csvfile:
    # reads first line of csv to determine keys for the tweet hash, tweets 
    # is an iterator through the list of tweet hashes the DictReader makes
    tweets = csv.DictReader(csvfile)
    # for all the tweets the reader finds
    for tweetData in tweets:
      # make sure its not a 'false tweet' from people using newlines in their tweet_text's
      if tweetData['time'] != "":
        # parse date/time into object
        date = time.strptime(tweetData['time'], tweet_time_fmt)
        # add day hash to list if it hasn't been added
        if not date.tm_mday in dates.keys():
          dates[date.tm_mday] = {'AM':0, 'PM':0}
        tweetData['tweet_text'] = tweetData['tweet_text'].lower()
        if tweetContainsKeyWords(tweetData['tweet_text']):
          # determine if morning or evening
          if date.tm_hour < 12:                     # hour = 0 - 11
            dates[date.tm_mday]['AM'] += 1
          else:                                     # hour = 12 - 23
            dates[date.tm_mday]['PM'] += 1

  ### produce plots
  ### source: http://people.duke.edu/~ccc14/pcfb/numpympl/MatplotlibBarPlots.html
  
  fig = plt.figure()
  ax = fig.add_subplot(121) # 1x2 grid, 1st subplot

  #### make data plot-friendly

  bar_width = 0.35
  indices = np.arange(len(dates))

  ams = []
  pms = []
  tickMarks = []

  for d in sorted(dates):
    ams.append(dates[d]['AM'])
    pms.append(dates[d]['PM'])
    tickMarks.append(str(date.tm_mon) + "/" + str(d))

  ##### get largest count and round up to nearest 100th
  maxCount = int(math.ceil(max(ams + pms) / 100.0)) * 100

  #### plot data

  ##### first plot

  amBars = ax.bar(indices, ams, bar_width, color='c')

  pmBars = ax.bar(indices+bar_width, pms, bar_width, color='g')

  ax.set_xlim(-bar_width, len(indices)+bar_width)
  ax.set_ylim(0, maxCount)
  ax.set_ylabel('Number of Tweets')
  ax.set_title('Tweets Containing Keywords per Day')
  ax.set_xticks(indices+bar_width)
  tickNames = ax.set_xticklabels(tickMarks)
  plt.setp(tickNames, rotation=45, fontsize=10)

  ax.legend((amBars[0], pmBars[0]), ('AM', 'PM'))

  ##### second plot, keyword count

  fig_text = ""

  ax2 = fig.add_subplot(122) # 1x2, 2nd subplot
  ax2.axis('off') # makes blank subplot

  # make text, sorts based on count in reverse (descending) order
  for word in sorted(keyword_counts, key=keyword_counts.get, reverse=True):
    fig_text = fig_text + word + "," + str(keyword_counts[word]) + "\n"

  # add title and text
  ax2.set_title("Occurances of Keywords")
  ax2.text(.1,.1,fig_text)

  #### save plots as image
  plt.savefig("tweets_per_day.png", dpi=96)


## if this program is being executed, and not used as a module, call main
if __name__ == "__main__":
  main()


######################################################################################################