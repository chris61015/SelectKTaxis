import os
import datetime
import time
import math
import numpy as np
import matplotlib.pyplot as plt

# longitude Range: 120.85~122.2
# latitude Range: 30.666666666666668~31.883333333333333

latMin = 30.666666666666668
latMax = 31.883333333333333
lonMin = 120.85
lonMax = 122.2

#Calculate the ratio of grids a taxi covered in a given time period
def coverRate(mlist):
  totalGrid = len(mlist) * len(mlist[0])
  count = 0
  for row in mlist:
    for col in row:
      if col:
        count+=1
  return count / float(totalGrid)

def rad(d):
    return d*math.pi/180.0

#Calculate the distance between two coordinates
def distance(lat1,lng1,lat2,lng2):
    radlat1=rad(lat1)
    radlat2=rad(lat2)
    a=radlat1-radlat2
    b=rad(lng1)-rad(lng2)
    s=2*math.asin(math.sqrt(math.pow(math.sin(a/2),2)+math.cos(radlat1)*math.cos(radlat2)*math.pow(math.sin(b/2),2)))
    earth_radius=6378.137
    s=s*earth_radius
    return s * 1000

#calculate how many rows and columns are there in our grid.
def numOfGrid():
  lonRange = distance( latMin,  lonMin,  latMin,  lonMax)
  latRange = distance( latMin,  lonMin,  latMax,  lonMin)
  return  int((latRange // 500) +1), int((lonRange // 500) + 1)

#Select Rows According to their record time
def filterTime(st, et, f):
  noOKData = []
  selRows = []
  for row in f:
    time = turnStrToTime(row.split(',')[0])
    lon = float(row.split(',')[2])
    lat = float(row.split(',')[3])
    if ((lon > lonMax) or (lon < lonMin) or (lat > latMax) or (lat < latMin)):
      noOKData.append(row)
    elif(st <= time and time < et):
      selRows.append(row)
    elif(time >= et):
      break       
  return noOKData,selRows

#change data format from string to datetime for comparing them
def turnStrToTime(str):
  return datetime.datetime.strptime(str,'%Y-%m-%dT%H:%M:%S+08:00')

#turn GPS coordinate into Grid ID
def gridCoor(mlist, selRows, m, n):
  print "DataCount:%d" % len(selRows)
  for r in selRows:
    lon = float(r.split(',')[2])
    lat = float(r.split(',')[3])
    col = int(distance(latMax,lon,latMax,lonMin) / 500)
    row = int(distance(lat,lonMin,latMax,lonMin) / 500)
    if (row>= 0 and row<m and col>=0 and col<n):
      mlist[row][col]+=1

    else:
      continue
    # print 'id:%d' % (row * len(r) + col + 1)

 #check if data goes out of the range of Shanghai City
def checkData(f):
  noOKData = []
  isOK = True
  for row in f:
    lon = float(row.split(',')[2])
    lat = float(row.split(',')[3])
    if ((lon > lonMax) or (lon < lonMin)):
      isOK = False
      noOKData.append(row) 
    if ((lat > latMax) or (lat < latMin)):
      isOK = False
      noOKData.append(row)
      
  return isOK, noOKData   

def retrieveRows(startTime, endTime):
  candidates = {}  
  dataPath = os.path.join(os.getcwd(), 'TaxiData')
  m, n = numOfGrid() 
  for csvFile in os.listdir(dataPath):
    if '.csv' not in csvFile:
      continue

    f = open(os.path.join(dataPath, csvFile)).readlines()
    noOKRows, selRows = filterTime(turnStrToTime(startTime), turnStrToTime(endTime), f) 
      
    mlist = [[0 for col in range(n)] for row in range(m)] #initialize the matrix to 0

    gridCoor(mlist, selRows, m, n)
    candidates[csvFile[7:-4]] = np.array(mlist)
    # else:  #if the coordinates of GPS is out of range, print its rows
    print "File Name is: %s, rows that exceed boundary:%s" % (csvFile,noOKRows)

  return candidates    
   
def selectKTaxis(K, AccuGridData, candidates):
  taxiList = []
  if K >= len(candidates.keys()):
    taxiList = candidates.keys()
  else :
    while(len(taxiList)<K):
      maxRate = 0
      tempGrid = []
      taxiNo = ''
      for (taxi,grid) in candidates.iteritems():
        tempGrid = AccuGridData + grid
        rate = coverRate(tempGrid)
        if rate > maxRate:
          maxRate = rate
          taxiNo = taxi
          # print maxRate
      print '-----------------------------segmentation line-----------------------------'    
      taxiList.append(taxiNo)
      AccuGridData += candidates.pop(taxiNo) 
  return taxiList, coverRate(AccuGridData)

def printCan(cand):
  for (taxi,grid) in cand.iteritems():
    count = 0
    for row in grid:
      for col in row:
        if col > 0:
          count+=1
    print "Taxi: %s, Count:%d" % (taxi,count)

def main():
  startTime = '2007-02-01T08:00:00+08:00'
  endTime = '2007-02-01T10:00:00+08:00'

  cand = retrieveRows(startTime, endTime)
  #print len(cand.values()[0]),len(cand.values()[0][0])

  printCan(cand)

  #draw Pic 
  KList = [i for i in range(1,2)]
  covRates = []
  for K in KList:
    print "K=%s" % K
    AccuGridData = np.zeros((len(cand.values()[0]),len(cand.values()[0][0])),dtype=np.int)
    candidates = cand.copy()
    # Copy data into grid matrix for calculation, and record the taxi list
    taxiList, covRate = selectKTaxis(K,AccuGridData,candidates)
    covRates.append(covRate)
      
    print "K=%s,covRate=%s" % (K,covRate)

  plt.plot(KList,covRate) 

  plt.xlabel("K") 
  plt.ylabel("CoverRate") 
  plt.title("K-CoverRate")

  # plt.show()    
  plt.savefig("K-CoverRate.png",dpi=300,format="png") 

if __name__ == '__main__':
  main()



