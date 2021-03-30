#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Compatible desde la version Facil2
'''
import pickle

from uuid import uuid1
from tempfile import gettempdir
from os import remove      as BORRAR
from os.path import join   as UNIR
from os.path import isfile as EXISTE

import logging
logger = logging.getLogger(__name__)


class ObjPagLog():
	"""docstring for ObjPagLog"""
	def __init__(self, up=[1,1], orden="Z", ancho=8.5, largo=11.0, rutarecursos=None):
		super(ObjPagLog, self).__init__()
		self.orden = orden
		self.adicionar=None
		self.Error=False
		if rutarecursos:
			self.nombre  = UNIR( rutarecursos,"temp", "Facil_PagLog{}".format(str( uuid1() )) )
		else:
			self.nombre  = UNIR( gettempdir(), "Facil_PagLog{}".format(str( uuid1() )) ) 	#nombre del archivo de salida
		self.cont_paginas = 1
		self.ancho=ancho
		self.largo=largo
		self.nombre_pdf=""
		self.Inicio()


		if isinstance(up,(list,tuple)):
			#print (up[0],ancho)
			self.despx=ancho / up[0] if up[0] else 1
			self.despy=largo / up[1] if up[1] else 1
			self.columnas= up[0]
			self.filas= up[1]
			self.max= up[0] * up[1]
		else:
			self.Error=True

	def SetNombrePDF(self, nombre):
		logger.debug(f"F2Spagina.SetNombrePDF: PDF [{nombre}]")
		self.nombre_pdf=nombre

	def SetID(self,idpag):
		self.idpag=idpag
		logger.debug(f"Id pag:{idpag}")

	def Inicio(self):
		self.col  = 1
		self.fila = 1
		self.paginas=[]
		self.posicion=0

	def AddPagina(self, campos):
		#logger.debug(campos)
		#logger.debug (f"Paginina logica col:{self.col} fila: {self.fila}")
		despx = (self.col -1 )  * self.despx
		despy = (self.fila -1 ) * self.despy
		self.posicion +=1
		self.paginas.append({
							 "pag_despx":despx,
							 "pag_despy":despy,
							"campos":campos})

		if self.orden=="Z":
			logger.debug ("Orden Z")
			self.col +=1
			if self.col > self.columnas:
				self.col=1
				self.fila +=1

		elif self.orden=="W":
			logger.debug ("Orden W")
			self.fila +=1
			if self.fila > self.filas:
				self.fila =1
				self.col +=1

		if self.posicion == self.max:
			self.SaltoPagina()

	def SaltoPagina(self):
		if self.paginas:
			nombre="{}_Pag{:010d}".format(self.nombre,self.cont_paginas)
			encabezado={
						"ancho":self.ancho,
						"largo":self.largo,
						"nombre_pdf":self.nombre_pdf,
						"idpag":self.idpag
						}

			logger.debug(f"Nombre Archivo [{nombre}]")
			#logger.debug(f"Guardar Encabezado {encabezado}")
			#logger.debug(f"Guardar Pagina fisica:{self.paginas}")

			archivo=open(nombre ,"wb")
			pickle.dump(encabezado,archivo)
			pickle.dump(self.paginas,archivo)
			archivo.close()
			self.Inicio()
			self.cont_paginas +=1

	def Fin(self):
		logger.debug ("Fin {};".format(len(self.paginas)))
		if len(self.paginas)>0:
			archivo=open("{}_Pag{:010d}".format(self.nombre,self.cont_paginas) ,"wb")
			pickle.dump(self.paginas,archivo)
			archivo.close()
		else:
			logger.warning ("No hay mas paginas")

	def LeerPagina(self, pagina=1):
		logger.info(f"LeerPagina: {pagina}/{self.cont_paginas-1}")
		nombre_arch="{}_Pag{:010d}".format(self.nombre,pagina)
		if not EXISTE(nombre_arch):
			logger.debug (f"No existe pagina nro{pagina}")
			return None

		archivo=open(nombre_arch ,"rb")
		encabezado =pickle.load(archivo)
		pagina =pickle.load(archivo)
		archivo.close()
		logger.debug(encabezado)
		#logger.debug(pagina)
		return encabezado,pagina

	def BorrarTemp(self):
		for pagina in range(1, self.cont_paginas):
			#print (pagina)
			nombre_arch="{}_Pag{:010d}".format(self.nombre,pagina)
			logger.info(f"borrar:{nombre_arch}")
			if EXISTE(nombre_arch):
				BORRAR(nombre_arch)
				logger.info("Borrado")

if __name__ =="__main__":
	ob=ObjPagLog(up=(3,2), orden="W", ancho=11, largo=8.5)
	ob.AddPagina("campos1")
	ob.SaltoPagina()
	ob.AddPagina("campos2")
	ob.AddPagina("campos2")
	ob.AddPagina("campos4")
	ob.AddPagina("campos5")
	ob.AddPagina("campos6")
	ob.AddPagina("campos8")
	#ob.AddPagina("campos9")
	#ob.AddPagina("campos10")
	ob.Fin()
	ob.LeerPagina(1)
	ob.LeerPagina(2)
	ob.LeerPagina(3)
	ob.LeerPagina(4)
	ob.LeerPagina(5)
	ob.BorrarTemp()

#junio ladr
#imporino Julio   97.000
