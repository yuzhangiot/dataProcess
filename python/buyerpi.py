import pycurl
import json
import binascii
import subprocess
import time
import struct
import os
from io import BytesIO
from random import randint
import pprint
try:
    # python 3
    from urllib.parse import urlencode
except ImportError:
    # python 2
    from urllib import urlencode

hosturl = 'http://localhost:8101'
contract_addr = '0x65ecdc40d3f1cd8a352ef4db4dad4b975cf61f17'
home = "/home/pi/"
txtfilename = "python/data/singleSMERdata_50.txt"

typeList = {
        "52617221": "EXT_RAR",
        "504B0304": "EXT_ZIP",
        "FFD8FF"  : "EXT_JPG",
        "424D"    : "EXT_BMP",
        "49492A00": "EXT_TIF",
        "89504E47": "EXT_PNG"
    }

def getVersion():
	c = pycurl.Curl()
	c.setopt(c.URL, hosturl)
	raw_result = BytesIO()

	# post_data = {'jsonrpc':'2.0','method':'web3_clientVersion','params':[],'id':67}
	data = json.dumps({'jsonrpc':'2.0','method':'web3_clientVersion','params':[],'id':67})
	pprint.pprint(data)
	# Form data must be provided already urlencoded.
	# postfields = urlencode(post_data)
	# Sets request method to POST,
	# Content-Type header to application/x-www-form-urlencoded
	# and data to send in request body.
	c.setopt(pycurl.POST, 1)
	c.setopt(c.POSTFIELDS, data)
	c.setopt(c.WRITEFUNCTION, raw_result.write)

	c.perform()
	c.close()
	# get raw path from contract
	#def getpath():
	de_result = json.loads(raw_result.getvalue())
	#abstract the addr alone
	addr = de_result['result']
	# pprint.pprint(addr)
	return addr

# Get local address
def getLocalAddr():
	c = pycurl.Curl()
	raw_result = BytesIO()
	c.setopt(c.URL, hosturl)
	data = json.dumps({"jsonrpc":"2.0","method":"eth_coinbase","params":[],"id":64})
	c.setopt(pycurl.POST, 1)
	c.setopt(c.POSTFIELDS, data)
	c.setopt(c.WRITEFUNCTION, raw_result.write)

	c.perform()
	c.close()
	#Decode result
	de_result = json.loads(raw_result.getvalue())
	#abstract the addr alone
	addr = de_result['result']
	# pprint.pprint(addr)
	return addr

#Get the sha3 data from string
def getSha3Data(strData):
	c = pycurl.Curl()
	raw_result = BytesIO()
	c.setopt(c.URL, hosturl)
	#convert string to hex string
	hex_data = binascii.b2a_hex(strData)
	 
	data = json.dumps({"jsonrpc":"2.0","method":"web3_sha3","params":[hex_data],"id":64})
	c.setopt(pycurl.POST, 1)
	c.setopt(c.POSTFIELDS, data)
	c.setopt(c.WRITEFUNCTION, raw_result.write)

	c.perform()
	c.close()
	#Decode result
	de_result = json.loads(raw_result.getvalue())
	#abstract the addr alone
	m_result = de_result.get('result')
	# pprint.pprint(addr)
	return m_result

#Get available sellers
def getSeller():
	c = pycurl.Curl()
	c.setopt(c.URL, hosturl)
	raw_result = BytesIO()
	params = [contract_addr,"0x0"]

	# post_data = {'jsonrpc':'2.0','method':'web3_clientVersion','params':[],'id':67}
	data = json.dumps({'jsonrpc':'2.0','method':'eth_getStorageAt','params':params,'id':1})
	pprint.pprint(data)
	# Form data must be provided already urlencoded.
	# postfields = urlencode(post_data)
	# Sets request method to POST,
	# Content-Type header to application/x-www-form-urlencoded
	# and data to send in request body.
	c.setopt(pycurl.POST, 1)
	c.setopt(c.POSTFIELDS, data)
	c.setopt(c.WRITEFUNCTION, raw_result.write)

	c.perform()
	c.close()
	# get raw path from contract
	#def getpath():
	de_result = json.loads(raw_result.getvalue())
	#abstract the addr alone
	m_result = de_result.get('result')
	# data_change = int(m_result,16)
	# pprint.pprint(addr)
	return m_result


