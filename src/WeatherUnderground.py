import urllib2
import json

from operator import itemgetter

#Structured pretty heavily off of the sample code on WUnderground
#https://www.wunderground.com/weather/api/d/docs?d=resources/code-samples
def getJSON_Response(apiKey='45cf8510dd6bc8a1', state='CA', city='Santa_Monica'):
    myURL = 'http://api.wunderground.com/api/%s/geolookup/tide/q/%s/%s.json' % (apiKey, state, city)    
    f = urllib2.urlopen(myURL)
    json_string = f.read()
    parsed_json = json.loads(json_string)
    f.close()
    return parsed_json

parsed_json = getJSON_Response()

#Bin the data according to tide event and extract the relevant height and time information
binnedData = {}
for tideEvent in parsed_json['tide']['tideSummary']:
    eventType = tideEvent['data']['type']
    #All units are in ft, but strip those off because we don't need them
    height = 0 if tideEvent['data']['height'] == '' else float(tideEvent['data']['height'].split()[0])
    time = tideEvent['date']['pretty']
    if eventType in binnedData:
        binnedData[eventType].append((height, time))
    else:
        binnedData[eventType] = [(height, time)]

#Start listing things off
tideSite = parsed_json['tide']['tideInfo'][0]['tideSite']
print "The tide site is %s" % (tideSite)


#Maximum and minimum a list of tuples inspired by
#http://stackoverflow.com/questions/13145368/find-the-maximum-value-in-a-list-of-tuples-in-python
for keys in binnedData.keys():
    print "Looking at data for %s events" % (keys)
    
    #Maximum tide height
    maxTuple = max(binnedData[keys], key=itemgetter(0))
    print "The maximum tide height was %0.3f and occured at %s" % (maxTuple[0], maxTuple[1])
    
    #Minimum tide height
    minTuple = min(binnedData[keys], key=itemgetter(0))
    print "The minimum tide height was %0.3f and occured at %s" % (minTuple[0], minTuple[1])
    
    #Average tide height
    avg = 0.0
    listLen = len(binnedData[keys])
    for events in binnedData[keys]:
        avg += float(events[0])/float(listLen)
    print "The average tide height was %0.3f" % (avg)
    
    #Median tide height
    sortedList = sorted(binnedData[keys], key=lambda item:item[0])
    if listLen % 2 == 1:
        median = sortedList[listLen//2][0]
    else:
        median = (sortedList[listLen//2 - 1][0] + sortedList[listLen//2][0])/2
    print "The median tide height was %0.3f\n" % (median)

