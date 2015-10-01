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
filename = "python/data/pidata.txt"

def processData(datapath):
	img = Image(filename = datapath)
	img.save(filename = home + "ether/test/test.jpg")


def storeData():
	datapath = home + "ether/test/test.bmp"
	count = 0
	mytime = []

	while (count < 100):
		old = time.clock()
		processData(datapath)
		new = time.clock()
		add = new - old
		mytime.append(add)
		count += 1

	# mt = np.array(mytime)

	file_object = open(filename, 'w')
	for item in mytime:
		file_object.write('%s\n' % item)
	file_object.close()

def readData():
	result=[]
	with open(filename,'r') as f:
		for line in f:
			result.append(map(float,line.split(',')))
	return result


storeData()
# processData(datapath)