#regist as a user
def registUser(id,action):
	c = pycurl.Curl()
	raw_result = BytesIO()
	c.setopt(c.URL, hosturl)
	my_addr = getLocalAddr()
	code_getpath_raw = getSha3Data("registBuyer(int256)")
	code_getpath = code_getpath_raw[:10]
	arg_01_raw = hex(id)
	arg_01 = (66 - len(arg_01_raw)) * '0' + arg_01_raw[2:]
	code_getpath_full = code_getpath + arg_01
	#get all params needed in this transaction
	#first, get coinbase address

	params = [{"from": my_addr, "to": contract_addr,"data": code_getpath_full}]


	data = json.dumps({'jsonrpc':'2.0','method':action,'params':params,'id':1})
	pprint.pprint(data)
	c.setopt(pycurl.POST, 1)
	c.setopt(c.POSTFIELDS, data)
	c.setopt(c.WRITEFUNCTION, raw_result.write)

	c.perform()
	#Decode result
	de_result = json.loads(raw_result.getvalue())
	#abstract the addr alone
	m_result = de_result.get('result')
	# convert hex to string
	# data_change = binascii.a2b_hex(m_result[2:])
	data_change = int(m_result,16)

	return data_change

def getStatus(id):
	c = pycurl.Curl()
	raw_result_path = BytesIO()
	raw_result_url = BytesIO()
	c.setopt(c.URL, hosturl)
	my_addr = getLocalAddr()
	code_getpath_raw = getSha3Data("getStatus(int256)")
	code_getpath = code_getpath_raw[:10]
	arg_01_raw = hex(id)
	arg_01 = (66 - len(arg_01_raw)) * '0' + arg_01_raw[2:]
	code_getpath_full = code_getpath + arg_01
	#get all params needed in this transaction
	#first, get coinbase address

	params = [{"to": contract_addr,"data": code_getpath_full}]


	data = json.dumps({'jsonrpc':'2.0','method':'eth_call','params':params,'id':1})
	c.setopt(pycurl.POST, 1)
	c.setopt(c.POSTFIELDS, data)
	c.setopt(c.WRITEFUNCTION, raw_result_path.write)

	c.perform()
	#Decode result
	de_result = json.loads(raw_result_path.getvalue())
	#abstract the addr alone
	m_result = de_result.get('result')
	# convert hex to string
	datapath = binascii.a2b_hex(m_result[2:])

	c.perform()
	c.close()
	return datapath

def transData(datapath,sendDataurl):
	# p = subprocess.call(["scp",datapath,sendDataurl])
	os.system("scp" + " " + datapath + " " + sendDataurl)
	# if (p):
	# 	return 1
	# else:
	# 	return 0

def callforProcess(id):
	c = pycurl.Curl()
	raw_result = BytesIO()
	c.setopt(c.URL, hosturl)
	my_addr = getLocalAddr()
	code_getpath_raw = getSha3Data("callforProcess(int256)")
	code_getpath = code_getpath_raw[:10]
	arg_01_raw = hex(id)
	arg_01 = (66 - len(arg_01_raw)) * '0' + arg_01_raw[2:]
	code_getpath_full = code_getpath + arg_01
	#get all params needed in this transaction
	#first, get coinbase address

	# params = [{"from": my_addr, "to": contract_addr,"value":hex(3000000),"data": code_getpath_full}]
	params = [{"from": my_addr, "to": contract_addr,"value":30000000,"data": code_getpath_full}]


	data = json.dumps({'jsonrpc':'2.0','method':'eth_sendTransaction','params':params,'id':1})
	pprint.pprint(data)
	c.setopt(pycurl.POST, 1)
	c.setopt(c.POSTFIELDS, data)
	c.setopt(c.WRITEFUNCTION, raw_result.write)

	c.perform()
	#Decode result
	de_result = json.loads(raw_result.getvalue())
	#abstract the addr alone
	# m_result = de_result.get('result')
	# convert hex to string
	# data_change = binascii.a2b_hex(m_result[2:])

	return de_result

