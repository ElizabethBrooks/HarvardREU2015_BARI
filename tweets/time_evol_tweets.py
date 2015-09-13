
# ## Useful libraries

import time                         # time/date parser
import csv                          # data parser
import numpy as np                  # arrays for plotting
import matplotlib.pyplot as plt     # plotting
import math                         # ceiling for y-max in plots
import twittercriteria as twc       # yaml, re, os

import os
import sys
sys.path.append(os.path.realpath('../census/'))
import bostonmap as bm
sys.path.append(os.path.realpath('./classifiers/'))
import posnegclassifier as pnc
import relevanceclassifier as rc
import re

spaths = {'positive':'/sentimentData/positive_Uncleaned.txt', 'negative':'/sentimentData/negative_Uncleaned.txt', 
         'neutral':'/sentimentData/neutral_Uncleaned.txt'}

paths = {'relevant':'/relevanceData/relevant.txt', 'irrelevant':'/relevanceData/irrelevant.txt'}

cats = spaths.keys()

clssfr = pnc.PosNegClassifierPerceptronSVM(spaths, twc.cleanForSentiment)
relClssfr = rc.RelevanceClassifierQuadraticSVM(paths, twc.cleanUpTweet)

handles = ['@boston_police',
           '@bostonglobe',
           '@bostonmarathon',
           '@redsox',
           '@barackobama',
           '@bostondotcom',
           '@stoolpresidente',
           '@nhlbruins',
           '@mlb',
           '@cnnbrk',
           '@ap',
           '@7news',
           '@fox25news',
           '@youranonnews',
           '@cnn',
           '@middlebrooks',
           '@dzhokhar_a',
           '@wcvb',
           '@cbsboston',
           '@universalhub',
           '@tdgarden',
           '@massstatepolice',
           '@j_tsar',
           '@huffingtonpost',
           '@wbcsays']

handle_reg = re.compile('|'.join(handles))

def containsHandle(tweet):
    return handle_reg.search(tweet) is not None

def getTimeString(currentHour):
    timeStr = ""
    if currentHour != 12 and currentHour != 24:
        timeStr += str(currentHour%12)
    else:
        timeStr += str(12)
    if currentHour < 12 or currentHour == 24:
        timeStr += ' AM'
    else:
        timeStr += ' PM'
    return timeStr

# ## Retrieving useful data with our `twitter_criteria` module
# retrieve the time format string from the criteria dictionary in twc
tweet_time_fmt = twc.getTwitterTimeFmt()

### get data

kwTweets = []
currentHour = 0

infoTweets = []

relTweets = []

relInfo = []

tweetList = []
textList = []

# negative = blue, positive = orange, neutral = green
sentimentTweets = {'positive':{'face':'#ffb347', 'edge':'w'}, 'negative':{'edge':'w', 'face':'#33ccff'},
                  'neutral':{'face':'#77dd77', 'edge':'w'}}

relevantTweets = {'tweets':{'edge':'w', 'face':'#33ccff'}, 'info':{'face':'#ffb347', 'edge':'w'}}
keywordTweets = {'tweets':{'edge':'w', 'face':'#33ccff'}, 'info':{'face':'#ffb347', 'edge':'w'}}

for c in cats:
    sentimentTweets[c]['data'] = []

count = 0
count2 = 0

