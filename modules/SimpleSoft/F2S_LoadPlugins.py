#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sys import path as PATH

def load_plugin(name):
    mod = __import__("plugin_%s" % name)
    return mod

def call_plugin(name, *args, **kwargs):
    plugin = load_plugin(name)
    salida = plugin.plugin_main(*args, **kwargs)
    return salida


def AdicionarRuta(ruta):
    if not ruta in PATH:
        PATH.extend([ruta])
        print (PATH)

if __name__==  '__main__':
    AdicionarRuta('/home/marco/Clientes/Solucionenlinea/siendo/trabajo/Plugins')
    call_plugin("prueba", 1234,estoes='otro')
