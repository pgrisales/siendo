#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Version 1.2
´'''
import sys
import os
import yaml
import pickle
import argparse
import logging
import logging.config
from F2S_PartirSpool import F2S_PartirDoc
from F2S_Dinamico    import objDinamico



# logging.debug('This is a debug message')
# logging.info('This is an info message')
# logging.warning('This is a warning message')
# logging.error('This is an error message')
# logging.critical('This is a critical message')



##logger = logging.getLogger("Facil SimpleSoft")
##logging.basicConfig(format='%(asctime)s - %(name)s - %(module)s - %(levelname)s - %(message)s')


with open('config.yaml', 'r') as f:
    log_cfg = yaml.safe_load(f.read())
print (log_cfg)
logging.config.dictConfig(log_cfg)
logger = logging.getLogger('Facil_simpleSoft')






class ObjFacil():
    """ Extractor de campos"""
    def __init__(self, rutarecursos, ambiente=""):
        logger.debug("Ruta recursos:{}".format (rutarecursos))
        logger.debug("Ambiente:{}".format (ambiente))

        self.ruta = rutarecursos
        self.encabezado=None
        self.selector=None
        self.Error=None
        self.AbrirAmbiente(ambiente)
        self.modo=0             #0=Dinamico, 1=Filas x Columnas 2=Campos, 3=csv, 4=pdf

    def AbrirAmbiente(self,nombre):
        #logger.info("AbrirAmbiente:{}".format(nombre))


        ruta=os.path.join(self.ruta,"ambientes",nombre)
        logger.debug ("archivo ambientes:{}".format(ruta))
        if not os.path.isfile(ruta):
            self.Error="No existe archivo: [{}]".format(ruta)
            return False
        
        try:
            pickled_file = open(ruta,"rb")
            self.encabezado=pickle.load(pickled_file)
            self.selector=pickle.load(pickled_file)
            pickled_file.close()
            return True
        except Exception as e:
            self.Error=e
            logger.error(e)
            return False

    def getEncabezado(self,contenido=None):
        logger.info("getEncabezado")
        salida=""
        if contenido:
            if contenido in self.encabezado:
                logger.debug ("Comando [{}]:{}".format(contenido,self.encabezado[contenido]) )
                salida= self.encabezado[contenido]
        else:
            salida= self.encabezado
        return salida

    def getModo(self):
        logger.info("getModo")
        if self.encabezado:
            if "modo" in selector.encabezado:
                self.modo=self.encabezado["modo"]
        else:
            self.Error("No exite encabezado")
        return self.modo

    def getSelector(self):
        logger.info("getSelector")
        logger.debug ("getSelector:{}".format(self.selector) )
        return self.selector

    def TextoSalto(self,lineas,selector):
        poslinea=0
        for linea in lineas:
            poslinea=+1
            buscar=linea.find(selector["textosalto"])
            if buscar>-1:
                if buscar==selector["col"]:  #determinar si esta en la Posicion absoluta
                    break
        return poslinea

    #Procesar Filas x Cols
    def Procesar(self, archivo=None,pagina=1):
        #Verifcar archivo de entrada de datos
        if self.Error:            return False
        if not os.path.isfile(archivo):
            logger.error ("No hay archivo de datos...{}".format(archivo))        
            return False

        obPaginas=F2S_PartirDoc(archivo=archivo, saltopag=self.getEncabezado('saltopag'))
        obPaginas.Procesar()
        #Dinamico
        sys.exit()

        if  self.getEncabezado('modo')==0:  #Modo dinamico
            if self.getEncabezado('unavez'):
                obDinamico=objDinamico( encabezado=self.getEncabezado(), 
                                        selector=self.getSelector(), 
                                        lineas=obPaginas.LeerPagina(pagina))#verifica la primera pagina
                ambiente=obDinamico.Procesar()
                logger.debug ("Ambiente encontrado:{}".format(ambiente))
                if not ambiente: 
                    obPaginas.BorrarTemp()
                    return False
        #leer ambiente
        self.AbrirAmbiente(ambiente)
        #procesar paginas
        for pag in range(pagina, obPaginas.paginas):
            lineas=obPaginas.LeerPagina(pag)
            cambio_salto=False



        # print (obPaginas.nombre)
        # for pagina in range(1,obPaginas.paginas+1):
        #     print (pagina)






        # modo = self.getEncabezado('modo') 
        # print ("modo:",modo)

        return True


def ProcArgumentos():
    parser = argparse.ArgumentParser(description='Facil Ver 1.2')
    parser.add_argument( '-d', '--debug',    dest='debug',    default=1 ,help='Nivel de log')
    parser.add_argument( '-p', '--ambiente', dest='ambiente', default="Dinamico.amb", help='Nombre del ambiente')
    parser.add_argument( '-r', '--recursos', dest='recursos', default="/home/marco/Clientes/maquitodo/Facil", help='Ruta de recursos')
    parser.add_argument( '-a', '--archivo' , dest='archivo',  default="/home/marco/Clientes/maquitodo/Facil/spools/Comprobantes_egreso.txt", help='Archivo de dato')
    return  parser.parse_args()

def ConfLog(nivel):
    niveles=(logging.INFO, logging.DEBUG, logging.CRITICAL, logging.ERROR, logging.WARNING,  logging.NOTSET)
    print (logging.DEBUG)
    logger.setLevel(niveles[nivel])


if __name__ =="__main__":
    args =ProcArgumentos()
    ConfLog(args.debug)
    ob=ObjFacil(rutarecursos=args.recursos, ambiente=args.ambiente)
    ob.Procesar(archivo=args.archivo)
                
    # logger.debug("This is a debug message")
    # logger.info("For your info")
    # logger.warning("This is a warning message")
    # logger.error("This is an error message")
    # logger.critical("This is a critical message")
