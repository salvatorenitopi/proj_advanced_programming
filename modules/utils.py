import os
import cStringIO
import urllib
import ssl
from PIL import Image


def save_img (name ,str_img):
	with open (name, "wb") as fh:
		fh.write (str_img)


def open_img (str_img):
	i = cStringIO.StringIO()
	i.write(str_img)
	img = Image.open(i)
	img.show()
	

def secure_delete(path, passes=1):
	with open(path, "wb") as delfile:
		length = delfile.tell()
		for i in range(passes):
			delfile.seek(0)
			delfile.write(os.urandom(length))
	os.remove(path)


def download_file (url,filename):
	try: 
		r = urllib.URLopener()
		r.retrieve(url, filename)
	except:
		ssl._create_default_https_context = ssl._create_unverified_context
		r = urllib.URLopener()
		r.retrieve(url, filename)