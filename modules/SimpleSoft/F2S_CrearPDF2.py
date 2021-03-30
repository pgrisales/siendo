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
    def __init__(self,encabezado, rutarecursos, o_paginalog):
        self.rutarecurso=rutarecursos
        self.encabezado=encabezado
        self.paginas=o_paginalog

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
        arch_formato =os.path.join(self.rutarecurso,"formatos", self.encabezado["formato"])
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
        for nropagina in range(1,self.paginas.cont_paginas+1):
            paglogica = self.paginas.LeerPagina(nropagina)
            contador +=1

            if not paglogica:
                if salvardoc==False:pdf_f2s.save()
                logger.warning(f"No existe pag.{nropagina} logica!!!")
                continue

            if idpag==None:
                idpag=paglogica[0]["idpag"]
                nombre_pdf = paglogica[0]["nombre_pdf"]
                pdf_f2s= canvas.Canvas(nombre_pdf,pagesize=tam)
                salvardoc=False
                logger.debug ("inicio -  PDF - canvas")

            if idpag !=paglogica[0]["idpag"]:
                #print ("Cambio de indice PDF indice")
                pdf_f2s.save()
                logger.info (f"Salvar Salida pdf:{nombre_pdf}")
                idpag=paglogica[0]["idpag"]
                nombre_pdf = paglogica[0]["nombre_pdf"]
                logger.debug ("Nuevo PDF")
                pdf_f2s= canvas.Canvas(nombre_pdf,pagesize=tam)
                salvardoc=False

            logger.info (f"idpag:{idpag}")
            logger.info (f"Salida pdf:{nombre_pdf}")


            #print ("*"*80)

            for pagina in paglogica[1]:
                #print (pagina)
                pdf_f2s.saveState()
                pdf_f2s.translate(pagina['pag_despx'] *inch, tam[1] - ((pagina['pag_despy'] *inch) + alto_imagen)  )
                formato.wrapOn(pdf_f2s, formato.drawWidth, formato.drawHeight)
                formato.drawOn(pdf_f2s, 0 , 0)
                #self.Grilla(pdf_f2s,tam)


                for campo in pagina["campos"]:
                    datos=pagina["campos"][campo]
                    #print (datos)
                    pdf_f2s.setFont(datos["letra"], datos["letra_alto"])
                    posx=datos["posx"] if "posx" in datos else 0
                    posy=datos["posy"] if "posy" in datos else 0
                    desx=datos["desp_x"] if "desp_x" in datos else 0
                    desy=datos["desp_y"] if "desp_y" in datos else 0
                    desy= desy * -1

                    if "fun_numero1" in datos:
                        fun_numero1=datos["fun_numero1"]
                    else:
                        fun_numero1=None
                    #print (fun_numero1)

                    if "codigo128" in datos:
                        logger.debug(datos)
                        codigobar=f2s_cod128.code128_image (chr(102)+datos["texto"][0])
                        pdf_f2s.drawImage(ImageReader(codigobar),datos["posx_cod"],posy + (datos["letra_alto"] * .72)+2,
                                            width=datos["ancho"], height=datos["alto"])

                    for linea in datos["texto"]:
                        if fun_numero1:
                            linea=linea.replace("$","")
                            linea=linea.replace(",","")
                            linea=linea.strip()
                            try:
                                linea=fun_numero1.format(float(linea))
                            except Exception as e:
                                pass

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
                pdf_f2s.restoreState()
            #print ("Salto de pagina")
            pdf_f2s.showPage()

        #print (f"Total Paginas PDF:{contador}")

    def Parrafo(self,datos, pdf_f2s):
        print ("Parrafo!")
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
            ruta=os.path.join(self.rutarecurso,"fonts",tipo[1])
            if os.path.isfile(ruta):
                pdfmetrics.registerFont(TTFont(tipo[0],ruta))
            else:
                logger.error(f"No existe el archivo:{ruta}")
