import pycurl
import json
import binascii
import subprocess
import struct
import time
from io import BytesIO
import pprint
from wand.image import Image
try:
    # python 3
    from urllib.parse import urlencode
except ImportError:
    # python 2
    from urllib import urlencode
#convert bmp to jpg
home = "/home/pi/"
txtfilename = "python/data/pidata_50.txt"
bmpnum = 50

def processData(datapath):
	img = Image(filename = datapath)
	img.save(filename = home + "ether/test/book.jpg")

def processBranchData(num,datapath):
	i = 0
	while (i<num):
		processData(datapath)
		i += 1


def storeData():
	datapath = home + "ether/test/book.bmp"
	count = 0
	mytime = []

	while (count < 50):
		old = time.time()
		# processData(datapath)
		processBranchData(bmpnum,datapath)
		new = time.time()
		add = new - old
		mytime.append(add)
		count += 1

	# mt = np.array(mytime)

	file_object = open(txtfilename, 'w')
	for item in mytime:
		file_object.write('%s\n' % item)
	file_object.close()

def readData():
	result=[]
	with open(txtfilename,'r') as f:
		for line in f:
			result.append(map(float,line.split(',')))
	return result


storeData()
# processData(datapath)



