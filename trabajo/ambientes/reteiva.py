#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pickle
import datetime

#modelo Filas x Columnas

encabezado={
			"nombre":"comporbante",
			"tampapel":{"ancho":8.5,"alto":5.5,"medida":"pul"},
			"pagup":{"up":(1,1), "uporden":"Z"},						# si esta activo se define la paginas logicas  [col], [Filas] y el orden "Z" or "W"
			"tipos":( ('Ubuntu',     'Ubuntu-R.ttf'), 					# (nombre logico, nombre fisico)  Nota debe estar en fonts
					  ('Ubuntu-Bold','Ubuntu-B.ttf'),
					  ('Ubuntu-Cond','Ubuntu-C.ttf'),
					  ('f2sCodigo128','Codigo128.ttf')					# Si se va a usar codigo de barras se debe colocar....!
					),
			"formato":"ReteIVA.png",
			"modo":1,													# Filas x Columnas
			  ############################
			 # Normalizacion de paginas #
			############################
			'saltopag':('MAQUITODO S.A.S',),
			'nolineablanco':True,
			'eliminartexto':("\f",
						"--------------------------------------------------------------------------------",
						"------------------ ----------------- -----------------",
						),
			'detallefijo':{"inicio":"CONCEPTO                MONTO TOTAL",
					"fin":"** TOTAL",
					"pasa":"* P A S A *",
					"viene":"* V I E N E *",
					"lineas":26,
					"largoEncabezado":15,			#Define nro de lineas que debe tener el encazado para que de hay en adelante inicie el detalle
					},

			##"pos_salto":-1,
			"saltolineadoc":3,										#Eliminar del inicio de documento un numero de lineas int(##)
			#"eliminarlineaxpag":2,
			  ###################################
			 # Funciones Generales por agrupar #
			###################################
			"nombre_pdf":{"selector":[{"fila":10,"columnas":(17,35)},{"fila":6,"columnas":(32,53)}], #Nombre PDF, campos=[Pos Campos]
						  "formato":"ReteIVA-{0}_{1}",		#Toma el orden de cmapos y los acomoda.. Nota deben estar equilibrados
						  #"ruta_pdf":"/home/www-data/web2py/applications/siendo/static/PDF",	#Esta tambien sera la ruta
						  #"ruta_pdf":"/home/marco/workspace/virtualenv3/web2py/web2py/applications/siendo/static/PDF",	#Esta tambien sera la ruta
						  "ruta_pdf":"/home/marco/Clientes/maquitodo/trabajo/PDF",	#Esta tambien sera la ruta
						 },
			"agrupar":{"fila":10,"columnas":(17,35)},			#Id de pagina simpre debe ir!!
			  ###################################
			 # Funciones Envio Correo web2py #
			#################################
			"correoweb2py":[
							{"fila":6,  "columnas":(32,53),"nombre":"nrodoc"},
							{"fila":6,  "columnas":(32,40),"nombre":"Fecha","convert":"fecha3"},	#Adicona el 1 dia del mes del formato JUN-2019
							{"fila":6,  "columnas":(45,53),"nombre":"Fecha_Hasta","convert":"fecha4"},#Adicona el Ultimo dia del mes del formato JUN-2019
							{"fila":18, "columnas":(62,80),"nombre":"valor","convert":"float"},
							{"fila":10,  "columnas":(17,40),"nombre":"nit","hasta":"-"},		#El nombre debe ser el mismo nombre del campo en la base de datos
							{"fila":9,  "columnas":(13,48),"nombre":"nombre"},
			],
			}


