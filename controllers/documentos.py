# -*- coding: utf-8 -*-
def index():
    consulta  =db.tbl_cliente.id_usuario==auth.user_id
    consulta &=db.tbl_recepcion.id_cliente==db.tbl_cliente.id
    consulta=db(consulta).select(db.tbl_recepcion.id,
                                 db.tbl_recepcion.nrodoc,
                                 db.tbl_recepcion.tipdoc,
                                 db.tbl_recepcion.fecha,
                                 limitby=(0,10),
                                cacheable=True)
    if consulta:
        formulario=SalidaBusqueda(consulta)
    else:
        formulario=DIV('No tiene documentos!!')
    buscador=DIV(
            INPUT(_type='date', _name="fecha", _id="fecha", _class='mx-2'),
            A( I ( _class="mx-2 fas fa-search-plus fa-lg text-white" ),
               _onclick="ajax('{}',['fecha'],':eval');".format(URL('AjaxBuscarFecha')),
               _class='btn btn-success' ),
            A('Mostrar Todos',_href=URL('index'),_class='mx-3 px-5 btn btn-success' )
        )

    return dict(formulario=formulario, buscador=buscador)

def SalidaBusqueda(consulta):
    tabla=TABLE( THEAD( TR(TH('Nro. Doc'),TH('Tipo Doc'), TH('fecha'), TH('Control') ) ),
                _class='table table-border')
    cuerpo=TBODY()
    for item in consulta:
        cuerpo.append(TR( TD (item.nrodoc), TD (item.tipdoc.descripcion), TD(item.fecha),
                         TD( SPAN ( A(I(" ",_class="far fa-file-pdf"),_class="btn btn-sm btn-danger btn-circle  text-white",
                _onclick="ajax('{}',['superid'],':eval');$('#visorPDF').modal('show');".format(URL("verpdf",vars=dict(idpdf=item.id)))),
            _class="d-inline-block", _tabindex="0",_title="Ver Docmento", **{'data-toggle':"tooltip", "data-placement":"top"}))
                         ))
    
    tabla.append(cuerpo)
    return DIV(tabla)


#Ajax
def  AjaxBuscarFecha():
    fecha=request.vars.fecha 
    if fecha==None or len(fecha.strip())==0:
        return "alert('Por favor ingrese la fecha');"

    consulta  =db.tbl_cliente.id_usuario==auth.user_id
    consulta &=db.tbl_recepcion.id_cliente==db.tbl_cliente.id
    consulta &=db.tbl_recepcion.fecha>=fecha
    consulta=db(consulta).select(db.tbl_recepcion.id,
                                 db.tbl_recepcion.nrodoc,
                                 db.tbl_recepcion.tipdoc,
                                 db.tbl_recepcion.fecha,
                                 limitby=(0,10 ),
                                cacheable=True)

    if consulta:
        formulario=SalidaBusqueda(consulta)
    else:
        formulario=DIV('No tiene documentos!!')
    salida="$('#resultado').html('{}');".format(XML(formulario))    
    return salida

#ajax
def verpdf():
    '''verpdf entrega el archivo pdf en stream para se visualido en pantalla'''
    id_recepccion=request.vars.idpdf
    salida = F2s_VerPDF(id_recepccion)
    return salida
