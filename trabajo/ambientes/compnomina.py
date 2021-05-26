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
			"formato":"comp_Nomina.png",
			"modo":1,													# Filas x Columnas
			  ############################
			 # Normalizacion de paginas #
			############################
			'saltopag':('| EMPRESA',),
			'nolineablanco':True,
			'eliminartexto':("\f",
						"====================================================================================================================================",
						"------------------------------------------------------------------------------------------------------------------------------------",
						"-------------------- ",
						"--------------",
						"-------------",
						),
			'detallefijo':{"inicio":"CODIGO    N O M B R E ",
					"fin":"T O T A L  --->",
					"pasa":"* P A S A *",
					"viene":"* V I E N E *",
					"lineas":26,
					"largoEncabezado":5,			#Define nro de lineas que debe tener el encazado para que de hay en adelante inicie el detalle
					},
            'posdetalle':10,    #Linea posicion detalle, por defecto si no se incluye es 50

			##"pos_salto":-1,
			"saltolineadoc":3,										#Eliminar del inicio de documento un numero de lineas int(##)
			#"eliminarlineaxpag":2,
			  ###################################
			 # Funciones Generales por agrupar #
			###################################
			"nombre_pdf":{"selector":[{"fila":10,"columnas":(1,15)},{"fila":1,"columnas":(23,49)}], #Nombre PDF, campos=[Pos Campos]
						  "formato":"comporbanteNomina-{0}_{1}",		#Toma el orden de cmapos y los acomoda.. Nota deben estar equilibrados
						  "ruta_pdf":"/home/www-data/web2py/applications/siendo/static/PDF",	#Esta tambien sera la ruta
						 },
			"agrupar":{"fila":10,"columnas":(1,15)},			#Id de pagina simpre debe ir!!
			  ###################################
			 # Funciones Envio Correo web2py #
			#################################
			"correoweb2py":[
							{"fila":1,  "columnas":(23,49),"nombre":"nrodoc"},
							{"fila":1,  "columnas":(106,114),"nombre":"Fecha","convert":"fecha2"},
							{"fila":1,  "columnas":(120,128),"nombre":"Fecha_Hasta","convert":"fecha2"},
							{"fila":6, "columnas":(40,56),"nombre":"valor","convert":"float"},
							{"fila":10,  "columnas":(1,15),"nombre":"nit"},		#El nombre debe ser el mismo nombre del campo en la base de datos
							{"fila":10,  "columnas":(15,44),"nombre":"nombre"},
			],
			}

