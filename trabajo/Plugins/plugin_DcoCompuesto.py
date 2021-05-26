#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Une varios campos para generar e nrodoc y el nombre del pdf
"""

import uuid
from os.path import join
from datetime import datetime

def plugin_main(*args, **kwargs):
    #print ('args  : ',args)
    #print ('kwargs: ',kwargs)
    #Creacion de NroDoc


    nit  = kwargs['objPagina'].campos['nit']['texto'][0]
    rango= kwargs['objPagina'].campos['rango_fecha']['texto'][0]
    rango=rango.replace(' ', '_')
    valor = nit + '_' + rango
    kwargs['objPagina'].campos['nrodoc']={'texto':[valor.upper()]}
    #creacion del nombre del PDF
    fecha_ano = datetime.now().strftime('%Y')
    fecha_mes = datetime.now().strftime('%m')
    salida = join(kwargs['ruta'], fecha_ano, fecha_mes, '{}_{}.pdf'.format( valor, uuid.uuid1()) ) #aqui se debe dar el nombre del directorio !!! como parametro
    #print (salida)
    kwargs['objPagina'].campos['nombrepdf']={'texto':[salida]}
