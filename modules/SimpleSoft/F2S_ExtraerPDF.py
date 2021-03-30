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
from SimpleSoft.Facil import ObjFacil

class ObjPDF():
    """docstring for ObjPDF"""
    def __init__(self, archpdf, selector, ruta_recursos, debug=True):
        self.error=None
        self.debug=debug
        self.ruta=ruta_recursos
        self.doc = PDFDocument()

        if debug: print ("Procesar:",archpdf, selector)
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
            #if self.debug: print (":",pagina)
            interpreter.process_page(page)
            layout = device.get_result()
            salida=[]

            for lt_obj in layout:
                if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
                    # if self.debug:
                    #     print ("\n\n")
                    #     print ("x0:{:=12f}  x1:{:=12f} y0:{:=12f}  y1:{:=12f} {}".format(lt_obj.x0, lt_obj.x1, lt_obj.y0, lt_obj.y1,lt_obj.get_text()))
                    #     print ("*"*40)

                    for selector in self.selectores:
                        # if self.debug:
                        #     print ("select_x:{:=12f}>=:{:=12f}x0   and  x1 {:=12f}<=:{:=12f} select_x1".format(selector["sel_posx"][0],
                        #                                                                                     lt_obj.x0,  
                        #                                                                                     lt_obj.x1, 
                        #                                                                                     selector["sel_posx"][1])
                                    # )
                    
                        if lt_obj.x0 >= selector["sel_posx"][0] and lt_obj.x1 <= selector["sel_posx"][1]:
                            if  lt_obj.y0 >= selector["sel_posy"][0] and lt_obj.y1 <= selector["sel_posy"][1]:
                                if self.debug: print ("SI*"*40)
                                texto=lt_obj.get_text()
                                if self.debug: 
                                    #print ("Selector:",selector["nombre"])
                                    #print (texto)
                                salida.append( { "nombre":selector["nombre"]          if "nombre"     in selector else "blanco",
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
                                                 "texto":texto
                                                 })
                                break

            temp=arch_salida+"-pag_{:06d}.tempo".format(pagina)
            print ("Nro pagina:",pagina)
            temp=open( temp ,"wb")
            pickle.dump(salida,temp)
            temp.close()
            break
            
        return arch_salida, pagina


if __name__ =="__main__":
    #Abre el ambiente
    ruta_install="/home/marco/workspace/virtualenv3/py3Facil/desarrollo/trabajo"
    ob=ObjFacil(ruta_install)
    ob.AbrirAmbiente("temporal.amb")


    ob=ObjPDF(  archpdf = "/home/marco/workspace/virtualenv3/py3Facil/desarrollo/trabajo/repositorio/datos.pdf",
                selector= ob.getSelector(),
                ruta_recursos=ruta_install)
    print (ob.Procesar())
