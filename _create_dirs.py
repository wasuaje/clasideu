# -*- coding: utf-8 -*-
### required - do no delete

#Script para ayudar a la automatizacion de la creacion de carpeta mensual para interfaces de SAP
#Creado por Wuelfhis Asuaje el 30/05/2012

import subprocess
import optparse
import re
import os
import time
import sys
import datetime

#directorio de destino de los archivos

#produccion
#TARGETDIR='c:\\'

#para pruebas
TARGETDIR='./'
meses={1:'Enero',2:'Febrero', 3:'Marzo', 4:'Abril', 5:'Mayo', 6:'Junio', \
			7:'Julio', 8:'Agosto', 9:'Septiembre', 10:'Octubre',11:'Noviembre', 12:'Diciembre'}

def runcmd(comando):
	p = subprocess.Popen(comando, shell=True, stdout=subprocess.PIPE)
	out = p.stdout.read().strip()
	return out  #This is the stdout from the shell command

def send_mail(emaillist,subject,message):
	import smtplib
	# Import the email modules we'll need
	from email.mime.text import MIMEText
	msg = MIMEText(message)

	for mail in emaillist:
		msg['Subject'] = subject
		msg['From'] = "SysAdmin@eluniversal.com"
		msg['To'] = mail
		mailto = mail
		# Send the message via our own SMTP server, but don't include the envelope header.
		s = smtplib.SMTP('10.3.0.130',25)		
		s.sendmail(msg['From'], mailto, msg.as_string())
		s.quit()
		
#Obtener nro del mes actual
curdate= datetime.date.today()
curyear=curdate.year
curmonth=curdate.month
curmonthname=meses[curmonth]
if curmonth == 1:
	prevmonthname=meses[12]
	curyear=curdate.year-1
else:
	prevmonthname=meses[curmonth-1]
	
dirtocreate=curmonthname+"_"+str(curyear)
dirtozip=prevmonthname+"_"+str(curyear)

#Si no existe el directorio lo creo
if not os.path.exists(TARGETDIR+dirtocreate):
    os.makedirs(TARGETDIR+dirtocreate)
else:
	print "Directorio ya existe"

#comprimir directorio anterior
import zipfile
myZipFile = zipfile.ZipFile(TARGETDIR+dirtozip+".zip", "w",zipfile.ZIP_DEFLATED )

# asi lo resolvieron en stackoverflow
target_dir = TARGETDIR+dirtozip
rootlen = len(target_dir) + 1
for base, dirs, files in os.walk(target_dir):
	for file in files:
		fn = os.path.join(base, file)
		print fn, fn[rootlen:]
		myZipFile.write(fn, fn[rootlen:])

myZipFile.close()
