#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gluon.html import *
from gluon import *

def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def Paginador(cantidad,pagina, maxlinea,datosbusqueda,add_variable={}):
    ruta="{}".format(current.request.function)
    nropaginas=cantidad / maxlinea  #Calculo max nro paginas
    if cantidad % maxlinea >0:      #Si hay una lineas de mas se suma la pagina
        nropaginas +=1

    paghtml=UL(_class="pagination")

    nropaginas=int(nropaginas)
    if nropaginas <=10:
        for pag in range(1, nropaginas+1):
            temp_vars=add_variable

            temp_vars["f2s_pagina"]=pag
            if datosbusqueda:
                temp_vars["f2s_buscar"]=datosbusqueda
            if pag == pagina:
                paghtml.append (LI(A(pag, _href=URL(ruta,vars=temp_vars,user_signature=True)),_class="active") )
            else:
                paghtml.append (LI(A(pag, _href=URL(ruta,vars=temp_vars,user_signature=True))) )
    else:
        #Primera pagina
        if pagina >1:
            temp_vars=add_variable
            if datosbusqueda:
                temp_vars["f2s_buscar"]=datosbusqueda
            temp_vars["f2s_pagina"]=1

            paghtml.append(LI(A(XML('<span class="glyphicon glyphicon-step-backward" aria-hidden="true"></span>'),
                                 _href=URL(ruta,vars=temp_vars,user_signature=True))))
            #Anterior
            temp_vars=add_variable
            temp_vars["f2s_pagina"]=pagina-1
            if datosbusqueda:
                    temp_vars["f2s_buscar"]=datosbusqueda

            paghtml.append(LI(A(XML('<span class="glyphicon glyphicon-backward" aria-hidden="true"></span>'),
                                     _href=URL(ruta,vars=temp_vars,user_signature=True))))


        if pagina ==1:
            inicio=1
        else:
            inicio = pagina - 4

        final= pagina + 4

        if final > nropaginas:
                final= nropaginas

        if inicio < 1:
                inicio =1


        for pag in range (inicio, final + 1):
            temp_vars=add_variable
            temp_vars["f2s_pagina"]=pag
            if datosbusqueda:
                    temp_vars["f2s_buscar"]=datosbusqueda
            if pag == pagina:
                paghtml.append (LI(A(pag, _href=URL(ruta,vars=temp_vars,user_signature=True)),_class="active") )
            else:
                paghtml.append (LI(A(pag, _href=URL(ruta,vars=temp_vars,user_signature=True))) )

        if nropaginas > pagina:
            temp_vars=add_variable
            temp_vars["f2s_pagina"]=pagina+1
            paghtml.append(LI(A(XML('<span class="glyphicon glyphicon-forward" aria-hidden="true"></span>'),
                _href=URL(ruta,vars=temp_vars,user_signature=True)
                    )    )    )

            #final
            temp_vars=add_variable
            temp_vars["f2s_pagina"]=nropaginas
            paghtml.append(LI(A(XML('<span class="glyphicon glyphicon-step-forward" aria-hidden="true"></span>'),
                _href=URL(ruta,vars=temp_vars,user_signature=True)
                        )    )    )

        paghtml=DIV(paghtml, _class="f2s_paginador")
    ##paghtml.append (DIV("inicio:",inicio,"final:",final,"nropaginas:",nropaginas,"pag:",pag))
    return paghtml

