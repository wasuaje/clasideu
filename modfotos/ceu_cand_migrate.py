#!/usr/bin/python
# -*- coding: utf-8 -*-


import os
import shutil
import subprocess
import random

#produccion
#ORIG="/manduca10/netapp/clasificados/proyectos/cvfuturo/root/imagenes/candidatos/Fotos/T/"
#DEST="/mnt/data01/root/scripts/ceu/"
#BASEDEST="/manduca10/netapp/clasificados/proyectos/empleos/root/imagenes/candidatos/Fotos/"


#### desarrollo #######
ORIG="/home/wasuaje/Documentos/desarrollo/clasideu/modfotos/manduca10/netapp/clasificados/proyectos/cvfuturo/root/imagenes/candidatos/Fotos/T/"
#DEST="/mnt/data01/root/scripts/ceu/"
DEST="/home/wasuaje/Documentos/desarrollo/clasideu/modfotos/manduca10/netapp/clasificados/proyectos/empleos/root/imagenes/candidatos/Fotos/"
##############
FOLD=0

#candidatosEmpleos.txt

if os.path.exists('error_log.txt'):
 os.remove('error_log.txt')
if os.path.exists('success_log.txt'):
 os.remove('success_log.txt')


def write_file(newLine,file):
  file = open(file+'.txt', 'a')
  file.write(newLine)
  file.close()

def run_cmd(comando):
  p = subprocess.Popen(comando, shell=True, stdout=subprocess.PIPE)
  out = p.stdout.read().strip()
  return out  #This is the stdout from the shell command

#ojanethramirez_1018960.jpg
#okeithledezma_mob_1019325.jpg
#osymbiotic_1019578.jpg


file = open("candidatos.txt")

for line in file:
	lon=len(line.split('_'))
	id=line.split('_')[lon-1]
	id=id.split('.')[0]	
	folder=(int(id)/5000)*5000
	#10 millones de numero al azar
	rannnum=int(random.random()*10000000)
	file=ORIG+line.replace('\n','')
	#print file,id
	if os.path.exists(file):
  		#si el candidato existen, creo la carpeta
  		if os.path.exists(DEST+str(folder)+"/"+id):
   			pass
  		else:
   			os.makedirs(DEST+str(folder)+"/"+id)
  		#original=DEST+str(folder)+'/'+"/"+id+"/original_"+id+'.jpg'
		original="'"+ORIG+line.replace('\n','')+"'"
  		conid=DEST+str(folder)+'/'+"/"+id+"/"+id+'_'+str(rannnum)+'.jpg'
  		#shutil.copy(file,original)
  		#shutil.copy(file,conid)
  		run_cmd("convert -strip %s -resize 432x468 %s" % (original,conid))
  		#run_cmd("convert -strip %s -resize 216x234 %s" % (original,conid) )
  		write_file(str(folder)+"/"+id+"/"+id+'_'+str(rannnum)+".jpg"+'\n','success_log')
 	else:
  		write_file(file+" -> no existe"+'\n','error_log')
