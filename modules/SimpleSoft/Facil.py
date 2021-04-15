#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pickle
import os
import logging
logger = logging.getLogger(__name__)

class ObjFacil():
    """docstring for Facil"""
    def __init__(self, rutarecursos):
        self.ruta = rutarecursos
        self.encabezado=None
        self.selector=None
        self.Error=None
        self.Debug=False
        self.pagina={}
        self.nombre_pdf=None
        self.web2pycorreo=[]

    def AbrirAmbiente(self,nombre):
        ruta=os.path.join(self.ruta,"ambientes",nombre)
        if self.Debug : print ("archivo ambientes:",ruta)
        if not os.path.isfile(ruta):
            self.Error="No existe archivo: [{}]".format(ruta)
            return
        try:
            pickled_file = open(ruta,"rb")
            self.encabezado=pickle.load(pickled_file)
            self.selector=pickle.load(pickled_file)
            pickled_file.close()

        except Exception as e:
            self.Error=e
            return

    def getEncabezado(self,contenido=None):
        salida=""
        if contenido:
            if contenido.lower() in self.encabezado:
                salida= self.encabezado[contenido.lower()]
        else:
            salida= self.encabezado
        return salida

    def getSelector(self):
        #print ("getSelector:",self.selector)
        return self.selector

    ################## Funciones Encabezado ###########################

    def getTamancho(self):
        tam=self.getTamaPapel()
        logger.debug(f"Tam papel:{tam}")
        if "medida" in tam:
            if tam["medida"]=="mm":
                tam=tam["ancho"] / 25.4
            elif tam["medida"]=="cm":
                tam=tam["ancho"] / 2.54
        return tam["ancho"]

    def getTamalto(self):
        tam=self.getTamaPapel()
        if tam["medida"]=="mm":
            tam=tam["alto"] / 25.4
        elif tam["medida"]=="cm":
            tam=tam["alto"] / 2.54
        return tam["alto"]

    def getTamaPapel(self):
        salida = self.getEncabezado("tampapel")
        if salida=="":
            salida={"ancho":11,"alto":8.5,"medida":"pul"},
        return salida

    def getUp(self):
        '''
        Busca la deficion de las paginas logicas
        up=(filas, columnas)    por defecto 1,1
        '''
        salida = self.getEncabezado("pagup")
        salida=salida["up"]
        if salida=="":
            salida=(1,1)

        return salida

    def getUpOrden(self):
        '''
        orden="Z" o "W"         por defecto Z
        '''
        salida = self.getEncabezado("pagup")
        salida = salida["uporden"]
        if salida=="":
            salida="Z"
        return

    def getPosDetalle(self):
        '''
        Posicion en lineas inicio del detalle por defecto es 50 si no se especifica.
        '''
        salida = self.getEncabezado("posdetalle")
        if salida=="":
            salida=50
        return salida

    def getTipos(self):
        '''
        Buscar el registro los tipos de letras
        '''
        salida = getEncabezado("tipos")
        if salida=="":
            salida=( ('Ubuntu',     'Ubuntu-R.ttf'),                   # (nombre logico, nombre fisico)  Nota debe estar en fonts
                      ('Ubuntu-Bold','Ubuntu-B.ttf'),
                      ('Ubuntu-Cond','Ubuntu-C.ttf'),
                      ('f2sCodigo128','Codigo128.ttf')
                    )
        return salida

    def getFormato(self):
        '''
        Buscar el Formato
        '''
        salida = getEncabezado("formato")
        if not os.path.isfile(os.path.join(self.ruta,salida)):
            logger.warning("No Existe el formato")
        return salida

    def getModo(self):
        '''
        Buscar el modelo de datos
        '''
        salida = getEncabezado("modo")
        if salida=="":
            salida=1        #por defecto filas x columnas

    def getPosSalto(self):
        '''
        Entrega la posicion donde esta lun list los textos que generan un saltos de pagina
        si es negativo se debe buscar en cualquier posicion
        '''
        salida = self.getEncabezado("pos_salto")
        if salida=="":
            salida=-1

        if isinstance(salida,int):
            salida=salida-1
        else:
            logger.warning("Debe ser un entero la posicion del salto, se deja por defecto -1")
            salida=-1

        return salida

    def getSaltoPagina(self):
        salida = self.getEncabezado("saltopag")
        if salida=="":
            salida=None
        #print (" getSaltoPagina:", salida)
        return salida

    def SaltoPagina(self,linea):
        salida=False

        saltos,posicion = self.getSaltoPagina()
        for saltopag in saltos:
                buscar=linea.find(saltopag["texto"])
                if buscar >-1:
                    if buscar == posicion:
                            salida=True
                            logger.debug("SaltoPagina..")
                            break
                    else:#en cualquier se encuentra el texto de salto
                        logger.debug("SaltoPagina..")
                        salida=True
                        break
        return salida

    def getSaltoLineaDoc(self):
        '''
        Define si se debe obiar el nro de linea
        '''
        salida = self.getEncabezado("saltolineadoc")
        if salida=="":
            salida=-1
        return salida

    def getNroLineaxPag(self):
        '''
        Define si se debe obiar el nro de linea
        '''
        salida = self.getEncabezado("lineasxpag")
        if salida=="":
            salida=0
        return salida

    def getMoverLineas(self):
        '''
        Desplaza las lineas cuando encuentra un texto
            #   Ejemplo ({"buscartexto":"SUMAS IGUALES", "nuevafila":60},....)
        '''
        #print("moverlineas")
        salida = self.getEncabezado("moverlineas")
        if salida=="":
            salida=None
        return salida

    def getEliminarLineaxPag(self):
        salida = self.getEncabezado("eliminarlineaxpag")
        if salida=="":
            salida=0
        return salida

    def getIDdoc(self):
        '''
        guarda la indentificacion de la pagina o id si no viene toma el nro de o_pagina
        '''
        agrupar = self.getEncabezado("agrupar")
        if agrupar=="":            agrupar=None
        return agrupar

    def getIniciopag(self):
        salida = self.getEncabezado("iniciopag")
        return salida

      ########################
     # Funciones Generales #
    ########################

    def NormalizarLinea(self,linea,separador=None):
        if isinstance( linea, bytes): linea=linea.decode("utf-8")
        linea=linea.replace("\r\n","")
        linea=linea.replace("\n","")
        if self.getEncabezado("eliminartexto"):
            for texto in self.getEncabezado("eliminartexto"):
                linea=linea.replace(texto,"")
        if separador!=None:
            #Verificar si esta en blanco
            temp=linea.replace(";","")
            if len(temp.strip())==0:linea=""

        ##?? linea=linea.strip()
        return linea

    def NormalizarLineas(self,lineas,separador=None):
        nrolinea=0
        nueva=[]
        for linea in lineas:
            nueva.append(self.NormalizarLinea(linea,separador))
            nrolinea +=1
            ##logger.debug("{:02d} |{}".format(nrolinea,linea))

        return nueva

    def AddCampoPagina(self, selector,texto):
        #print (selector)
        if "fun_formato" in selector:
            texto=selector["fun_formato"].format(texto.strip())
            #print (texto)

        if "codigo128" in selector:
            self.pagina[ selector["nombre"] ]= {
            "letra_alto":selector["letra_alto"],
            "alinear":selector["alinear"],
            "letra":selector["letra"],
            "posx":selector["posx"],
            "posy":selector["posy"],
            "texto":[texto],
            "alto":selector["alto"],
            "ancho":selector["ancho"],
            "posx_cod":selector["posx_cod"],
            "codigo128":True
            }
        else:
            if  selector["nombre"] in self.pagina:
                self.pagina[selector["nombre"]]["texto"].append(texto)
            else:
                if "fun_numero1" in selector:
                    #print ("AddCampoPagina", selector)
                    self.pagina[ selector["nombre"] ]= {
                    "letra_alto":selector["letra_alto"],
                    "alinear":selector["alinear"],
                    "letra":selector["letra"],
                    "posx":selector["posx"],
                    "posy":selector["posy"],
                    "desp_x": selector["desp_x"],
                    "desp_y": selector["desp_y"],
                    "texto":[texto],
                    "fun_numero1": selector["fun_numero1"]
                    }
                else:
                    self.pagina[ selector["nombre"] ]= {
                    "letra_alto":selector["letra_alto"],
                    "alinear":selector["alinear"],
                    "letra":selector["letra"],
                    "posx":selector["posx"],
                    "posy":selector["posy"],
                    "desp_x": selector["desp_x"],
                    "desp_y": selector["desp_y"],
                    "texto":[texto],
                    }
        if "colortexto_rgb" in selector:
            #print (self.pagina[ selector["nombre"] ])
            self.pagina[ selector["nombre"] ]["colortexto_rgb"]=selector["colortexto_rgb"]
            #print (self.pagina[ selector["nombre"] ])

      #################
     # Funciones PDF #
    ##################
    def setPDF(self):
        '''
        Extrae la informacion ingresarda del encabezado.
        Entrega el selector de datos para el nombre del PDF
        Determina la ruta para guarda el PDF con el formato
        entregado desde el ambiente.
        '''
        encabezado=self.getEncabezado("nombre_pdf")
        if isinstance(encabezado,dict):
            selector=encabezado["selector"]
            ruta=""
            if "ruta_pdf" in encabezado:
                ruta =encabezado["ruta_pdf"]
                if not os.path.isdir(ruta):
                    os.makedirs(ruta)
            else:
                ruta="./"
            if "formato" in encabezado:
                formato=encabezado["formato"]
            else:
                formato="{}"
        else:
            logger.warning("no esta paramaterizado el PDF, se da un nombre genrerico")
            formato="defecto"
            selector=None
        self.format_pdf=os.path.join(ruta,formato)
        self.format_pdf +=".pdf"
        logger.debug(f"Facil.setPDF[{self.nombre_pdf}]")
        return selector

    def SetNombrePDF(self,nombre):
        print ("SetNombrePDF", nombre)
        self.nombre_pdf = self.format_pdf.format(*nombre)
        logger.debug(f"Facil.SetNombrePDF:{self.nombre_pdf}")

    def getRutaPDF(self):
        '''
        Ruta donde se guarda el PDF, si no tiene se guarda donde se este ejecutando el progama
        '''
        from datetime import datetime
        ahora=datetime.now()
        salida = self.getEncabezado("ruta_pdf")
        if salida=="":
            salida="./"
        else:
            salida=f"{salida}{os.sep}{ahora.year}{os.sep}{ahora.month}"
            if not os.path.isdir: os.makedirs(salida)
        return salida

    def getSobreScribirPDF(self):
        """
        Define si se sobrescribe el PDF, por defecto si
        """
        salida = self.getEncabezado("sobre_escribir_pdf")
        if salida=="":
            salida=True

    ####################
     # Funciones Web2py #
    ####################
    def getWeb2pyCorreo(self):
        web2py=self.getEncabezado("correoweb2py")
        if web2py=="":
            web2py=None
        return web2py

    def addRegWeb2py(self,registro):
        #print("addRegWeb2py")
        self.web2pycorreo.append(registro)

    ##Nuevas
    def getNoLineaBlanco(self):
        salida = self.getEncabezado("nolineablanco")
        if salida=="":  salida=False
        return salida

    def getDetalleFijo(self):
        salida = self.getEncabezado("detallefijo")
        if salida=="":  salida=None
        return salida

    def getElinarTexto(self):
        salida = self.getEncabezado("eliminartexto")
        if salida=="":salida=None
        return salida


if __name__ =="__main__":
    print ("inicio")
    temp="/home/marco/workspace/virtualenv3/py3Facil/desarrollo/trabajo"
    ob=ObjFacil(temp)
    ob.AbrirAmbiente("temporal.amb")
    print (ob.getEncabezado())
    print (ob.getEncabezado("iddoc"))
    print (ob.getEncabezado("falso"))
    print (ob.getSelector())
