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
import F2S_LoadPlugins
from SimpleSoft.F2S_CrearPDF3  	import objF2S_PDF

from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine, LTTextBoxHorizontal
#from Facil import ObjFacil

import logging
logger = logging.getLogger(__name__)


class ObClonPagina():
    def __init__(self):
        self.encabezado={'ancho': 8.5,
                         'largo': 11,
                        'nombre_pdf': '',
                        'idpag': ''}

        self.campos={}

    def VerContenido(self):
        print ('Campos Seleccionados:')
        for i in self.campos:
            print (i,':')
            for j in self.campos[i]:
                print ('    ',j,':', self.campos[i][j])


class ObjPDF():
    """docstring for ObjPDF"""
    def __init__(self, archpdf, ambiente, ruta_recursos, ruta_app, debug=False):
        self.error=None
        self.debug=debug
        self.ruta=ruta_recursos
        self.doc = PDFDocument()
        self.debug=True
        self.ruta_app=ruta_app
        self.obPagina=ObClonPagina()
        self.documentos={}
        if isinstance (ambiente,dict):
            self.ambiente= ambiente
        else:
            self.ambiente=self.LeerAmbiente(ruta_recursos, ambiente)
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

        F2S_LoadPlugins.AdicionarRuta(op.join(ruta_recursos,'Plugins'))
        #F2S_LoadPlugins.call_plugin("prueba", 1234,estoes='otro')


    def LeerAmbiente(self, rutatrabajo, archivo):
        ruta =op.join(rutatrabajo,'ambientes', archivo)
        if not op.isfile(ruta):
            print (f'No existe el ambiente:{ruta}')
            self.error=True
            return

        pickled_file = open(ruta,"rb")
        salida=pickle.load(pickled_file)
        pickled_file.close()
        return salida

    def BorrarBasura(self, texto):
        salida =''
        for letra in texto:
            #print (letra.encode('utf-8'))
            if len(letra.encode('utf-8'))==1:
                salida +=letra
        return salida

        for item in self.ambiente['borrar']:
            #print ("replace:",item)
            texto = texto.replace(item.encode('utf-8'), '')
        #print (texto.encode('utf-8'))
        return texto

    def VistaPdf(self):
        rsrcmgr = PDFResourceManager()
        laparams = LAParams()
        laparams.char_margin = 1.0
        laparams.word_margin = 1.0
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        extracted_text = ''
        salida=[]
        for pagina, page in enumerate(self.doc.get_pages()):
            if self.debug: print ("pagina:",pagina)
            interpreter.process_page(page)
            layout = device.get_result()
            for lt_obj in layout:
                #print (lt_obj)
                if  isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
                    texto=self.BorrarBasura( lt_obj.get_text() )
                    #print (texto.encode('utf-8'))
                    if self.debug: print ("'x0':{:=20},  'x1':{:=20},  'y0':{:=20},  'y1':{:=20}, {} ".format(lt_obj.x0, lt_obj.x1, lt_obj.y0, lt_obj.y1, lt_obj.get_text()))
                    salida.append((lt_obj.x0, lt_obj.x1, lt_obj.y0, lt_obj.y1, texto))

        return salida

    def SetPagClon(self,texto, nombre, alinear,desp_x,desp_y,letra,letra_alto,posx,posy):
        #Recibe los datos y configuracion de salida al pdf
        if not nombre in self.obPagina.campos:
            self.obPagina.campos[nombre]={
                            'alinear':alinear,
                            'desp_x':desp_x,
                            'desp_y':desp_y,
                            'letra':letra,
                            'letra_alto':letra_alto,
                            'posx':posx,
                            'posy':posy,
                            'texto':[]
                            }
        if isinstance(texto,list):
            if isinstance(self.obPagina.campos[nombre]['texto'], list):
                for adicionar in texto:
                    self.obPagina.campos[nombre]['texto'].append(adicionar)
            else:
                self.obPagina.campos[nombre]['texto']=texto
        else:
            self.obPagina.campos[nombre]['texto'].append(texto)

    def Ubiacion(self,objeto):
        salida =None
        for bloque in  self.ambiente['bloques']:
            if objeto.x0 >= bloque['x0'] and objeto.x1 <=bloque['x1'] and objeto.y0>=bloque['y0'] and objeto.y1<=bloque['y1']:
                texto=self.BorrarBasura( objeto.get_text() )
                texto=texto.split("\n")
                if self.debug:
                    print ('-'*50)
                    for nroln, linea in enumerate(texto):
                        print ('{:02d}|{}'.format(nroln+1, linea))
                    print ('-'*50)

                for selector in bloque['selectores']:
                    print (selector['nombre'])

                    if 'filas' in selector:
                        if 'concatenar' in selector:
                            temp=''
                        else:
                            temp=[]

                        for fila in range( selector['filas'][0], selector['filas'][1]+1):
                            if fila >len(texto): break

                            if isinstance(temp, list):
                                temp.append(texto[fila-1][selector['cols'][0]-1 :selector['cols'][1]].strip()) #Texto Extraido)
                            else:
                                temp+= texto[fila-1][selector['cols'][0]-1 :selector['cols'][1]].strip() #Texto Extraido

                    else:
                        if selector['fila']>len(texto):continue
                        temp=texto[selector['fila']-1][selector['cols'][0]-1 :selector['cols'][1]].strip()

                    self.SetPagClon(temp,selector['nombre'],selector['alinear'],
                                selector['desp_x'],selector['desp_y'],selector['letra'],
                                selector['letra_alto'],selector['posx'],selector['posy'])

    def ProcPag(self):
        '''
        ProcPag
        =======
            Lee el pdf de entrada y extrae los datos de acuerdo al Ambiente.
            Genera el obPagina que contiene las Coordenas y datos para la generacion
            del nuevo PDF.
        '''
        rsrcmgr = PDFResourceManager()
        laparams = LAParams()
        laparams.char_margin = 1.0
        laparams.word_margin = 1.0
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for pagina, page in enumerate(self.doc.get_pages()):
            if self.debug:print ('pag_proceso:', pagina)
            interpreter.process_page(page)
            layout = device.get_result()
            for lt_obj in layout:
                if not isinstance(lt_obj, LTTextBoxHorizontal): ## or isinstance(lt_obj, LTTextBox) or not isinstance(lt_obj, LTTextLine) :
                    continue
                self.Ubiacion(lt_obj)
            if 'funciones' in self.ambiente:    #inicia finciones para despues de la captura de datos
                #print (self.ambiente['funciones'])
                for procedimiento in self.ambiente['funciones']:
                    if procedimiento.find('F2S_LoadPlugins.call_plugin')==0:
                        eval(procedimiento)
            yield pagina

    def Procesar(self):
        if self.debug:print("Procesar()")
        if self.error:return
        for procpag in self.ProcPag():
            if self.debug:
                print ('procpag:',procpag)
                self.obPagina.VerContenido()
            camposweb2py={}
            for procedimiento in self.ambiente['web2pycampos']:
                if procedimiento.find('F2S_LoadPlugins.call_plugin')==0:
                    try:
                        item,valor =  eval(procedimiento)
                        camposweb2py[item]=valor
                    except Exception as e:
                        print ('Error en el plugin revisar datos:',e)
                else:
                    if procedimiento in self.obPagina.campos:
                        camposweb2py[procedimiento]=self.obPagina.campos[procedimiento]['texto'][0]
                    else:
                        print (f'Error: campo [{procedimiento}] no se a seleccionado en el ambiente:')

            if self.debug:print ('camposweb2py::', camposweb2py )
            self.documentos['{}'.format(procpag)]={'camposweb2py':camposweb2py, 'datos':self.obPagina}
            #Crear PDF...
            print ('aqui')
            o_salidapdf = objF2S_PDF(self.ambiente, self.ruta_app,camposweb2py['nombrepdf'], self.obPagina)  #Se crea una nueva instancia por cada nueva pagina...!!!
            o_salidapdf.Procesar()
            print ('fue')
            #Limpiar datos de la pagina procesada. Reinicio!!!!
            self.obPagina=ObClonPagina()



        return True


if __name__ =="__main__":
    import sys
    ob=ObjPDF(  archpdf = sys.argv[1],
                ruta_recursos=sys.argv[2],
                ambiente = sys.argv[3],
                debug= False
            )
    if not ob.error:
        ob.VistaPdf()
        print ('*'*50)
        salida =ob.Procesar()
        #print (ob.Procesar())
        print (ob.documentos['0']['datos'].campos)
        print (ob.documentos['1']['datos'].campos)
        print (ob.documentos['10']['datos'].campos)
