import csv
import xml.dom.minidom
import sys
import os


def createTrkPt(gpxDoc, row, count):
  # This creates a  element for a row of data.
  # A row is a dict.
  
  # create trkpt tag and its attribute
  trkptElement = gpxDoc.createElement('trkpt')
  trkptElement.setAttribute('lat', row['Latitude'])
  trkptElement.setAttribute('lon', row['Longitude'])
  
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
  timeElement.appendChild(gpxDoc.createTextNode(row['Time']))
  
  
  return trkptElement

def createGPX(csvReader, gsxPath, fileName):
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
  for row in csvReader:
    count += 1
    trkptElement = createTrkPt(gpxDoc, row, count)
    trkSegElement.appendChild(trkptElement)
  
  gpxFile = open(os.path.join(gsxPath, fileName), 'w')
  gpxFile.write(gpxDoc.toprettyxml('  ', newl = '\n', encoding = 'utf-8'))

def main():
  # This reader opens up 'google-addresses.csv', which should be replaced with your own.
  # It creates a KML file called 'google.gpx'.
  
  # If an argument was passed to the script, it splits the argument on a comma
  # and uses the resulting list to specify an order for when columns get added.
  # Otherwise, it defaults to the order used in the sample.
  
  # order = ['Time','TaxiNo','Longitude','Latitude']
  dataPath = os.path.join(os.getcwd(), 'TaxiData')
  gsxPath = os.path.join(os.getcwd(), 'gsvData')

  if not os.path.exists(gsxPath):
    os.mkdir(gsxPath)

  for csvFile in os.listdir(dataPath): 
    if '.csv' not in csvFile:
      continue
    csvreader = csv.DictReader(open(os.path.join(dataPath, csvFile)))
    gpx = createGPX(csvreader, gsxPath,'%s.gpx' % csvFile.split('.')[0])

if __name__ == '__main__':
  main()