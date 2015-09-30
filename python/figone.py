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

def processData(datapath):
	img = Image(filename = datapath)
	img.save(filename = "/Users/joseph_zhang/ether/test/abc.jpg")

datapath = "/Users/joseph_zhang/ether/test/abc.bmp"
processData(datapath)
