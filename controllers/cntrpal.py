# -*- coding: utf-8 -*-
# ---
@auth.requires(auth.has_membership ('Super') )
def index():
    temp='''var confirmar=confirm(
            "Se van a borrar todos los datos del cliente, esta seguro???");
            if (confirmar){ajax('ajax_borrarTodo','[id]','resultado');}
            else {alert('no borrado');}
        '''

    btn_borrardatos=A('Borrar todos Datos', _class='btn btn-warning', _name='btn_borrardatos',
                        _onclick=temp)
    return dict(btn_borrardatos=btn_borrardatos)

@auth.requires(auth.has_membership ('Super') )
def ajax_borrarTodo():
    db(db.auth_user.id>2).delete()
    db(db.tbl_recepcion.id>0).delete()
    db(db.tbl_control_maestro.id>0).delete()
    db.commit()
    db.executesql ('ALTER TABLE auth_user AUTO_INCREMENT = 3;')
    db.executesql ('ALTER TABLE tbl_cliente AUTO_INCREMENT = 1;')
    db.executesql ('ALTER TABLE tbl_recepcion AUTO_INCREMENT = 1;')
    db.executesql ('ALTER TABLE tbl_control_maestro AUTO_INCREMENT = 1;')
    return "Se a eliminado los datos;"
