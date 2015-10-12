import pycurl
import json
import binascii
import subprocess
import struct
import time
from io import BytesIO
import pprint
from wand.image import Image
import numpy as np
from pylab import *
try:
    # python 3
    from urllib.parse import urlencode
except ImportError:
    # python 2
    from urllib import urlencode
#convert bmp to jpg
home = "/Users/joseph_zhang/ether/sketch/gitdataprocess/"
# bmpnum = "1"
# txtfilename = "python/data/cool4data.txt"

def processData(datapath):
	img = Image(filename = datapath)
	img.save(filename = home + "ether/test/book.jpg")

def drawPic(smer,pi,cool4):
	figure(figsize=(8,6), dpi=80)

	subplot(1,1,1)

	X = np.linspace(1, 50, 50,endpoint=True)
	# C,S = np.cos(X), np.sin(X)

	plot(X, smer, color="blue", linewidth=1.5, linestyle="-", label="SMER")
	plot(X, pi, color="green", linewidth=1.5, linestyle=":", label="RaspberryPi")
	plot(X, cool4, color="red", linewidth=1.5, linestyle="--", label="Linux Server")

	# plot(X, S, color="green", linewidth=1.0, linestyle="-")

	xlim(0,50.0)

	xticks(np.linspace(0,50,6,endpoint=True))

	ylim(-10,150)

	yticks(np.linspace(-10.000,150,17,endpoint=True))
	legend(loc='upper left')

	# savefig("exercice_2.png",dpi=72)

	show()

def drawPicTen(smer,pi,cool4):
	figure(figsize=(8,6), dpi=80)

	subplot(1,1,1)

	X = np.linspace(1, 50, 50,endpoint=True)

	plot(X, smer, color="blue", linewidth=1.5, linestyle="-", label="SMER")
	plot(X, pi, color="green", linewidth=1.5, linestyle=":", label="RaspberryPi")
	plot(X, cool4, color="red", linewidth=1.5, linestyle="--", label="Linux Server")

	xlim(0,50.0)
	xticks(np.linspace(0,50,6,endpoint=True))

	ylim(-20,360)
	yticks(np.linspace(-20.000,360,20,endpoint=True))
	legend(loc='upper left')

	show()

def drawPicFifteen(smer,pi,cool4):
	figure(figsize=(8,6), dpi=80)

	subplot(1,1,1)

	X = np.linspace(1, 50, 50,endpoint=True)

	plot(X, smer, color="blue", linewidth=1.5, linestyle="-", label="SMER")
	plot(X, pi, color="green", linewidth=1.5, linestyle=":", label="RaspberryPi")
	plot(X, cool4, color="red", linewidth=1.5, linestyle="--", label="Linux Server")

	xlim(0,50.0)
	xticks(np.linspace(0,50,6,endpoint=True))

	ylim(-20,650)
	yticks(np.linspace(-40.000,760,21,endpoint=True))
	legend(loc='upper left')

	show()

def drawPicColum(single,multi):
	figure(figsize=(8,8), dpi=80)

	subplot(1,1,1)

	n = 2
	X = np.arange(n)
	# Y1 = (1-X/float(n)) * np.random.uniform(0.5,1.0,n)
	# Y2 = (1-X/float(n)) * np.random.uniform(0.5,1.0,n)
	Y = [single,multi]

	bar(X, Y, facecolor='#9999ff', edgecolor='white')
	# bar(X, +Y2, facecolor='#ff9999', edgecolor='white', label="RaspberryPi")

	for x,y in zip(X,Y):
		text(x+0.4, y+0.05, '%.2f' % y, ha='center', va= 'bottom')

	xticks([0.3, 1.4],
       [r'$\"single SMER system"$', r'$+\"multi-SMER system"$'])
	xlim(-0.3,2.3)
	ylim(0.0,+1500.00)
	# legend(loc='upper left')

	show()

