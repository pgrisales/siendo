#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Inserta lineas en blanco, al inicio de un campo [a]
con la longitud del campo [desde]
"""

#def Fun_AdLinea(objPagina=None, desde='debitos', a='creditos'):
def plugin_main(*args, **kwargs):
    # print ('args  : ',args)
    # print ('kwargs: ',kwargs)
    # print (dir(kwargs['objPagina']))
    # print (kwargs['objPagina'].campos[kwargs['desde']]['texto'])

    if kwargs['desde'] in kwargs['objPagina'].campos:
        for ln in range(0, len (kwargs['objPagina'].campos[kwargs['desde']]['texto'])):
            kwargs['objPagina'].campos[kwargs['a']]['texto'].insert(0,'')
    #print (kwargs['objPagina'].campos[kwargs['a']])
