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
from SimpleSoft.F2S_PagLogicas 	import ObjPagLog
from SimpleSoft.F2S_CrearPDF2  	import objF2S_PDF
from SimpleSoft.F2S_PartirSpool	import ObjPartirDoc
from SimpleSoft.Facil 			import ObjFacil

logger = logging.getLogger(__name__)



class ObjFilas():
	"""Manejo de Campos"""
	def __init__(self, facil, rutarecursos, borrartemp=False ):
		#print ("Print ObjFilas.inicio")
		self.Facil = facil
		self.rutarecursos  = rutarecursos
		self.nombrepdf =[]
		self.pagina={}
		self.pycorreo={}
		self.lleno=False
		self.borrartemp=borrartemp
		self.listaPycorreo={}
		temp=os.path.join(rutarecursos, "temp")
		if not os.path.isdir(temp):
			os.makedirs(temp)

	def Fun_Fecha1(self,fecha):
		#ajutar fecha de entrada ej:'2019-SEP-17'
		mes={"ENE":"01","FEB":"02","MAR":"03","ABR":"04","MAY":"05","JUN":"06",
			"JUL":"07","AGO":"08","SEP":"09","OCT":"10","NOV":"11","DIC":"12"}
		#print (fecha)
		fecha=fecha.strip()
		pos=fecha[5:8]
		fecha=fecha.replace(pos,mes[pos])
		#print (fecha)
		return fecha

	def Fun_Fecha2(self,fecha):
		#ajutar fecha de entrada ej:'20190917'
		fecha=fecha.strip()
		#print (fecha)
		fecha=f"{fecha[0:4]}-{fecha[4:6]}-{fecha[6:8]}"
		return fecha

	def Fun_Fecha3(self,fecha):
		#formato Jun-2019 y entegar Año-Mes-01
		mes={"ENE":"01","FEB":"02","MAR":"03","ABR":"04","MAY":"05","JUN":"06",
			"JUL":"07","AGO":"08","SEP":"09","OCT":"10","NOV":"11","DIC":"12"}
		fecha=fecha.strip()
		pos=fecha[0:3]
		fecha=fecha.replace(pos,mes[pos])
		fecha=f"{fecha[3:]}-{fecha[0:2]}-01"
		return fecha

	def Fun_Fecha4(self,fecha):
		#formato Jun-2019 y entegar Año-Mes-Ultimo dia del mes...
		import calendar
		try:
			mes={"ENE":"01","FEB":"02","MAR":"03","ABR":"04","MAY":"05","JUN":"06",
				"JUL":"07","AGO":"08","SEP":"09","OCT":"10","NOV":"11","DIC":"12"}
			fecha=fecha.strip()
			pos=fecha[0:3]
			fecha=fecha.replace(pos,mes[pos])
			diafin=calendar.monthrange(int({fecha[3:]}),int({fecha[0:2]}))[1]
			fecha=f"{fecha[3:]}-{fecha[0:2]}-diafin"
		except Exception as e:
			fecha=None
		return fecha

	def Fun_Fecha5(self,fecha):
		#ENERO        31 DEL 2020 entegar Año-Mes-Dia
		meses={"ENERO":"01","FEBRERO":"02","MARZO":"03","ABRIL":"04","MAYO":"05","JUNIO":"06",
			"JULIO":"07","AGOSTO":"08","SEPTIEMBRE":"09","OCTUBRE":"10","NOVIEMBRE":"11","DICIEMBRE":"12"}

		mes=fecha[:-13].strip()
		if mes in meses:
			mes=meses[mes]
		else:
			mes="01"
		#print ("[{}]".format(mes))
		salida ="{}-{}-{}".format (fecha[-4:],mes, fecha[13:15])
		#print ("Fun_Fecha5:")
		#print (fecha)
		#print  (salida)
		return salida

	def Fun_SinGion(self,campo):
		#deja solo el texto ante del sin_guion
		salida=campo
		posicion=campo.find("-")
		if posicion>-1:
			salida =campo[:posicion]
		return salida

	def ExtraerPDF(self,prefijo,campos, encabezado):
		#seleccion de campos
		for items in  encabezado["selector"]:
			if items["prefijo"]!=prefijo:break
			logger.debug(f"Estraer_PDF : {items}")
			for selcampos in items["campos"]:
				calculo=selcampos -1
				if calculo <= (len(campos)-1):
					self.nombrepdf.append(campos[calculo])
		self.lleno=True
		logger.debug(f"Estraer PDF:{self.nombrepdf}")

	def ExtarerPyCoreo(self, prefijo,campos):

		if "pycorreo" in self.encabezado:
			selector = self.encabezado["pycorreo"]
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
			texto=texto.strip()
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
					if "fun_numero1" in selector:
						temp=selector["fun_numero1"]
					else:
						temp=None

					self.pagina[ selector["nombre"] ]= {
						"letra_alto":selector["letra_alto"],
						"alinear":selector["alinear"],
						"letra":selector["letra"],
						"posx":selector["posx"],
						"posy":selector["posy"],
						"texto":[texto],
						"fun_numero1":temp
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
		poslinea=0
		iniciodoc=True
		agrupar=None
		o_paginalog=ObjPagLog(	up=self.Facil.getUp(),
								orden=self.Facil.getUpOrden(),
								ancho=self.Facil.getTamancho(),
								largo=self.Facil.getTamalto(),
								rutarecursos=self.Facil.ruta )
		o_partir=ObjPartirDoc (	ruta		 =self.Facil.ruta,
								archivo		 =archivo,
								saltopag	 =self.Facil.getSaltoPagina(),
								offsetpag    =self.Facil.getEliminarLineaxPag(),
								offsetdoc    =self.Facil.getSaltoLineaDoc(),
								lnXpag       =self.Facil.getNroLineaxPag(),
								moverlineas  =self.Facil.getMoverLineas(),
								detallefijo	 =self.Facil.getDetalleFijo(),
								nolineablanco=self.Facil.getNoLineaBlanco(),
								eliminartexto=self.Facil.getElinarTexto(),
								iniciopag    =self.Facil.getIniciopag(),
                                ln_posicion  =self.Facil.getPosDetalle()
							)
		o_partir.Procesar()

		selector_pdf=self.Facil.setPDF()		#Devuelve el selector para PDF or None
		agrupar=self.Facil.getIDdoc()			#Devuelve el selector para IDdoc or None
		web2py=self.Facil.getWeb2pyCorreo()		#Devuelve el selector para Web2py or None
		iddoc_anterior=None
		poslinea=0

		for pagina in range (1,o_partir.paginas):
			logger.debug(f"Procesando pagina nro:{pagina}")
			lineas=o_partir.LeerPagina(pagina)


			self.Facil.pagina={}
			#lineas=self.Facil.NormalizarLineas(lineas)

			for selector in self.Facil.getSelector():

				#logger.debug(f"Selector: {selector}")
				#ok
				if "filas" in selector:
					extraerlineas= lineas[ selector["filas"][0]-1 :selector["filas"][1]  ]
					for linea in extraerlineas:
						texto = linea[selector["columnas"][0]-1:selector ["columnas"][1]-1 ]
						self.Facil.AddCampoPagina(selector,texto)
				elif "fila" in selector:
					extraerlineas= lineas[ selector["fila"] -1 ]
					texto = extraerlineas[selector["columnas"][0]-1:selector ["columnas"][1]-1 ]
					self.Facil.AddCampoPagina(selector,texto)

			#Define el ID de la pagina dado en el campo agrupar
			if agrupar:
				iddoc=lineas[agrupar["fila"]-1]
				iddoc=iddoc[ agrupar["columnas"][0]-1 : agrupar["columnas"][1]-1]
				iddoc=iddoc.strip()
			else:
				logger.warning("No existe id pagina")
				iddoc=f"{pagina}"
			logger.debug(f"iddoc: [{iddoc}]")
			o_paginalog.SetID(iddoc)


			if not iddoc_anterior==iddoc:
				iddoc_anterior=iddoc
				if selector_pdf:
					texto=[]
					for selector in selector_pdf:
						extraerlineas= lineas[ selector["fila"] -1 ]
						temp = extraerlineas[selector["columnas"][0]-1:selector ["columnas"][1]-1 ]
						texto.append(temp.strip())
					#print (texto)
					if len(texto)<1:
						logger.warning("Error no exite campo dentro del spool para el nombre del PDF")
						self.Facil.SetNombrePDF("defecto")
					else:
						self.Facil.SetNombrePDF(texto)
				#print ("*"*80)
			o_paginalog.SetNombrePDF(self.Facil.nombre_pdf)
			o_paginalog.AddPagina(self.Facil.pagina)
			if web2py:
				print("web2py...web2py..")
				registroweb2py={}
				for selector in web2py:
					# print ("selector aqui", selector)
					if "selector" in selector:
						campo=""
						for selrango in selector["selector"]:
							# print ("sel rango:...........................")
							# print (selrango)
							temporal=lineas[selrango["fila"]-1]
							# print (temporal)
							temporal=temporal[selrango["columnas"][0] -1 : selrango["columnas"][1] -1  ]
							campo +=temporal.strip() +"_"
						campo=campo[:-1]
					else:
						campo=lineas[selector["fila"]-1]
						campo=campo[selector["columnas"][0] -1 : selector["columnas"][1] -1  ]

					if "hasta" in selector:
						buscar=campo.find(selector["hasta"])
						campo=campo[:buscar]

					if "convert" in selector:
						if selector["convert"]=="float":
							campo = campo.replace (",","")
							campo = campo.replace ("$","")
							campo = campo.strip()
							try:
								campo = float(campo)
							except Exception as e:
								pass
						elif selector["convert"]=="fecha1":
							campo= self.Fun_Fecha1(campo.strip())
						elif selector["convert"]=="fecha2":
							campo= self.Fun_Fecha2(campo.strip())
						elif selector["convert"]=="fecha3":
							campo= self.Fun_Fecha3(campo.strip())
						elif selector["convert"]=="fecha5":
							campo= self.Fun_Fecha5(campo.strip())
						elif selector["convert"]=="sin_guion":
							campo= self.Fun_SinGion(campo.strip())

					registroweb2py["pdf"]=self.Facil.nombre_pdf
					if isinstance(campo,str):
						registroweb2py[selector["nombre"]]=campo.strip()
					else:
						registroweb2py[selector["nombre"]]=campo

				print ("registroweb2py:",registroweb2py)

				self.Facil.addRegWeb2py(registroweb2py)
			logger.debug("Fin de pagina ******")

		logger.debug( f"Nro paginas: {o_paginalog.cont_paginas}" )
		obPDF = objF2S_PDF(self.Facil.encabezado, self.Facil.ruta, o_paginalog )
		obPDF.Procesar()
		if self.borrartemp:
			o_partir.BorrarTemp()
			o_paginalog.BorrarTemp()

		#print("self.Facil.web2pycorreo",self.Facil.web2pycorreo)
		return self.Facil.web2pycorreo


if __name__ =="__main__":
	import argparse
	parser = argparse.ArgumentParser(description='Facil Ver 1.2')
	parser.add_argument( '-c', '--config',    dest='config',  default='config.ini' ,help='Configurarcion del loggin')
	parser.add_argument( '-r', '--recursos', dest='recursos', default="/home/marco/Clientes/maquitodo/trabajo", help='Ruta de recursos')
	parser.add_argument( '-f', '--archivo' , dest='archivo',  default="/home/marco/Clientes/maquitodo/trabajo/spools/nomina2.txt", help='Archivo de dato')
	parser.add_argument( '-a', '--ambiente', dest='ambiente', default="compnomina.amb", help='Nombre del ambiente')
	argumentos =  parser.parse_args()

	logging.config.fileConfig(argumentos.config, disable_existing_loggers=False)
	ob=ObjFacil(rutarecursos=argumentos.recursos)
	ob.AbrirAmbiente(argumentos.ambiente)
	obFilasCol=ObjFilas(ob, argumentos.recursos)
	obFilasCol.Procesar(argumentos.archivo)
