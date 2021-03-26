#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import shutil
import subprocess
import random
import glob
#produccion
#ORIG="/mnt/data01/netapp/clasificados/proyectos/cvfuturo/root/cvword/"
#DEST="/mnt/data01/root/scripts/ceu/"
#BASEDEST="/mnt/data01/netapp/clasificados/proyectos/cvfuturo/root/cvword/"


#### desarrollo #######
ORIG="/home/wasuaje/Documentos/desarrollo/clasideu/modword/cvword/"
#DEST="/mnt/data01/root/scripts/ceu/"
DEST="mnt/data01/netapp/clasificados/proyectos/cvfuturo/root/cvword/"
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
#004489.docx|1112973.docx


file = open("wordCandidatos1.csv")

for line in file:
  line=line.replace('\n','')
  archivo_old,id=line.split('|')
  archivo_new=id
  id=archivo_new.split('.')[0] 
  archivo_old='T_'+archivo_old  
  #print id,archivo_old,archivo_new  
  folder=(int(id)/5000)*5000  
  file=ORIG+archivo_old.decode('utf8')
  
  if os.path.exists(file):
      #print file
    	#si el candidato existen, pregunto si existe la carpeta, sino creo la carpeta
      if os.path.exists(DEST+str(folder)+"/"+id):
        pass
      else:
        os.makedirs(DEST+str(folder)+"/"+id)  		
      original=file
      nuevo=DEST+str(folder)+"/"+id+"/"+archivo_new
      shutil.copy(original,nuevo)
      #shutil.copy(file,conid)
      #run_cmd("convert -strip %s -resize 432x468 %s" % (original,conid))
      #run_cmd("convert -strip %s -resize 216x234 %s" % (original,conid) )
      write_file(nuevo+'\n','success_log')
      os.remove(original)
  else: 
      write_file(file.encode('utf-8')+" -> no existe"+'\n','error_log')
