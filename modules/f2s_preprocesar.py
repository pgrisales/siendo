#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from facil import Obj_Facil
class Obj_Prepoceso():
    """docstring for Obj_Prepoceso."""
    fecha=None

    def __init__(self, archivo):
        self.archivo =open(archivo,"rb")


    def getFecha(self):
        self.archivo.read(265)  #No leer
        fecha=self.archivo.read(10).decode("latin-1")
        fecha=fecha.replace("/","-")
        self.archivo.readline()
        return fecha

    def Procesar(self):
        cuenta=""
        inicioCliente=True
        inicioDetalle=False
        clienteActual=""
        Facil=Obj_Facil(request.folder,"ambiente")
        fecha=self.getFecha()

        x=0
        for linea in self.archivo.readlines():
            linea=linea.decode("latin-1")
            #print ("linea--->",linea,"<<---linea")
            #print ("inicioCliente:",inicioCliente)
            if len(linea.strip())==0:
                #print ("liena en blanco")
                continue
            if linea.find("Total")>-1:
                #print ("total")
                continue

            if linea[0]=="|" or linea[0]=="+" or linea[0]=="-":
                #Buscar Cuenta
                if linea[2:11].strip()=="Cuenta  :":
                    #print("cuenta")
                    if cuenta != linea[25:60].strip():
                        cuenta = linea[25:60].strip()
                        cuenta=cuenta
                #print ("encabezado borrar")
                continue
            #Inicio cliente
            if inicioCliente:
                #print("inicioCliente")
                if linea.find("Cupo:")>-1:
                    #print ("Cupo.....")
                    cliente=linea[0:17].strip()
                    total_corriente=0
                    total_30d=0
                    total_60d=0
                    total_90d=0
                    total_mas=0

                    total_corriente_dolar=0
                    total_30d_dolar=0
                    total_60d_dolar=0
                    total_90d_dolar=0
                    total_mas_dolar=0

                    dolar=False

                    if cliente != clienteActual:
                        if clienteActual!="":
                            Facil.GenPdf()


                        Facil.setEncabezado(linea)
                        Facil.setEncCampo("fecha",fecha)
                        Facil.setEncCampo("cuenta",cuenta)
                        Facil.setEncCampo("corriente","200")
                        Facil.setEncCampo("30dias","3,000")
                        Facil.setEncCampo("60dias","6,000")
                        Facil.setEncCampo("90dias","9,000")
                        Facil.setEncCampo("mas90","19,000")

                        x+=1
                        if x >1:
                            break

                    clienteActual=cliente
                    inicioCliente=False
                    inicioDetalle=True
                continue

            #inicio detalle
            if inicioDetalle:
                print ("inicioDetalle")
                #print(linea)
                fin=linea.find("                                                     ________")
                if linea.find("\f")>-1 or fin>-1:
                    #print ("fin de pagina")
                    #self.archsalida.write("Saltopag-->>>")
                    inicioDetalle=False
                    inicioCliente=True
                    #print ("Fin del cliente",inicioCliente)
                    continue
                if linea.find("Cupo:")>-1:
                    print("repite el cupo???")
                    continue

                print("detalle calculo total")
                if linea.find("DOLAR")>-1:
                    dolar=True
                    if  len(linea[52:66].strip() )>0:
                        valor = float(linea[52:66].replace(",","") )
                        total_corriente_dolar +=valor
                        grupo="corriente"
                    elif len(linea[66:80].strip() )>0:
                        valor = float(linea[66:80].replace(",","") )
                        total_30d_dolar +=valor
                        grupo="30 Dias"
                    elif len(linea[80:94].strip() )>0:
                        valor = float(linea[80:94].replace(",","") )
                        total_60d_dolar +=valor
                        grupo="60 Dias"
                    elif len(linea[94:108].strip() )>0:
                        valor = float(linea[94:108].replace(",","") )
                        total_90d_dolar +=valor
                        grupo="90 Dias"
                    elif len(linea[108:122].strip() )>0:
                        valor = float(linea[108:122].replace(",","") )
                        total_mas_dolar +=valor
                        grupo="mas de 90 Dias"
                    valor="{:,.0f}".format(valor)
                    Facil.modUltimo_reg(valor)
                    return

                if  float(linea[52:66].replace(",","") )>0:
                    valor = float(linea[52:66].replace(",","") )
                    total_corriente +=valor
                    grupo="corriente"
                elif float(linea[66:80].replace(",","") )>0:
                    valor = float(linea[66:80].replace(",","") )
                    total_30d +=valor
                    grupo="30 Dias"
                elif float(linea[80:94].replace(",","") )>0:
                    valor = float(linea[80:94].replace(",","") )
                    total_60d +=valor
                    grupo="60 Dias"
                elif float(linea[94:108].replace(",","") )>0:
                    valor = float(linea[94:108].replace(",","") )
                    total_90d +=valor
                    grupo="90 Dias"
                elif float(linea[108:122].replace(",","") )>0:
                    valor = float(linea[108:122].replace(",","") )
                    total_mas+=valor
                    grupo="mas de 90 Dias"

                valor="{:,.0f}".format(valor)
                linea=linea[0:52] + '{:>15}'.format(valor)
                Facil.setDetalle(linea,grupo=grupo)

                #self.archsalida.write(linea)



        self.archivo.close()
        #self.archsalida.close()
if __name__=="__main__":
    o=Obj_Prepoceso("/home/marco/workspace/virtualenv3/web2py/applications/siendo/trabajo/spools/estado_credito.txt")
    o.Procesar()
    # dbt = DAL('sqlite:memory:')
    # dbt.define_table('persona',
    #     Field('nombre'),
    #     format='%(nombre)s')
    # dbt.define_table('cosa',
    #     Field('id_propietario', 'reference persona'),
    #     Field('nombre'),
    #     format='%(nombre)s')
    #
    # if not dbt(dbt.persona).count():
    #     id = dbt.persona.insert(nombre="Máximo")
    #     dbt.cosa.insert(id_propietario=id, nombre="Silla")
    #
    # consulta=dbt(dbt.persona).select()
    # print (consulta)
