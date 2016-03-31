import csv
import xml.dom.minidom
import sys
import os


def createTrkPt(gpxDoc, row, count):
  # This creates a  element for a row of data.
  # A row is a dict.
  
  # create trkpt tag and its attribute
  trkptElement = gpxDoc.createElement('trkpt')
  trkptElement.setAttribute('lat', row[3])
  trkptElement.setAttribute('lon', row[2])
  
  # create name tag
  posElement = gpxDoc.createElement('name')
  posElement = trkptElement.appendChild(posElement)
  posElement.appendChild(gpxDoc.createTextNode('Position_%s' % str(count)))
  
  # create ele tag 
  eleElement = gpxDoc.createElement('ele')
  eleElement = trkptElement.appendChild(eleElement)
  eleElement.appendChild(gpxDoc.createTextNode('0.0'))
  
  
  # time
  timeElement = gpxDoc.createElement('time')
  timeElement = trkptElement.appendChild(timeElement)
  timeArr = row[1].split(' ')
  timeFormat = '%sT%s+08:00' % (timeArr[0], timeArr[1])
  timeElement.appendChild(gpxDoc.createTextNode(timeFormat))
  
  
  return trkptElement

def createGPX(txtReader, gsxPath, fileName):
  # This constructs the KML document from the CSV file.
  gpxDoc = xml.dom.minidom.Document()
  
  gpxElement = gpxDoc.createElementNS('http://www.topografix.com/GPX/1/1', 'gpx')
  gpxElement.setAttribute('xmlns','http://www.topografix.com/GPX/1/1')
  gpxElement.setAttribute('version','1.1')
  gpxElement.setAttribute('creator','TrackConverter')
  gpxElement = gpxDoc.appendChild(gpxElement)
  documentElement = gpxDoc.createElement('trk')
  documentElement = gpxElement.appendChild(documentElement)

  nameElement = gpxDoc.createElement('name')
  nameElement = documentElement.appendChild(nameElement)
  nameElement.appendChild(gpxDoc.createTextNode(fileName.split('.')[0])) 

  trkSegElement = gpxDoc.createElement('trkseg')
  trkSegElement = documentElement.appendChild(trkSegElement)

  # Skip the header line.
  # csvReader.next()
  
  count = 0
  for row in txtReader:
    count += 1
    trkptElement = createTrkPt(gpxDoc, row.strip().split(','), count)
    trkSegElement.appendChild(trkptElement)
  
  gpxFile = open(os.path.join(gsxPath, fileName), 'w')
  gpxFile.write(gpxDoc.toprettyxml('  ', newl = '\n', encoding = 'utf-8'))

def main():
  # This reader opens up 'google-addresses.csv', which should be replaced with your own.
  # It creates a KML file called 'google.gpx'.
  
  # If an argument was passed to the script, it splits the argument on a comma
  # and uses the resulting list to specify an order for when columns get added.
  # Otherwise, it defaults to the order used in the sample.
  
  # order = ['Taxi_Id','Date_Time','Longitude','Latitude']
  gsxPath = os.path.join(os.getcwd(), 'gsvData')

  if not os.path.exists(gsxPath):
    os.mkdir(gsxPath)

  for dirPath, dirNames, fileNames in os.walk(os.getcwd()):
    for fileName in fileNames:
        if '.txt' in fileName:
          txtreader = open(os.path.join(dirPath,fileName)).readlines()
          gpx = createGPX(txtreader, gsxPath,'%s.gpx' % fileName.split('.')[0])

if __name__ == '__main__':
  main()