def Control_Buscar(busqueda,datosbusqueda):
    if not isinstance (busqueda,list):
        return DIV("")
    salida=DIV(_class="panel panel-primary")
    salida.append( DIV ("Buscador",_class="panel-heading", _id="a", _onclick="jQuery('#f2s_frmbuscador').slideToggle()"))
    contendor=DIV(_id='f2s_frmbuscador', _class="panel-body")
    contador=0

    for fila in busqueda:
        if len(datosbusqueda)>0:
            contendor.append (INPUT(_id='f2s_buscar', _name='f2s_buscar', _placeholder=fila["ayuda"], _value=datosbusqueda[contador]))
        else:
            contendor.append (INPUT(_id='f2s_buscar', _name='f2s_buscar', _placeholder=fila["ayuda"]))

        contador +=1

    contendor.append (INPUT(_type='submit',_class="btn btn-primary", _value="Buscar"))
    contendor.append (A("LIMPIAR",_class="btn btn-default",_href=URL(

                                                                        current.request.controller,
                                                                        current.request.function)
                        )
                    )

    salida.append(contendor)
    salida=FORM(salida)
    control=0

    if salida.accepts(current.request,current.session):
        current.response.flash = 'Trabajo realizado'
        control=1   #Indica que se debe ir a la primera pagina
    elif salida.errors:
        current.salida.flash = 'Error en busqueda'

    return salida,control

def Adicional_Consulta(busqueda):
    datosbusqueda=[]
    adicion_consulta=None       #adiciona a la consulta final la busqueda

    if current.request.vars.f2s_buscar:
        datosbusqueda=current.request.vars.f2s_buscar
        if not isinstance(datosbusqueda, list):
            datosbusqueda=[current.request.vars.f2s_buscar]

        #revisa que tenga datos a buscar..
        contador=0
        for fila in busqueda:
            #por el momento solo se buscar campos texto......
            if len(datosbusqueda[contador].strip())<1:
                contador +=1
                continue

            if adicion_consulta:
                adicion_consulta |=fila["campo"].ilike ("%{}%".format(datosbusqueda[contador]))
            else:
                adicion_consulta =fila["campo"].ilike ("%{}%".format(datosbusqueda[contador]))

            contador +=1

    return datosbusqueda, adicion_consulta


