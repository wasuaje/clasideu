# -*- coding: utf-8 -*-
"""
Script check_terfaces.py:
Author: Wuelfhis Asuaje
Fecha: 20-02-2014
Segun ASI-549
Para revisar si hay concordancia en las interfaces sap generadas
"""
"""
Los requerimientos:

los formatos de los archivos son los siguientes: 
cobeatra ddmmyyyy( fecha dia anterior).txt 
cobros ddmmyyyy( fecha dia anterior).txt 
complementa ddmmyyyy( fecha dia anterior).txt 
faccon ddmmyyyy( fecha dia anterior).txt 
faccre ddmmyyyy( fecha dia actual).txt 
faccreaq ddmmyyyy( fecha dia anterior).txt 
faceatra ddmmyyyy( fecha dia anterior).txt 
facint ddmmyyyy( fecha dia actual).txt 
faconnc ddmmyyyy( fecha dia anterior).txt 
facrep ddmmyyyy( fecha dia actual).txt 
notasdc ddmmyyyy( fecha dia anterior).txt 
prevencla ddmmyyyy( fecha dia actual).txt 
preventa ddmmyyyy( fecha dia actual).txt 

solo para estas el tamaño del archivo puede ser 0, pero deben estar en disco : 
Complementa 
faccreaq 
faconnc 
facrep 
notasdc 

Si cobros tiene registro faccon tambien deberia de tener registros. 
El total de interfaces generadas deberia ser 13. 
Si notasdc tiene registro faconnc tambien deberia de tener registros. 

"""
import  os
import datetime
from datetime import timedelta
import smtplib


def send_mail(emaillist,subject,message):        	
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

#ALGUNAS VARIABLES, LISTAS Y CONSTANTES QUE NECESITARE LUEGO
#lista = ['jbarrera@eluniversal.com','wasuaje@eluniversal.com','sistemas-publicaciones@eluniversal.com']

## PARA DESARROLLO
lista = ['wasuaje@eluniversal.com']
##

meses={1:'Enero',2:'Febrero', 3:'Marzo', 4:'Abril', 5:'Mayo', 6:'Junio', \
	   7:'Julio', 8:'Agosto', 9:'Septiembre', 10:'Octubre',11:'Noviembre', 12:'Diciembre'}
mensajes=[]
errores=[]
NO_FILES=13
files_size_cero=['complementa','faccreaq','faconnc','notasdc']
files=['cobeatra','cobros','complementa','faccon','faccre','faccreaq','faceatra',
		'facint','faconnc','facrep','notasdc','prevencla','preventa' ]
actuales=['faccre','facint','facrep','prevencla','preventa']
str_fecha = datetime.datetime.now().strftime("%d%m%Y")
str_fecha_ant = (datetime.datetime.now() - timedelta(days=1)).strftime("%d%m%Y")

## PARA DESARROLLO
#
str_fecha = (datetime.datetime.now() - timedelta(days=30)).strftime("%d%m%Y")
str_fecha_ant = (datetime.datetime.now() - timedelta(days=31)).strftime("%d%m%Y")
#
##

und="c:\\"
##  PARA DESARROLLO ##
und="/home/wasuaje/Documentos/desarrollo/clasideu/"
##
folder = und+meses[datetime.datetime.now().month]+"_"+str(datetime.datetime.now().year)+"/"

##  PARA DESARROLLO ##
folder = und+meses[1]+"_"+str(datetime.datetime.now().year)+"/"
## 


count_files=0
count_cero=0

for i in files:
	if i in actuales:
		thefile = folder+i+str_fecha+".txt"
	else:
		thefile = folder+i+str_fecha_ant+".txt"
	#print thefile
	if os.path.exists(thefile):
		count_files+=1
		if os.path.getsize(thefile) > 0 and i in files_size_cero:			
			errores.append("AVISO %s Tiene tamano mayor a 0 (cero):" % thefile)		

if count_files <> 13:
	errores.append("El numero de interfaces no coincide:"+str(count_files))



f1=os.path.normpath(folder+'cobros'+str_fecha_ant+".txt")
f2=os.path.normpath(folder+'faccon'+str_fecha_ant+".txt")
f3=os.path.normpath(folder+'notasdc'+str_fecha_ant+".txt")
f4=os.path.normpath(folder+'faconnc'+str_fecha_ant+".txt")
try:

	if ( os.path.getsize(f1) > 0 and os.path.getsize(f2) == 0 ) or ( os.path.getsize(f2) > 0 and os.path.getsize(f1) == 0 ):
		errores.append("cobros tiene registros y faccon no tiene ( o viceversa) !")

	if ( os.path.getsize(f3) > 0 and os.path.getsize(f4) == 0) or ( os.path.getsize(f4) > 0 and os.path.getsize(f3) == 0 ):
		errores.append("notasdc tiene registros y facconnc no  ( o viceversa) !")
except:
	errores.append("Ha ocurrido un error inesperado, alguno de estos archivos no existe:\n %s \n %s \n %s \n %s \n" % (f1,f2,f3,f4))


# se correo de notificacion
message = "" 
if len(errores)>0:
	exito="FALLO - "
	for i in errores:
		message += i+"\n"
else:
	exito="EXITO - "	
	message="Revision finalizada sin errores, \n"
	message+="Numero de interfaces encontradas %s \n" % count_files	
	message+="las interfaces de %s y %s parecen estar correctas" % ( str_fecha,str_fecha_ant)

subject = exito+"Revision de concordancia de Interfases SAP - "+str_fecha

###send_mail(lista,subject,message)
send_mail(lista,subject,message)
