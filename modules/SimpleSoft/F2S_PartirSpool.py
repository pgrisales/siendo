#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
from uuid import uuid1
from os	import remove		as BORRAR
from os.path import join 	as UNIR
from os.path import isfile 	as EXITE
from os.path import isdir 	as DIRECTORIO
from os import makedirs 	as CREAR

logger = logging.getLogger(__name__)


class ObjPartirDoc():
	"""Parte un documento en paginas"""
	def __init__(self, ruta, archivo,
					saltopag=None, oviarsalto=True, lnXpag=0,
					 offsetdoc=0, offsetpag=0, posicion=0, moverlineas=None,nolineablanco=True,
					 unirpaglog=None,eliminartexto=None,detallefijo=None, prueba=True, iniciopag=None, ln_posicion=50):
		logger.info("Archivo:{}".format(archivo) )
		if not DIRECTORIO(UNIR(ruta,"temp")): CREAR(UNIR(ruta,"temp"))
		self.nombre     = UNIR( ruta,"temp", "Facil_Partir{}".format(str(uuid1())) ) 	#nombre del archivo de salida
		self.archivo    = archivo			#Archivo de datos
		self.saltopag   = saltopag			#Debe ser una lista
		#self.posicion   = posicion		#posicion fija del salto de pagina si es negativo, en cualquier lugar de la linea
		self.paginas    = 0				#Contador de paginas
		self.lineasxpag	= lnXpag
		self.offsetdoc=offsetdoc
		self.offsetpag=offsetpag
		self.oviarsalto=oviarsalto
		self.moverlineas=moverlineas
		self.unirpaglog=unirpaglog
		self.eliminartexto=eliminartexto
		self.detallefijo=detallefijo
		self.nolineablanco=nolineablanco
		self.prueba=prueba
		self.iniciopag=iniciopag
		self.ln_posicion=ln_posicion

	def ProcesarCR(self,linea):
		linea=linea.replace("\r\n","")
		linea=linea.replace("\n","")
		#Eliminar texto
		if self.eliminartexto:
			for eliminar in self.eliminartexto:
				#print (eliminar)
				linea=linea.replace(eliminar,"")
		#procesar Linea
		partir=linea.split("\r")
		salida=list(partir.pop(0))
		for texto in partir:
			if len(texto)==0:continue
			if texto==salida:continue
			posx = -1
			for letra in texto:
				posx +=1
				if len(salida)-1 >=posx:
					if salida[posx]==" ":
						salida[posx]=letra
				else:
					salida.append(letra)
		salida="".join(salida)
		salida+= "\n"
		#logger.debug ("salida final",salida)
		return salida

	def BuscarFinPag(self, linea):
		'''Buscar el salto de pagina, si devuelve una lista >1 es que hubo salto(s) '''
		salida=[]
		if isinstance(linea,bytes):
			linea=linea.decode("Latin-1")
		haysalto=False
		for salto in self.saltopag:
			buscar=linea.find(salto)
			#print ("salto:",buscar, salto)
			if buscar >-1:
				while buscar >-1:
					salida.append(linea[:buscar])
					haysalto=True
					if self.oviarsalto:
						linea=linea[buscar+len(salto):]
					else:
						linea=linea[buscar:]
					buscar=linea.find(salto)

		return haysalto, salida

	def Fun_GuardarAchivo(self,encabezado,detalle):

		#Acondiciona la posicion del detalle debajo de encabezado...
		calculo=self.ln_posicion - len(encabezado)
		if calculo>0:
			for i in range(0,calculo ):
				encabezado.append('\n')


		paginas=int(len(detalle) / self.detallefijo["lineas"])
		if len(detalle) % self.detallefijo["lineas"]>0:	paginas +=1
		pagina=1
		lineaxpag=self.detallefijo["lineas"]

		while detalle:
			if lineaxpag==self.detallefijo["lineas"]:
				arcsalida =open("{}.pag{:06d}".format(self.nombre, self.paginas), "wb")
				logger.debug("{}.pag{:06d}".format(self.nombre, self.paginas))
				for item in encabezado:
					arcsalida.write(item.encode("Latin-1"))
				#kaos#linea="Pag:{:02d} de: {:02d}\n".format(pagina, paginas)
				#kaos#arcsalida.write(linea.encode("Latin-1"))
			linea=detalle.pop(0)
			arcsalida.write(linea.encode("Latin-1"))
			lineaxpag -=1
			if lineaxpag ==0 or len(detalle)==0:
				arcsalida.close()
				self.paginas +=1
				pagina +=1
				lineaxpag=self.detallefijo["lineas"]

	def Fun_DetalleFijo(self):
		#print ("Fun_DetalleFijo")
		archivo = open(self.archivo,"rb")
		self.paginas=1
		arcsalida =open("{}.pag{:06d}".format(self.nombre, 1), "wb")
		logger.debug("{}.pag{:06d}".format(self.nombre, 1))
		detalle=[]
		act_detalle=True
		total=[]
		act_total=False
		encabezado=[]
		act_encabeado=True
		act_viene=False
		tempoffsetpag=self.offsetpag
		iniciopagina=True

		archivo = open(self.archivo,"rb")
		#print ("self.offsetdoc",self.offsetdoc)
		for linea in archivo.readlines():


			if self.offsetdoc>0:					#Actua solo en la primera pagina
				self.offsetdoc -=1
				continue
			if tempoffsetpag>0 and self.paginas>1:	#Actua despues de la primera Pagina
				tempoffsetpag-=1
				continue
			linea=linea.decode('latin-1')
			if self.iniciopag and iniciopagina:						#la primeralinea inicia cuando encuenta este textos
				print ("Busqueda de inicio de pagina")
				if linea.find(self.iniciopag)>-1:
					iniciopagina=False
				else:
					continue

			if act_encabeado:
				#print ("encabezado")
				if linea.find(self.detallefijo["inicio"])>-1:
					nrolineasxpag=self.detallefijo["lineas"]
					act_encabeado=False
					act_detalle=True
					detalle=[]								#inicio del detalle por lo general son el titulo que no se utiliza
					continue
				if self.moverlineas:
					for moverlineas in self.moverlineas:
						print (moverlineas)
						if linea.find(moverlineas["buscartexto"])>-1:
							#print ('contxxxxxxxxxxxxxxxxxxxxxxxxxxx')
							calculo=moverlineas["nuevafila"] - len(encabezado)
							if calculo>0:
								for item in range(1,calculo):
									encabezado.append("\n")

				encabezado.append(self.ProcesarCR(linea))
				continue
			#print (self.detallefijo)
			if "pasa" in self.detallefijo:
				if linea.find(self.detallefijo["pasa"])>-1:
					#print ("pasa!.............")
					act_viene=True
			if "viene" in self.detallefijo:
				if linea.find(self.detallefijo["viene"])>-1:
					#print ("viene!")
					act_viene=False
					continue
			if act_viene:continue
			if act_detalle:
				print (encabezado)
				#print ("Detalle")
				linea=self.ProcesarCR(linea)
				if linea.find(self.detallefijo["fin"])>-1:
					##print ("fin del detealle")
					act_detalle=False
					act_total=True
					if self.nolineablanco and linea=="\n":continue
					if len(encabezado)<self.detallefijo["largoEncabezado"]:
						for i in range(len(encabezado),self.detallefijo["largoEncabezado"]):
							encabezado.append("\n")

					encabezado.append(linea)
					continue

				if self.nolineablanco and linea=="\n":continue
				detalle.append(linea)
				continue
			if act_total:
				haysalto, salida = self.BuscarFinPag(linea)
				if not haysalto:


					if self.moverlineas:
						for moverlineas in self.moverlineas:
							print (moverlineas)
							if linea.find(moverlineas["buscartexto"])>-1:
								#print ('piecontxxxxxxxxxxxxxxxxxxxxxxxxxxx')
								calculo=moverlineas["nuevafila"] - len(encabezado)
								if calculo>0:
									for item in range(1,calculo):
										encabezado.append("\n")


					linea=self.ProcesarCR(linea)
					if self.nolineablanco and linea=="\n":continue
					encabezado.append(linea)
					continue
				else:
					encabezado.append(salida[0])


				self.Fun_GuardarAchivo(encabezado,detalle)
				detalle=[]
				act_detalle=True
				total=[]
				act_total=False
				encabezado=[]
				act_encabeado=True
				act_viene=False
				tempoffsetpag=self.offsetpag
				iniciopagina=True
				print ("fin de pagina")
				# if salida:
				# 	encabezado.append(salida[1])

		archivo.close()
		if len(detalle)>0:
			if len(encabezado)<self.detallefijo["largoEncabezado"]:
				for i in range(len(encabezado),self.detallefijo["largoEncabezado"]):
					encabezado.append("\n")

			self.Fun_GuardarAchivo(encabezado,detalle)

		return True

	def Procesar(self):
		if not EXITE(self.archivo):
			logger.debug("Error el archivo:[{}] No existe".format(self.archivo))
			return False
			self.paginas=1
		if self.detallefijo: return self.Fun_DetalleFijo()

		archivo = open(self.archivo,"rb")
		arcsalida =open("{}.pag{:06d}".format(self.nombre, 1), "wb")
		logger.debug("{}.pag{:06d}".format(self.nombre, 1))
		nrolinea=0
		arcabierto=True
		activarsalto=False
		if self.offsetpag>0:
			tempoffsetpag=self.offsetpag
		else:
			tempoffsetpag=0
		inicio=True
		for linea in archivo.readlines():
			if self.offsetdoc>0:
				self.offsetdoc -=1
				continue
			if tempoffsetpag>0 and self.paginas>1:
				tempoffsetpag-=1
				continue
			linea=self.ProcesarCR(linea.decode('latin-1'))

			nrolinea += 1
			if self.lineasxpag>0 and nrolinea == self.lineasxpag:
				#print ("salto x linea")
				arcsalida.write(linea.encode('latin-1') )
				if self.prueba: print(f"{nrolinea}   {linea}")
				arcsalida.close()
				self.paginas +=1
				arcsalida =open("{}.pag{:06d}".format(self.nombre, self.paginas ), "wb")
				nrolinea=0
				continue
			#Ajustar lineas
			if self.moverlineas:
				for moverlinea in self.moverlineas:
					buscar=linea.find(moverlinea['buscartexto'])
					if buscar>-1:
						print ('nuevafila',moverlinea ['nuevafila'], '-',nrolinea)
						if nrolinea < moverlinea ['nuevafila']:
							calculo=moverlinea ['nuevafila']-nrolinea
							print ('calculo:',calculo)
							for i in range(calculo):
								arcsalida.write('enblanco\n'.encode('latin-1'))
							nrolinea=moverlinea ['nuevafila']
							continue
			#Salto de pagina con texto:
			haysalto, salida = self.BuscarFinPag(linea)
			if haysalto:
				temp=salida.pop()
				arcsalida.write(temp.encode('latin-1') )
				if self.prueba:	print(f"{nrolinea}   {temp [:-1]}")
				arcsalida.close()
				arcabierto=False
				self.paginas +=1
				if self.offsetpag>0:tempoffsetpag=self.offsetpag
				if self.prueba: print(f"Salto pagina--------- normal {self.paginas}")
				#print (f'salida={salida}')
				if salida:
					arcabierto=True
					if self.prueba: print(f"open-aqui1-pag {self.paginas}")
					arcsalida =open("{}.pag{:06d}".format(self.nombre, self.paginas ), "wb")
					while len(salida)>1:
						arcsalida.write(salida.pop().encode('latin-1') )
						arcsalida.close()
						if self.prueba: print("Salto pagina---------")
						self.paginas +=1
						if self.prueba: print(f"open aqui2 --pag{self.paginas}")
						arcsalida =open("{}.pag{:06d}".format(self.nombre, self.paginas ), "wb")
					linea=salida.pop()
					arcsalida.write(linea.encode('latin-1') )
					nrolinea=1
					if self.prueba: print(f"{nrolinea}   {linea[:-1]}")
				else:
					#self.paginas +=1
					if self.prueba: print(f"open--pag{self.paginas}")
					arcsalida =open("{}.pag{:06d}".format(self.nombre, self.paginas ), "wb")
					nrolinea=0
					continue
			else:

				arcsalida.write(linea.encode('latin-1') )
				if self.prueba:	print(f"{nrolinea}   {linea[:-1]}")
		if arcabierto:
			arcsalida.close()
		print ("Final")
		return True

	def BorrarTemp(self):
		for pagina in range(1,self.paginas):
			archivo="{}.pag{:06d}".format(self.nombre, pagina)
			BORRAR(archivo)
		return True

	def LeerPagina(self,nropag):
		archivo =open("{}.pag{:06d}".format(self.nombre, nropag), "rb")
		lineas=[]
		for linea in archivo.readlines():
			linea=linea.decode("latin-1")
			linea.replace("\n","")
			lineas.append(linea)
		archivo.close()
		return lineas

