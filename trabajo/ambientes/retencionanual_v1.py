#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pickle
import datetime

#modelo Filas x Columnas

encabezado={
			"nombre":"Retencion_Anual",
			"tampapel":{"ancho":8.5,"alto":5.5,"medida":"pul"},
			"pagup":{"up":(1,1), "uporden":"Z"},						# si esta activo se define la paginas logicas  [col], [Filas] y el orden "Z" or "W"
			"tipos":( ('Ubuntu',     'Ubuntu-R.ttf'), 					# (nombre logico, nombre fisico)  Nota debe estar en fonts
					  ('Ubuntu-Bold','Ubuntu-B.ttf'),
					  ('Ubuntu-Cond','Ubuntu-C.ttf'),
					  ('f2sCodigo128','Codigo128.ttf')					# Si se va a usar codigo de barras se debe colocar....!
					),
			"formato":"retencion_anual.png",
			"modo":1,													# Filas x Columnas
			  ############################
			 # Normalizacion de paginas #
			############################
			'saltopag':('\f',),
			'nolineablanco':True,
			'eliminartexto':(
						"--------------------------------------------------------------------------------",
						"------------------- -------------------",
						),
			'moverlineas':(
							{"buscartexto":"ANO GRAVABLE", "nuevafila":5},
							{"buscartexto":"RETENIDO", "nuevafila":10},
							{"buscartexto":"Fecha Expedicion", "nuevafila":30},
						),
			'detallefijo':{"inicio":"C O N C E P T O",
					"fin":"** TOTAL",
					"lineas":20,
					"largoEncabezado":10,			#Define nro de lineas que debe tener el encazado para que de hay en adelante inicie el detalle
					},
			##"pos_salto":-1,
			"lineasxpag":66,
			#"saltolineadoc":8,										#Eliminar del inicio de documento un numero de lineas int(##)
			#"eliminarlineaxpag":8,
			"iniciopag":"CERTIFICADO",

			  ###################################
			 # Funciones Generales por agrupar #
			###################################
			"nombre_pdf":{"selector":[{"fila":1,"columnas":(1,80)},#Titulo
									  {"fila":5,"columnas":(32,80)}, #Año
									  {"fila":11,"columnas":(17,48)}], #nit Nombre PDF, campos=[Pos Campos]
						  "formato":"{0}-{1}_{2}",		#Toma el orden de cmapos y los acomoda.. Nota deben estar equilibrados
						  "ruta_pdf":"/home/www-data/web2py/applications/siendo/static/PDF",	#Esta tambien sera la ruta
						 },

			"agrupar":{"fila":11,"columnas":(22,40)},			#Id de pagina simpre debe ir!!
			##################################
			 # Funciones Envio Correo web2py #
			#################################
			"correoweb2py":[
							{"selector":[
											{"fila":1, "nombre":"Titulo","columnas":(1,80)},
											{"fila":5,"columnas":(45,80)},#Año
										  	{"fila":11,"columnas":(17,48)},#nit
										  ],
										  "nombre":"nrodoc"}, #Nro de cedula + fecha
							{"fila":22,  "columnas":(19,48),"nombre":"Fecha","convert":"fecha5"},
							{"fila":19, "columnas":(61,81),"nombre":"valor","convert":"float"},
							{"fila":11,  "columnas":(17,48),"nombre":"nit", "convert":"sin_guion"},
							{"fila":10,  "columnas":(12,48),"nombre":"nombre"},#nombre del proveedor
			],
			}

