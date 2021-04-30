#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Inserta lineas en blanco, al inicio de un campo [a]
con la longitud del campo [desde]
y la limita con el largo del campo [limite] si viene..
"""

def plugin_main(*args, **kwargs):
    # print ('args  : ',args)
    # print ('kwargs: ',kwargs)
    # print (dir(kwargs['objPagina']))
    # print (kwargs['objPagina'].campos[kwargs['desde']]['texto'])

    if kwargs['desde'] in kwargs['objPagina'].campos:
        for ln in range(0, len (kwargs['objPagina'].campos[kwargs['desde']]['texto'])):
            kwargs['objPagina'].campos[kwargs['a']]['texto'].insert(0,'')
    else:
        kwargs['objPagina'].campos[kwargs['a']]['texto'].insert(0,'')
    #borrar la linea adiciona en a si sobrepas la columna Cuenta
    if kwargs['limite'] in kwargs['objPagina'].campos:

        limite =len ( kwargs['objPagina'].campos[kwargs['limite']]['texto'] )
        elementos =len (kwargs['objPagina'].campos[kwargs['a']]['texto'])
        if  elementos > limite:
            kwargs['objPagina'].campos[kwargs['a']]['texto']=kwargs['objPagina'].campos[kwargs['a']]['texto'][:limite]