if __name__ =="__main__":
	import argparse
	from Facil 			import ObjFacil
	parser = argparse.ArgumentParser(description='Facil Ver 1.3')
	parser.add_argument( '-f', '--archivo' , dest='archivo',  help='Ruta y nombre del archivo de datos')
	parser.add_argument( '-r', '--recursos', dest='recursos',   help='Ruta del recurso (trabajo)')
	parser.add_argument( '-a', '--ambiente', dest='ambiente', help='Nombre completo del ambiente')
	argumentos =  parser.parse_args()

	obfacil=ObjFacil(rutarecursos=argumentos.recursos)
	obfacil.AbrirAmbiente(argumentos.ambiente)
	encabezado = obfacil.getEncabezado()
	for x in encabezado:
		print ("{} = {}".format(x,encabezado[x]))

	print(obfacil.getSaltoLineaDoc())

	ob=ObjPartirDoc(
					argumentos.recursos,
					prueba=True,
					archivo      =argumentos.archivo,
					saltopag     =obfacil.getSaltoPagina(),
					offsetpag    =obfacil.getEliminarLineaxPag(),
					nolineablanco=obfacil.getNoLineaBlanco(),
					offsetdoc    =obfacil.getSaltoLineaDoc(),
					lnXpag       =obfacil.getNroLineaxPag(),
					moverlineas  =obfacil.getMoverLineas(),
					eliminartexto=obfacil.getElinarTexto(),
					detallefijo  =obfacil.getDetalleFijo(),
					iniciopag    =obfacil.getIniciopag(),
		)

	ob.Procesar()
	print ("Nombre temportal :",ob.nombre)
	print ("Numero de paginas:",ob.paginas)
	for pagina in range(1,ob.paginas):
		x=1
		archivo="{}.pag{:06d}".format(ob.nombre, pagina)
		print (archivo)
		archivo=open(archivo,"r")
		for linea in archivo.readlines():
			print ("{}  [{}]".format (x, linea[:-1]  ) )
			x+=1
			archivo.close()
