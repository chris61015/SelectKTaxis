import os
import datetime
import time
import math
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

#turn GPS coordinate into Grid ID
def gridCoor(gridSet, selRows, m, n):
  for r in selRows:
    lon = float(r.split(',')[2])
    lat = float(r.split(',')[3])
    col = int(distance(latMax,lon,latMax,lonMin) / 500)
    row = int(distance(lat,lonMin,latMax,lonMin) / 500)
    if (row>= 0 and row<m and col>=0 and col<n):
      gridSet.add((row * m + col + 1))
    else:
      print "Row:%s, Column:%s" % (row, col)
      continue
    
def selectKTaxis(K, candidates):
  AccuSetData = set()
  taxiList = []
  if K >= len(candidates.keys()):
    taxiList = candidates.keys()
  else :
    while(len(taxiList)<K):
      maxRate = 0
      tempGridSet = set()
      taxiNo = ''
      for (taxi,gridSet) in candidates.iteritems():
        # print "taxi:%s, len:%d" % (taxi, len(gridSet))
        tempGridSet = AccuSetData | gridSet
        rate = len(tempGridSet - AccuSetData) 
        if rate > maxRate:
          maxRate = rate
          taxiNo = taxi 

       # if selected taxis covers all road segments, we choose taxis that cover the most road segments   
      if taxiNo == '':
        # break
        for (taxi,gridSet) in candidates.iteritems():
          # print "(%s, %d)" % (taxi, len(gridSet))
          rate = len(gridSet) 
          if rate > maxRate:
            maxRate = rate
            taxiNo = taxi         
        # print taxiNo,maxRate
      taxiList.append(taxiNo)
      AccuSetData.update(candidates.pop(taxiNo))
    # print len(AccuSetData)
  return taxiList

def genSet(file):
  candidates = {}
  for line in file:
    data = line.strip('\r\n').split(' ')
    if 'node' in data[-1]:
      continue
    if data[1] in candidates.keys():
      dataSet = candidates[data[1]]
    else:
      dataSet = set()

    candidates[data[1]] = dataSet.union(set([data[-1]]))
  return candidates

def filterProbCars(file):
  candidates = {}
  for line in file:
    data = line.strip('\r\n').split(' ')
    if ('node' in data[-1]) or ('_0' not in data[1]):
      continue
    if data[1] in candidates.keys():
      dataSet = candidates[data[1]]
    else:
      dataSet = set()

    candidates[data[1]] = dataSet.union(set([data[-1]]))
  return candidates


def calAvgCoverRate(cand, carList):
  #create RoadPassRate Dictionary
  roadpassrate = {}
  for i in range(1, 289):
    roadpassrate['road-%d' % i] = 0

  for taxi in carList:
    traceSet = cand[taxi]
    for roadSeg in traceSet:
        roadpassrate[roadSeg] += 1

  # Sort key of Dictionary, and print its key-value pair
  # for key in sorted(roadpassrate, key=lambda x: int(x[4:]), reverse=True):
  #   print "%s: %s" % (key, roadpassrate[key])
  # print sum(roadpassrate.itervalues())
  print "AvgCoverRate: %f" % (float(sum(roadpassrate.itervalues()))/len(roadpassrate))  
  return roadpassrate

def drawBarChart(passRate, fileName):
  # print passRate
  data = Counter([v for v in passRate.itervalues()])
  # print data
  length = len(data)
  x = np.arange(1, length+1)
  labels = sorted([k for k in data.keys()])
  # print labels
  y = [data[index] for index in labels]
  # print y

  plt.xticks(x, labels)
  plt.xlabel('Road Pass Times')
  plt.ylabel('Count')
  plt.title("Road Pass Times-Count Chart")
  plt.bar(x,y,align = 'center')
  for a,b in zip(x, y):
    plt.text(a, b, str(b))
  plt.savefig("%s.png" % fileName.split('.')[0],dpi=300,format="png") 
  plt.clf()
  # plt.xlabel("K") 
  # plt.ylabel("CoverRate") 
  # plt.title("K-CoverRate")

  # # plt.show()    
  # plt.savefig("K-CoverRate.png",dpi=300,format="png") 
  

def main():

  #draw Pic 
  # KList = [i for i in range(1,2)]
  KList = [36]
  covRates = []
  
  dataPath = os.getcwd()
  for txtFile in os.listdir(dataPath):
    if '.txt' not in txtFile:
      continue

    f = open(os.path.join(dataPath, txtFile)).readlines()
    del f[0]
    cand = genSet(f)
 
    for K in KList:
      candidates = cand.copy()
      # Copy data into grid matrix for calculation, and record the taxi list
      taxiList = selectKTaxis(K,candidates)

      print "FileName = %s" % txtFile
      print "K = %s" % len(taxiList)
      print "taxiList:%s" % ','.join(taxiList)

      print "Greedy-Avg Cover Rate of Selected K Taxis"
      roadPassRate = calAvgCoverRate(cand, taxiList)
      drawBarChart(roadPassRate, txtFile)

    probCars = filterProbCars(f)
    print "probCars:%s" % ','.join(probCars)
    print "Avg Cover Rate of Probing Cars"
    probPassRate = calAvgCoverRate(cand, probCars)
    drawBarChart(probPassRate, 'Prob-'+txtFile)  
   
    print "------------------------Segmentation Line------------------------"

if __name__ == '__main__':
  main()



