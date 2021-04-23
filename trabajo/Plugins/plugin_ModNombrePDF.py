#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Asigna un nombre unico para el pdf, y la path relativo a la fecha creada por la
applicacion.

entrada = 20/04/2021 , 124235324
salida = 20212004/12312312{uuid}.pdf
"""
import uuid

def plugin_main(*args, **kwargs):
    print ('args  : ',args)
    print ('kwargs: ',kwargs)
    fecha = kwargs['fecha'][0]
    fecha = '{}{}{}'.format(fecha[-4:], fecha[3:5], fecha[:2])
    nrodoc = kwargs['nrodoc'][0]
    nombre= kwargs['nombre']
    salida = '{}/{}/{}_{}.pdf'.format(nombre,fecha,nrodoc,uuid.uuid1())
    print (salida)
    return 'nombrepdf',salida
