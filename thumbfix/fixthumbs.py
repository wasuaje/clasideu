#!/usr/bin/python
# Script que revisa un directorio en busca de .jpgs sin thumbs y viceversa
# Ejecuta un comando para el primer caso y Genera un archivo con la segunda
# no acepta parametros
# Fecha 30/03/2011
# comando a ejecutar    /usr/bin/convert -thumbnail 45 $f jpg:$f.thumb
# Genera:
# sin_thumbs.txt = todos aquellos archivos que no tenian thumbs y se legeneraron
# sin_originales.txt = todos los que tenian thumbs y no tenian original
# Cambiar entra las dos lineas siguientes para desarrollo y para produccion
import os,time,glob,commands
#PATH="/manduca10/netapp/clasificados/proyectos/cvfuturo/root/imagenes/candidatos/Fotos/T"
PATH='/home/wasuaje/Documentos/desarrollo/clasideu/thumbfix'
h=0
i=0
FILETYPES  = ['*.jpg','*.jpg.thumb']

if os.path.exists("sin_originales.txt"):
    os.remove("sin_originales.txt")

if os.path.exists("sin_thumbs.txt"):
    os.remove("sin_thumbs.txt")

def write_file(newLine,filename):
    file = open(filename, "a")
    file.write(newLine)
    file.close()
   
for idx,tipos in enumerate(FILETYPES):
    ficheros = os.path.join(PATH, tipos)
    for filename in glob.iglob(ficheros):        ##para python 2.4 glob.glob(ficheros)
	print "created: %s" % time.ctime(os.path.getmtime(filename))
        if idx==0:            #aplica solo a jpg
            if os.path.exists(filename+".thumb"):
                pass
            else:
                print "genero archivo"
                commands.getoutput("/usr/bin/convert -thumbnail 45"+filename+" jpg:"+filename+".thumb")
                write_file(filename+"\n","sin_thumbs.txt")
                h=h+1

        if idx==1:            #aplica solo a jpg.thumb
            nothumb=filename.replace(".thumb","")
            if os.path.exists(nothumb):
                pass
            else:
                print "genero archivo"
                write_file(filename+"\n","sin_originales.txt")
                i=i+1
