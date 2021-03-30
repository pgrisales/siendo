# -*- coding: utf-8 -*-
import os
import zipfile
from PIL import Image
import cv2
import base64

class ObjImagen():
	def __init__(self, db, db1, ruta):
		self.nroprocesos=0
		self.db=db
		self.db1=db1
		self.ruta=ruta
		self.idproceso=0


	def ProcesosParaInicio(self):
		#Revisar la tabla proceso   [tbl_proceso] y buscar los que este pendientes
		lstprocesos=self.db(self.db.tbl_proceso.estado=="ingreso").select()
		for item in lstprocesos:
			self.idproceso=item.id
			self.ArchivoValido(item.archivo)
			


	def ArchivoValido(self, archivo):
		#Determinar si es un zip y descomprimir
		rutacompleta= os.path.join(self.ruta,"uploads",archivo)
		if not os.path.isfile(rutacompleta):
			print ("archivo no existe")
			return False


		try:
			zipfile.PyZipFile(rutacompleta)
			#descomprimir
			# crear nuevos procesos
			print ("zip")
		except Exception as e:
			#no es un zip
			print ("no zip")

		area=self.DetectarCara(rutacompleta)
		if len(area) == 0:
			self.db(self.db.tbl_proceso.id==self.idproceso).update(mensaje="Error no contiene rostro humano",estado="error" )
			self.db.commit()
			print ("Error no contiene rostro humano")
			return

		self.db(self.db.tbl_proceso.id==self.idproceso).update(estado="proceso" )
		self.db.commit()		
		nuevonombre, idpersona=self.Convertir(area, rutacompleta, archivo)
		print (nuevonombre, idpersona)

		usuario=self.db1(self.db1.tstpersona.idpersona==idpersona).isempty()
		print(usuario)
		if usuario:
			self.db(self.db.tbl_proceso.id==self.idproceso).update(mensaje="Error no existe usuario",estado="error" )
			print ("error no existe usuario")
			self.db.commit()
			return

		#usuario existe!!
		foto="data:image/jpg;base64,"
		with open(nuevonombre,"rb") as img_arch:
			foto +=base64.b64encode(img_arch.read()).decode('utf-8')
		print (foto)
		self.db1(self.db1.tstpersona.idpersona==idpersona).update(psrfoto=foto)
		self.db1.commit()
		self.db(self.db.tbl_proceso.id==self.idproceso).update(estado="finalizado" )
		self.db.commit()		

		return True

	def DetectarCara(self, ruta):
		img = cv2.imread(ruta)
		# Pasamos la ruta del XML
		rmodulo=os.path.join(self.ruta,"modules","haarcascade_frontalface_alt.xml")
		cascade = cv2.CascadeClassifier(rmodulo)
		rects = cascade.detectMultiScale(img, 1.3, 4, cv2.CASCADE_SCALE_IMAGE, (80,80))
		if len(rects) == 0:
			return rects
		rects[:, 2:] += rects[:, :2]
		return rects

	def Convertir(self, rects,archentrada,archsalida):
		archsalida=archsalida.split(".")
		deco=base64.b16decode(archsalida[3],archsalida[2])
		deco=deco.decode("utf-8")
		deco=deco[0:deco.find(".") ]
		archsalida=os.path.join(self.ruta,'uploads',deco+".jpg")
		for x1, y1, x2, y2 in rects:
			factorx=250
			factory=500
			x1 -= factorx
			y1 -= factory
			x2 += factorx
			y2 += factory
			imagcorte=Image.open(archentrada)
			area=(x1, y1, x2, y2)
			corte=imagcorte.crop(area)
			ancho, alto = corte.size
			if ancho >500:
				print (ancho, alto)
				porcentaje=ancho / 500
				ancho =500
				alto = int (alto / porcentaje)
				print (ancho, alto)
				corte=corte.resize((ancho,alto))
		corte.save(archsalida)
		try:
			deco=int(deco)
		except Exception as e:
			deco=0
		return archsalida, deco

#Verificar si el idpersona  existe en la tabla [tstpersona]
#Ajustar al rosto
#Guardar en la tabla