def Fun_Grilla(db, consulta,campos=None,titulos=None,seleccion={}, links=None, busqueda=None,rutaselect=None,izquierda=None,add_variable=None, lnxpag=None,alinearcols=None,unir=None,ordenar=None):

    def_variable={}
    if isinstance(add_variable, dict) :
        for nombre in add_variable:
            def_variable[nombre]=add_variable[nombre]

    f2s_id=None

    #[] seleccion del la fila..
    if current.request.vars.f2s_id and seleccion:
        if "ruta"in seleccion:
            f2s_id=current.request.vars.f2s_id
            def_variable["id"]=f2s_id
            redirect(URL(*seleccion["ruta"],vars=def_variable,user_signature=True))

    pagina  = int(current.request.vars.f2s_pagina or 1)

    maxlinea=current.request.vars.f2s_lineas  or 10

    if lnxpag:
        if isinstance (lnxpag,int):
            maxlinea = lnxpag

    f2s_ordenar=current.request.vars.f2s_ordenar or None
    f2s_orden_arriba=current.request.vars.f2s_orden_arriba or None

    if ordenar:
        f2s_ordenar=ordenar

    if f2s_ordenar:
        def_variable["f2s_ordenar"]=f2s_ordenar
    if f2s_orden_arriba:
        def_variable["f2s_orden_arriba"]=f2s_orden_arriba

    error=""
    salida=DIV(_id="F2S_grilla", _name="F2S_grilla")
    #salida.append(DIV("PRUEBA1:",f2s_id))
    #control de busqueda
    datosbusqueda,add_consulta=Adicional_Consulta(busqueda)

    if add_consulta:
        cantidad=db((consulta)&(add_consulta)).count()
    else:
        cantidad=db(consulta).count()

    #crea el placeholder en los input

    ayuda=[]
    if busqueda:
        for fila in busqueda:
            ayuda.append({"ayuda":fila['ayuda']})
        #Lectura formulario de busqueda y control para la primera busqueda
        fromulario_busqueda, control=Control_Buscar(ayuda,datosbusqueda)

        if control==1:
            pagina=1
    else:
        fromulario_busqueda=""

    if cantidad==0:
        '''No hay registro'''
        salida.append(DIV(DIV(fromulario_busqueda, _class="col-md-12"),
                          DIV("No existen registros, Cambia la busqueda o pulsa el boton [LIMPIAR]",
                            XML(' <button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>') ,
                            _class="col-md-7 alert alert-warning",
                            role="alert"),
                     _class="row")
                    )

        return salida

    #paginador
    paginador=Paginador(cantidad,pagina,maxlinea,datosbusqueda,def_variable)
    salida.append(DIV(DIV(fromulario_busqueda, _class="col-md-12"),
                      DIV(paginador,_align="right",_class="col-md-7"),
                      DIV("Nro de Registros {}".format(cantidad),_class="f2s_nroreg", _align="right", _style="margin-right: 20px;"),
                     _class="row"))

    #control busqueda
    if add_consulta:
        busqueda=((consulta)&(add_consulta))
    else:
        busqueda=consulta

    pagina = pagina -1
    if pagina <0:
        pagina=0

    if campos:			#campos a mostrar
        if seleccion:
            if isinstance(seleccion, dict):
                if "campo" in seleccion:
                    campos.insert (0,seleccion["campo"])
                else:
                    error +="No exites key=campo"
            else:
                campos.insert (0,seleccion)

        if f2s_ordenar:

            (ts, fs) = f2s_ordenar.split('.')
            if int(f2s_orden_arriba)==1:
                sortby = db[ts][fs]
            else:
                sortby = ~db[ts][fs]
            datos=db(busqueda).select(*campos,
                                        left=izquierda,
                                        limitby=( (pagina*maxlinea), (pagina*maxlinea)+maxlinea),
                                        orderby=sortby)
        else:
            datos=db(busqueda).select(*campos,
                                        left=izquierda,
                                         limitby=( (pagina*maxlinea), (pagina*maxlinea)+maxlinea) )
        lstcolumnas = datos.colnames
    else:
        datos=db(consulta).select(left=izquierda,
                                    limitby=((pagina*maxlinea), (pagina*maxlinea)+maxlinea  ))
        lstcolumnas = datos.colnames
        #Lista las tablas usada en la consulta
        tablas= list(set(map(lambda c: c.split('.')[0], lstcolumnas)))


        salida.append (lstcolumnas)
        salida.append (tablas)

    tabla=TABLE()
    par=0
    lineas=[]


    for fila in datos:


        if par==0:
            linea=TR(_class="w2p_odd odd with_id")
            par=1
        else:
            linea=TR(_class="w2p_even even with_id")
            par=0
        col1=True
        poscol=0
        alineartd="text-align: left;"

        if unir:
            unir_datos,poscolunir,cols_omitir,alineartd_unir=unir_campos(fila,unir,lstcolumnas)
        else:
            unir_datos=None
            poscolunir=-1
            cols_omitir=None

        for columna in lstcolumnas:
            if cols_omitir:
                if columna in cols_omitir:
                    continue

            if alinearcols:
               if poscol <=len(alinearcols)-1:
                    if alinearcols[poscol]=="D":
                        alineartd="text-align: right;"
                    elif alinearcols[poscol]=="C":
                        alineartd="text-align: center;"
                    else:
                        alineartd="text-align: left;"

            if poscol==poscolunir:
                linea.append (TD(unir_datos,_style=alineartd_unir))
                poscol +=1
                continue
            poscol +=1
            if "ruta" in seleccion and col1:
                linea.append(TD(INPUT( _name="f2s_id",
                                        _id="f2s_id",
                                        _type="checkbox",
                                        _value=fila[columna]
                                        )
                                )
                            )
                col1=False
                continue

            elif col1:
                col1=False
                continue

            linea.append (TD(fila[columna],
                                _style=alineartd))

        if poscol == poscolunir:
            linea.append (TD(unir_datos,_style=alineartd_unir))


        if links:
            for link in links:
                linea.append(TD(link(fila)))

        lineas.append(linea)
    tabla.append(TBODY(lineas))

    if "ruta" in seleccion:
        lineas=[TH(SPAN("Todos",BR(),
                    INPUT(_onclick="$('input:checkbox').prop('checked', this.checked);eventos=2;", _value="on", _type="checkbox")),
                    _style="vertical-align:middle; ")]
    else:
        lineas=[]
    #Direccion del orden
    if f2s_orden_arriba:
        if isinstance(f2s_orden_arriba,list):
            f2s_orden_arriba=f2s_orden_arriba[0]
        f2s_orden_arriba=int(f2s_orden_arriba)

        if f2s_orden_arriba==1:
            f2s_orden_arriba=2
        else:
            f2s_orden_arriba=1
    else:
        f2s_orden_arriba=2
    contador=1
    for titulo in titulos:
        #organizar sorteo
        f2s_buscar=current.request.vars.f2s_buscar or None

        icono=""


        if f2s_buscar:
            #camibo orden busqueda
            def_variable["f2s_ordenar"]=campos[contador]
            def_variable["f2s_buscar"]=f2s_buscar
            def_variable["f2s_orden_arriba"]=f2s_orden_arriba
            def_variable["f2s_pagina"]=1

            sorteo=A(titulo,icono,_href=URL(    current.request.controller,
                                                current.request.function,
                                                vars=def_variable
                                            )
                                        )
        else:
            def_variable["f2s_pagina"]=1
            #if f2s_ordenar:
            def_variable["f2s_orden_arriba"]=f2s_orden_arriba
            def_variable["f2s_ordenar"]=campos[contador]

            sorteo=A(titulo,icono,_href=URL(current.request.controller,current.request.function,
                                        vars=def_variable)
                    )

        lineas.append(TH(CENTER(SPAN(sorteo)),_style="vertical-align:middle; "))
        contador +=1

    if links:
        if len (links)==1:
            lineas.append(TH(SPAN("Controles")))
        else:
            lineas.append(TH(CENTER(SPAN("Controles")),_colspan=len(links),_style="vertical-align:middle; "))
    tabla.append(THEAD(TR((lineas))))
    salida.append(DIV(
                            DIV(tabla,
                                _class="web2py_table"
                                ),
                            _class="web2py_grid "
                            ),

                )
    #Ruta para el selector
    contenedor=[]
    if ("ruta" in seleccion):
        if not "titulo" in seleccion:
            seleccion["titulo"]=T("Enviar")

        contenedor.append(BUTTON(seleccion["titulo"],
                            _class="btn btn-primary",
                            )
                        )
    if len(lineas)>6:
        salida.append(DIV(DIV(contenedor,_class="col-md-5"),DIV(paginador,_class="col-md-7"),_class="row"))
    else:
        salida.append(DIV(DIV(contenedor,_class="col-md-5"),_class="row"))
    salida.append(INPUT(_id="f2s_orden_arriba",_name="f2s_orden_arriba",_value=f2s_orden_arriba, _hidden=True))
    salida=FORM(salida,user_signature=True)
    return salida

def unir_campos(fila,unir,lstcolumnas):
	#Estructura:
	#	pos
	#	0		formato, ejemplo: "{1} {2} [{0}]"
	#	1		Columna posicion de la tabla
	#   2       alinear
	#	3 -1	Campos a unir
	#	-1		Campo a oviar
	#Ejemplo:
	#	unir =["{1} {2} [{0}]",10,"I","auth_user.username","auth_user.first_name","auth_user.last_name","tbl_itempedido.separador1"]

	unir_datos=[]
	for columna in lstcolumnas:
		if columna in unir[3:-1]:
			unir_datos.append(fila[columna])

	unidos=unir[0].format(*unir_datos)
	if  unir[2]=="D":
		alineartd="text-align: right;"
	elif unir[2]=="C":
		alineartd="text-align: center;"
	else:
		alineartd="text-align: left;"

	return unidos,unir[1],unir[3:],alineartd
