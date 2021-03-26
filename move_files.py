# -*- coding: IBM850 -*- 
#### -*- coding: utf-8 -*-
### required - do no delete

# Script para automatizar movimiento de archivos a mes anterior
# Creado por Infraestructura de Sistemas el 14/11/2013

import subprocess
import optparse
import re
import os
import time
import sys
import datetime
import shutil

#produccion
#TARGETDIR = 'c:\\'

#desarrollo
TARGETDIR = '/home/wasuaje/Documentos/desarrollo/clasideu'


lista = ['jbarrera@eluniversal.com','wasuaje@eluniversal.com','sistemas-publicaciones@eluniversal.com']
lista = ['wasuaje@eluniversal.com']
#lista = ['jbarrera@eluniversal.com']

meses={1:'Enero',2:'Febrero', 3:'Marzo', 4:'Abril', 5:'Mayo', 6:'Junio', \
			7:'Julio', 8:'Agosto', 9:'Septiembre', 10:'Octubre',11:'Noviembre', 12:'Diciembre'}
         
def creartxt():
    archi=open('log_mv.txt','w')
    archi.close()

def write_file(newLine):
    file = open("log_mv.txt", "a")
    file.write(newLine)
    file.close()

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
		s = smtplib.SMTP('10.3.0.130')		
		s.sendmail(msg['From'], mailto, msg.as_string())
		s.quit()


#se crea el archivo del log de trabajo
creartxt()	
#Obtener fecha actual
curdate= datetime.date.today()
#separo la fecha en dia mes año
curyear=curdate.year
curmonth=curdate.month
curmonthname=meses[curmonth]

linea="Comienzo de proceso: %s" % curdate
write_file(linea+"\n")


if curmonth == 1:              #Para mes de enero, restar uno al año
	prevmonthname=meses[12]
	curyear=curdate.year-1	
	prevmonth=12
else:
	prevmonthname=meses[curmonth-1]
	prevmonth=curmonth-1
# **************** para efecto de pruebas ******************
#	
curmonthname=meses[6]
prevmonthname=meses[5]
prevmonth=5
#
# **** fin data de prueba comentar para produccion *********

dirsrc=os.path.join(TARGETDIR,curmonthname+"_"+str(curyear))
dirtarget=os.path.join(TARGETDIR,prevmonthname+"_"+str(curyear))

filelist=[]

#archivos tipo *31102013.txt  *mesaño.txt
if os.path.exists(dirsrc) and os.path.exists(dirtarget):	
	for base,dirs,files in os.walk(dirsrc):
		for fl in files:			
   			fn = os.path.join(base, fl)
   			_file='%02d' % prevmonth+str(curyear)   			
    			if _file in fn:    				
    				linea="Moviendo archivo: "+ fn +"a: "+dirtarget
    				write_file(linea+"\n")
    				try:
    					shutil.move(fn,dirtarget)
    					filelist.append(fn)
    				except:
    					pass
    				

if len(filelist) > 0:
	linea="Proceso finalizado con exito"
	write_file(linea+"\n")

	## se escribe en el log del programa
	linea="Enviando mensaje de finalizacion"
	write_file(linea+"\n")

	# se correo de notificacion
	subject = "EXITO - Movimiento de Archivos "
	message = "Se movieron los archivos correctamente de %s \n a %s  \n" % (dirsrc,dirtarget)
	message +="Lista de archivos\n" 
	for i in filelist:
		message +="\t %s \n" % i
	
else:
	subject = "ERROR - Movimiento de Archivos "
	message = "No se movieron los archivos, no se encontro ninguno"

send_mail(lista,subject,message)






