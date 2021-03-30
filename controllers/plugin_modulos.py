# -*- coding: utf-8 -*-

@auth.requires(lambda: auth.has_membership('Administradores') or auth.has_membership ('Super') )
def ServerCorreo():
    id_server=request.vars.idserver or 0
    consulta=db(db.tbl_parametros.id==id_server).select(db.tbl_parametros.id).first()
    if consulta==None:
        return DIV("No existe Configuracion!!", _class="alert alert-danger")

    db.tbl_parametros.id.writable=False
    db.tbl_parametros.id.readable=False
    db.tbl_parametros.id_modulo.readable=False
    db.tbl_parametros.id_modulo.writable=False
    formulario=SQLFORM(db.tbl_parametros, consulta.id)
    if formulario.process().accepted:
        response.flash = 'el formulario tiene errores'
    elif formulario.errors:
        response.flash = 'por favor complete el formulario'
    return formulario