def bytes2hex(bytes):
    num = len(bytes)
    hexstr = u""
    for i in range(num):
        t = u"%x" % bytes[i]
        if len(t) % 2:
            hexstr += u"0"
        hexstr += t
    return hexstr.upper()

def filetype(filename):
    binfile = open(filename, 'rb')
    tl = typeList
    ftype = 'unknown'
    for hcode in tl.keys():
        numOfBytes = len(hcode) / 2
        binfile.seek(0)
        hbytes = struct.unpack_from("B"*numOfBytes, binfile.read(numOfBytes))
        f_hcode = bytes2hex(hbytes)
        if f_hcode == hcode:
            ftype = tl[hcode]
            break
    binfile.close()
    return ftype

def checkData(datapath):
	re = filetype(datapath)
	return re


def confirmation(id):
	c = pycurl.Curl()
	raw_result = BytesIO()
	c.setopt(c.URL, hosturl)
	my_addr = getLocalAddr()
	code_getpath_raw = getSha3Data("confirm(int256)")
	code_getpath = code_getpath_raw[:10]
	arg_01_raw = hex(id)
	arg_01 = (66 - len(arg_01_raw)) * '0' + arg_01_raw[2:]
	code_getpath_full = code_getpath + arg_01
	#get all params needed in this transaction
	#first, get coinbase address

	params = [{"from": my_addr, "to": contract_addr,"data": code_getpath_full}]


	data = json.dumps({'jsonrpc':'2.0','method':"eth_sendTransaction",'params':params,'id':1})
	pprint.pprint(data)
	c.setopt(pycurl.POST, 1)
	c.setopt(c.POSTFIELDS, data)
	c.setopt(c.WRITEFUNCTION, raw_result.write)

	c.perform()
	#Decode result
	de_result = json.loads(raw_result.getvalue())
	#abstract the addr alone
	m_result = de_result.get('result')
	# convert hex to string
	data_change = binascii.a2b_hex(m_result[2:])
	# data_change = int(m_result,16)

	return data_change

	#Create a filter
def createNewBlockFilter():
	c = pycurl.Curl()
	c.setopt(c.URL, hosturl)
	raw_result = BytesIO()

	# post_data = {'jsonrpc':'2.0','method':'web3_clientVersion','params':[],'id':67}
	data = json.dumps({'jsonrpc':'2.0','method':'eth_newBlockFilter','params':[],'id':73})
	# Form data must be provided already urlencoded.
	# postfields = urlencode(post_data)
	# Sets request method to POST,
	# Content-Type header to application/x-www-form-urlencoded
	# and data to send in request body.
	c.setopt(pycurl.POST, 1)
	c.setopt(c.POSTFIELDS, data)
	c.setopt(c.WRITEFUNCTION, raw_result.write)

	c.perform()
	c.close()
	# get raw path from contract
	#def getpath():
	de_result = json.loads(raw_result.getvalue())
	#abstract the addr alone
	mid = de_result['result']
	# pprint.pprint(addr)
	return mid

def getFilterChanges(fid):
	c = pycurl.Curl()
	c.setopt(c.URL, hosturl)
	raw_result = BytesIO()

	# post_data = {'jsonrpc':'2.0','method':'web3_clientVersion','params':[],'id':67}
	data = json.dumps({'jsonrpc':'2.0','method':'eth_getFilterChanges','params':[fid],'id':73})
	# Form data must be provided already urlencoded.
	# postfields = urlencode(post_data)
	# Sets request method to POST,
	# Content-Type header to application/x-www-form-urlencoded
	# and data to send in request body.
	c.setopt(pycurl.POST, 1)
	c.setopt(c.POSTFIELDS, data)
	c.setopt(c.WRITEFUNCTION, raw_result.write)

	c.perform()
	c.close()
	# get raw path from contract
	#def getpath():
	de_result = json.loads(raw_result.getvalue())
	#abstract the addr alone
	bid = de_result['result']
	# pprint.pprint(addr)
	return bid

