#!python

import urllib2
import json
import sys

from operator import itemgetter
from pprint import pprint

#Define this outside all function definitions to use it in all standalone functions for input validation
validFeatures = ['alerts', 'almanac', 'astronomy', 'conditions', 'currenthurricane', 'forecast', 
                     'forecast10day', 'geolookup', 'history', 'hourly', 'hourly10day', 'planner', 
                     'rawtide', 'tide', 'webcams', 'yesterday']

#Structured pretty heavily off of the sample code on WUnderground
#https://www.wunderground.com/weather/api/d/docs?d=resources/code-samples
def getJSON_Response(apiKey='45cf8510dd6bc8a1', state='CA', city='Santa_Monica', feature='tide'):
    if feature not in validFeatures:
        print "Invalid feature given\n\nValid features:"
        pprint(validFeatures)
        return {}
    
    try:
        myURL = 'http://api.wunderground.com/api/%s/geolookup/%s/q/%s/%s.json' % (apiKey, feature, state, city)    
        f = urllib2.urlopen(myURL)
        json_string = f.read()
        parsed_json = json.loads(json_string)
        f.close()
        return parsed_json
    #Called if urlopen fails to connect (i.e. the API is down or otherwise unavailable)
    except IOError:
        print "WeatherUnderground API is currently unavailable"
        return {}
        

def binData(parsed_json, feature='tide'):
    if feature not in validFeatures:
        print "Invalid feature given\n\nValid features:"
        pprint(validFeatures)
        return {}
    
    #Essentially, bin the data into a dictionary of lists
    binnedData = {}
    #Bin the data according to tide event and extract the relevant height and time information
    if feature=='tide':
        for tideEvent in parsed_json['tide']['tideSummary']:
            #The type of event (high tide, low tide, moonrise, moonset, sunrise, sunset)
            eventType = tideEvent['data']['type']
            
            #All units are in ft, but strip those off because we don't need them (split by spaces and take first)
            height = 0 if tideEvent['data']['height'] == '' else float(tideEvent['data']['height'].split()[0])
            
            #Keep the pretty time to use in printing the time
            prettyTime = tideEvent['date']['pretty']
            
            #Also include a version of time in terms of number of minutes since midnight
            #Useful for calculating the median time of (sun/moon)(rise/set)
            timeInMinutes = 60 * int(tideEvent['date']['hour']) + int(tideEvent['date']['min'])
            
            #If a key already exists in the dictionary, append to that list, otherwise, make the new list
            if eventType in binnedData:
                binnedData[eventType].append((height, prettyTime, timeInMinutes))
            else:
                binnedData[eventType] = [(height, prettyTime, timeInMinutes)]
    #Bin the data by just adding it all to one list with a corresponding key of 'temps'
    elif feature=='hourly':
        for hourlyEvent in parsed_json['hourly_forecast']:
            temp = hourlyEvent['temp']['english']
            if 'temps' in binnedData:
                binnedData['temps'].append(temp)
            else:
                binnedData['temps'] = [temp]
    #For any other feature type, we don't really need to bin anything
    return binnedData

def printBinnedResults(binnedData, parsed_json, feature='tide'):
    if feature not in validFeatures:
        print "Invalid feature given\n\nValid features:"
        pprint(validFeatures)
        return
    
    if feature=='tide':
        #Extract the tide site
        tideSite = parsed_json['tide']['tideInfo'][0]['tideSite']
        print "The tide site is %s\n" % (tideSite)
        
        #Calculate some basic statistics about the tide height data
        #Maximum and minimum a list of tuples inspired by
        #http://stackoverflow.com/questions/13145368/find-the-maximum-value-in-a-list-of-tuples-in-python
        for keys in binnedData.keys():
            print "Looking at data for %s events" % (keys)
            
            #Maximum tide height
            maxTuple = max(binnedData[keys], key=itemgetter(0))
            print "The maximum tide height was %0.3f ft and occured at %s" % (maxTuple[0], maxTuple[1])
            
            #Minimum tide height
            minTuple = min(binnedData[keys], key=itemgetter(0))
            print "The minimum tide height was %0.3f ft and occured at %s" % (minTuple[0], minTuple[1])
            
            #Average tide height
            avg = 0.0
            listLen = len(binnedData[keys])
            for events in binnedData[keys]:
                avg += events[0]
            print "The average tide height was %0.3f ft" % (avg/listLen)
            
            #Median tide height
            sortedList = sorted(binnedData[keys], key=lambda item:item[0])
            #If the list has odd length, the median is the middle index
            if listLen % 2 == 1:
                median = sortedList[listLen//2][0]
            #Otherwise, it's the average of the two middle indices
            else:
                median = (sortedList[listLen//2 - 1][0] + sortedList[listLen//2][0])/2
            print "The median tide height was %0.3f ft" % (median)
            
            #Median times of sunrise, sunset, moonrise, and moonset events
            if keys == 'Sunrise' or keys == 'Sunset' or keys == 'Moonrise' or keys == 'Moonset':
                #Sort the data according to the "time in minutes" from binData
                sortedList = sorted(binnedData[keys], key=lambda item:item[2])
                #Use the same median logic as above
                if listLen % 2 == 1:
                    median = sortedList[listLen//2][2]
                else:
                    median = (sortedList[listLen//2 - 1][2] + sortedList[listLen//2][2])/2
                
                timeStr = "The median time of %s was " % (keys.lower())
                #Check if we're printing AM or PM
                if median//60 < 12:
                    timeStr += "%d:%d AM\n\n" % (median//60, median % 60)
                else:
                    timeStr += "%d:%d PM\n\n" % (median//60 - 12, median % 60)
                print timeStr
            else:
                print "\n"
    
    elif feature=='hourly':
        #Print the average temperature
        avg = 0.0
        listLen = len(binnedData['temps'])
        for temp in binnedData['temps']:
            avg += float(temp)
        print "The average temperature was %0.3f F" % (avg/listLen)
    else:
        print "Data for %s was successfully obtained" % (feature)
    return

def printMainUsage():
    print "Usage: WeatherUnderground.py [-h] [--help] feature\n"
    print "Valid features:"
    pprint(validFeatures)
    return

def main(argVector=['WeatherUnderground.py']):
    if len(argVector) < 2 or argVector[1] == '-h' or argVector[1] == '--help':
        printMainUsage()
        return
    
    feature = argVector[1]
    
    if feature not in validFeatures:
        print "Invalid feature given\n"
        printMainUsage()
        return
    
    parsed_json = getJSON_Response(feature=feature)
    #If an error occurs, parsed_json should return an empty dict
    if parsed_json == {}:
        print "Error occurred when fetching JSON, exiting..."
        return
    #Therefore, if we reach this point, some kind of data was returned from getJSON_Response
    binnedData = binData(parsed_json, feature=feature)
    printBinnedResults(binnedData, parsed_json, feature=feature)

if __name__ == '__main__':
    main(sys.argv)
    