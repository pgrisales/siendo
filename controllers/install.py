# -*- coding: utf-8 -*-
# try something like
def inicio():
    ################## DEFECTO #################
    creargrupos()
    crearadmin()
    return "ok"

def limpiar():
    comando='''SET FOREIGN_KEY_CHECKS = 0;
    truncate tbl_cliente;
    truncate tbl_recepcion;
    truncate scheduler_task;
    truncate scheduler_run;
    truncate tbl_control_maestro;
    truncate tbl_control_procg;
    DELETE FROM auth_user where id>2;
    ALTER TABLE auth_user AUTO_INCREMENT =3;
    SET FOREIGN_KEY_CHECKS = 1;
    '''
    db.executesql(comando)
    return "OK"

def crearindex():
    sql="create index nrodoc_idx on tbl_recepcion (nrodoc);"
    db.executesql(comando)

def creargrupos():
    if db(db.auth_group).isempty():
        db.auth_group.insert (role="Super",description="SimpleSoft")
        db.auth_group.insert (role="Administradores",description="Grupo dedicado a la parametrizacion  e importar/exporta datos")
        db.auth_group.insert (role="Gerencia",description="Grupo dedicado a ver el comportamiento de los indicadores del sistema")
        db.auth_group.insert (role="Empleados",description="Consutlas de empleados")
        db.auth_group.insert (role="Proveedor",description="Consulta de proveedores")
        return "ok"
    else:
        return "ya Fueron Craeados"


def crearadmin():
    if db(db.auth_user).isempty():
        db.auth_user.insert (first_name="Super",
                             last_name="SimpleSoft",
                             username="super",
                             password=str(CRYPT(salt=True)('Terero.2021')[0])
                             )
        db.auth_user.insert (first_name="Administrador",
                             last_name="Sistema",
                             username="admin",
                             password=str(CRYPT(salt=True)('admin')[0])
                             )
        idamin=db.auth_membership.insert(user_id=1,group_id=1)
        idamin=db.auth_membership.insert(user_id=2,group_id=2)
        return "ok"
    else:
        return "Ya fue creado el usuario admin"


def prueba():
    idtarea=37
    funcion='var estado_tarea=0;'
    funcion+='function generarEstado(){ajax('
    funcion+="'{}',['idtarea'],':eval');".format(URL("VerEstado", vars=dict(idtarea=idtarea)))
    funcion+="};estado_tarea = setInterval(generarEstado(), 5000);"

    salida= A("estado", _class="btn btn-success", _onclick= funcion)
    return locals()

def VerEstado():
    idtarea=request.vars.idtarea or None
    if not idtarea: return "alert('no hay tarea'); clearInterval(estado_tarea);"
    return "alert('ok');"#" clearInterval(estado_tarea);"