def transBranchData(num,datapath,sentDataurl):
	i = 0
	datapathBr = ""
	while (i<num):
		datapathmid = datapath + str(i) + ".bmp" + " "
		datapathBr += datapathmid
		i += 1
	transData(datapathBr,sentDataurl)

def receiveBranchData(num,dataurl,revDatapath):
	i = 0
	dataurlBr = ""
	while (i<num):
		dataurlmid = dataurl + str(i) + ".jpg" + " "
		dataurlBr += dataurlmid
		i += 1
	transData(dataurlBr,revDatapath)


def buySingle(sellerid):
	while True:
		# seller_num = getSeller()
		# sid = randint(0,seller_num-1)
		sid = sellerid
		pprint.pprint("No. " + str(sid) + " has been choosen")
		registUser(sid,"eth_sendTransaction")
		time.sleep(5)
		suc = registUser(sid,"eth_call")
		if (suc == 1):
			pprint.pprint("No. " + str(sid) + " has been successful connected!")
			break
		else:
			pprint.pprint("No. " + str(sid) + " is busy, retry after 10s...")
			continue

	# transData(datapath,sentDataurl)
	transBranchData(bmpnum,datapath,sentDataurl)
	pprint.pprint("data transform complete!")
	pprint.pprint("ask for processing...")
	callforProcess(sid)
	processCount = 0
	proFlag = True
	confirmFlag = False
	fid = createNewBlockFilter()
	while True:
		m_filter = getFilterChanges(fid)
		if (m_filter == []):
			time.sleep(5)
			pprint.pprint(getStatus(sid))
		else:
			m_status = getStatus(sid)
			pprint.pprint(m_status)
			if (m_status[:len("finished")] == "finished" and (confirmFlag==False)):
				# transData(getDataurl,getdatapath)
				receiveBranchData(bmpnum,getDataurl,getdatapath)
				c_result = checkData(checkDatapath)
				if (c_result == "EXT_JPG"):
					confirmation(sid)
					confirmFlag = True
					pprint.pprint(m_status)
					pprint.pprint("data check complete")
				else:
					pprint.pprint(m_status)
					pprint.pprint("data check failed,retry...")
					callforProcess(sid)
			elif (m_status[:len("processing...")] == "processing..."):
				pprint.pprint("right now, a minute!")
			elif(processCount > 3 and proFlag):
				callforProcess(sid)
				proFlag = False
			elif (m_status[:len("finished")] == "finished" and (confirmFlag==True)):
				confirmation(sid)
			elif (m_status[:len("idle")] == "idle" and (confirmFlag==True)):
				confirmFlag = False
				break
			else:
				pprint.pprint("wait a minute, data is processing...")
				processCount += 1
				if(processCount%3 == 0):
					proFlag = True

sid=0
bmpnum = 50
datapath = home + "ether/test/book"
getdatapath = home + "ether/test/"
checkDatapath = home + "ether/test/book0.jpg"
sentDataurl = "joseph@192.168.10.8:/home/joseph/ether/test/"
getDataurl = "joseph@192.168.10.8:/home/joseph/ether/test/book"

mytime = []
i=0
while (i < 75):
	old = time.time()
	buySingle(38)
	new = time.time()
	add = new - old
	mytime.append(add)
	i += 1

file_object = open(txtfilename, 'w')
for item in mytime:
	file_object.write('%s\n' % item)
file_object.close()

# getVersion()





# datapath = "/Users/joseph_zhang/ether/sketch/dataProcess/test.jpg"
# print checkData(datapath)
# time.sleep(2)
# print getSeller()
# print registUser(0,"eth_sendTransaction")
# print registUser(0,"eth_call")
# print getStatus(0)
# print callforProcess(0)
# print confirmation(0)




