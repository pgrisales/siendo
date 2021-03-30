# -*- coding: utf-8 -*-
import xmltodict
from xml.dom import minidom

class ObjFactura():
    """
    Lector de factura electronica
    """
    def __init__(self, archivo):
        try:
            arch=open(archivo,"rb").read()
            #print "self.archivo:",self.archivo
            self.root=xmltodict.parse(arch)
        except Exception as e:
            print ({"error":"{}".format(e)})


    def Extraer(self):
        #print (self.root)
        self.nrofac = self.root["fe:Invoice"]["cbc:ID"]
        #self.nroresolucion = self.root["fe:Invoice"]["ext:UBLExtensions"]["ext:UBLExtension"]["ext:ExtensionContent"]["sts:DianExtensions"]#["sts:InvoiceControl"]["sts:InvoiceAuthorization"]
        self.fechafac=    self.root["fe:Invoice"]["cbc:IssueDate"]
        self.horafac=     self.root["fe:Invoice"]['cbc:IssueTime']
        #self.fechafacvec= self.root["fe:Invoice"]["cbc:DueDate"]
        #print (self.fechafacvec)
        self.cufe=self.root["fe:Invoice"]["cbc:UUID"]["#text"]
        self.totalfac= self.root["fe:Invoice"]["fe:LegalMonetaryTotal"]["cbc:PayableAmount"]["#text"]
        self.proveedor= self.root["fe:Invoice"]["fe:AccountingSupplierParty"]["fe:Party"]["fe:PartyLegalEntity"]["cbc:RegistrationName"]
        self.nit= self.root["fe:Invoice"]["fe:AccountingSupplierParty"]["fe:Party"]["cac:PartyIdentification"]["cbc:ID"]['#text']


        self.cliente=self.root["fe:Invoice"]['fe:AccountingCustomerParty']["fe:Party"]["fe:PartyLegalEntity"]["cbc:RegistrationName"]
        self.nitcliente=self.root["fe:Invoice"]['fe:AccountingCustomerParty']["fe:Party"]['cac:PartyIdentification']["cbc:ID"]['#text']
        self.depto=self.root["fe:Invoice"]['fe:AccountingCustomerParty']["fe:Party"]["fe:PhysicalLocation"]["fe:Address"]["cbc:Department"]
        self.ciudad=self.root["fe:Invoice"]['fe:AccountingCustomerParty']["fe:Party"]["fe:PhysicalLocation"]["fe:Address"]["cbc:CityName"]
        self.direcion=self.root["fe:Invoice"]['fe:AccountingCustomerParty']["fe:Party"]["fe:PhysicalLocation"]["fe:Address"]["cac:AddressLine"]["cbc:Line"]

        print (self.nrofac)
        print (self.fechafac," Vence")#,self.fechafacvec)
        print (self.cufe)
        print (self.totalfac)
        print (self.nit)
        print (self.proveedor)
        print (self.cliente)
        print (self.nitcliente)
        print (self.depto)
        print (self.ciudad)
        print (self.direcion)

        self.detalle=[]
        for items in self.root["fe:Invoice"]['fe:InvoiceLine']:
            self.detalle.append({
                            "item": items['cbc:ID'],
                            "cantidad": items['cbc:InvoicedQuantity']["#text"],
                            "vlr_unidad":items["cbc:LineExtensionAmount"]["#text"],
                            "moneda":items["cbc:LineExtensionAmount"]["@currencyID"],
                            #"valor":items["cbc:LineExtensionAmount"]
                        })
        for items in self.detalle:
            print (items)
            print ("="*20)

if __name__ =="__main__":

    obf=ObjFactura("/home/marco/Clientes/JAVIER/repositorio/face_f08903191930000001DA6.xml")
    #obf=ObjFactura("/home/marco/workspace/genesis/lectorxml/face_f0890312749000000D7D9.xml")
    obf.Extraer()
