#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Prueba los datos
'''
import argparse
import sys
import os

sys.path.append('./SimpleSoft')

from SimpleSoft.Facil 			import ObjFacil
from SimpleSoft.F2S_filascol 	import ObjFilas

if __name__ =="__main__":

    parser = argparse.ArgumentParser(description='Facil Ver 1.3')
    parser.add_argument( '-f', '--archivo' , dest='archivo',  help='Ruta y nombre del archivo de datos')
    parser.add_argument( '-r', '--recursos', dest='recursos',   help='Ruta del recurso (trabajo)')
    parser.add_argument( '-a', '--ambiente', dest='ambiente', help='Nombre completo del ambiente')
    #parser.add_argument( '-d', '--debug',    dest='debug',    default=1 ,help='Nivel de log')
    ##parser.add_argument( '-c', '--config',    dest='config',  default='config.ini' ,help='Configurarcion del loggin')
    argumentos =  parser.parse_args()


    #logging.config.fileConfig(argumentos.config, disable_existing_loggers=False)
    ob=ObjFacil(rutarecursos=argumentos.recursos)
    ob.AbrirAmbiente(argumentos.ambiente)
    obFilasCol=ObjFilas(ob, argumentos.recursos)
    campos=obFilasCol.Procesar(argumentos.archivo)
    print ('Web2py campos:',campos)
