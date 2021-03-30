# -*- coding: utf-8 -*-
# ---
from os.path import join as UNIR

def index():
    tarea=0
    formulario = SQLFORM.factory(
        Field('archivo', 'upload', label="Archivo de datos"))
    if formulario.process().accepted:
        response.flash = 'formulario aceptado'
        archivo=UNIR(request.folder,"uploads",formulario.vars.archivo)
        print (archivo)
        archivo=open(archivo,"r")
        nrolinea=0
        novedad=[]
        for linea in archivo.readlines():
            nrolinea +=1
            linea=linea.replace("\n","")
            linea=linea.split(",")
            #print (linea)
            if len(linea[0].strip())==0:
                novedad.append([nrolinea,"Nombre en blanco", linea])
                continue
            if len(linea[1].strip())==0:
                novedad.append([nrolinea,"NIT en blanco", linea])
                continue

            db.tbl_cliente.insert(  nombre=linea[0],
                                    nit=linea[1],
                                    correo1=linea[2],
                                    correo2=linea[3],
                                    #correo3=linea[4]
            )

        print ("Novedad:",novedad)

    elif formulario.errors:
        response.flash = 'el formulario tiene errores'
    return locals() #dict(formulario=formulario)