def drawPicEarn(cool0,cool4,ubuntu):
	figure(figsize=(8,8), dpi=80)

	subplot(1,1,1)

	# Z = (cool0,cool4,ubuntu)
	# pie(Z)
	# legend(loc='upper left')
	figure(1, figsize=(6,6))
	ax = axes([0.1, 0.1, 0.8, 0.8])
	labels = 'Server01', 'Server02', 'Labtop'
	# summy = cool0 + cool4 + ubuntu
	# cool0_str = str(cool0)
	# cool0 = float(cool0_str[:6])
	# cool0 *= 1000
	# cool4_str = str(cool4)
	# cool4 = float(cool4_str[:5])
	# cool4 *= 100
	# ubuntu_str = str(ubuntu)
	# ubuntu = float(ubuntu_str[:1])
	fracs = [cool0, cool4, ubuntu]
	total = sum(fracs)
	explode=(0.05, 0, 0)
	pie(fracs, explode=explode, labels=labels,
	    autopct=lambda(p): '{:.0f}'.format(p * total / 100),
	    shadow=True, startangle=90)
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
	sortlist = sorted(numlist)
	midnum = sortlist[49]
	for item in numlist:
		if (item[0]>midnum[0]):
			continue
		else:
			result.append(item)
	return result

def summoney(numlist):
	result = 0
	for item in numlist:
		result += item[0]
	return result

def readDataFromFile(bmpnum):
	bmpnum = str(bmpnum)
	smerfile = home + "python/data/singleSMERdata_" + bmpnum + ".txt"
	smerdata = readData(smerfile)
	pifile = home + "python/data/pidata_" + bmpnum + ".txt"
	pidata = readData(pifile)
	cool4file = home + "python/data/cool4data_" + bmpnum + ".txt"
	cool4data = readData(cool4file)
	return smerdata,pidata,cool4data

def drawFigone():
	smerdata,pidata,cool4data = readDataFromFile(1)
	smerdatafilter = myfilter(smerdata)
	pidatafilter = pidata[:50]
	cool4datafilter = cool4data[:50]
	drawPic(smerdatafilter,pidatafilter,cool4datafilter)

def drawFigTwo():
	smerdata,pidata,cool4data = readDataFromFile(10)
	smerdatafilter = myfilter(smerdata)
	# print max(smerdata)
	drawPicTen(smerdatafilter,pidata,cool4data)

def drawFigThree():
	smerdata,pidata,cool4data = readDataFromFile(50)
	smerdatafilter = myfilter(smerdata)
	drawPicFifteen(smerdatafilter,pidata,cool4data)

def drawFigSix():
	multismerdata = readData(home + "python/data/multiSMERdata_10.txt")
	singlesmerdata = readData(home + "python/data/singleSMERdata_200.txt")
	multismerdata_avr = multismerdata[0]
	singlesmerdata_avr = np.array(singlesmerdata[0])
	print int(multismerdata_avr[0])
	print int(singlesmerdata_avr[0])
	drawPicColum(int(singlesmerdata_avr[0]),int(multismerdata_avr[0]))

def drawFigSeven():
	cool0_earn = readData(home + "python/data/multiSMERearn_cool0.txt")
	cool4_earn = readData(home + "python/data/multiSMERearn_cool4.txt")
	ubuntu_earn = readData(home + "python/data/multiSMERearn_ubuntu.txt")
	cool0_earn_sum = summoney(cool0_earn)
	cool4_earn_sum = summoney(cool4_earn)
	ubuntu_earn_sum = summoney(ubuntu_earn)

	drawPicEarn(cool0_earn_sum,cool4_earn_sum,ubuntu_earn_sum)
	
# drawFigone()
# drawFigTwo()
# drawFigThree()
# drawFigSix()
drawFigSeven()


	# print np.mean(smerdatafilter)
	# print np.mean(pidatafilter)
	# print np.mean(cool4datafilter)



# datapath = home + "ether/test/book.jpg"

# processData(datapath)


# old = time.time()
# print old
# time.sleep(1)
# new = time.time()
# add = new -old
# # add *= 10000
# print add


