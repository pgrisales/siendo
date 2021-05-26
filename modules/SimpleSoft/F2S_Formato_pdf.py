#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Creacion de datos con formato PDF
#
from PyPDF2 import PdfFileReader, PdfFileWriter
import uuid
import os


class ObjFormatoPDF(object):
    """
        Recibe el archivo PDF
        Recibe Ruta y nombre del archivo de salida pdf.
        Parte el formato pdf en paginas si tiene mas de una pagina.
        Recibe los datos posicionados en formato PDF.
        selecciona por defecto la primera pagina como el formato.
        mezcla los  datos con el formato seleccionado.
        Genera el nuevo pdf en la ruta y nombre de salida.

        Controla los errores de busqueda y recepcion de Archivo
    """

    def __init__(self, ruta, formato, pagformato=1):
        self.paginaformato=pagformato
        self.ruta=ruta
        self.formato= formato
        self.error=None
        self.idpdf='/tmp/F2S_Partirpdf_{}'.format(uuid.uuid1())
        VerificarArch(formato)

    def VerificarArch(self, archivo):
        if not os.path.isfile(archivo):
            self.error='No se encuentra archivo:{}'.format(archivo)
            return False
        return True

    def Procesar(self):
        self.PartirPDF()


    def PartirPDF(self):
        pdf = PdfFileReader(self.formato)
        for pag in range(pdf.getNumPages()):
            pdf_writer = PdfFileWriter()
            pdf_writer.addPage(pdf.getPage(pag))
            archsalida = '{}_pag_{}.pdf'.format(self.ippdf, pag+1)
            with open(archsalida, 'wb') as out:
                pdf_writer.write(out)
        print('Pags. Procesadas: {}'.format(pdf.getNumPages()))

if __name__='__main__':
