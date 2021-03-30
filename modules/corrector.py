# -*- coding: utf-8 -*-
# 1 paso:

# db.tbl_recepcion.truncate()                                 
# db.commit()

#Mover los archivos de la ruta:
#      /home/www-data/web2py/applications/siendo/uploads
#     a:
#      /home/atascon/paso/uploads
# 2.)
# listar archivos y fecha de creacion.

#Actualizar
#3.) fechaenvio=db.tbl_recepcion.fecha
#4.) estado="T"

import os  
import time
import datetime


def TipoDoc(archivo):
    arch=open(archivo,"rb")

    datos=arch.read(500)
    arch.close()
    salida=0
    datos=datos.decode("latin-1")
    if datos.find("|COMPROBANTES DE EGRESOS|")>-1:salida=1
    elif datos.find("CERTIFICADO DE RETENCION POR IVA")>-1:salida=3
    else:
        datos=datos[293:295]
        if datos=="NQ" or datos=="LV" or datos=="LC"  or datos=="PQ":salida=2 #nomina
    return salida


ruta="/home/atascon/paso/uploads"
for archivo in os.listdir(ruta): 
    print (archivo) 
    archivo = os.path.join(ruta,archivo)
    fecha=time.ctime(os.path.getmtime( archivo))
    print("last modified: %s" % fecha)
    fecha=datetime.datetime.strptime(fecha,"%a %b %d %H:%M:%S %Y")
    print("last modified:{}/{:02d}".format (fecha.year,fecha.month) )
    modulo=TipoDoc(archivo)
    if modulo==0: continue
    GenerarPDF(archivo,modulo, fecha_arreglo=fecha)





