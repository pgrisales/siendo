# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------
#sicodes
# SIstema COntrol de DESpacho

@auth.requires_login()
def lst_usr():
    db.auth_user.last_name.readable=False
    db.auth_user.last_name.writable=False
    db.auth_user.id.readable=False
    db.auth_user.id.writable=False
    db.auth_user.email.readable=False
    db.auth_user.email.writable=False
    links = [ lambda row: A('Ingresar',_class='button btn btn-success',_href=URL("pedidos","index",args=[row.id]))]
    busqueda=SQLFORM.grid(db.auth_user.id>2,
                          deletable=False,
                          editable=False,
                          details=False,
                          create=False,
                          csv=False,
                          maxtextlength=64,
                          headers={"auth_user.first_name":"Nombre", "auth_user.username":"Usuario del sistema"}
                          #links=links,

                          )

    return locals()


def login():

     return dict(form=auth.login())


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())



@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()

def prueba():
    from gluon.tools import Expose
    return dict(archivos=Expose('/home/www-data/',extensions=['.pdf']))

def Mensajes():
    if not auth.user:return ("")
    salida=""
    consulta =db.tbl_mensajes.created_by==auth.user.id
    consulta &=db.tbl_mensajes.visto==False
    consulta =db(consulta).select(orderby=~db.tbl_mensajes.created_on,limitby=(0,5))
    niveles=("fa fa-bug media-object bg-silver-darker","fab fa-google text-warning media-object-icon f-s-14")
    if consulta:
        salida=A(I(_class="fa fa-bell"), SPAN(len(consulta), _class="label"),
        _href="javascript:;", _class="dropdown-toggle f-s-14", **{'data-toggle':'dropdown'},)
        mensajes=UL(_class="dropdown-menu media-list dropdown-menu-right")
        mensajes.append(LI (f"Mensajes ({len(consulta)})", _class="dropdown-header"))
    return salida

def FunTabla(estadoc,estadoe):



    tabla=TABLE(_class='table')
    tabla.append(TBODY(
                        TR(TD('Pendientes:'),TD(SPAN(estadoc+estadoe, _class='badge badge-soft-success mr-2'), _class='font-weight-bold text-right')),
                        TR(TD('Sin Correo:'),TD(estadoc, _class='text-right')),
                        TR(TD('Por enviar:'),TD(estadoe, _class='text-right')),
                    ))
    return tabla

def FunTitulo(titulo,color='bg-danger',campana=True):
    if campana:
        salida =DIV(I(_class="fas fa-bell fa-2x m-4 fa-border fa-pull-left"),titulo, _class='card-header text-white {}'.format(color))
    else:
        salida =DIV(I(_class="fas fa-lightbulb fa-2x m-4 fa-border fa-pull-left"),titulo, _class='card-header text-white {}'.format(color))
    return salida



@auth.requires_login()
def index():
    if  ( not auth.has_membership("Super")
            and not auth.has_membership("Administradores")
            and not auth.has_membership("Gerencia")
            and not auth.has_membership("Empleados")
            and not auth.has_membership("Proveedor")): redirect(URL('documentos','index'))

    consulta=db.tbl_modulo.id>0
    modulos=[salida ['id'] for salida in db(consulta).select(db.tbl_modulo.id, cacheable=True).as_list()]
    consulta &=db.tbl_recepcion.tipdoc==db.tbl_modulo.id
    consulta &= (db.tbl_recepcion.estado=='C')|(db.tbl_recepcion.estado=='E')
    contar=db.tbl_recepcion.id.count()

    formulario=[]
    consulta=db(consulta).select(contar,
                                 db.tbl_recepcion.tipdoc,
                                 db.tbl_recepcion.estado,
                                 groupby = db.tbl_recepcion.tipdoc|db.tbl_recepcion.estado,
                                 orderby =db.tbl_recepcion.tipdoc|db.tbl_recepcion.estado,
                                 cacheable=True)
    if consulta:
        estadoc=0
        estadoe=0
        titulo=''
        id_recepcion=None
        for item in consulta:
            if id_recepcion==None:
                id_recepcion=item.tbl_recepcion.tipdoc
                if id_recepcion in modulos: modulos.remove((id_recepcion))

            if item.tbl_recepcion.tipdoc==id_recepcion:
                titulo=FunTitulo(item.tbl_recepcion.tipdoc.descripcion,'bg-danger')

                if item.tbl_recepcion.estado=='C':
                    estadoc=item[contar]
                else:
                    estadoe=item[contar]
            else:
                cuerpo=DIV(_class='card-body')
                cuerpo.append(FunTabla(estadoc,estadoe))
                formulario.append(DIV(titulo,cuerpo, _class='card m-5'))
                estadoc=0
                estadoe=0
                if id_recepcion in modulos: modulos.remove(id_recepcion)
                id_recepcion=item.tbl_recepcion.tipdoc

                titulo=FunTitulo(item.tbl_recepcion.tipdoc.descripcion,'bg-danger')
                if item.tbl_recepcion.estado=='C':
                    estadoc=item[contar]
                else:
                    estadoe=item[contar]
        if id_recepcion in modulos: modulos.remove(id_recepcion)
        cuerpo=DIV(_class='card-body border-right border-bottom border-danger')
        cuerpo.append(FunTabla(estadoc,estadoe))
        formulario.append(DIV(titulo,cuerpo, _class='card m-5'))
    #Sin pendientes
    consulta=db(db.tbl_modulo.id.belongs(modulos)).select(db.tbl_modulo.descripcion, cacheable=True)
    for item in consulta:
        titulo=FunTitulo(item.descripcion, 'bg-primary', False)
        cuerpo=DIV(_class='card-body border-right border-bottom border-primary')
        cuerpo.append(FunTabla(0,0))
        formulario.append(DIV(titulo,cuerpo, _class='card m-5'))

    return dict(formulario=formulario, consulta=modulos)
