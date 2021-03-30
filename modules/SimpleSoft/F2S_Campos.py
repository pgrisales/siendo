#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Compatible desde la version Facil2
'''
import os, sys
import logging
import logging.config
from uuid import uuid1
from datetime import datetime
from SimpleSoft.F2S_PagLogicas import ObjPagLog
from SimpleSoft.F2S_CrearPDF2  import objF2S_PDF

logger = logging.getLogger(__name__)


#logger = logging.getLogger(__name__)
#logging.basicConfig(format='%(asctime)s - %(name)s - %(module)s - %(levelname)s - %(message)s')

class ObjCampos():
	"""Manejo de Campos"""
	def __init__(self, encabezado, selector, rutarecursos ):
		self.encabezado    = encabezado
		self.selector 	   = selector
		self.rutarecursos  = rutarecursos
		self.nombrepdf =[]
		self.pagina={}
		self.pycorreo={}
		self.lleno=False
		self.listaPycorreo={}

	def ExtraerPDF(self,prefijo,campos, encabezado):
		#seleccion de campos
		for items in  encabezado["selector"]:
			if items["prefijo"]!=prefijo:break
			logger.debug(f"Estraer_PDF : {items}")
			for selcampos in items["campos"]:
				calculo=selcampos -1
				#print (calculo)
				if calculo <= (len(campos)-1):
					self.nombrepdf.append(campos[calculo])
		self.lleno=True

		logger.debug(f"Estraer PDF:{self.nombrepdf}")

	def ExtarerPyCoreo(self, prefijo,campos):

		if "pycorreo" in self.encabezado:
			selector = self.encabezado["pycorreo"]
			#print (selector)

			if "correo_para" in selector:
				if selector["correo_para"]["prefijo"]==prefijo:
					if selector["correo_para"]["campo"]  <= len(campos):
						self.pycorreo["correo_para"]=campos[selector["correo_para"]["campo"]-1]

			if "correo_copia" in selector:
				if selector["correo_copia"]["prefijo"]==prefijo:
					if selector["correo_copia"]["campo"]  <= len(campos):
						self.pycorreo["correo_para"]=campos[selector["correo_copia"]["campo"]-1]

			if "correo_oculta" in selector:
				if selector["correo_oculta"]["prefijo"]==prefijo:
					if selector["correo_oculta"]["campo"]  <= len(campos):
						self.pycorreo["correo_oculta"]=campos[selector["correo_oculta"]["campo"]-1]

			if "correo_asunto" in selector:
				if selector["correo_asunto"]["prefijo"]==prefijo:
					if selector["correo_asunto"]["campo"]  <= len(campos):
						self.pycorreo["correo_asunto"]=campos[selector["correo_asunto"]["campo"]-1]

			if "correo_bandera" in selector:
				if selector["correo_bandera"]["prefijo"]==prefijo:
					if selector["correo_bandera"]["campo"]  <= len(campos):
						self.pycorreo["correo_bandera"]=campos[selector["correo_bandera"]["campo"]-1]

		logger.debug(self.pycorreo)

	def TraerNombrePDF(self):
		salida=None
		for item in self.nombrepdf:
			if salida:
				salida +=f"-{item}"
			else:
				salida=f"{item}"
		return salida

	def SaltoPagina(self,linea):
		salida=False
		if "saltopagina" in self.encabezado:
			for saltopag in self.encabezado["saltopagina"]:
				buscar=linea.find(saltopag["texto"])
				if buscar >-1:
					if "colmuna" in saltopag:
						#Falta vericar si es entero columna!!!
						if buscar == saltopag["colmuna"]-1:
							salida=True
							logger.debug("SaltoPagina..")
							break
					else:
						logger.debug("SaltoPagina..")
						salida=True
						break
		return salida

	def EliminarCRLF(self, linea):
		logger.debug("EliminarCRLF")
		if isinstance( linea, bytes): linea=linea.decode("utf-8")
		linea=linea.replace("\r\n","")
		linea=linea.replace("\n","")
		#Verificar si esta en blanco
		temp=linea.replace(";","")
		if len(temp.strip())==0:linea=""
		linea=linea.strip()
		return linea

	def ExtraerPrefijo(self,campo,prefijo):
		salida =campo [:self.encabezado["ancho_prefijo"] ].strip()
		if len(salida)<=0:
			salida=prefijo
		else:
			campo=campo[ self.encabezado["ancho_prefijo"]: ]
		logger.debug(f"ExtraerPrefijo: [{salida}], {campo}")

		return salida, campo

	def AddCampoPag(self,campos, selectores):
		for selector in  selectores:
			if selector["campo"] -1 > len(campos):continue	#estar dentro del rango de campos
			texto=campos[ selector["campo"] -1 ]
			logger.debug(f"Texto: {texto}")
			if selector["nombre"] in self.pagina:
				pass
			else:
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
					self.pagina[ selector["nombre"] ]= {
						"letra_alto":selector["letra_alto"],
						"alinear":selector["alinear"],
						"letra":selector["letra"],
						"posx":selector["posx"],
						"posy":selector["posy"],
						"texto":[texto],
						}

	def Set_PyCorreo(self,iddoc):
		#esto hay que pulir por que esta solo para agrupar
		if not iddoc in self.listaPycorreo:
			temp=self.TraerNombrePDF()
			temp+=".pdf"
			self.pycorreo["nombre_pdf"]=os.path.join(self.encabezado["ruta_pdf"], temp )
			self.listaPycorreo[iddoc]=self.pycorreo
			self.pycorreo={}

	def GenerarPyCorreo(self):
		logger.info("GenerarPyCorreo")
		if not  "pycorreo" in self.encabezado: return
		ruta = self.encabezado["pycorreo"]["ruta"]
		if not os.path.isdir(ruta):
			os.makedirs(ruta)

		for idcod in self.listaPycorreo:
			fecha =datetime.now()
			logger.info(f"idcod:{idcod}-->{self.listaPycorreo[idcod]}")
			nombre=f"{str( uuid1())}-{fecha.day}-{fecha.month}-{fecha.year}-{fecha.hour}-{fecha.minute}-{fecha.second}.mail"
			nombre =os.path.join(ruta,nombre)
			arch=open(nombre,"w")
			arch.write(f"enviar::{self.listaPycorreo[idcod]['correo_para']}<|>")
			arch.write(f"pdf::{self.listaPycorreo[idcod]['nombre_pdf']}<|>")
			arch.write(f"asunto::{self.listaPycorreo[idcod]['correo_asunto']}<|>")
			arch.write(f"bandera::{self.listaPycorreo[idcod]['correo_bandera']}<|>")
			arch.write(f"rutavirtual::\n")
			arch.close()
			logger.info(f"{nombre}")

	def Procesar(self,archivo):
		logger.debug(f"Procesar:{archivo}")
		if not os.path.isfile(archivo):
			logger.error(f"No existe el archivo de datos: {archivo}")
			return False

		if "saltolineainicio" in self.encabezado:
			saltolinea_ini=self.encabezado["saltolineainicio"]
			if not isinstance(saltolinea_ini, int):
				saltolinea_ini=None
				logger.warning("encabezado.saltolineainicio, no es entero")
		else:
			saltolinea_ini=None

		logger.debug(f"SaltoLoinea: {saltolinea_ini}")

		poslinea=0
		iniciodoc=True
		agrupar=None
		prefijo=""
		o_paginalog=ObjPagLog(	up=self.encabezado["pagup"]["up"],
								orden=self.encabezado["pagup"]["uporden"],
								ancho=self.encabezado["tampapel"]["ancho"],
								largo=self.encabezado["tampapel"]["alto"],
								rutarecursos=self.rutarecursos,
							)
		arch_entrada=open(archivo,"r")
		for campos in arch_entrada.readlines():
			poslinea +=1
			if saltolinea_ini>0:		#Control salto de linea al inicio..
				logger.debug("Saltar linea al inicio")
				saltolinea_ini -=1
				poslinea=0
				continue
			if "fin_doc" in self.encabezado:
				if campos.find(self.encabezado["fin_doc"])>-1:
					logger.debug("-- Fin documento --")
					fin=True
					break

			campos=self.EliminarCRLF(campos)
			if len(campos)<=0: continue 	#Elimina lineas en blanco

			if iniciodoc:					#Obiviar el primer salto de pagina al inicio del documento
				iniciodoc=False
				saltopag=False
			else:
				salto_pag=self.SaltoPagina(campos)

			campos=campos.split(self.encabezado["sep_campo"])
			prefijo, campos[0]=self.ExtraerPrefijo(campos[0],prefijo)

			if "agrupar" in self.encabezado:
				logger.debug("Agrupar")
				if self.encabezado["agrupar"]["prefijo"] == prefijo:
					if agrupar==None:
						print (self.encabezado["agrupar"]["campo"]-1, campos)
						agrupar=campos [ self.encabezado["agrupar"]["campo"]-1 ]
						temp=agrupar
						logger.debug(f"inicio: {temp}")
						o_paginalog.SetID(agrupar)
					else:
						temp=campos[self.encabezado["agrupar"]["campo"]-1 ]
						logger.debug(f"No iguales: {temp} == {agrupar}")

					if agrupar != temp:
						agrupar = temp

						o_paginalog.SaltoPagina()
						o_paginalog.SetID(agrupar)
						self.nombrepdf=[]
			else:
				if SaltoPagina:
					logger.debug("Salto flata----")
					o_paginalog.SaltoPagina()


				logger.debug(f"Valor agrupar:{agrupar}, Anterior {temp}")
			#y si esta el perfijo en una lineas mas abajo de la primera???? falta
			if "nombre_pdf" in self.encabezado:  self.ExtraerPDF(prefijo,campos,self.encabezado["nombre_pdf"])
			if "pycorreo" in self.encabezado:    self.ExtarerPyCoreo(prefijo,campos)

			for items in self.selector:
				if prefijo==items["prefijo"]:
					self.AddCampoPag(campos, items["campos"])



			logger.debug(self.pagina)
			o_paginalog.AddPagina(self.pagina)
			self.Set_PyCorreo(agrupar)
			nombrepdf=self.TraerNombrePDF()
			nombrepdf +=".pdf"
			nombrepdf=os.path.join(self.encabezado["ruta_pdf"], nombrepdf)

			o_paginalog.SetNombrePDF (nombrepdf)
			logger.debug("Nombre Pdf:",self.TraerNombrePDF())

			self.lleno=False
			self.nombrepdf=[]

			self.pagina={}

			#Salto de pagina
			if iniciodoc:
				iniciodoc=False
		arch_entrada.close()
		o_paginalog.SaltoPagina()
		logger.debug("Generar PDF")


		obPDF = objF2S_PDF(self.encabezado, self.rutarecursos, o_paginalog)
		obPDF.Procesar()

		self.GenerarPyCorreo()
		#o_paginalog.BorrarTemp()
		# print (o_paginalog.cont_paginas)
		# for i in range(1,19):
		# 	o_paginalog.LeerPagina(i)




if __name__ =="__main__":
	from SimpleSoft.Facil import ObjFacil
	import argparse
	parser = argparse.ArgumentParser(description='Facil Ver 1.2')
	parser.add_argument( '-c', '--config',    dest='config',  default='config.ini' ,help='Configurarcion del loggin')
	parser.add_argument( '-r', '--recursos', dest='recursos', default="/home/marco/Clientes/niko_celis/inst-sanignacion-oyola/trabajo", help='Ruta de recursos')
	parser.add_argument( '-a', '--archivo' , dest='archivo',  default="/home/marco/Clientes/niko_celis/inst-sanignacion-oyola/trabajo/spools/pruebavarios.csv", help='Archivo de dato')
	parser.add_argument( '-p', '--ambiente', dest='ambiente', default="CompPago.amb", help='Nombre del ambiente')
	argumentos =  parser.parse_args()

	logging.config.fileConfig(argumentos.config, disable_existing_loggers=False)
	ob=ObjFacil(rutarecursos=argumentos.recursos)
	temp=os.path.join(argumentos.recursos, "temp")
	if not os.path.isdir(temp):
		os.makedirs(temp)

	ob.AbrirAmbiente(argumentos.ambiente)
	obCampos=ObjCampos(ob.getEncabezado(), ob.getSelector(), argumentos.recursos)
	obCampos.Procesar(argumentos.archivo)
