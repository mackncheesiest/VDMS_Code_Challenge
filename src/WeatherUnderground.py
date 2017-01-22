import urllib2
import json

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

#print(parsed_json)

tideSite = parsed_json['tide']['tideInfo'][0]['tideSite']
print "The tide site is %s" % (tideSite)


"""
location = parsed_json['location']['city']
temp_f = parsed_json['current_observation']['temp_f']
print "Current temperature in %s is: %s" % (location, temp_f)
"""