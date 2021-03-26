#!/bin/bash

# Argumentos = -p proyecto -m micrositio -a accion [A]ctivar | [D]esactivar
# Para trabajar con micrositios usar hdl_micrositios -m nombrelmicrositio -a A (para activar) ó 
#									 hdl_micrositios -m nombrelmicrositio -a D (para desactivar)
#
# Para trabajar con proyectos usar hdl_micrositios -m nombrelmicrositio -p nombre del proyecto -a A (para activar) ó
#								   hdl_micrositios -m nombrelmicrositio -a D (para desactivar)
# 

#Texto estandar a mostrar en caso de usar la ayuda o si hay un error en los parametros
usage()
{
cat << EOF
Utilizacion: $0 opciones

Este script automatiza el proceso de activar/desactivar proyectos y micrositios.

OPTIONS:
   	-h      Muestra este mensaje
	-p		Proyecto
	-m		Micrositio
	-a		Accion a realizar solo acepta A o D
EOF
}

PROYECTO=
MICROSITIO=
ACCION=

while getopts "hp:m:a:" OPTION
do
     case $OPTION in
         h)
             usage
             exit 1
             ;;
         p)
             PROYECTO=$OPTARG
             ;;
         m)
             MICROSITIO=$OPTARG
             ;;
         a)
             ACCION=$OPTARG
             ;;
         ?)
             usage
             exit
             ;;
     esac
done

# siempre debe haber al menos un micrositio y una accion a realizar
if [[ -z $MICROSITIO ]] || [[ -z $ACCION ]] 
then
     usage
     exit 1
fi

#tacitamente al enviar un proyecto y un micrositio estoy usando el archivo de proyectos
if [[ ! -z $PROYECTO ]] && [[ ! -z $MICROSITIO ]] 
then
	if [ $ACCION = A ]		#si estoy activando
	then	
	    echo "RewriteRule ^/micrositio/$MICROSITIO/$PROYECTO.*$ http://clasificados.eluniversal.com/inmuebles/nuevosproyectos.shtml [R,L]" >> proyectosInactivos.conf    
	fi
	if [ $ACCION = D ]		# si estoy desactivando
	then			
	    sed /$MICROSITIO.*$PROYECTO/d proyectosInactivos.conf > proyectosInactivos.conf.tmp
	    mv proyectosInactivos.conf proyectosInactivos.conf.bkp
	    mv proyectosInactivos.conf.tmp proyectosInactivos.conf	    	    
	fi
fi

#si el proyecto esta vacio y el micrositio no estoy usando el archivo de micrositios
if [[ -z $PROYECTO ]] && [[ ! -z $MICROSITIO ]] 
then
	if [ $ACCION = A ]		#si estoy activando
	then	
	    echo "RewriteRule ^/micrositio/$MICROSITIO/.*$ http://clasificados.eluniversal.com/inmuebles/micrositios.shtml [R,L]" >> micrositiosInactivos.conf
	fi
	if [ $ACCION = D ]		# si estoy desactivando
	then	
	    sed /$MICROSITIO/d micrositiosInactivos.conf > micrositiosInactivos.conf.tmp
	    mv micrositiosInactivos.conf micrositiosInactivos.conf.bkp
	    mv micrositiosInactivos.conf.tmp micrositiosInactivos.conf
	fi
fi



