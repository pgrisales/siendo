#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from gluon.storage import Storage
from f2s_Cliente import Obj_Cliente
class Obj_EstadoCuenta():

    """Manejo del estado de cuenta del cliente."""
    encabezado=Storage({"fecha":"", "cuenta":""})

    def __init__(self, db, ruta):
        self.db = db
        self.ruta=ruta  #Ruta raiz del PDF

    def setEncabezado(self,fecha,linea,cuenta):
        '''Procesa el Encabezado y inicializa las varibles'''
        self.encabezado.fecha={"texto":fecha,
                                "letra":"Ubuntu",
                                "alto":10,
                                "alinear":0,
                                "posx":100,
                                "posy":100,
                                "rotar":0}
        self.encabezado.cuenta={"texto":cuenta,
                                "letra":"Ubuntu",
                                "alto":10,
                                "alinear":0,
                                "posx":100,
                                "posy":100,
                                "rotar":0}
        selector=[
                    Storage({"campo":"nit",
                            "col_ini":0,
                            "col_fin":17,
                            "letra":"Ubuntu",
                            "alto":10,
                            "alinear":0,
                            "posx":100,
                            "posy":100,
                            "rotar":0

                            }),
                    Storage({"campo":"nombre",
                            "col_ini":17,
                            "col_fin":53,
                            "letra":"Ubuntu",
                            "alto":12,
                            "alinear":1,
                            "posx":200,
                            "posy":200,
                            "rotar":0
                            }),

                ]

        for item in selector:
            self.encabezado[item.campo]={"texto":linea[item.col_ini:item.col_fin].strip(),
                                        "letra":item.letra,
                                        "alto":item.alto,
                                        "alinear":item.alinear,
                                        "posx":item.posx,
                                        "posy":item.posy,
                                        "rotar":item.rotar,
                                        }

        print (self.encabezado.fecha["texto"], self.encabezado.fecha["letra"])

    def setDetalle(self,detalle):
        '''Procesa el detalle'''
        pass

    def GenerarPDF(self):
        '''Genera el pdf'''
        pass

    def FinDetalle(self):
        '''Genera PDF y Crea el campo en labase de datos'''
