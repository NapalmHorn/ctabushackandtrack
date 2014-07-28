#!/usr/bin/python

# import modules as needed
import webbrowser
import urllib
from xml.etree.ElementTree import parse
import time

def fetchBusData(bus_number) :
# Input = busnumber
# output = filename of xml data retrieved 
# This functions gets data from cta on a specific bus, creates xml file with that data.
    u = urllib.urlopen('http://ctabustracker.com/bustime/map/getBusesForRoute.jsp?route=' + str(bus_number))
    data = u.read()
    f = open('rt'+  str(bus_number) +'.xml', 'wb')
    f.write(data)
    f.close()
    #print('Wrote: rt'+  str(bus_number) +'.xml')
    return 'rt'+  str(bus_number) +'.xml'

def monitorBus(times_to_monitor, interval, bus_id, davesLoc):
    # inputs the number of iterations to monitor, time between checks, bus id, and reference location.
    # will print 'taxi cab' distance to location 
    while times_to_monitor > 0:
        times_to_monitor -= 1
        #get new data every interval seconds.
        outputXMLfilename = fetchBusData(22)
        doc = parse(outputXMLfilename)
        for bus in doc.findall('bus'):
            d = bus.findtext('d')
            lat = float(bus.findtext('lat'))
            lon = float(bus.findtext('lon'))
            id = str(bus.findtext('id'))
            #only print for the selected bus
            if id == bus_id:
                print "Bus id", id, "distance and coordinates" , 69 * taxiCabDistance((lat , lon), davesLoc ), lat, lon
        if times_to_monitor: time.sleep(interval)
        
    return

def taxiCabDistance(p1, p2):
    return max(p1[0] - p2[0],p2[0] - p1[0]) + max(p1[1] - p2[1],p2[1] - p1[1]) 
   
def main():
#    outputXMLfilename = fetchBusData(22)
    outputXMLfilename = 'rt'+  str(22) +'.xml'
    doc = parse(outputXMLfilename)
    mapUrl = 'http://maps.googleapis.com/maps/api/staticmap?&size=600x300'
    davesLoc = ( 41.980262, -87.668452)
    bestBus = (1000000,None, None, None )
    for bus in doc.findall('bus'):
        d = bus.findtext('d')
        lat = float(bus.findtext('lat'))
        lon = float(bus.findtext('lon'))
        id = str(bus.findtext('id'))
        print d , lat , lon, id
        if taxiCabDistance((lat , lon), davesLoc ) < bestBus[0]:
            bestBus = (taxiCabDistance((lat , lon), davesLoc ), id, lat, lon)
        #print bestBus
        mapUrl = mapUrl + '&markers=%7Clabel:' + id[-1] + '%7C' + str(lat) + ',' + str(lon) 
    #webbrowser.open(mapUrl)
    #print mapUrl
    #print bestBus
    monitorBus(4, 15, bestBus[1], davesLoc)  # just watch the bus for a minute irl should be hours.
    return
# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
    main()