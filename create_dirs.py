# -*- coding: IBM850 -*- 

#### -*- coding: utf-8 -*-
### required - do no delete

#Script para ayudar a la automatizacion de la creacion de carpeta mensual para interfaces de SAP
#Creado por Infraestructura de Sistemas el 30/05/2012


import subprocess
import optparse
import re
import os
import time
import sys
import datetime


#produccion
TARGETDIR = 'c:\\'
ZIPDIR = 'd:\\'

#desarrollo
#TARGETDIR = ''
#ZIPDIR = ''

lista = ['jbarrera@eluniversal.com','wasuaje@eluniversal.com','sistemas-publicaciones@eluniversal.com']
#lista = ['wasuaje@eluniversal.com']
#lista = ['jbarrera@eluniversal.com']

meses={1:'Enero',2:'Febrero', 3:'Marzo', 4:'Abril', 5:'Mayo', 6:'Junio', \
			7:'Julio', 8:'Agosto', 9:'Septiembre', 10:'Octubre',11:'Noviembre', 12:'Diciembre'}

def create_bat(newLine):
    file = open("c:\Extra\Contax\copia_a.bat", "w")
    file.write(newLine)
    file.close()
         
def creartxt():
    archi=open('log.txt','w')
    archi.close()


def write_file(newLine):
    file = open("log.txt", "a")
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
		
#Obtener nro del mes actual
curdate= datetime.date.today()

curyear=curdate.year
curyear2=curdate.year
curmonth=curdate.month

curmonthname=meses[curmonth]

if curmonth == 1:
	prevmonthname=meses[12]
	curyear=curdate.year-1
	curyear2=curdate.year
else:
	prevmonthname=meses[curmonth-1]

## adicion para eliminar cada dos meses
if curmonth < 3:    #para enero y febrero
  monthtodelete=curmonth+10
  curyear3=curdate.year-1
  monthtodelete=meses[monthtodelete]
else:
  monthtodelete=curmonth-2
  curyear3=curdate.year
  monthtodelete=meses[monthtodelete]

# **************** para efecto de pruebas ******************
#	
# curmonthname=meses[10]
# prevmonthname=meses[9]
#
# **** fin data de prueba comentar para produccion *********

dirtocreate=curmonthname+"_"+str(curyear2)
dirtozip=prevmonthname+"_"+str(curyear)
dirtodelete=monthtodelete+"_"+str(curyear3)


linea="el directorio a crear es: "+ dirtocreate
write_file(linea+"\n")

linea="el directorio a Comprimir es: "+ dirtodelete
write_file(linea+"\n")


print 'dirtocreate = '+ dirtocreate
print 'dirtobatch = '+ dirtozip
print 'dirtodeleteandzip = '+ dirtodelete


#Si no existe el directorio lo creo
if not os.path.exists(TARGETDIR+dirtocreate):
    os.makedirs(TARGETDIR+dirtocreate)
    print 'Se creo el Directorio: '+ (TARGETDIR+dirtocreate)
    
    ## se escribe en el log del programa
    linea="Se creo el Directorio: "+ (TARGETDIR+dirtocreate)
    write_file(linea+"\n")
    
else:
    print 'Directorio ya existe: '+(TARGETDIR+dirtocreate)
       
    ## se escribe en el log del programa
    linea="El DIRECTORIO YA EXISTE "+(TARGETDIR+dirtocreate)
    write_file(linea+"\n")
    

#comprimir directorio anterior
import zipfile

zip_file = ZIPDIR+dirtodelete

file_camino=ZIPDIR+chr(92)+ dirtodelete+ '.zip'

## se escribe en el log del programa
linea="Archivo a comprimir ZIP: "+ (ZIPDIR+dirtodelete)+'.zip'
write_file(linea+"\n")
    

#print 'dirtozip : '+dirtozip
#print 'file_camino  '+file_camino
#print 'archivo : '+archivo

zip = zipfile.ZipFile(file_camino, 'w', zipfile.ZIP_DEFLATED)

rootlen = len(TARGETDIR+dirtodelete) + 1
for base, dirs, files in os.walk(TARGETDIR+dirtodelete):
   for file in files:
      fn = os.path.join(base, file)
      zip.write(fn, fn[rootlen:])
zip.close()

#nueva adicion 19/02/14 ASI-2521
#si el zip tiene tamaño mayor a cero elimino la carpeta base
import shutil

if os.path.getsize(file_camino)>0: 
  try:
    shutil.rmtree(TARGETDIR+dirtodelete)
  except OSError:
    print "No se pudo eliminar carpeta: "+(TARGETDIR+dirtodelete)
  else:
    linea="Se elimina la carpeta luego de zipeada: "+(TARGETDIR+dirtodelete)
    print linea
    write_file(linea+"\n")
else:
  linea="No se pudo eliminar la carpeta archivo zip vacio"
  print linea
  write_file(linea+"\n")


## se escribe en el log del programa
linea="Se comparte la carpeta creada "+(TARGETDIR+dirtocreate)
print linea
write_file(linea+"\n")
#Se comparte la carpeta
comando= 'net share '+ dirtocreate+'='+TARGETDIR+dirtocreate+' /unlimited'
runcmd(comando)

## Se modifica el archivo copiar_a.bat ubicado en c:\Extra\Contax
## y se le coloca el nuevo directorio donde debe grabar

linea="Se comienza a modificar el archivo copia_a.bat del mes "+ dirtozip
print linea
write_file(linea+"\n")

cmd=""

lista2=('co*','fac*','no*','pre*','cu*','zo*','ma*','are*')
lista3=('co*','fac*','no*','pre*','cu*','zo*','are*')

for val in lista2:
     cmd+="xcopy c:\Saptemp\enviados\%s  c:\%s /Y \n" % (val,dirtocreate)     

for val in lista3:
     cmd+="del c:\Saptemp\enviados\%s \n" % val

linea="Se modifico el archivo copia_a.bat al mes "+ dirtocreate
print linea
write_file(linea+"\n")
#el comando de creacion en si
create_bat(cmd)

## se escribe en el log del programa
linea="Se envia el mensaje de finalizacion "
print linea
write_file(linea+"\n")


# se correo de notificacion
subject = "Procesamiento  Interfases SAP al mes "+dirtocreate
message = "Se comprimio y elimino la carpeta "+TARGETDIR+dirtodelete+"\n" 
message += "Adicionalmente se creo y compartio la carpeta "+TARGETDIR+dirtocreate+"\n" 
message += "Se creo el nuevo archivo copia_a.bat apuntando al mes actual\n"
###send_mail(lista,subject,message)
send_mail(lista,subject,message)