selector=[
			{"fila":6, "nombre":"Periodo",
			"columnas":(32,53),
			"letra":"Ubuntu-Bold", "letra_alto":9, "posx":507, "posy":264 , "alinear":"C",
			"desp_y":0,
			"desp_x":0,
			},
			{"fila":9, "nombre":"Retenido",
			"columnas":(13,48),
			"letra":"Ubuntu-Bold", "letra_alto":10, "posx":120 , "posy":240 , "alinear":"I",
			"desp_y":0,
			"desp_x":0,
			},
			{"fila":10, "nombre":"Nit",
			"columnas":(17,40),
			"letra":"Ubuntu-Bold", "letra_alto":10, "posx":453 , "posy":240 , "alinear":"I",
			"desp_y":0,
			"desp_x":0,
			},
			{"fila":11, "nombre":"Direccion",
			"columnas":(13,50),
			"letra":"Ubuntu", "letra_alto":10, "posx":120, "posy":221, "alinear":"I",
			"desp_y":0,
			"desp_x":0,
			},
			{"fila":14, "nombre":"Ciudad retencion",
			"columnas":(41,60),
			"letra":"Ubuntu", "letra_alto":10, "posx":273.651, "posy":204.70, "alinear":"I",
			"desp_y":0,
			"desp_x":0,
			},
			#Detalle
			{"fila":25, "nombre":"concepto Iva",
			"columnas":(1,24),
			"posx":58.3, "posy": 166.52, "alinear":"I",
			"letra":"Ubuntu", "letra_alto":10,
			"desp_y":11,
			"desp_x":0,
			},
			{"fila":25, "nombre":"concepto Tasa",
			"columnas":(40,55),
			"posx":58.3, "posy": 155.52, "alinear":"I",
			"letra":"Ubuntu", "letra_alto":10,
			"desp_y":11,
			"desp_x":0,
			},
			{"fila":25, "nombre":"concepto Base",
			"columnas":(55,74),
			"posx":58.3, "posy": 144.52, "alinear":"I",
			"letra":"Ubuntu", "letra_alto":10,
			"desp_y":11,
			"desp_x":0,
			},

			{"filas":(25,31), "nombre":"Concepto",
			"columnas":(1,24),
			"posx":58.3, "posy": 133.52, "alinear":"I",
			"letra":"Ubuntu", "letra_alto":10,
			"desp_y":11,
			"desp_x":0,
			},
			{"filas":(25,31), "nombre":"Monto Total",
			"columnas":(25,44),
			"posx":352.14, "posy": 133.52, "alinear":"D",
			"letra":"Ubuntu", "letra_alto":10,
			"desp_y":11,
			"desp_x":0,
			},
			{"filas":(25,31), "nombre":"Valor Base",
			"columnas":(44,62),
			"posx":455, "posy": 133.52, "alinear":"D",
			"letra":"Ubuntu", "letra_alto":10,
			"desp_y":11,
			"desp_x":0,
			},
			{"filas":(25,31), "nombre":"Valor Retenido",
			"columnas":(62,80),
			"posx":554.73, "posy": 133.52, "alinear":"D",
			"letra":"Ubuntu", "letra_alto":10,
			"desp_y":11,
			"desp_x":0,
			},
			#Totales
			{"fila":18, "nombre":"Total Monto Total",
			"columnas":(25,44),
			"posx":352.14, "posy": 75.31, "alinear":"D",
			"letra":"Ubuntu-Bold", "letra_alto":10,
			"desp_y":11,
			"desp_x":0,
			},
			{"fila":18, "nombre":"Total Valor Base",
			"columnas":(44,62),
			"posx":455, "posy": 75.31, "alinear":"D",
			"letra":"Ubuntu-Bold", "letra_alto":10,
			"desp_y":11,
			"desp_x":0,
			},
			{"fila":18, "nombre":"Total Valor Retenido",
			"columnas":(62,80),
			"posx":554.73, "posy": 75.31, "alinear":"D",
			"letra":"Ubuntu-Bold", "letra_alto":10,
			"desp_y":11,
			"desp_x":0,
			},
			{"filas":(21,22), "nombre":"Fecha Expedicion",
			"columnas":(19,50),
			"posx":400 , "posy": 34, "alinear":"I",
			"letra":"Ubuntu", "letra_alto":9,
			"desp_y":11,
			"desp_x":0,
			},
			{"fila":20, "nombre":"Nota",
			"columnas":(7,50),
			"posx":103 , "posy": 54, "alinear":"I",
			"letra":"Ubuntu", "letra_alto":10,
			"desp_y":11,
			"desp_x":0,
			},

			# {"parrafo":{"ancho":250, "alto":300 },
			# 	"sel_posx":(46,506), "sel_posy":(521,602),"nombre":"observacion",
			# 	"letra":"Ubuntu", "letra_alto":9, "posx":110, "posy":335, "desp_y":11,
			# 	"alinear":"I"},
			# 		]

		]

archivo=open("reteiva.amb","wb")
pickle.dump(encabezado,archivo)
pickle.dump(selector,archivo)
archivo.close()
