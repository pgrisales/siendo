# -*- coding: utf-8 -*-
def index():
    x="aqui"
    return locals()

def lectura():
    pagina=request.vars.start or 0
    elementos_por_pagina=request.vars.length or 10
    direccion = request.vars["order[0][dir]"] or None
    ordenarpor= int(request.vars['order[0][column]']) or 0

    if ordenarpor==0:
        ordenar=db.tbl_cliente.id
    elif ordenarpor==1:
        ordenar=db.tbl_cliente.nombre
    elif ordenarpor==2:
        ordenar=db.tbl_cliente.tipodoc
    elif ordenarpor==3:
        ordenar=db.tbl_cliente.nit
    elif ordenarpor==4:
        ordenar=db.tbl_cliente.correo1
    elif ordenarpor==5:
        ordenar=db.tbl_cliente.correo2
    elif ordenarpor==6:
        ordenar=db.tbl_cliente.correo2
    elif ordenarpor==7:
        ordenar=db.tbl_cliente.correo3
    else:
        ordenar=db.tbl_cliente.nombre





    print (request.vars)

    print(f" ordenarpor:{ordenarpor},  direccion:{direccion}")


    pagina=int(pagina)
    elementos_por_pagina=int(elementos_por_pagina)

    limitby=(pagina, pagina+elementos_por_pagina )
    print (limitby)

    consulta=db.tbl_cliente.id>0
    #registrado &=db.tbl_cliente.proveedor==proveedores
    total=db(consulta).count()
    if direccion =="asc":
        consulta=db(consulta).select(orderby=ordenar, limitby=limitby)
    else:
        consulta=db(consulta).select(orderby=~ordenar, limitby=limitby)

    campos=[]
    for registro in consulta:
        campos.append((
                        registro.id,
                        registro.nombre,
                        registro.tipodoc if registro.tipodoc else "",
                        registro.nit,
                        registro.correo1 if registro.correo1 else "",
                        registro.correo2 if registro.correo2 else "" ,
                        registro.correo3 if registro.correo3 else "",
                      )
                    )
    salida ={
                "data": campos,
                "recordsTotal":total,
                "recordsFiltered":total#len(consulta)
                }
    return response.json(salida)