selector=[
			{"fila":1, "nombre":"Numero",
			"columnas":(23,32),
			"letra":"Ubuntu-Bold", "letra_alto":12, "posx":498.750, "posy":300 , "alinear":"C",
			"desp_y":0,
			"desp_x":0,
			},
			{"fila":1, "nombre":"Numero-cont",
			"columnas":(32,48),
			"letra":"Ubuntu-Bold", "letra_alto":8, "posx":498.750, "posy":287 , "alinear":"C",
			"desp_y":0,
			"desp_x":0,
			},
			{"fila":10, "nombre":"Nombre Empleado",
			"columnas":(1,44),
			"letra":"Ubuntu-Bold", "letra_alto":10, "posx":100, "posy":264.75, "alinear":"I",
			"desp_y":0,
			"desp_x":0,
			},
			{"fila":3, "nombre":"Cargo",
			"columnas":(104,127),
			"letra":"Ubuntu", "letra_alto":9, "posx":413, "posy":264.75, "alinear":"I",
			"desp_y":0,
			"desp_x":0,
			},
			{"fila":3, "nombre":"Centro de Costo",
			"columnas":(13,40),
			"letra":"Ubuntu", "letra_alto":10, "posx":100, "posy":250.50, "alinear":"I",
			"desp_y":0,
			"desp_x":0,
			},
			{"fila":3, "nombre":"Fecha Ingreso",
			"columnas":(54,64),
			"letra":"Ubuntu", "letra_alto":10, "posx":413, "posy":250.50 , "alinear":"I",
			"desp_y":0,
			"desp_x":0,
			},
			{"fila":3, "nombre":"C.O. Oficina",
			"columnas":(71,95),
			"letra":"Ubuntu", "letra_alto":10, "posx":100, "posy":237, "alinear":"I",
			"desp_y":0,
			"desp_x":0,
			},
			{"fila":2, "nombre":"Tipo Nomina",
			"columnas":(14,50),
			"letra":"Ubuntu", "letra_alto":10, "posx":413, "posy":237, "alinear":"I",
			"desp_y":0,
			"desp_x":0,
			},
			{"fila":7, "nombre":"Nro Cta",
			"columnas":(6,20),
			"letra":"Ubuntu", "letra_alto":10, "posx":444, "posy":203.68, "alinear":"I",
			"desp_y":0,
			"desp_x":0,
			},
			#Detalle
			{"filas":(10,31), "nombre":"Concepto",
			"columnas":(45,63),
			"posx":55, "posy": 164, "alinear":"I",
			"letra":"Ubuntu", "letra_alto":9,
			"desp_y":9,
			"desp_x":0,
			},
			{"filas":(10,31), "nombre":"Descripcion",
			"columnas":(64,89),
			"posx":110, "posy": 164, "alinear":"I",
			"letra":"Ubuntu", "letra_alto":9,
			"desp_y":9,
			"desp_x":0,
			},
			{"filas":(10,31), "nombre":"Cant. Horas",
			"columnas":(89,103),
			"posx":322.9, "posy": 164, "alinear":"D",
			"letra":"Ubuntu", "letra_alto":9,
			"desp_y":9,
			"desp_x":0,
			},
			{"filas":(10,31), "nombre":"Devengado",
			"columnas":(103,117),
			"posx":432.2, "posy": 164, "alinear":"D",
			"letra":"Ubuntu", "letra_alto":9,
			"desp_y":9,
			"desp_x":0,
			"fun_numero1":"{:,.0f}"
			},
			{"filas":(10,31), "nombre":"Deducido",
			"columnas":(117,132),
			"posx":538.91, "posy": 164, "alinear":"D",
			"letra":"Ubuntu", "letra_alto":9,
			"desp_y":9,
			"desp_x":0,
			"fun_numero1":"{:,.0f}"
			},
			#Totales
			{"fila":6, "nombre":"Total Cant. Horas",
			"columnas":(88,103),
			"posx":322.9, "posy": 35.34, "alinear":"D",
			"letra":"Ubuntu-Bold", "letra_alto":10,
			"desp_y":0,
			"desp_x":0,
			},
			{"fila":6, "nombre":"Total Devengado",
			"columnas":(103,117),
			"posx":432.2, "posy": 35.34, "alinear":"D",
			"letra":"Ubuntu-Bold", "letra_alto":10,
			"desp_y":0,
			"desp_x":0,
			"fun_numero1":"{:,.0f}"

			},
			{"fila":6, "nombre":"Total Deducido",
			"columnas":(117,132),
			"posx":538.91, "posy": 35.34, "alinear":"D",
			"letra":"Ubuntu-Bold", "letra_alto":10,
			"desp_y":0,
			"desp_x":0,
			"fun_numero1":"{:,.0f}"

			},

			{"fila":6, "nombre":"Neto a pagar",
			"columnas":(40,58),
			"posx":538.91, "posy": 18, "alinear":"D",
			"letra":"Ubuntu-Bold", "letra_alto":12,
			"desp_y":0,
			"desp_x":0,
			"fun_numero1":"$ {:,.0f}"
			},
			{"fila":1, "nombre":"Periodo liq.",
			"columnas":(106,128),
			"posx":146.2 , "posy": 16.78, "alinear":"I",
			"letra":"Ubuntu", "letra_alto":10,
			"desp_y":0,
			"desp_x":0,
			},

			# {"parrafo":{"ancho":250, "alto":300 },
			# 	"sel_posx":(46,506), "sel_posy":(521,602),"nombre":"observacion",
			# 	"letra":"Ubuntu", "letra_alto":9, "posx":110, "posy":335, "desp_y":11,
			# 	"alinear":"I"},
			# 		]

		]

archivo=open("compnomina.amb","wb")
pickle.dump(encabezado,archivo)
pickle.dump(selector,archivo)
archivo.close()
