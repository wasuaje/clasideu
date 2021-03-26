
#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import shutil
import subprocess
import random
import glob
#produccion
ORIG="/mnt/data01/netapp/clasificados/proyectos/cvfuturo/root/cvword/"
DEST="/mnt/data01/root/scripts/ceu/"
#BASEDEST="/mnt/data01/netapp/clasificados/proyectos/cvfuturo/root/cvword/"

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
  if folder==0:
  	print line,id
  	