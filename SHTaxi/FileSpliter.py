#encoding=utf8
import os

class splitFile(object):
	"""docstring for splitFile"""
	def __init__(self, fileName):
		super(splitFile, self).__init__()
		self.fileName = fileName		

	def split_File(self, numOfFile):
		if self.fileName and os.path.exists(self.fileName):
			try:
				lineObj = open(self.fileName).readlines()
				numOfLines = len(lineObj)

				linesPerFile = numOfLines / numOfFile + 1

				line_Cnt = 0;
				file_Cnt = 1;
				temp_content=[]

				for line in lineObj:
					if (line_Cnt < linesPerFile):
						line_Cnt+=1
					else:
						self.write_File(file_Cnt, temp_content)
						file_Cnt+=1
						temp_content=[]
						line_Cnt=0
					temp_content.append(line)		

			except Exception, e:
				print(e);
			else:
				self.write_File(file_Cnt, temp_content)
			finally:
				pass	
		else:
			print('The file does not exist')

	def write_File(self, file_Cnt, content):
		smallFileName = "part" + str(file_Cnt) + ".txt"
		try:
			f = open(smallFileName, 'w')
			f.writelines(content)			
		except Exception, e:
			print (e)
		else:
			pass
		finally:
			pass


if __name__=='__main__':
	sf = splitFile("Taxi_Shanghai.csv")
	sf.split_File(5);