selector=[
			{"fila":1, "nombre":"Titulo",
			"columnas":(1,80),
			"letra":"Ubuntu-Bold", "letra_alto":14, "posx":306, "posy":295 , "alinear":"C",
			"desp_y":0,
			"desp_x":0,
			"colortexto_rgb":(0.1,0.2,1)
			},
			{"fila":5, "nombre":"año",
			"columnas":(32,80),
			"letra":"Ubuntu-Bold", "letra_alto":14, "posx":306, "posy":280 , "alinear":"C",
			"desp_y":0,
			"desp_x":0,
			"fun_formato":'AÑO {}',
			"colortexto_rgb":(0.1,0.2,1)

			},
			{"fila":22, "nombre":"Fecha",
			"columnas":(19,48),
			"letra":"Ubuntu", "letra_alto":9, "posx":420, "posy":320 , "alinear":"I",
			"desp_y":0,
			"desp_x":0,
			},
			{"fila":10, "nombre":"Proveedor",
			"columnas":(12,48),
			"letra":"Ubuntu", "letra_alto":9, "posx":105, "posy":240 , "alinear":"I",
			"desp_y":0,
			"desp_x":0,
			},
			{"fila":11, "nombre":"Nit",
			"columnas":(17,48),
			"letra":"Ubuntu", "letra_alto":9, "posx":105, "posy":255 , "alinear":"I",
			"desp_y":0,
			"desp_x":0
			},
			{"fila":12, "nombre":"Direccion",
			"columnas":(12,53),
			"letra":"Ubuntu", "letra_alto":9, "posx":105, "posy":226 , "alinear":"I",
			"desp_y":0,
			"desp_x":0,
			},
			{"fila":12, "nombre":"ciudad",
			"columnas":(54,80),
			"letra":"Ubuntu", "letra_alto":9, "posx":400, "posy":226 , "alinear":"I",
			"desp_y":0,
			"desp_x":0,
			},
			{"fila":15, "nombre":"retCiudad",
			"columnas":(41,80),
			"letra":"Ubuntu", "letra_alto":9, "posx":245, "posy":213 , "alinear":"I",
			"desp_y":0,
			"desp_x":0,
			},
			{"fila":16, "nombre":"consigCiudad",
			"columnas":(41,80),
			"letra":"Ubuntu", "letra_alto":9, "posx":245, "posy":197 , "alinear":"I",
			"desp_y":0,
			"desp_x":0,
			},
			{"fila":19, "nombre":"TotalBase",
			"columnas":(30,61),
			"letra":"Ubuntu-Bold", "letra_alto":10, "posx":451, "posy":47 , "alinear":"D",
			"desp_y":0,
			"desp_x":0,
			},
			{"fila":19, "nombre":"TotalRetenido",
			"columnas":(61,81),
			"letra":"Ubuntu-Bold", "letra_alto":10, "posx":539, "posy":47 , "alinear":"D",
			"desp_y":0,
			"desp_x":0,
			},
			{"fila":23, "nombre":"Firma",
			"columnas":(19,48),
			"letra":"Ubuntu", "letra_alto":8, "posx":360, "posy":25 , "alinear":"I",
			"desp_y":0,
			"desp_x":0,
			},
			#Detalle
			{"filas":(24,42), "nombre":"Concepto",
			"columnas":(1,35),
			"posx":55, "posy": 140, "alinear":"I",
			"letra":"Ubuntu", "letra_alto":9,
			"desp_y":9,
			"desp_x":0,
			},
			{"filas":(24,42), "nombre":"tasa",
			"columnas":(36,41),
			"posx":333, "posy": 140, "alinear":"D",
			"letra":"Ubuntu", "letra_alto":9,
			"desp_y":9,
			"desp_x":0,
			},
			{"filas":(24,42), "nombre":"Base",
			"columnas":(42,61),
			"letra":"Ubuntu", "letra_alto":9, "posx":451, "posy":140 , "alinear":"D",
			"desp_y":9,
			"desp_x":0,
			},
			{"filas":(24,42), "nombre":"Retenido",
			"columnas":(61,81),
			"letra":"Ubuntu", "letra_alto":9, "posx":539, "posy":140, "alinear":"D",
			"desp_y":9,
			"desp_x":0,
			},

		]

archivo=open("retencionanual.amb","wb")
pickle.dump(encabezado,archivo)
pickle.dump(selector,archivo)
archivo.close()
