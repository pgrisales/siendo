#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pickle
ambiente={
    "nombre":"Comp_Reteiva",
    "tampapel":{"ancho":8.5,"alto":5.5,"medida":"pul"},
    "pagup":{"up":(1,1), "uporden":"Z"},						# si esta activo se define la paginas logicas  [col], [Filas] y el orden "Z" or "W"
    "tipos":( ('Ubuntu',     'Ubuntu-R.ttf'), 					# (nombre logico, nombre fisico)  Nota debe estar en fonts
    		  ('Ubuntu-Bold','Ubuntu-B.ttf'),
    		  ('Ubuntu-Cond','Ubuntu-C.ttf'),
    		  ('f2sCodigo128','Codigo128.ttf')					# Si se va a usar codigo de barras se debe colocar....!
    		),
    "formato":"reteiva_enter.png",
    'pag_despx':0,                                              #Mueve el formato  con respecto  a los datos.
    'pag_despy':0,
    "modo":4,                                                   # Lectura PDF

    'idpag':'{nrodoc}',
    'web2pycampos':[
                     'nrodoc',
                     'F2S_LoadPlugins.call_plugin("ExtraerDatos", texto=self.obPagina.campos["nit"]["texto"], indice=1, separador="-")',
                     'F2S_LoadPlugins.call_plugin("ModNomCliente", entregadoa=self.obPagina.campos["retenidoa"]["texto"])',
                     'F2S_LoadPlugins.call_plugin("ModFecha1", fecha=self.obPagina.campos["fecha"]["texto"])',
                     'F2S_LoadPlugins.call_plugin("ModValorTotal", valor_total=self.obPagina.campos["total_monto"]["texto"])',
                     'nombrepdf'
                     ],
    'funciones':['F2S_LoadPlugins.call_plugin("DcoCompuesto", objPagina=self.obPagina, ruta="Comp_Reteiva" )'],    #Genera el nombre del pdf y nrodoc
    #Mejoras:
    #Esto hay crear otra variable, para dividir encabazado de seleccion....!!!!
    'bloques':[
        {   #titulo
            'x0':       152.159939136,  'x1':   459.3171693899372,
            'y0':    684.351566259264,  'y1':    698.204840717952,
            'selectores':[
                        {'nombre':'titulo',
                            'fila':1,
                            'cols':(1,80),
                            'letra':'Ubuntu-Bold',
                            'letra_alto':14,
                            'posx':420,
                            'posy':307,
                            'alinear':'C',
                            'desp_y':0,
                            'desp_x':0,
                            'colortexto_rgb':(0,0,128),
                            'texto': []},
                        ],
        },
        {   #Rango de Fecha
            'x0':       200,  'x1':   414,
            'y0':    674.697210121008,  'y1':   683.1831267266399,
                        'selectores':[
                        {'nombre':'rango_fecha',
                            'fila':1,
                            'cols':(1,80),
                            'letra':'Ubuntu-Bold',
                            'letra_alto':8,
                            'posx':420,
                            'posy':298,
                            'alinear':'C',
                            'desp_y':0,
                            'desp_x':0,
                            'texto': []},
                        ],
        },
        {   #Retenido a
            'x0':  100,  'x1':  500,
            'y0':    621.537231385008,  'y1':     641.06314357464,
            'selectores':[
                {'nombre':'retenidoa',
                'fila':1,
                'cols':(1,90),
                'letra':'Ubuntu-Bold',
                'letra_alto':9,
                'posx':126,
                'posy':239,
                'alinear':'I',
                'desp_y':0,
                'desp_x':0,
                'texto': []},
            ],
        },
        {   #Nit
            'x0':  100,  'x1':  500,
            'y0':    621.537231385008,  'y1':     641.06314357464,
            'selectores':[
                {'nombre':'nit',
                    'fila':2,
                    'cols':(1,90),
                    'letra':'Ubuntu-Bold',
                    'letra_alto':9,
                    'posx':450,
                    'posy':239,
                    'alinear':'I',
                    'desp_y':0,
                    'desp_x':0,
                    'texto': []},
                ],
        },
        {   #Direccion
            'x0':  105.47995780800001,  'x1':  500.0 ,
            'y0':    589.977244009008,  'y1':   609.5031561986399,
            'selectores':[
                {'nombre':'direccion',
                    'fila':1,
                    'cols':(1,90),
                    'letra':'Ubuntu',
                    'letra_alto':9,
                    'posx':126,
                    'posy':222,
                    'alinear':'I',
                    'desp_y':0,
                    'desp_x':0,
                    'texto': []},
                ],
        },
        {   #Ciudad donde practico retención
                    'x0':       250,  'x1':   500,
                    'y0':   568.9167724332001,  'y1':       576.584769366,
                    'selectores':[
                        {'nombre':'ciudad_pract',
                            'fila':1,
                            'cols':(1,90),
                            'letra':'Ubuntu',
                            'letra_alto':9,
                            'posx':198,
                            'posy':205,
                            'alinear':'I',
                            'desp_y':0,
                            'desp_x':0,
                            'texto': []},
                        ],
        },
        {   #Ciudad donde se consignó la retención
                    'x0':       250,  'x1':   500,
                    'y0':      556.9167772332,  'y1':       564.584774166,
                    'selectores':[
                        {'nombre':'ciudad_cons',
                            'fila':1,
                            'cols':(1,90),
                            'letra':'Ubuntu',
                            'letra_alto':9,
                            'posx':455,
                            'posy':205,
                            'alinear':'I',
                            'desp_y':0,
                            'desp_x':0,
                            'texto': []},
                        ],
        },
        #Detalle iva retenido
        {   #concepto
            'x0':          20.9999916,  'x1':  200,
            'y0':    509.576916169152,  'y1':    516.763953294336,
            'selectores':[
                {'nombre':'concepto_tasa',
                    'fila':1,
                    'cols':(1,90),
                    'letra':'Ubuntu',
                    'letra_alto':9,
                    'posx':60,
                    'posy':180,
                    'alinear':'I',
                    'desp_y':0,
                    'desp_x':0,
                    'texto': []},
                ],
        },
        {   #tasa
            'x0':  210,  'x1':    255,
            'y0':    509.576916169152,  'y1':    516.763953294336,
            'selectores':[
                {'nombre':'tasa',
                    'fila':1,
                    'cols':(1,90),
                    'letra':'Ubuntu',
                    'letra_alto':9,
                    'posx':300,
                    'posy':180,
                    'alinear':'I',
                    'desp_y':0,
                    'desp_x':0,
                    'texto': []},
                ],
        },
        {   #tasa base
            'x0':        260.0,  'x1':  310.0,
            'y0':    509.576916169152,  'y1':    516.763953294336,
            'selectores':[
                {'nombre':'tasa_base',
                    'fila':1,
                    'cols':(1,90),
                    'letra':'Ubuntu',
                    'letra_alto':9,
                    'posx':468,
                    'posy':180,
                    'alinear':'I',
                    'desp_y':0,
                    'desp_x':0,
                    'texto': []},
                ],
        },
        #Detalle
        {   #concepto +
        'x0':        20.9,  'x1':  300.0,
         'y0':  482.01340719456,  'y1':  505.74639770135997,
        'selectores':[{'nombre':'concepto',
                            'fila':1,
                            'cols':(1,90),
                            'letra':'Ubuntu',
                            'letra_alto':9,
                            'posx':60,
                            'posy':140,
                            'alinear':'I',
                            'desp_y':11,
                            'desp_x':0,
                            'texto': []
                        },
                    ],
        },
        {   #col monto_total +
        'x0':       210.0,          'x1':   403.0,
        'y0':  481.05892757635206,  'y1':    505.74639770135997,
        'selectores':[{'nombre':'col_monto_total',
                        'fila':1,
                        'cols':(1,90),
                        'letra':'Ubuntu',
                        'letra_alto':9,
                        'posx':350,
                        'posy':140,
                        'alinear':'D',
                        'desp_y':11,
                        'desp_x':0,
                        'texto': []},
                    ],
        },
        {   #col vr base +
            'x0':410.0,          'x1':   498.0,
            'y0':  481.05892757635206,  'y1':    505.74639770135997,
            'selectores':[{'nombre':'col_vr_base',
                            'fila':1,
                            'cols':(1,90),
                            'letra':'Ubuntu',
                            'letra_alto':9,
                            'posx':455,
                            'posy':140,
                            'alinear':'D',
                            'desp_y':11,
                            'desp_x':0,
                            'texto': []},
                        ],
        },
        {   #col vr retenido +
        'x0':500.0,          'x1':   593.0,
        'y0':  481.05892757635206,  'y1':    505.74639770135997,
        'selectores':[{'nombre':'col_vr_retenido',
                        'fila':1,
                        'cols':(1,90),
                        'letra':'Ubuntu',
                        'letra_alto':9,
                        'posx':555,
                        'posy':140,
                        'alinear':'D',
                        'desp_y':11,
                        'desp_x':0,
                        'texto': []},
                    ],
        },
        #totales
        {   #total monto_total +
        'x0':       210.0,          'x1':   402.5659228778521,
        'y0':    456.049497580128,  'y1':        463.34981466,
        'selectores':[{'nombre':'total_monto',
                        'fila':1,
                        'cols':(1,90),
                        'letra':'Ubuntu-Bold',
                        'letra_alto':9,
                        'posx':350,
                        'posy':75,
                        'alinear':'D',
                        'desp_y':0,
                        'desp_x':0,
                        'texto': []},
                    ],
        },
        {   #total vr base +
        'x0':410.0,          'x1':   497.4858910445827,
        'y0':    456.049497580128,  'y1':        463.34981466,
        'selectores':[{'nombre':'total_vr_base',
                        'fila':1,
                        'cols':(1,90),
                        'letra':'Ubuntu-Bold',
                        'letra_alto':9,
                        'posx':455,
                        'posy':75,
                        'alinear':'D',
                        'desp_y':0,
                        'desp_x':0,
                        'texto': []},
                    ],
        },
        {   #total vr retenido +
        'x0':500.0,          'x1':   592.5258570916546,
        'y0':456.049497580128,  'y1':        463.34981466,
        'selectores':[{'nombre':'total_vr_retenido',
        'fila':1,
        'cols':(1,90),
        'letra':'Ubuntu-Bold',
        'letra_alto':9,
        'posx':555,
        'posy':75,
        'alinear':'D',
        'desp_y':0,
        'desp_x':0,
        'texto': []},
        ],
        },
        #Generales
        {   #fecha +
        'x0':       144.839942064,  'x1':   204.8044027980636,
        'y0':    350.697339721008,  'y1':     359.18325632664,
        'selectores':[{'nombre':'fecha',
            'fila':1,
            'cols':(1,90),
            'letra':'Ubuntu',
            'letra_alto':8,
            'posx':405,
            'posy':34,
            'alinear':'I',
            'desp_y':0,
            'desp_x':0,
            'texto': []},
            ],
        },


    ]
}

opcional=False

archivo=open("reteiva_enterprice.amb","wb")
pickle.dump(ambiente,archivo)
archivo.close()
