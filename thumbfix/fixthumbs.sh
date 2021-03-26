#!/bin/bash
# Script que revisa un directorio en busca de .jpgs sin thumbs y viceversa
# Ejecuta un comando para el primer caso y Genera un archivo con la segunda
# no acepta parametros
# Fecha 30/03/2011
# comando a ejecutar convert -resize 45 <nombreOriginal> <nombreOriginal>.thumb 
# Genera:
# sin_thumbs.txt = todos aquellos archivos que no tenian thumbs y se le generaron
# sin_originales.txt = todos los que tenian thumbs y no tenian original

# Cambiar entra las dos lineas siguientes para desarrollo y para produccion
#DIR="/manduca10/netapp/clasificados/proyectos/cvfuturo/root/imagenes/candidatos/Fotos/T"
DIR="/home/wasuaje/Documentos/desarrollo/clasideu/thumbfix"
JPGS=`ls *.jpg`
THUMBS=`ls *.jpg.thumb`

rm -f sin_originales.txt
rm -f sin_thumbs.txt

cd $DIR

for f in $JPGS
do
 if [ ! -f $f.thumb ]; then
   /usr/bin/convert -thumbnail 45 $f jpg:$f.thumb
   echo $f >> sin_thumbs.txt
 fi
done

for g in $THUMBS
do
 tpath=`echo ${g/.thumb/}`
  if [ ! -f  $tpath ]; then 
    echo $tpath  >> sin_originales.txt
  fi
done
