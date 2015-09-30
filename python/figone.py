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

def processData(datapath):
	img = Image(filename = datapath)
	img.save(filename = "/Users/joseph_zhang/ether/test/test.jpg")

def drawPic(mt):
	figure(figsize=(8,6), dpi=80)

	subplot(1,1,1)

	X = np.linspace(1, 100, 100,endpoint=True)
	# C,S = np.cos(X), np.sin(X)

	plot(X, mt, color="blue", linewidth=1.0, linestyle="-")

	# plot(X, S, color="green", linewidth=1.0, linestyle="-")

	xlim(0,100.0)

	xticks(np.linspace(0,100,11,endpoint=True))

	ylim(0.030,0.040)

	yticks(np.linspace(0.000,0.10,11,endpoint=True))

	# savefig("exercice_2.png",dpi=72)

	show()

datapath = "/Users/joseph_zhang/ether/test/test.bmp"
count = 0
mytime = []

while (count < 100):
	old = time.clock()
	processData(datapath)
	new = time.clock()
	add = new - old
	mytime.append(add)
	count += 1

mt = np.array(mytime)
# processData(datapath)
drawPic(mt)



