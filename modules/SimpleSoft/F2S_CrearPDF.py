#!/usr/bin/env python3
# -*- coding: iso-8859-1 -*-
import os
import pickle

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

from datetime import datetime
import calendar


import SimpleSoft.F2S_CodigoBarras as f2s_cod128



class objF2S_PDF():
    """docstring for objF2S_PDF"""
    def __init__(self, rutarecurso, encabezado, campos, rutadatos, paginas, rutasalida=None, debug=True):
        self.rutarecurso=rutarecurso
        self.rutasalida=rutasalida
        self.encabezado=encabezado
        self.rutadatos=rutadatos
        self.paginas=paginas
        self.campos=campos

    def adicionales(self,convenio,codiac):
        self.convenio=convenio
        self.codiac=codiac

    def Procesar(self):
        print ("Procesando!!!")
        #print (self.encabezado)

        arch_formato =os.path.join(self.rutarecurso,"formatos", self.encabezado["formato"])

        self.CargarFonts(self.encabezado["tipos"])
        if "tampapel" in self.encabezado:
            tam=self.encabezado["tampapel"]
            ancho=tam["ancho_pul"]* inch
            alto =tam["alto_pul"] * inch
            tam=(ancho,alto)
        else:
            tam=letter

        nombre_pdf="CuotaExtraordinaria_{:%Y-%m-%d %H:%M}.pdf".format(datetime.now())

        nombre_pdf=os.path.join(self.rutasalida,nombre_pdf)
        print ("nombre_pdf:",nombre_pdf)

        pdf_f2s= canvas.Canvas(nombre_pdf,pagesize=tam)

        margenX=0

        for pagina in range(1, self.paginas+1):
            doc=self.LeerPagina(pagina)
            #print (doc)
            formato = Image(arch_formato)
            formato.drawHeight=alto#formato.drawHeight-32
            formato.drawWidth=ancho/2#formato.drawWidth-32
            formato.wrapOn(pdf_f2s, formato.drawWidth, formato.drawHeight)
            formato.drawOn(pdf_f2s, 0 + margenX, 0)

            for campopag in doc:
                #print (campopag)

                datos=doc[campopag]
                #print (datos)
                #print (datos["letra"], datos["letra_alto"],datos["texto"])

                if "parrafo" in datos:
                    self.Parrafo(datos,pdf_f2s)
                    continue


                pdf_f2s.setFont(datos["letra"], datos["letra_alto"])
                posx=datos["posx"] if "posx" in datos else 0
                posy=datos["posy"] if "posy" in datos else 0
                desx=datos["desp_x"] if "desp_x" in datos else 0
                desy=datos["desp_y"] if "desp_y" in datos else 0
                desy= desy * -1
                
                posx=posx + margenX


                for linea in datos["texto"]:

                    ##MACHETE
                    if campopag=="nrocuenta":
                        linea=linea.replace(",","")
                        nrocuenta=int(linea.strip())
                    elif campopag=="codigocliente":
                        codigocliente=int(linea.strip())
                    ######

                    if datos["alinear"]=="C":
                        pdf_f2s.drawCentredString(posx, posy, linea)
                    elif datos["alinear"]=="D":
                        pdf_f2s.drawRightString(posx, posy, linea)
                    else:
                        pdf_f2s.drawString(posx, posy, linea )
                    posx +=desx
                    posy +=desy

                ####machete
                if campopag=="Fecha":
                    formato1="%m/%d/%y"
                    #print ("aqui", type(datos["texto"][0]) )
                    fecha = datetime.strptime(datos["texto"][0], formato1)
                    ultimo=calendar.monthrange(fecha.year ,fecha.month)
                    mes=fecha.month
                    fechaprint="{}/{}/{}".format (mes, ultimo[1], fecha.year)
                    fechacod ="{}{:02d}{}".format ( fecha.year, mes, ultimo[1] ) #SUBTOT

                    pdf_f2s.setFont("Ubuntu", 11)
                    pdf_f2s.drawRightString(190 + margenX, 180, fechaprint)
                elif campopag=="total":
                    valorcod=datos["texto"][-1]
                    pdf_f2s.setFont("Ubuntu", 11)
                    pdf_f2s.drawRightString(380 + margenX, 180, valorcod)
                    valorcod=valorcod.replace(",","")
                    valorcod=int(valorcod.strip())


            pdf_f2s.setFont("Ubuntu", 10)
            pdf_f2s.drawRightString(380 + margenX, 544, self.convenio)

            if valorcod>0:
                pdf_f2s.setFont("Ubuntu", 8)
                codigo="(415){}(8020){:06}{:08}(3900){:010}(96){}".format(self.codiac,codigocliente,nrocuenta,valorcod,fechacod)
                pdf_f2s.drawCentredString(198 + margenX, 40, codigo)

                posy=50 
                posx=10 + margenX
                codigobar=f2s_cod128.code128_image (chr(102)+codigo)
                pdf_f2s.drawImage(ImageReader(codigobar),posx,posy,width=380, height=60)


            ###################
            if pagina % 2==0:
                pdf_f2s.showPage()
                margenX=0
            else:
                margenX = 5.5 * inch
        
        pdf_f2s.save()

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
        #Carga de los fonts
        for tipo in tipos:
            ruta=os.path.join(self.rutarecurso,"fonts",tipo[1])
            if os.path.isfile(ruta):
                pdfmetrics.registerFont(TTFont(tipo[0],ruta))

    def LeerPagina(self, pagina):
        """ 
        Buscar la pagina con los datos extraidos desde F2S_ExtraerPDF, y entrega la lectura.
        """

        temp=self.rutadatos +"-pag_{:06d}.tempo".format(pagina)
        #Leer pagina extraida
        pickled_file = open(temp,"rb")
        datos=pickle.load(pickled_file)
        pickled_file.close()
        return datos

 