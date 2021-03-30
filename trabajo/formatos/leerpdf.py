#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import copy
import base64
from PIL import Image
import numpy as np


# def LeerImagen(archivo):
#     datos=open(archivo,'rb').read()
#     datos=base64.b64encode(datos)
#     datos=datos.decode('utf-8')
#     print (archivo)
#     im = Image.open(archivo)
#     print (im.size)
#     ancho=pxtomm(im.size[0])
#     largo=pxtomm(im.size[1])
#     ancho="{:06f}".format(ancho)
#     largo="{:06f}".format(largo)
#     print (ancho,largo,datos)
#     return ancho,largo,datos
#
# imagen="logo.png"
# lectura = LeerImagen(imagen)
# g=ET.SubElement(raiz,"ns0:g")
# grafica_f2s=ET.SubElement(g,"imagen")
# grafica_f2s.attrib['x']='10'
# grafica_f2s.attrib['y']='10'
# grafica_f2s.attrib['width']=lectura[0]
# grafica_f2s.attrib['height']=lectura[1]
# grafica_f2s.attrib['href']=lectura[2]
# grafica_f2s.attrib['preserveAspectRatio']='none'
# grafica_f2s.attrib['id']='graficas_f2s'
# grafica_f2s.attrib['inkscape:svg-dpi']='1'
# raiz.append(grafica_f2s)


def get_attr(xml):
    attributes = []
    for child in (xml):
        if len(child.attrib)!= 0:
            attributes.append(child.attrib)
        get_attr(child)
    return attributes

def pxtomm(valor):
    convertir=valor * 0.2645833333
    return convertir

def LeerImagen(archivo):
    datos=open(archivo,'rb').read()
    datos=base64.b64encode(datos)
    datos=datos.decode('utf-8')
    return datos



tree = ET.parse('estado_cuenta.svg')

raiz =tree.getroot()
print (raiz)
print ("*"*20)





for hijo in raiz:
    print (hijo)


print ("*"*20)
for nodo in tree.iter('{http://www.w3.org/2000/svg}g'):
    for hijo in nodo:
        print( hijo.attrib.get("id"),"y:",hijo.attrib.get("y"),
                "x:",hijo.attrib.get("x")#,hijo.attrib.get("style")
            )

        #Clonar un elememnto
        if hijo.attrib.get("id")=="Fecha":
            hijo[0].text="fecha!1"
            print (hijo[0].text)
            nuevohijo=copy.deepcopy (hijo)
            print ("+"*20)
            calculo=float(nuevohijo.attrib.get("y")) + 50
            nuevohijo.set("y",'{:02f}'.format(calculo))
            nuevohijo[0].text="fecha!2"
            print ("+"*20)
        #Cargar imagen
        if hijo.attrib.get("id")=="F2S_Grafico1":
            datos=LeerImagen("logo.png")
            hijo.set("{http://www.w3.org/1999/xlink}href",f"data:image/png;base64,{datos}")
            print (hijo.items())

#adicionar al nodo '{http://www.w3.org/2000/svg}g' un element
raiz.append(nuevohijo)

#Guardar cambio
tree.write("estado1.svg",xml_declaration=True, encoding='utf-8')
#Guardar PDF
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF, renderPM

drawing = svg2rlg("estado1.svg")
renderPDF.drawToFile(drawing, "estado1.pdf")
renderPM.drawToFile(drawing, "estado1.png", fmt="PNG")
