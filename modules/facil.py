#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import copy
import uuid
import base64
from gluon.storage import Storage
from gluon import DAL, Field
import xml.etree.ElementTree as ET


arch_ambiente={"encabezado":{"selector1":[
                                    Storage({"campo":"nit",
                                        "col_ini":0,"col_fin":17
                                        }),
                                    Storage({"campo":"nombre",
                                            "col_ini":17,"col_fin":53
                                        }),

                                    ],
                            "formato":"estado_cuenta.svg",
                            "indice":Storage({"col_ini":0,"col_fin":17}),
                          },
                "detalle":{
                          "nrocol_detalle":2,
                          "orden_detalle":"Z",
                          "selector":[
                                Storage({"campo":"nrofactura",
                                         "col_ini":0,"col_fin":14
                                      }),
                                Storage({"campo":"fec_doc",
                                         "col_ini":14,"col_fin":22
                                      }),
                                Storage({"campo":"fec_vto",
                                         "col_ini":23,"col_fin":31
                                      }),
                                Storage({"campo":"dias",
                                         "col_ini":31,"col_fin":36
                                      }),
                                Storage({"campo":"plazo",
                                         "col_ini":40,"col_fin":52
                                      }),
                                Storage({"campo":"valor",
                                         "col_ini":52,"col_fin":68
                                      }),
                                ]
                          }
                }

class Obj_Facil():
    """Procesa y guarda los datos"""
    encabezado={}

    def __init__(self, ruta, archivo):
        #print (ruta)
        self.arch=archivo       # Nombre del achivo ambiente
        self.dbt = DAL('sqlite:memory:')
        self.ruta=ruta          #Ruta raiz de la aplicacion. request.folder
        self.amb_encabezado=Storage(arch_ambiente["encabezado"])
        self.amb_detalle=Storage(arch_ambiente["detalle"])
        self.dbt.define_table('detalle',
            Field('identidad'),
            Field('valor'),
            )

    def setEncabezado(self,linea):
        print ("setEncabezado")
        self.encabezado["campos"]=[]
        for selector in self.amb_encabezado.selector1:
            self.encabezado["campos"].append({"id":selector.campo,
                          "datos":linea[selector.col_ini:selector.col_fin].strip(),
                        })
        indice_ini=self.amb_encabezado.indice.col_ini
        indice_fin=self.amb_encabezado.indice.col_fin
        self.encabezado["indice"]=linea[indice_ini:indice_fin].strip()
        self.dbt(self.dbt.detalle).delete() #Inicio campos detalle

    def setEncCampo(self,id,valor):
        self.encabezado["campos"].append({"id":id, "datos":valor})

    def setDetalle(self,linea,grupo=0):
        print ("crear detalle")
        #print (self.amb_detalle.selector)
        for item in self.amb_detalle.selector:
            valor=linea[item.col_ini:item.col_fin].strip()
            #print (item.campo,valor)
            self.dbt.detalle.insert(identidad=item.campo,valor=valor)
        self.dbt.commit()

    def modUltimo_reg(self,datos):#Modifica el ultimo reg. de detalle
        print ("modUltimo_reg")

    def getDatos(self, atributo):
        salida=None
        for campo in self.encabezado["campos"]:
            if campo["id"]==atributo:
                salida=campo["datos"]
                return salida

    def getDetalle(self,atributo):
        print ("getDetalle:",atributo)
        consulta= self.dbt(self.dbt.detalle).select()
        print (consulta)

        consulta= self.dbt(self.dbt.detalle.identidad==atributo).select(self.dbt.detalle.valor)
        salida=[]
        for item in salida:
            print(item)
            salida.append(item.valor)
        return salida


    def GenPdf(self):
        print ("*"*40)
        print ("GenPdf")
        #print (self.encabezado)
        nombre=str (uuid.uuid4())
        #consulta= self.dbt(self.dbt.detalle).select()
        #print (consulta)
        #return

        ruta=os.path.join(self.ruta,"trabajo","temp",f"{nombre}")
        formato=os.path.join(self.ruta,"trabajo","formatos",self.amb_encabezado.formato)
        #print (ruta,formato)

        tree = ET.parse(formato)
        raiz =tree.getroot()
        #Generar encabezado
        for nodo in tree.iter('{http://www.w3.org/2000/svg}g'):
            for hijo in nodo:
                atributo=hijo.attrib.get("id")
                print (atributo)
                if atributo[-5:]=="_col1":
                    #Detalle
                    columna=self.getDetalle(atributo[:-5])
                    print ("detalle:",columna)
                else:
                    datos=self.getDatos(atributo)
                    if datos:
                        hijo[0].text=datos

                #detalle
                #Control Detalle



        #         #Clonar un elememnto
        #         if hijo.attrib.get("id")=="Fecha":
        #             hijo[0].text="fecha!1"
        #             print (hijo[0].text)
        #             nuevohijo=copy.deepcopy (hijo)
        #             print ("+"*20)
        #             calculo=float(nuevohijo.attrib.get("y")) + 50
        #             nuevohijo.set("y",'{:02f}'.format(calculo))
        #             nuevohijo[0].text="fecha!2"
        #             print ("+"*20)
        #         #Cargar imagen
        #         if hijo.attrib.get("id")=="F2S_Grafico1":
        #             datos=LeerImagen("logo.png")
        #             hijo.set("{http://www.w3.org/1999/xlink}href",f"data:image/png;base64,{datos}")
        #             print (hijo.items())
        #
        # #adicionar al nodo '{http://www.w3.org/2000/svg}g' un element
        # raiz.append(nuevohijo)
        #
        # #Guardar cambio
        tree.write(f"{ruta}.svg",xml_declaration=True, encoding='utf-8')






if __name__=="__main__":
    o=Obj_Facil("ambinte.amb")
    o.setEncabezado("linea")