with open('test_tweets_4_12_22.csv') as csvfile:
    # reads first line of csv to determine keys for the tweet hash, tweets 
    # is an iterator through the list of tweet hashes the DictReader makes
    tweets = csv.DictReader(csvfile)
    # for all the tweets the reader finds
    for tweetData in tweets:
        # make sure its not a 'false tweet' from people using newlines in their tweet_text's
        if tweetData['time'] != "":
            # parse date/time into object
            date = time.strptime(tweetData['time'], tweet_time_fmt)
            #if date.tm_mday == 15 and twc.tweetContainsKeyword(tweetData['tweet_text']):
            if date.tm_mday == 12:
                count2 += 1
                if date.tm_hour == currentHour:
                    if twc.tweetContainsKeyword(tweetData['tweet_text'].lower()):
                        kwTweets.append(tweetData)
                        if containsHandle(tweetData['tweet_text']):
                            infoTweets.append(tweetData)
                    tweetList.append(tweetData)
                    textList.append(tweetData['tweet_text'])
                elif date.tm_hour == currentHour + 1:
                    currentHour += 1
                    timeStr = getTimeString(currentHour)
                    results = relClssfr.classify(textList)
                    for i in range(0, len(results)):
                        if results[i] == 0:
                            relTweets.append(tweetList[i])
                            if containsHandle(textList[i]):
                                relInfo.append(tweetList[i])

                    results = clssfr.classify(textList)
                    for i in range(0, len(results)):
                        sentimentTweets[cats[results[i]]]['data'].append(tweetList[i])

                    # for sentiment in sentimentTweets.keys():
                    #     boston = bm.GreaterBostonScatter(sentimentTweets[sentiment]['data'])
                    #     boston.plotMap(outname='the12th_' + sentiment + '_' + str(currentHour).zfill(3),
                    #         title='Locations of ' + sentiment.title() + ' Tweets At ' + timeStr)
                    boston = bm.ColoredGBScatter(sentimentTweets)
                    boston.plotMap(outname='the12th_sentiments_' + str(currentHour).zfill(3),
                             title='Locations of Sentiment Tweets At ' + timeStr)

                    # keywordTweets['tweets']['data'] = kwTweets
                    # keywordTweets['info']['data'] = infoTweets

                    # boston = bm.ColoredGBScatter(keywordTweets)
                    # boston.plotMap(outname='the12th_keyword_' + str(currentHour).zfill(3),
                    #          title='Locations of Keyword-Relevant Tweets At ' + timeStr)

                    # relevantTweets['tweets']['data'] = relTweets
                    # relevantTweets['info']['data'] = relInfo

                    # boston = bm.ColoredGBScatter(relevantTweets)
                    # boston.plotMap(outname='the12th_rel_' + str(currentHour).zfill(3),
                    #          title='Locations of Relevant-Classified Tweets At ' + timeStr)

                    # boston = bm.GreaterBostonScatter(relTweets)
                    # boston.plotMap(outname='the12th_rel_' + str(currentHour).zfill(3),
                    #     title='Locations of Relevant Tweets At ' + timeStr)
                    # boston = bm.GreaterBostonScatter(kwTweets)
                    # boston.plotMap(outname='the12th_keyword_'+str(currentHour).zfill(3),
                    #     title='Locations of Keyword Tweets At ' + timeStr)

                    if twc.tweetContainsKeyword(tweetData['tweet_text']):
                        kwTweets.append(tweetData)
                        if containsHandle(tweetData['tweet_text']):
                            infoTweets.append(tweetData)
                    plt.close('all')
                    print "Done with " + timeStr
                    del tweetList
                    del textList
                    tweetList = [tweetData]
                    textList = [tweetData['tweet_text']]
            elif date.tm_mday == 18:
                count += 1

print count
print count2


currentHour += 1
timeStr = getTimeString(currentHour)
results = relClssfr.classify(textList)                    
for i in range(0, len(results)):
    if results[i] == 0:
        relTweets.append(tweetList[i])
        if containsHandle(textList[i]):
            relInfo.append(tweetList[i])

results = clssfr.classify(textList)
for i in range(0, len(results)):
    sentimentTweets[cats[results[i]]]['data'].append(tweetList[i])

# for sentiment in sentimentTweets.keys():
#     boston = bm.GreaterBostonScatter(sentimentTweets[sentiment]['data'])
#     boston.plotMap(outname='the12th_' + sentiment + '_' + str(currentHour).zfill(3),
#         title='Locations of ' + sentiment.title() + ' Tweets At ' + timeStr)

# boston = bm.GreaterBostonScatter(relTweets)
# boston.plotMap(outname='the12th_rel_' + str(currentHour).zfill(3),
#     title='Locations of Relevant Tweets At ' + timeStr)

# boston = bm.GreaterBostonScatter(kwTweets)
# boston.plotMap(outname='the12th_keyword_'+str(currentHour).zfill(3),
#     title='Locations of Keyword Tweets At ' + timeStr)

boston = bm.ColoredGBScatter(sentimentTweets)
boston.plotMap(outname='the12th_sentiments_' + str(currentHour).zfill(3),
         title='Locations of Sentiment Tweets At ' + timeStr)

# keywordTweets['tweets']['data'] = kwTweets
# keywordTweets['info']['data'] = infoTweets

# boston = bm.ColoredGBScatter(keywordTweets)
# boston.plotMap(outname='the12th_keyword_' + str(currentHour).zfill(3),
#          title='Locations of Keyword-Relevant Tweets At ' + timeStr)

# relevantTweets['tweets']['data'] = relTweets
# relevantTweets['info']['data'] = relInfo

# boston = bm.ColoredGBScatter(relevantTweets)
# boston.plotMap(outname='the12th_rel_' + str(currentHour).zfill(3),
#          title='Locations of Relevant-Classified Tweets At ' + timeStr)

plt.close('all')
print "Done with " + timeStr

print "Number of total keyword tweets: " + str(len(kwTweets))
print "Number of total keyword-handle tweets: " + str(len(infoTweets))

print "Number of total relevant tweets: " + str(len(relTweets))
print "Number of total relevant-handle tweets: " + str(len(relInfo))
