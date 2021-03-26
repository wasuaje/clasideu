#! /usr/bin/env python
#Script para ayudar a la automatizacion de la creacion de micrositios de clasificados.eluniversal.com
#Recibe un domainname y solicita a spro la creacion, crea una regla de micrositio en la ruta 
#especificada, informa a los desasrroladores del cambio y por confirmar: reinicia el site clasificados
#para que tome lo nuevos datos
#Creado por Wuelfhis Asuaje el 12/07/2010
#Uso ./create_ms.py domainname
#    python create_ms.py domainname

import subprocess
import optparse
import re
import os
import time
import sys

#para reiniciar apache
#DOAPACHE='/usr/local/apache-2.2.11/bin/apachectl restart'
DOAPACHE="/manduca10/netapp/clasificados/proyectos/scripts/apache_start_stop.sh"
#directorio de destino de los archivos
#TARGETDIR='/usr/local/apache-2.2.11/conf/virtualHosts_19/micrositios/'
#para pruebas
TARGETDIR='/micrositios/'


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
		msg['From'] = "Sysadmin"
		msg['To'] = mail
		mailto = mail
		# Send the message via our own SMTP server, but don't include the envelope header.
		s = smtplib.SMTP('localhost')		
		s.sendmail(msg['Subject'], mailto, msg.as_string())
		s.quit()
		
def run(dominio):
#mail to spro creation
	sbj_arecord="A record creation"
	msg_arecord="We need the following A record to be created\n\n"		
	msg_arecord=msg_arecord+dominio+".eluniversal.com\n\n"
	msg_arecord=msg_arecord+"It must point to 204.228.236.11\n\n"
	msg_arecord=msg_arecord+"Thanks\n"
	send_mail(["wasuaje@eluniversal.com"],sbj_arecord,msg_arecord)		#para pruebas
#	send_mail("support@solutionpro.com","sbj_arecord",msg_arecord)		#produccion

#mail to Andre malave DNS interno
#	sbj_arecord="Cambios en DNS"
#	msg_arecord="Andres necesitamos por favor este Registo A \n\n"		
#	msg_arecord=msg_arecord+dominio+".eluniversal.com\n\n"
#	msg_arecord=msg_arecord+"Este debe apuntar a 204.228.236.11\n\n"
#	msg_arecord=msg_arecord+"Muchas Gracias\n"
#	send_mail(["wasuaje@eluniversal.com"],sbj_arecord,msg_arecord)		#para pruebas
#	send_mail(["amalave@eluniversal.com"],sbj_arecord,msg_arecord)		#produccion


#micrositio rule creation
	txt_ms="<VirtualHost 204.228.236.11:80>\n"
	txt_ms=txt_ms+"ServerName "+dominio+".eluniversal.com\n"
	txt_ms=txt_ms+"ServerAlias "+dominio+".eluniversal.com\n" 
	txt_ms=txt_ms+"RewriteEngine On\n"
	txt_ms=txt_ms+"RewriteRule ^(.*) http://clasificados.eluniversal.com/micrositio/"+dominio+"%{REQUEST_URI} [P,QSA,L]\n"
	txt_ms=txt_ms+"</VirtualHost>\n"
	fp = open(TARGETDIR+dominio+".conf", 'w')
	fp.write(txt_ms)
	fp.close()
	
#mail to developers and me
	sbj_arecord="Se creo un Registro A y su regla de micrositio"
	msg_arecord="Se creo un Registro A y su regla de micrositio\n\n"
	msg_arecord=msg_arecord+"Bajo el nombre de   "+dominio+".eluniversal.com\n\n"
	msg_arecord=msg_arecord+"Y apuntando a la direccion IP 204.228.236.11\n\n\n"
	msg_arecord=msg_arecord+"Tambien se creo un archivo de configuracion para micrositio con el sigueinte texto:\n\n"
	msg_arecord=msg_arecord+txt_ms+"\n"
	lista=["wasuaje@eluniversal.com","desarrolladoresclasificados@eluniversal.com"]
#	lista=["wasuaje@eluniversal.com"]
	send_mail(lista,sbj_arecord,msg_arecord)		#para pruebas
#	send_mail("support@solutionpro.com",sbj_arecord,msg_arecord)		#produccion

	comando="ssh manduca7 "+DOAPACHE+" stop"
	runcmd(comando)		#mando a ejecutar el reinicio de apache
	time.sleep(5)
	comando="ssh manduca7 "+DOAPACHE+" start"
        runcmd(comando)         #mando a ejecutar el reinicio de apache


if __name__ == "__main__":

        if len(sys.argv) == 2:
        	run(sys.argv[1])        
        else:
	        print "Necesita un nombre de dominio para ejecutar el script"
	        sys.exit(2)
	        sys.exit(0)

else:
        print "usage: %s domainname" % sys.argv[0]
        sys.exit(2)






