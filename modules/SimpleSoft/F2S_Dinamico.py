#!/usr/bin/env python3
# -*- coding: utf-8 -*-
class objDinamico():
	"""Selector dinamico de datos"""
	def __init__(self, encabezado, selector, lineas):
		super(objDinamico, self).__init__()
		self.lineas     = lineas
		self.selector   = selector
		self.encabezado = encabezado
		print (selector)
		
	def Procesar(self):
		for selector in self.selector:
			if "linea" in selector:		#procesar una sola linea
				if selector["linea"] <= len(self.lineas):
					linea = self.lineas[selector["linea"]-1]
					print(linea)
					if "texto" in selector:
						buscar=linea.find(selector["texto"])
						if buscar:
							if "poscol" in selector:				#por posicion de columna
								if buscar == selector["poscol"] :
									return selector["ambiente"]
							else:
								return selector["ambiente"]			#No importa la columna
					else:
						pass

			else:
				pass
				#for linea in self.lineas:
		return None






