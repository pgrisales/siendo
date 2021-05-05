#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Parte los datos de acuerdo a un separador, y retorna el indice seleccionado
N-12963889-8
"""

def plugin_main(*args, **kwargs):
    # print ('args  : ',args)
    # print ('kwargs: ',kwargs)
    texto = kwargs['texto'][0]
    separador=kwargs['separador']
    indice=kwargs['indice']
    texto=texto.split(separador)
    if indice < len(texto):
        salida=texto[indice]
    else:
        salida =''
    return 'nit', salida
