# -*- coding: utf-8 -*-
import re

def fun_input(ident, titulo, fondo="",tipo="text",valor="" ):
	salida = DIV(_class="form-group")
	if tipo=="checkbox":
		salida.append(INPUT(_type="checkbox",_id=ident, _name=ident, value=valor))
		salida.append("|")
		salida.append(LABEL(titulo))
	elif tipo=="textarea":
		salida.append(LABEL(titulo,_for=f"lb_{titulo}"))
		salida.append(TEXTAREA(valor, _cols=60))
	else:
		salida.append(LABEL(titulo,_for=f"lb_{titulo}"))
		salida.append(INPUT(_type=tipo, _id=ident, _name=ident, _class="form-control",_placeholder=fondo, value=valor) )

	return salida

def es_correo_valido(correo):
    if correo==None: return None
    expresion_regular = r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"
    return re.match(expresion_regular, correo) is not None

def fun_ActivarDataTable():
	##Envia los script necesario para activar datatable
	response.files.append(URL('static','js/jquery.dataTables.js'))
	response.files.append(URL('static','js/dataTables.buttons.min.js'))
	response.files.append(URL('static','js/buttons.flash.min.js'))
	response.files.append(URL('static','js/jszip.min.js'))
	response.files.append(URL('static','js/pdfmake.min.js'))
	response.files.append(URL('static','js/vfs_fonts.js'))
	response.files.append(URL('static','js/buttons.html5.min.js'))
	response.files.append(URL('static','js/buttons.print.min.js'))
	response.files.append(URL('static','css/jquery.dataTables.min.css'))
	response.files.append(URL('static','css/buttons.dataTables.min.css'))

def itemmenus(contenedor,items):
	menus=LI(contenedor, _class="nav-header alert-primary")
	for item in items:
		menus.append(LI(A(DIV(
							DIV(I(_class=item[0], _style="color:yellow"), _class="col-sm-2"),
							DIV(item[1],_class="col-sm-10 nav-header"),
							_class="row"),
						_href=item[2])
						))
	return menus

def fun_Menu():
	salida=UL(_class="nav")
	salida.append(itemmenus("",(
									("fas fa-home",T('Home'), URL('default', 'index')),
									)))

	if auth.has_membership("Administradores") or auth.has_membership("Super"):
		salida.append(itemmenus("ADMINISTRACION",(
						("fas fa-users-cog fa-xs","Administrar",URL('administrar', 'index')),
						("fas fa-hammer fa-xs","Parametros",URL('parametros', 'index')),
				)))
	if auth.has_membership("Administradores") or auth.has_membership("Super") or auth.has_membership("Gerencia"):
		salida.append(itemmenus("MODULOS",(
					("fab fa-telegram-plane fa-xs",T('Comprobante de Pago a Proveedores'), URL('compegreso', 'index')),
					("fab fa-deploydog fa-xs", T('Comprobante de Pago a Empleados'), URL('compnomina', 'index')),
					("fas fa-certificate fa-xs",T('Certificación de Retención por IVA'), URL('retiva', 'index')),
					("fas fa-wallet fa-xs",T('Ret. Fuente, Ret. ICA'), URL('compretencionanual', 'index')),
 				)))
	#if auth.has_membership("Proveedor") or auth.has_membership("Empleados") or auth.has_membership("Super"):
	salida.append(itemmenus("DOCUMENTOS",(
									("fas fa-book fa-xs",T('Publicaciones'), URL('documentos', 'index')),
		)))
	if auth.has_membership("Super"):
		salida.append(itemmenus("GENERAL",(
									("fas fa-radiation-alt",T('Configuracion'), URL('cntrpal', 'index')),
		)))


	salida.append(
		LI(XML('<a href="javascript:;" class="sidebar-minify-btn" data-click="sidebar-minify"><i class="fa fa-angle-double-left"></i></a>'),
		)
	)
	return salida


def BuscarEnClientes(tipo):
    fecha_inicio=request.vars.fecha_inicio or None
    fecha_final=request.vars.fecha_final   or None
    nit=request.vars.nit_correo            or None
    salida=""
    consulta =db.tbl_recepcion.tipdoc==tipo

    if fecha_inicio:
        fecha_inicio +=" 00:00:00"
        consulta &= db.tbl_recepcion.fechaenvio>=fecha_inicio
    if fecha_final:
        fecha_final += " 23:59:59"
        consulta &= db.tbl_recepcion.fechaenvio<=fecha_final

    subconsulta=None
    if nit:
        nit=f"%{nit}%"
        idclientes=db(db.tbl_cliente.nit.like(nit) | db.tbl_cliente.nombre.like(nit)).select(db.tbl_cliente.id)

        if idclientes:
            for idcliente in idclientes:
                if subconsulta:
                    subconsulta |=db.tbl_recepcion.id_cliente==idcliente.id
                else:
                    subconsulta =db.tbl_recepcion.id_cliente==idcliente.id
        else:
            salida =DIV("No se encontro la busqueda solicitada",_class="alert alert-danger", _role="alert")
            return salida

    tempo  =db.tbl_recepcion.estado=="Q"
    tempo |=db.tbl_recepcion.estado=="T"
    tempo |=db.tbl_recepcion.estado=="F"
    #### Nuevo
    consulta &=tempo
    if  subconsulta:            consulta &= subconsulta
    ####
    x=consulta
    consulta=db(consulta).select()
    tabla=TABLE(_class="table table-striped")
    #tabla.append(THEAD(TR(TH("Empleados"),TH("Doc. id"), TH("Nro. Doc."), TH("Estado"),TH("Fecha Envio"), TH("Controles"))))
    tabla.append(THEAD(TR(TH("Empleados"),TH("Doc. id"), TH("Nro. Doc."), TH("Fecha Envio"), TH("Controles"))))
    #tabla.append(TR(TD(fecha_inicio),TD(tempo), TD(x), TD(consulta)))
    for item in consulta:
        tabla.append(TR(TD(item.id_cliente.nombre),
                        TD(item.id_cliente.nit),
                        TD(item.nrodoc),
                        #TD(T(item.tarea.status)),
                        TD(item.fechaenvio),
                        TD(  SPAN (
                                A(I(" ",_class="far fa-file-pdf"),_class="btn btn-sm btn-danger btn-circle  text-white",
                                    _onclick="ajax('{}',['superid'],':eval');$('#visorPDF').modal('show');".format(URL("verpdf",vars=dict(idpdf=item.id)))),
                                _class="d-inline-block", _tabindex="0",_title="Ver Docmento", **{'data-toggle':"tooltip", "data-placement":"top"}),
                            "|",
                            SPAN (A(I(" ",_class="fas fa-mail-bulk"),_class="btn btn-sm btn-success btn-circle btn text-white",
                                    _onclick="$('#DialModal').modal('show');ajax('{}',['usrid'],':eval');".format(URL('ReenvioCorreo',vars=dict(id_recepcion=item.id)))),
                            _class="d-inline-block", _tabindex="0",_title="Reeviar Correo", **{'data-toggle':"tooltip"}),
                        _align="right"
                        )
                    )
                )
    salida=tabla
    return salida
