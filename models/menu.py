# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# ----------------------------------------------------------------------------------------------------------------------
# this is the main application menu add/remove items as required
# ----------------------------------------------------------------------------------------------------------------------

response.menu = [
    (T('Home'), "fas fa-home", URL('default', 'index'), [])
]

# ----------------------------------------------------------------------------------------------------------------------
# provide shortcuts for development. you can remove everything below in production
# ----------------------------------------------------------------------------------------------------------------------
#
if not configuration.get('app.production'):
    _app = request.application
    response.menu += [
        (T('Administrar'), "fas fa-users-cog", URL('administrar', 'index')),
        (T('Parametros'), "fas fa-hammer", URL('parametros', 'index')),
        (T('Comprobante de Pago a Proveedores'), "fab fa-telegram-plane", URL('compegreso', 'index')),
        (T('Comprobante de Pago a Empleados'), "fab fa-deploydog", URL('compnomina', 'index')),
        (T('Certificación de Retención por IVA'), "fas fa-certificate", URL('compegreso', 'index')),
        (T('Estado de Cartera de Clientes'),"fas fa-wallet", URL('compegreso', 'index')),
        #(T('Subir Clientes excel'), False, URL('subirplano', 'index')),
    ]
