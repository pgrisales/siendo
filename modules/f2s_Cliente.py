#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from gluon.validators import CRYPT

class Obj_Cliente():
    """
    Consulta el cliente, busca id
    """

    def __init__(self, db):
        self.db = db

    def Buscar_Cliente(self,nit,nombre=None,proveedor=True):
        """
        Buscar por el nit al cliente,
        si no existe lo crea siempre y cuando se envie el nombre
        """
        db=self.db
        id_cliente=None
        nit=nit.replace(".","").strip()
        buscar=db(db.tbl_cliente.nit==nit).select(db.tbl_cliente.id).first()
        if buscar:
            id_cliente=buscar.id
        else:
            if nombre:
                print("se crear por que no exites nit")
                user_id=db.auth_user.insert(first_name=nombre,
                        last_name=nit,
                        username=nit,
                        password=str(CRYPT(salt=True)(nit)[0])
                        )
                db.commit()
                id_cliente=db.tbl_cliente.insert(  nit=nit,
                                        nombre=nombre,
                                        id_usuario=user_id,
                                        proveedor=proveedor
                                    )
                db.commit()
        return id_cliente

if __name__=="__main__":
    o=Obj_Cliente(db)
    print (o.Buscar_Cliente("900975111"))
