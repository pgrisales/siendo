# -*- coding: utf-8 -*-
def index():
    db.auth_user.id.readable=False
    db.auth_user.username.writable=False
    db.auth_user.username.readable=False
    formulario=SQLFORM(db.auth_user,auth.user.id,
                    showid=True,
                    formstyle='table3cols',
                    col3 = {'first_name':A('¿Qué es esto?',_href='http://www.google.com/search?q=define:name')},
                    submit_button='Guardar Cambio',
                    )
    if formulario.process().accepted:
           response.flash = 'formulario aceptado'
           

           redirect(URL("default","index"))

    elif formulario.errors:
       response.flash = 'el formulario tiene errores'
    else:
       response.flash = 'por favor complete el formulario'

    return dict(formulario=formulario)
