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
from pdfminer.layout import LAParams, LTTextBox, LTTextLine, LTTextBoxHorizontal
#from Facil import ObjFacil

import logging
logger = logging.getLogger(__name__)



class ObjPDF():
    """docstring for ObjPDF"""
    def __init__(self, archpdf, ambiente, ruta_recursos):
        self.error=None
        self.ruta=ruta_recursos
        self.doc = PDFDocument()
        self.ambiente=ambiente
        self.debug=True
        #logger.debug (f"Procesar:{archpdf} {selector}")
        if  op.isfile (archpdf):
            print ("Existe archivo de datos")
            fp = open(archpdf, 'rb')
            parser = PDFParser(fp)
            parser.set_document(self.doc)
            self.doc.set_parser(parser)
            self.doc.initialize('')
        else:
            self.error="No existe Archivo:[{}]".format(archpdf)

    def BorrarBasura(self, texto):
        salida =''
        for letra in texto:
            #print (letra.encode('utf-8'))
            if len(letra.encode('utf-8'))==1:
                salida +=letra
        return salida

        for item in self.ambiente['borrar']:
            print ("replace:",item)
            texto = texto.replace(item.encode('utf-8'), '')
        print (texto.encode('utf-8'))
        return texto

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
                    texto=self.BorrarBasura( lt_obj.get_text() )
                    print (texto.encode('utf-8'))
                    if self.debug: print ("x0:{:=5f}  x1:{:=5f} y0:{:=5f}  y1:{:=5f} ".format(lt_obj.x0, lt_obj.x1, lt_obj.y0, lt_obj.y1))
                    salida.append((lt_obj.x0, lt_obj.x1, lt_obj.y0, lt_obj.y1, texto))
            break
        return salida

    def Ubiacion(self,x0,x1,y0,y1,texto):
        salida =None
        for bloque in ambiente['bloques']:
            if bloque['x0']>=x0 and bloque['x1']<=x1 and bloque['y0']>=y0 and bloque['y1']<=y1:
                texto=self.BorrarBasura( texto )
                texto=texto.split("\n")
                print (texto)

                for selector in bloque['selectores']:
                    if 'filas' in selector:
                        print ('aqui')
                        for fila   in range( selector['filas'][0], selector['filas'][1]  ):
                            if fila >len(texto): break
                            print ('fila:',fila-1, texto[fila-1])
                            print (texto[fila-1][selector['cols'][0]-1 :selector['cols'][1]].strip())

                    else:
                        if selector['fila']<=len(texto):
                            print (selector['nombre'])
                            print (texto[selector['fila']-1][selector['cols'][0]-1 :selector['cols'][1]].strip())
        print ('-'*50)

    def Procesar(self):
        print("Procesar()")

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
            print ("ObjPDF:",pagina)
            interpreter.process_page(page)
            layout = device.get_result()
            temp=0
            for lt_obj in layout:
                #print (lt_obj)
                #print (isinstance(lt_obj, LTTextBoxHorizontal))
                if not isinstance(lt_obj, LTTextBoxHorizontal): ## or isinstance(lt_obj, LTTextBox) or not isinstance(lt_obj, LTTextLine) :
                    continue

                self.Ubiacion(lt_obj.x0,lt_obj.x1,lt_obj.y0,lt_obj.y1, lt_obj.get_text())
                    # texto=lt_obj.get_text()
                    # texto=self.BorrarBasura( lt_obj.get_text() )
                    # if texto.find('x0:  x1: y0:  y1:'):
                    #     texto=texto.split("\n")
                    #     print (texto, temp)
                    #     salida.append(texto)
                    #     temp +=1

        return salida


            # temp=arch_salida+"-pag_{:06d}.tempo".format(pagina)
            # temp=open( temp ,"wb")
            # pickle.dump(salida,temp)
            # temp.close()
        #return arch_salida, pagina


if __name__ =="__main__":
    #Abre el ambiente
    #ruta_install="/home/marco/workspace/virtualenv3/py3Facil/desarrollo/trabajo"
    #ob=ObjFacil(ruta_install)
    #ob.AbrirAmbiente("recaudo.amb")

    ambiente={'bloques':[
                        {   #Coordenas
                            'x0': 21.6,
                            'x1': 454.68,
                            'y0': 400.166,
                            'y1': 569.95,
                            #selector
                            'selectores':
                                [{'nombre':'nrodoc',
                                    'fila':8,
                                    'cols':(66,80)
                                },
                                {'nombre':'fecha',
                                    'fila':10,
                                    'cols':(66,80)
                                },
                                {'vlr_letras':'fecha',
                                    'filas':(14,16),
                                    'cols':(16,80),
                                    'concatenar':True
                                }

                                ],
                        }
                ]
            }



    ob=ObjPDF(  archpdf = "/home/marco/workspace/virtualenv3/web2py/applications/siendo/trabajo/spools/ce26749_makita.pdf",
                ambiente = ambiente,
                ruta_recursos='ruta_install',)

    ob.VistaPdf()
    print ('*'*50)
    salida =ob.Procesar()
    for i in salida:
        print (i)
    #print (ob.Procesar())
