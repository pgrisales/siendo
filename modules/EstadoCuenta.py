# -*- coding: utf-8 -*-
import  os
class F2S_Estado():
	"""docstring for ClassName"""
	def __init__(self, archivo=None):
		self.archivo = archivo
		self.Error=None
	def Procesar(self, archivo=None):
		if archivo: self.archivo=archivo
		if not os.path.isfile(self.archivo):
			self.Error=f"No existe el archivo {self.archivo}"
			return False
		arch=open(self.archivo,"rb")

		nit=None
		cuenta=1
		for linea in arch.readlines():
			linea=linea.decode("latin-1")
			linea=linea.replace("\n","")
			linea=linea.replace("\r","")
			linea=linea.strip()
			if len(linea)<1: continue										#Lineas en blanco
			if  linea[0]=="-" or linea[0]=="|" or  linea[0]=="+" or  linea[0]=="_" or  linea[0]=="\f" : continue	#Eliminar encabezado
			if cuenta>230:
				break
			cuenta +=1
			if nit==None:
				nit = linea[137:154].strip()
				print (f"Nit:{nit}")
				continue
			if len(linea[137:154].strip())>0:
				print (linea)
				if nit != linea[137:154].strip():
					nit = linea[137:154].strip()
					print (f"Cambio  a Nit:{nit}")
				else:
					print ("mismo nit")
				continue


			print ("linea:{}".format(linea))

		arch.close()

if __name__ == "__main__":
	print ("Inicio")
	ob=F2S_Estado("/home/marco/Clientes/IngenieriaGrafica/trabajo/spools/UFCC2021.PAX")
	ob.Procesar()
