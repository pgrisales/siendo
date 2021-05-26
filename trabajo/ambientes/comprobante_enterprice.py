#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pickle
ambiente={
    "nombre":"comprobante_enter",
    "tampapel":{"ancho":8.5,"alto":11.5,"medida":"pul"},
    "pagup":{"up":(1,1), "uporden":"Z"},						# si esta activo se define la paginas logicas  [col], [Filas] y el orden "Z" or "W"
    "tipos":( ('Ubuntu',     'Ubuntu-R.ttf'), 					# (nombre logico, nombre fisico)  Nota debe estar en fonts
    		  ('Ubuntu-Bold','Ubuntu-B.ttf'),
    		  ('Ubuntu-Cond','Ubuntu-C.ttf'),
    		  ('f2sCodigo128','Codigo128.ttf')					# Si se va a usar codigo de barras se debe colocar....!
    		),
    "formato":"comporbante.png",
    'pag_despx':0,                                              #Mueve el formato  con respecto  a los datos.
    'pag_despy':0,
    "modo":5,                                                   # Lectura PDF version 2
    "limite_total":{'texto':'Sumas Iguales:', 'y0':-2, 'y1':2},      #texto para extraer limite en y=-2 y1=+2
    'idpag':'{nrodoc}',
    'web2pycampos':['nrodoc','nit',
                    'F2S_LoadPlugins.call_plugin("ModNomCliente", entregadoa=self.obPagina.campos["entregadoa"]["texto"])',
                    'F2S_LoadPlugins.call_plugin("ModFecha1", fecha=self.obPagina.campos["fecha"]["texto"])',
                    'F2S_LoadPlugins.call_plugin("ModValorTotal", valor_total=self.obPagina.campos["valor_total"]["texto"])',
                    'F2S_LoadPlugins.call_plugin("ModNombrePDF", nombre="ComprPago", fecha=self.obPagina.campos["fecha"]["texto"], nrodoc=self.obPagina.campos["nrodoc"]["texto"])',
                    ],
    'funciones':[##'F2S_LoadPlugins.call_plugin("AdLinea", objPagina=self.obPagina, desde="debitos", a="creditos", limite="Auxiliar")',
                 'F2S_LoadPlugins.call_plugin("MontoEscrito", objPagina=self.obPagina, campo="montoescrito")',
                    ],    #preproceso de datos
    #Mejoras:
    #Esto hay crear otra variable, para dividir encabazado de seleccion....!!!!
    'bloques':[
        {   #Coordenas Nro Doc
            'x0':  431.99991222496595,  'x1':   508.8146969274376,
            'y0':    732.896226841392,  'y1':     739.74630410136,
            'selectores':[
                        {'nombre':'nrodoc',
                            'fila':1,
                            'cols':(1,20),
                            'letra':'Ubuntu-Bold',
                            'letra_alto':9,
                            'posx':468,
                            'posy':765,
                            'alinear':'I',
                            'desp_y':0,
                            'desp_x':0,
                            'texto': []},
                        ],
        },
        {   #Coordenas Fecha
            'x0':  431.99982719999997,  'x1':  480.01458277112874,
            'y0':    722.216231113392,  'y1':     729.06630837336,

            'selectores':[
                        {'nombre':'fecha',
                            'fila':1,
                            'cols':(1,20),
                            'alinear': 'I',
                            'desp_x': 0,
                            'desp_y': 0,
                            'letra': 'Ubuntu-Bold',
                            'letra_alto': 9,
                            'posx': 468,
                            'posy': 750,
                            'texto': []},

                    ],
        },
        {   #Coordenas entregadoa
            'x0':          71.9999712,  'x1':  418.4,
            'y0':    689.456244217392,  'y1':     696.30632147736,
            'selectores':[
                        {'nombre':'entregadoa',
                            'fila':1,
                            'cols':(14,80),
                            'alinear': 'I',
                            'desp_x': 0,
                            'desp_y': 0,
                            'letra': 'Ubuntu-Bold',
                            'letra_alto': 10,
                            'posx': 95,
                            'posy': 700,
                            'texto': []},

                    ],
        },
        {   #Coordenas Nro id cliente o nit
            'x0':  419.99983199999997,  'x1':   492.0146118472478,
            'y0':    689.456244217392,  'y1':     696.30632147736,
            'selectores':[
                        {'nombre':'nit',
                            'fila':1,
                            'cols':(1,20),
                            'letra':'Ubuntu-Bold',
                            'letra_alto':9,
                            'posx':450,
                            'posy':700,
                            'alinear':'I',
                            'desp_y':0,
                            'desp_x':0,
                            'texto': []},

                    ],
        },
        {   #Coordenas Valor Total
            'x0':        509.999796,  'x1':   582.0145758472478,
            'y0':    606.176277529392,  'y1':     613.02635478936,

            'selectores':[
                        {'nombre':'valor_total',
                            'fila':1,
                            'cols':(1,80),
                            'alinear': 'D',
                            'desp_x': 0,
                            'desp_y': 0,
                            'letra': 'Ubuntu-Bold',
                            'letra_alto':10,
                            'posx': 560,
                            'posy': 630,
                            'texto': []},

                    ],
        },
        {   #Coordenas Valor Total montoescrito
            'x0':        509.999796,  'x1':   582.0145758472478,
            'y0':    606.176277529392,  'y1':     613.02635478936,

            'selectores':[
                        {'nombre':'montoescrito',
                            'fila':1,
                            'cols':(1,80),
                            'alinear': 'I',
                            'desp_x': 0,
                            'desp_y': 0,
                            'letra': 'Ubuntu',
                            'letra_alto': 8,
                            'posx': 95,
                            'posy': 690,
                            'desp_y':11,
                            'texto': [],
                            'parrafo':{'ancho':460, 'alto': 36}
                            },

                    ],
        },
        #informacion Consignacion
        {   #*Coordenas banco
            'x0':          71.9999712,  'x1':   163.2146974450129,
            'y0':    649.376260249392,  'y1':     656.22633750936,

            'selectores':[
                        {'nombre':'info_id_banco',
                            'fila':1,
                            'cols':(1,3),
                            'posx':80,
                            'posy':445,
                            'alinear':'C',
                            'letra':'Ubuntu',
                            'letra_alto':9,
                            'desp_y':11,
                            'desp_x':0,
                            'texto': []},

                    ],
        },
        {   #*Coordenas banco
            'x0':          71.9999712,  'x1':   163.2146974450129,
            'y0':    649.376260249392,  'y1':     656.22633750936,
            'selectores':[
                        {'nombre':'info_nombre_banco',
                            'fila':1,
                            'cols':(4,20),
                            'posx':110,
                            'posy':445,
                            'alinear':'I',
                            'letra':'Ubuntu',
                            'letra_alto':9,
                            'desp_y':11,
                            'desp_x':0,
                            'texto': []},

                    ],
        },
        {   #Coordenas Cuenta cliente encabezado
            'x0':  419.99983199999997,  'x1':   540.0146603994858,
            'y0':    649.376260249392,  'y1':     656.22633750936,
            'selectores':[
                {'nombre':'cuenta',
                'fila':1,
                'cols':(1,60),
                'alinear': 'I',
                'desp_x': 0,
                'desp_y': 0,
                'letra': 'Ubuntu',
                'letra_alto': 9,
                'posx': 270,
                'posy': 445,
                'texto': []},
            ],
        },
        {   #Coordenas T. Cta
            'x0':          71.9999712,  'x1':  418.4,
            'y0':    689.456244217392,  'y1':     696.30632147736,

            'selectores':[
                        {'nombre':'titular_cuenta',
                            'fila':1,
                            'cols':(14,46),
                            'alinear': 'I',
                            'desp_x': 0,
                            'desp_y': 0,
                            'letra': 'Ubuntu',
                            'letra_alto': 9,
                            'posx': 405,
                            'posy': 445,
                            'texto': []},

                    ],
        },
        #Egresos
        {   #Egreso bancos id
        'x0':   24.0,  'x1':   73.0,
        'y0':    606.176277529392,  'y1':     613.02635478936,
        'selectores':[
                {'nombre':'banco_id',
                'fila':1,
                'cols':(1,20),
                'alinear': 'I',
                'desp_x': 0,
                'desp_y': 0,
                'letra': 'Ubuntu',
                'letra_alto': 9,
                'posx': 342,
                'posy': 580,
                'texto': []},
            ],
        },
        {   #Egreso bancos Desp Egresos
            'x0':  102.0,  'x1':   262.0,
            'y0':    606.176277529392,  'y1':   613.02635478936,
            'selectores':[
                {'nombre':'Egreso_Descripcion',
                'fila':1,
                'cols':(1,80),
                'alinear': 'I',
                'desp_x': 0,
                'desp_y': 0,
                'letra': 'Ubuntu',
                'letra_alto': 9,
                'posx': 72,
                'posy': 580,
                'texto': []},
            ],
        },
        {   #egresos col valor`
            'x0':        509.999796,  'x1':   582.0145758472478,
            'y0':    606.176277529392,  'y1':     613.02635478936,

            'selectores':[
                        {'nombre':'egreso_valor',
                            'fila':1,
                            'cols':(1,80),
                            'alinear': 'D',
                            'desp_x': 0,
                            'desp_y': 0,
                            'letra': 'Ubuntu',
                            'letra_alto': 9,
                            'posx': 560,
                            'posy': 580,
                            'texto': []},

                    ],
        },
        {   #egresos  valor total`
            'x0':        509.999796,  'x1':   582.0145758472478,
            'y0':    606.176277529392,  'y1':     613.02635478936,

            'selectores':[
                        {'nombre':'egreso_valor_total',
                            'fila':1,
                            'cols':(1,80),
                            'alinear': 'D',
                            'desp_x': 0,
                            'desp_y': 0,
                            'letra': 'Ubuntu-Bold',
                            'letra_alto': 10,
                            'posx': 560,
                            'posy': 490,
                            'texto': []},

                    ],
        },
        #
        {   #Coordenas Nota
            'x0':  53.999978399999996,  'x1':  529.2146426601958,
            'y0':   583.9762864093921,  'y1':     590.82636366936,
            'selectores':[
            {'nombre':'nota',
            'filas':(1,2),
            'cols':(1,150),
            'alinear': 'I',
            'desp_x': 0,
            'desp_y': 0,
            'letra': 'Ubuntu',
            'letra_alto': 9,
            'posx': 50,
            'posy': 70,
            'desp_y':11,
            'parrafo':{'ancho':200, 'alto': 100},
            'texto': []},
            ],
        },
        {   #Coordenas Autorizado por
            'x0':   503.039798784,      'x1':   584.6546451989522,
            'y0':    392.936362825392,  'y1':     476.22640950936,
            'selectores':[
            {'nombre':'autorizado_por',
            'fila':1,
            'cols':(1,80),
            'alinear': 'I',
            'desp_x': 0,
            'desp_y': 0,
            'letra': 'Ubuntu',
            'letra_alto': 8,
            'posx': 280,
            'posy': 36,
            'desp_y':11,
            'texto': []},
            ],
        },
        #sumas Iguales
        {   #Coordenas Total Debitos
            'x0':         425.9998296,  'x1':  498.01460944724784,
            'y0':    449.936340025392,  'y1':     533.22638670936,
            'total':True,        #Indicador para campo total
            'selectores':[
            {'nombre':'total_debitos',
            'fila':1,
            'cols':(1,80),
            'alinear': 'D',
            'desp_x': 0,
            'desp_y': 0,
            'letra': 'Ubuntu-Bold',
            'letra_alto': 10,
            'posx': 458,
            'posy': 85,
            'texto': []},
            ],
        },
        {   #Coordenas Total Creditos
            'x0':   518.5197925919999,  'x1':   590.5347008224146,
            'y0':    449.936340025392,  'y1':     533.22638670936,
            'total':True,        #Indicador para campo total
            'selectores':[
            {'nombre':'total_creditos',
            'fila':1,
            'cols':(1,80),
            'alinear': 'D',
            'desp_x': 0,
            'desp_y': 0,
            'letra': 'Ubuntu-Bold',
            'letra_alto': 10,
            'posx': 570,
            'posy': 85,
            'texto': []},
            ],
        },

        #Detalle
        {   #Coordenas auxiliar
            'x0':        19.0,  'x1':   77.5,
            'y0':    460.976335609392,  'y1':     552.78637888536,
            'detalle':True,
            'selectores':[
                        #Columna auxiliar
                        {'nombre':'Auxiliar',
                            'filas':(1,80),
                            'cols':(1,20),
                            'alinear': 'I',
                            'desp_x': 0,
                            'desp_y': 0,
                            'letra': 'Ubuntu',
                            'letra_alto': 9,
                            'posx': 36,
                            'posy': 394,
                            'desp_y':11,
                            'texto': []},

                    ],
        },
        {   #Coordenas C.O.
            'x0':        82.559966976,  'x1':   96.97470273783846,
            'y0':    460.976335609392,  'y1':     552.78637888536,
            'detalle':True,
            'selectores':[
                        #Columna auxiliar
                        {'nombre':'c.o.',
                            'filas':(1,80),
                            'cols':(1,20),
                            'alinear': 'I',
                            'desp_x': 0,
                            'desp_y': 0,
                            'letra': 'Ubuntu',
                            'letra_alto': 9,
                            'posx': 108,
                            'posy': 396,
                            'desp_y':11,
                            'texto': []},
                    ],
        },
        {   #Detalle col tercero
            'x0':       124.559950176,  'x1':   186.9747493174452,
            'y1':     552.78637888536,  'y0':    460.976335609392,
            'detalle':True,
            'selectores':[
                        #Columna Debitos
                        {'nombre':'terceros',
                            'filas':(1,80),
                            'cols':(1,20),
                            'letra':'Ubuntu',
                            'letra_alto':9,
                            'posx':150,
                            'posy':394,
                            'alinear':'I',
                            'desp_y':11,
                            'desp_x':0,
                            'texto': []},

                    ],
        },
        {   #Coordenas D. Cruce / M. Pago
            'x0':  335.51986579199996,  'x1':  407.53501738909915,
            'y0':    511.976315209392,  'y1':     552.78637888536,
            'detalle':True,
            'selectores':[
                        #Columna auxiliar
                        {'nombre':'cruce_pago',
                            'filas':(1,80),
                            'cols':(1,20),
                            'alinear': 'I',
                            'desp_x': 0,
                            'desp_y': 0,
                            'letra': 'Ubuntu',
                            'letra_alto': 9,
                            'posx': 234,
                            'posy': 394,
                            'desp_y':11,
                            'texto': []},

                    ],
        },
        {   #Detalle col Debitos
            'x0':        424.79983008,  'x1':  496.81460992724783,
            'y0':    511.976315209392,  'y1':     552.78637888536,
            'detalle':True,                     #se ve afectado por el total
            'selectores':[
                        #Columna Debitos
                        {'nombre':'debitos',
                            'guadarpos':0, #esto esta relacion con 'iniciotexo' para el calculo de posy
                            'filas':(1,80),
                            'cols':(1,20),
                            'letra':'Ubuntu',
                            'letra_alto':9,
                            'posx':458,
                            'posy':394,
                            'alinear':'D',
                            'desp_y':11,
                            'desp_x':0,
                            'texto': []},

                    ],
        },
        {   #Detalle col Creditos -++ busque la longitud de debubio y sumar al principio
            'x0':   518.5202098168331,  'x1':   590.5351954383191,
            'y0':    460.976335609392,   'y1':   550,
            'detalle':True,                     #se ve afectado por el total
            'selectores':[
                        #Columna Debitos
                        {'nombre':'creditos',
                            'iniciotexto':{'campo':'debitos'},
                            'filas':(1,80),
                            'cols':(1,20),
                            'letra':'Ubuntu',
                            'letra_alto':9,
                            'posx':570,
                            'posy':400,
                            'alinear':'D',
                            'desp_y':11,
                            'desp_x':0,
                            'texto': []},

                    ],
        },


]}

opcional=False

archivo=open("comprobante_enterprice.amb","wb")
pickle.dump(ambiente,archivo)
archivo.close()
## banco marco 380 8901 et 3205
