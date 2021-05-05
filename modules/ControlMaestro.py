# -*- coding: utf-8 -*-

import logging
import time

def Procesar():
    print("Procesar")
    trabajos=[]
    try:
        while True:
            #print (".")
            buscar=db(db.tbl_control_maestro.estado=='I').select()
            for trabajo in buscar:
                print("Asignado")
                trabajo.update_record(estado="P")
                db.commit()
                print ('trabajo:', trabajo.args)
                datos=eval(trabajo.args)
                print (datos)
                GenerarPDF(datos["archivo"],datos['modulo'])
                trabajo.update_record(estado="F")
                db.commit()
                print ("Fin Generar PDF")
            time.sleep(10)
            db.commit()

    except KeyboardInterrupt:
        print ("finalizado. por ctl+c ")


if __name__=="__main__":
    logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] (%(threadName)-10s) %(message)s',)
    Procesar()
    print ("fin ")
