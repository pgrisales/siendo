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

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    if auth.has_membership(0,auth.user_id, "Separadores"):
       redirect (URL("separadores","index"))

    if auth.has_membership(0,auth.user_id, "Empacadores"):
        redirect (URL("empacadores","index"))

    if auth.has_membership(0,auth.user_id, "Transportadores"):
        redirect (URL("transportadores","index"))


    response.flash = T("Bienvenidos")
    return dict(message=T('Sistema de Control de Documentos'))


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

def panelcontrol():
    consulta=(db.tbl_modulo.id>0).select(cacheable=True)
    return consulta
