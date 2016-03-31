import os

def main():
  
  dataPath = os.path.join(os.getcwd(), 'TaxiData')
  gsxPath = os.path.join(os.getcwd(), 'gsvData')

  if not os.path.exists(gsxPath):
    os.mkdir(gsxPath)

  sumOfLines = 0
  for csvFile in os.listdir(dataPath): 
    if '.csv' not in csvFile:
      continue
    f =  open(os.path.join(dataPath, csvFile)).readlines()
    print 'File Name:%s, LineCount:%d' % (csvFile ,len(f))  
    sumOfLines += len(f)
  
  print 'Sum Of Lines: %d' % sumOfLines
 
if __name__ == '__main__':
  # main()
  for i in range(10000):
    print i