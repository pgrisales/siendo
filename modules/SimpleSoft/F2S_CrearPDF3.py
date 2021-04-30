#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os,sys
import calendar
import logging
from datetime import datetime

import SimpleSoft.F2S_CodigoBarras as f2s_cod128

from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import letter
from reportlab.graphics import renderPDF
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import Paragraph
from reportlab.platypus import Image
from reportlab.lib.utils import ImageReader
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.colors import pink, black, red, blue, green


logger = logging.getLogger(__name__)



class objF2S_PDF():
    """docstring for objF2S_PDF"""
    def __init__(self,encabezado, ruta_app,nombre_pdf, o_paginalog):
        self.nombre_pdf = self.VerificarRuta(ruta_app,nombre_pdf)
        self.encabezado = encabezado
        self.pagina=o_paginalog
        self.ruta_app=ruta_app

        # Create handlers
        c_handler = logging.StreamHandler()
        c_handler.setLevel(logging.DEBUG)
        # Create formatters and add it to handlers
        c_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        c_handler.setFormatter(c_format)
        # Add handlers to the logger
        logger.addHandler(c_handler)


    def VerificarRuta(self, ruta_app, nombrepdf):
        nombre=os.path.split(nombrepdf)[0:-1]
        ruta=os.path.join(ruta_app, 'static','PDF', nombre[0])
        if not os.path.isdir(ruta):
            os.makedirs(ruta)
        ruta=os.path.join(ruta_app, 'static','PDF', nombrepdf)
        return  ruta

    def Grilla(self,pdf_f2s,tam):
        import numpy
        pdf_f2s.setStrokeColor(pink)
        pdf_f2s.grid(numpy.arange(0, tam[0], 72/4),numpy.arange(0, tam[1], 72/4) )
        pdf_f2s.setStrokeColor(black)
        pdf_f2s.setFont("Helvetica", 8)
        for x in  numpy.arange(0, tam[0], 72/4):
            pdf_f2s.drawString(x,0, "{:.0f}".format(x))
            pdf_f2s.drawString(x,tam[1]-5, "{:.0f}".format(x))
        for y in  numpy.arange(0, tam[1], 72/4):
            pdf_f2s.drawRightString(18,y, "{:.0f}".format(y))
            pdf_f2s.drawRightString(tam[0]-5,y, "{:.0f}".format(y))


    def Procesar(self):
        logger.debug("Creacion PDF")
        arch_formato =os.path.join(self.ruta_app,'trabajo',"formatos", self.encabezado["formato"])
        logger.debug(f"Formato:{arch_formato}")
        self.CargarFonts(self.encabezado["tipos"])

        if "tampapel" in self.encabezado:
            tam=self.encabezado["tampapel"]
            ancho=tam["ancho"]* inch
            alto =tam["alto"] * inch
            tam=(ancho,alto)
        else:
            tam=letter
        logger.debug(f"Tamaño papel {tam}")
        idpag=None
        ancho_imagen=tam[0]/float(self.encabezado["pagup"]["up"][0])
        alto_imagen=tam[1]/self.encabezado["pagup"]["up"][1]
        formato = Image(arch_formato, ancho_imagen, alto_imagen)
        contador=0
        salvardoc=True

        pdf_f2s= canvas.Canvas(self.nombre_pdf,pagesize=tam)
        pdf_f2s.saveState()
        pdf_f2s.translate(self.encabezado['pag_despx'] *inch, tam[1] - ((self.encabezado['pag_despy'] *inch) + alto_imagen)  )
        formato.wrapOn(pdf_f2s, formato.drawWidth, formato.drawHeight)
        formato.drawOn(pdf_f2s, 0 , 0)
        pdf_f2s.restoreState()
        #self.Grilla(pdf_f2s,tam)

        for items in self.pagina.campos:
            datos = self.pagina.campos[items]

            #print (items, ':', datos)
            #print ('*-'*20)
            posx=datos["posx"] if "posx" in datos else 0
            posy=datos["posy"] if "posy" in datos else 0
            desx=datos["desp_x"] if "desp_x" in datos else 0
            desy=datos["desp_y"] if "desp_y" in datos else 0
            desy =desy *-1      #Subir


            #print ('posiciones:', posx, posy, datos["alinear"] )
            if "parrafo" in datos:
                self.Parrafo(datos,pdf_f2s)
                continue

            pdf_f2s.setFont(datos["letra"],datos["letra_alto"])

            for linea in datos["texto"]:
                if "colortexto_rgb" in datos:
                    #print (datos["colortexto_rgb"])
                    pdf_f2s.setFillColorRGB(*datos["colortexto_rgb"])

                if datos["alinear"]=="C":
                    pdf_f2s.drawCentredString(posx, posy, linea.strip() )
                elif datos["alinear"]=="D":
                    pdf_f2s.drawRightString(posx, posy, linea.strip() )
                elif datos["alinear"]=="I":
                    pdf_f2s.drawString(posx, posy, linea.strip()  )
                else:
                    pdf_f2s.drawString(posx, posy, linea )
                if "colortexto_rgb" in datos:
                    pdf_f2s.setFillColor(black)
                posx +=desx
                posy +=desy
        pdf_f2s.showPage()
        pdf_f2s.save()
        return


    #
    def Parrafo(self,datos, pdf_f2s):
        #print ("Parrafo!")
        style = ParagraphStyle(
            name='Normal',
            fontName=datos["letra"],
            fontSize=datos["letra_alto"],
            leading = datos["desp_y"],
        )
        texto=""
        for linea in datos["texto"]:
            texto += linea + "\n"
        #print (texto)

        p = Paragraph(texto.strip(), style)
        w, h = p.wrapOn(pdf_f2s, datos["parrafo"]["ancho"], datos["parrafo"]["alto"])
        p.drawOn(pdf_f2s, datos["posx"], datos["posy"]-h)

    def CargarFonts(self,tipos):
        logger.debug("Cargar Fonts")
        #Carga de los fonts
        for tipo in tipos:
            ruta=os.path.join(self.ruta_app,'trabajo',"fonts",tipo[1])
            print(f"fonts archivo:{ruta}")
            if os.path.isfile(ruta):
                pdfmetrics.registerFont(TTFont(tipo[0],ruta))
            else:
                logger.error(f"No existe el archivo:{ruta}")
                print(f"No existe el archivo:{ruta}")
