#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

Requermientos:
pip3 install pdfminer3k
pip3 install ply
"""

import os.path as op
from os import makedirs
import uuid
import pickle

from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine
#from Facil import ObjFacil

import logging
logger = logging.getLogger(__name__)



class ObjPDF():
    """docstring for ObjPDF"""
    def __init__(self, archpdf, selector, ruta_recursos):
        self.error=None
        self.ruta=ruta_recursos
        self.doc = PDFDocument()

        logger.debug (f"Procesar:{archpdf} {selector}")
        if  op.isfile (archpdf):
            print ("Existe archivo de datos")
            fp = open(archpdf, 'rb')
            parser = PDFParser(fp)
            parser.set_document(self.doc)


            self.doc.set_parser(parser)
            self.doc.initialize('')
        else:
            self.error="No existe Archivo:[{}]".format(archpdf)

        self.selectores = selector


    def VistaPdf(self):
        rsrcmgr = PDFResourceManager()
        laparams = LAParams()
        laparams.char_margin = 1.0
        laparams.word_margin = 1.0
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        extracted_text = ''
        pagina=0
        salida=[]
        for page in self.doc.get_pages():
            pagina +=1
            if self.debug: print (":",pagina)
            interpreter.process_page(page)
            layout = device.get_result()
            for lt_obj in layout:
                if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
                    texto=lt_obj.get_text()
                    if self.debug: print ("x0:{:=5f}  x1:{:=5f} y0:{:=5f}  y1:{:=5f} \n-> {}".format(lt_obj.x0, lt_obj.x1, lt_obj.y0, lt_obj.y1, texto))
                    salida.append((lt_obj.x0, lt_obj.x1, lt_obj.y0, lt_obj.y1, texto))
            break
        return salida

    def Procesar(self):
        print("Procesar()")
        if self.error: return
        arch_salida=op.join(self.ruta,"temporal")
        if not op.isdir(arch_salida): makedirs(arch_salida)
        arch_salida=op.join(arch_salida,"{}".format(uuid.uuid4()))      #Archivo temporal
        rsrcmgr = PDFResourceManager()
        laparams = LAParams()
        laparams.char_margin = 1.0
        laparams.word_margin = 1.0
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        extracted_text = ''
        pagina=0
        for page in self.doc.get_pages():
            pagina +=1
            print ("ObjPDF:",pagina)
            #if self.debug: print (":",pagina)
            interpreter.process_page(page)
            layout = device.get_result()
            salida={}

            for lt_obj in layout:
                if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
                    for selector in self.selectores:
                        if lt_obj.x0 >= selector["sel_posx"][0] and lt_obj.x1 <= selector["sel_posx"][1]:
                            if  lt_obj.y0 >= selector["sel_posy"][0] and lt_obj.y1 <= selector["sel_posy"][1]:

                                #if self.debug: print ("SI*"*40)
                                texto=lt_obj.get_text()
                                #if self.debug:
                                #    print ("Selector:",selector["nombre"])
                                #print ("seleccion", texto)

                                #El texto se parte por salto de linea \n y se guarda en lista,
                                texto=texto.split("\n")
                                #Campo nombre
                                nombre=selector["nombre"] if "nombre" in selector else "blanco"
                                if not nombre in salida:
                                    #Nuevo campo
                                    salida[nombre]={
                                                 "letra":selector["letra"]            if "letra"      in selector else "Ubuntu",
                                                 "letra_alto":selector["letra_alto"]  if "letra_alto" in selector else 10,
                                                 "posx":selector["posx"]              if "posx"       in selector else 100,
                                                 "posy":selector["posy"]              if "posy"       in selector else 100,
                                                 "desp_x":selector["desp_x"]          if "desp_x"     in selector else 0,
                                                 "desp_y":selector["desp_y"]          if "desp_y"     in selector else 0,
                                                 "alinear":selector["alinear"]        if "alinear"    in selector else "I",
                                                 "formato":selector["formato"]        if "formato"    in selector else None,
                                                 "decode":selector["decode"]          if "decode"     in selector else None,
                                                 "color":selector["color"]            if "color"      in selector else None,
                                                 "fondo":selector["fondo"]            if "fondo"      in selector else None,
                                                 "rotar":selector["rotar"]            if "rotar"      in selector else None,
                                                 "texto":[]
                                                 }
                                    #print (selector)
                                    if "parrafo" in selector:
                                        #print ("aqui"*20)
                                        salida[nombre]["parrafo"]=selector["parrafo"]
                                        #print (salida)

                                #Adicionar al campo mas texto
                                fila=0      #Control Selector Fila
                                for t in texto:
                                    fila +=1
                                    if "filas" in selector:
                                        if type(selector["filas"]) ==list or  type(selector["filas"]) ==tuple:
                                            if not fila in selector["filas"]: continue
                                        elif type(selector["filas"])==int or type(selector["filas"])==float:
                                            if fila !=selector["filas"]: continue
                                        elif type(selector["filas"])==str:
                                            if fila !=int(selector["filas"]): continue
                                    #print (texto, fila,t)

                                    #Esto se debe volver funcion de campos!!!!
                                    if nombre=="textocuota":
                                        if t.find("Anticipo")==0:
                                            t="Anticipo Cuota"
                                        elif t.find("Cuota")==0:
                                            t="Cuota Extraordinaria"
                                        elif t=="":
                                            continue
                                    if nombre=="Saldos" or nombre=="Cuotas"or nombre=="total":
                                        if t=="":
                                            continue
                                    #······························<<

                                    salida[nombre]["texto"].append(t)

                                #break

            temp=arch_salida+"-pag_{:06d}.tempo".format(pagina)
            temp=open( temp ,"wb")
            pickle.dump(salida,temp)
            temp.close()
        return arch_salida, pagina


if __name__ =="__main__":
    #Abre el ambiente
    ruta_install="/home/marco/workspace/virtualenv3/py3Facil/desarrollo/trabajo"
    ob=ObjFacil(ruta_install)
    ob.AbrirAmbiente("recaudo.amb")


    ob=ObjPDF(  archpdf = "/home/marco/workspace/virtualenv3/py3Facil/desarrollo/trabajo/repositorio/malo.pdf",#datos.pdf",  malo.pdf
                selector= ob.getSelector(),
                ruta_recursos=ruta_install,
                debug=True)
    print (ob.Procesar())
