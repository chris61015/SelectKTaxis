#encoding=utf8
import operator
import os

def sortByTaxi_No (fileName):
	try:
		table = []
		for line in open(fileName).readlines():
			row = line.split()
			table.append(row)
		
	except Exception, e:
		print e
	else:
		return sorted(table, key=operator.itemgetter(1))
	finally:
		pass

def writeFile(taxiNo, content, folderPath):
	try:
		fileName = "TaxiNo_%s.csv" % (taxiNo)
		filePath = os.path.join(folderPath,fileName)
		outputFile = open(filePath, 'w')
		outputFile.writelines("\n".join(content))

	except Exception, e:
		print e
	else:
		content[:] = []
	finally:
		outputFile.close()


def writeFileByTaxiNo(row, content, taxiNo, folderPath):

	if (taxiNo!="" and row[1]!=taxiNo):
		writeFile(taxiNo, content, folderPath)

	content.append(",".join(row))
	return row[1] 


def changeTimeStamp(data, folderPath, initTime): 
	
	content = []
	taxiNumber = ""
	for row in data:
		row[0]= '%sT%s+08:00' % (initTime,convertTime(row[0]))
		taxiNumber = writeFileByTaxiNo(row, content,taxiNumber, folderPath)
	writeFile(taxiNumber, content, folderPath) # print the last number of Taxi	

def convertTime(sec):
	second = complementZero(int(sec) % 60)
	minute = complementZero(int(sec) % (60 * 60) / 60)
	hour = complementZero(int(sec) / (60*60))

	return hour+":"+minute+":"+second

def complementZero(num):
	if num < 10:
		return "0"+str(num)
	else:
		return str(num)

if __name__=='__main__':

	folderPath = './TaxiData'
	if not os.path.exists(folderPath):
		os.mkdir(folderPath)

	sortedData = sortByTaxi_No("metadata-Taxi_Shanghai_2007-02-01.txt")
	changeTimeStamp(sortedData, folderPath, "2007-02-01")
