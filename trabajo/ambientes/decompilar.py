#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  7 08:41:09 2021

@author: marco
"""
import sys
import pickle
import os

def AbrirAmbiente(nombre):
    if not os.path.isfile(nombre):
        print ("No existe archivo: [{}]".format(nombre) )
        return
    pickled_file = open(nombre,"rb")
    encabezado=pickle.load(pickled_file)
    selector=pickle.load(pickled_file)
    pickled_file.close()
    
    salida =open(nombre[:-3] + 'py', 'w')
    salida.write('#!/usr/bin/env python\n')
    salida.write('# -*- coding: utf-8 -*-\n')
    salida.write('import pickle\n')
    salida.write('import datetime\n')
    salida.write('#modelo Filas x Columnas\n')
    salida.write('encabezado={\n')
    
    for item in encabezado:
        texto='    {"'+ item + '":{}'.format(encabezado[item])+'},\n'
        salida.write(texto)
    salida.write('}\nselector=[\n')

    for campo in selector:
        salida.write('          {')
        for item in campo:
            if item=='nombre' or item=='letra' or item=='alinear':
                texto="            '"+ item + "':'{}'".format(campo[item]) + ',\n'
            else:
                texto="            '"+ item + "':{}".format(campo[item]) + ',\n'
            salida.write(texto)
        salida.write('          },\n')
            
    salida.write(']\n')
        
    salida.close()
    
    
AbrirAmbiente(sys.argv[1])

