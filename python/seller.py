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

hosturl = 'http://localhost:8101'
contract_addr = '0x65ecdc40d3f1cd8a352ef4db4dad4b975cf61f17'
# identiy the file type

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
	print data
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
	m_result = de_result['result']
	# pprint.pprint(addr)
	return m_result

#Regist as a seller
def registSeller(action):
	c = pycurl.Curl()
	raw_result = BytesIO()
	c.setopt(c.URL, hosturl)
	my_addr = getLocalAddr()
	code_getpath_raw = getSha3Data("registSeller()")
	code_getpath = code_getpath_raw[:10]

	#get all params needed in this transaction
	#first, get coinbase address

	params = [{"from": my_addr, "to": contract_addr,"data": code_getpath}]


	data = json.dumps({'jsonrpc':'2.0','method':action,'params':params,'id':1})
	print data
	c.setopt(pycurl.POST, 1)
	c.setopt(c.POSTFIELDS, data)
	c.setopt(c.WRITEFUNCTION, raw_result.write)

	c.perform()
	#Decode result
	de_result = json.loads(raw_result.getvalue())
	#abstract the addr alone
	m_result = de_result['result']
	# convert hex to string
	# data_change = binascii.a2b_hex(m_result[2:])
	data_change = int(m_result,16)

	return data_change


#get status from contract

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
	m_result = de_result['result']
	# convert hex to string
	datapath = binascii.a2b_hex(m_result[2:])

	c.perform()
	c.close()
	return datapath

def finish(id):
	c = pycurl.Curl()
	raw_result = BytesIO()
	c.setopt(c.URL, hosturl)
	my_addr = getLocalAddr()
	code_getpath_raw = getSha3Data("finish(int256)")
	code_getpath = code_getpath_raw[:10]
	arg_01_raw = hex(id)
	arg_01 = (66 - len(arg_01_raw)) * '0' + arg_01_raw[2:]
	code_getpath_full = code_getpath + arg_01
	#get all params needed in this transaction
	#first, get coinbase address

	params = [{"from": my_addr, "to": contract_addr,"data": code_getpath_full}]


	data = json.dumps({'jsonrpc':'2.0','method':'eth_sendTransaction','params':params,'id':1})
	print data
	c.setopt(pycurl.POST, 1)
	c.setopt(c.POSTFIELDS, data)
	c.setopt(c.WRITEFUNCTION, raw_result.write)

	c.perform()
	#Decode result
	de_result = json.loads(raw_result.getvalue())
	#abstract the addr alone
	# m_result = de_result['result']
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

#checking the data validity

def checkData(datapath):
	# datapath = getPath("input")

	datapath = "/Users/joseph_zhang/ether/sketch/dataProcess/book.jpg"

	re = filetype(datapath)
	return re


#convert bmp to jpg

def processData(datapath):
	img = Image(filename = datapath)
	img.save(filename = "/home/joseph/ether/test/book.jpg")

def processBranchData(num,datapath):
	i = 0
	while (i<num):
		processData(datapath)
		i += 1

#Create a filter
def createNewBlockFilter():
	c = pycurl.Curl()
	c.setopt(c.URL, hosturl)
	raw_result = BytesIO()

	# post_data = {'jsonrpc':'2.0','method':'web3_clientVersion','params':[],'id':67}
	data = json.dumps({'jsonrpc':'2.0','method':'eth_newBlockFilter','params':[],'id':73})
	print data
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



registSeller("eth_sendTransaction")
fid = createNewBlockFilter()
sid = 0
bmpnum = 10
idle_flag = True
datapath = "/home/joseph/ether/test/book.bmp"
m_status = "idle"
print "registing...Please wait..."
time.sleep(10)

while True:
	m_filter = getFilterChanges(fid)
	# print m_filter
	if (m_filter == []):
		time.sleep(1)
		print getStatus(sid)
	else:
		sid = registSeller("eth_call")
		sid -= 1
		print "I'm seller " + str(sid)
		m_status = getStatus(sid)
		print m_status
		print idle_flag
		if ((m_status[:len("processing...")] == "processing...") and (idle_flag == True)):
			print "start processing..."
			# processData(datapath)
			processBranchData(bmpnum,datapath)
			idle_flag = False
			finish(sid)
		elif((m_status[:len("processing...")] == "processing...") and (idle_flag == False)):
			finish(sid)
		elif(m_status[:len("finished")] == "finished"):
			idle_flag = True
			print getStatus(sid)
			print "The data process is complete!"
		else:
			print "wait a minute..."

# print registSeller("eth_sendTransaction")
# print registSeller("eth_call")
# print getStatus(0)
# m = m[:len("processing...")]

# print finish(0)

# registSeller("eth_sendTransaction")

# datapath = "/Users/joseph_zhang/ether/sketch/dataProcess/test.bmp"
# processData(datapath)
















    # try:
    #     while True:
    #         time.sleep(1)
    # except KeyboardInterrupt:
    #     observer.stop()
    # observer.join()
