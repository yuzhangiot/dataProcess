import pycurl
import json
import binascii
import subprocess
import struct
import time
from io import BytesIO
import pprint
from wand.image import Image
from pylab import *
try:
    # python 3
    from urllib.parse import urlencode
except ImportError:
    # python 2
    from urllib import urlencode
#convert bmp to jpg
home = "/Users/joseph_zhang/ether/sketch/gitdataprocess/"
bmpnum = "1"
# txtfilename = "python/data/cool4data.txt"

def processData(datapath):
	img = Image(filename = datapath)
	img.save(filename = home + "ether/test/book.jpg")

def drawPic(smer,pi,cool4):
	figure(figsize=(8,6), dpi=80)

	subplot(1,1,1)

	X = np.linspace(1, 50, 50,endpoint=True)
	# C,S = np.cos(X), np.sin(X)

	plot(X, smer, color="blue", linewidth=1.0, linestyle="-", label="SMER")
	plot(X, pi, color="green", linewidth=1.0, linestyle=":", label="RaspberryPi")
	plot(X, cool4, color="red", linewidth=1.0, linestyle="--", label="Linux Server")

	# plot(X, S, color="green", linewidth=1.0, linestyle="-")

	xlim(0,50.0)

	xticks(np.linspace(0,50,6,endpoint=True))

	ylim(-10,190)

	yticks(np.linspace(-10.000,190,21,endpoint=True))
	legend(loc='upper left')

	# savefig("exercice_2.png",dpi=72)

	show()

def storeData():
	datapath = home + "ether/test/book.bmp"
	count = 0
	mytime = []

	while (count < 100):
		old = time.time()
		processData(datapath)
		new = time.time()
		add = new - old
		mytime.append(add)
		count += 1

	# mt = np.array(mytime)

	file_object = open(txtfilename, 'w')
	for item in mytime:
		file_object.write('%s\n' % item)
	file_object.close()

def readData(filename):
	result=[]
	with open(filename,'r') as f:
		for line in f:
			result.append(map(float,line.split(',')))
	return result

def myfilter(numlist):
	result = []
	for item in numlist:
		if (item[0]>112):
			continue
		else:
			result.append(item)
	return result

smerfile = home + "python/data/singleSMERdata_" + bmpnum + ".txt"
smerdata = readData(smerfile)
pifile = home + "python/data/pidata_" + bmpnum + ".txt"
pidata = readData(pifile)
cool4file = home + "python/data/cool4data_" + bmpnum + ".txt"
cool4data = readData(cool4file)


smerdatafilter = myfilter(smerdata)
pidatafilter = pidata[:50]
cool4datafilter = cool4data[:50]

drawPic(smerdatafilter,pidatafilter,cool4datafilter)


# datapath = home + "ether/test/book.jpg"

# processData(datapath)


# old = time.time()
# print old
# time.sleep(1)
# new = time.time()
# add = new -old
# # add *= 10000
# print add


