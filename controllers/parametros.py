# -*- coding: utf-8 -*-
from os.path import join as UNIR
@auth.requires(lambda: auth.has_membership('Administradores') or auth.has_membership ('Super') )
def index():
    lugar = request.vars.lugar or 2
    modulos = [OPTION(item.descripcion,_value=item.id) for item in db().select(db.tbl_modulo.ALL)]
    modulos.insert(0,OPTION("Seleccionar Modulo",_value=0))
    modulos = SELECT(*modulos, _class= "form-control",_id="idserver", _name="idserver",
                    _onchange="ajax('{}',['idserver'],'result_Server');".format(URL('formServer',vars=dict(lugar=1))),
                    requires=IS_IN_DB(db,db.tbl_modulo.id,"%(descripcion)s"),
                    )


    #registrado=LstProveedores()
    #empleados=LstProveedores(False)
    registrado=TABLE(THEAD(TR(TH("NIT"),TH("Proveedor"), TH("Correo Envio"),TH("Control",_align="right"))),
                        _class="table table-striped table-bordered", _id="tabla_proveedores")

    empleados=TABLE(THEAD(TR(TH("Cedula"),TH("Nombre Empleado"), TH("Correo Envio"),TH("Control",_align="right"))),
                    _class="table table-striped table-bordered", _id="tabla_empleados", _style="width: 100%;")

    titulos=SQLFORM.grid(db.tbl_modulo,
                        csv=False,
                        create=False,
                        details=False,
                        deletable=False,
                        maxtextlength=80,
                        fields=[db.tbl_modulo.descripcion,db.tbl_modulo.ambiente],
                        )
    return dict(registrado=registrado, empleados=empleados,modulos=modulos,lugar=lugar,titulos=titulos)


@auth.requires(lambda: auth.has_membership('Administradores') or auth.has_membership ('Super') )
def fun_ModCorreo():
    modulos=db(db.tbl_modulo.id>0).select()
    if not modulos:
        salida=DIV("No hay modulos instalados!!", _class="alert alert-danger")
        return salida
    opciones=[""]
    for modulo in modulos:
        opciones.append(OPTION(modulo.descripcion, _value=modulo.id))
    salida=DIV(
            SELECT(*opciones,_class="form-control", _id="id_correomol",_name="id_correomol",
            _onchange="ajax('{}',['id_correomol'],':eval');".format(URL("leerCorreoMod"))),
            DIV(_id='resultado_parametro')
    )
    return salida
#ajax de fun_ModCorreo
@auth.requires(lambda: auth.has_membership('Administradores') or auth.has_membership ('Super') )
def leerCorreoMod():
    id_mod=request.vars.id_correomol or 0
    consulta=db(db.tbl_parametros.id==id_mod).select().first()
    db.tbl_parametros.id.writable=False
    db.tbl_parametros.id.readable=False
    #db.tbl_parametros.cuerpohtml.widget=ckeditor.widget
    formulario=SQLFORM(db.tbl_parametros, consulta.id if consulta else  None)
    # if formulario.process().accepted:
    return formulario
    salida=salida=DIV()
    #return "alert('{}');".format(consulta.id if consulta else "no exites")
    salida.append(fun_input("hostname", "Servidor",tipo="text",valor=consulta.servidor_correo if consulta else ""))
    salida.append(fun_input("puerto", "Puerto",tipo="text",valor=consulta.puerto if consulta else ""))
    salida.append(fun_input("Usuario", "Usuario",tipo="text",valor=consulta.usuario if consulta else ""))
    salida.append(fun_input("password", "Clave",tipo="text",valor=consulta.password if consulta else ""))
    salida.append(fun_input("tls", "TLS activo",tipo="checkbox",valor=consulta.tls if consulta else ""))
    salida.append(fun_input("enviado_por", "Enviado Por",tipo="text",valor=consulta.enviado_por if consulta else ""))
    salida.append(fun_input("asunto", "Asunto",tipo="text",valor=consulta.asunto if consulta else ""))
    salida.append(fun_input("devolver", "Devolver",tipo="text",valor=consulta.devolver if consulta else ""))
    salida.append(fun_input("cuerpo", "Cuerpo",tipo="textarea",valor=consulta.cuerpo if consulta else ""))
    salida.append(fun_input("cuerpohtml", "Cuerpo html",tipo="text",valor=consulta.cuerpohtml if consulta else ""))
    salida="$('#resultado_parametro').html('{}');".format(salida)

@auth.requires(lambda: auth.has_membership('Administradores') or auth.has_membership ('Super') )
def fun_BotonActivo(valor, idusr):
    if valor:
        salida=SPAN(A(I(_class="fas fa-user-check"),_class= "btn btn-sm btn-success btn-circle btn text-white",
                        _onclick="ajax('{}',['usuarios'],':eval');".format(URL("switcheActivar",vars=dict(id_usuario=idusr)))),
                        _class="d-inline-block", _tabindex="0",_title="Desactivar", **{'data-toggle':"tooltip"})
    else:
        salida=SPAN(A(I(_class="fas fa-check"),_class= "btn btn-sm btn-danger btn-circle btn text-white",
                    _onclick="ajax('{}',['usuarios'],':eval');".format(URL("switcheActivar",vars=dict(id_usuario=idusr)))),
                    _class="d-inline-block", _tabindex="0",_title="Activar", **{'data-toggle':"tooltip"})
    return salida
@auth.requires(lambda: auth.has_membership('Administradores') or auth.has_membership ('Super') )
def LstProveedores(proveedores=True):
    registrado  =db.tbl_cliente.id>0
    registrado &=db.tbl_cliente.proveedor==proveedores
    registrado=db(registrado).select(orderby=db.tbl_cliente.nombre)

    if proveedores:
        salida =TABLE(_class="table table-striped table-bordered", _id="tabla_proveedores")
        encabezado=THEAD(TR(TH("NIT"),TH("Proveedor"), TH("Correo Envio"),TH("Control",_align="right")))
    else:
        salida =TABLE(_class="table table-striped table-bordered", _id="tabla_empleados")
        encabezado=THEAD(TR(TH("Cedula"),TH("Nombre"), TH("Correo Envio"),TH("Control",_align="right")))

    cuerpo=TBODY()
    for item in registrado:

        if proveedores:
            nombre=item.nombre
        else:
            nombre=f"{item.id_usuario.first_name} {item.id_usuario.last_name}"

        btnactivo=fun_BotonActivo(item.is_active,item.id)
        btncorreo=SPAN(A(I(_class="fas fa-mail-bulk"), _class= "btn btn-sm btn-primary btn-circle btn text-white",
                        _onclick='''$('#DialModal').modal('show');
                                    ajax('{}',['usuario'],':eval');'''.format(URL("guardarCorreo",vars=dict(id_usuario=item.id))) ),
                    _class="d-inline-block", _tabindex="0",_title="Cambio Correo", **{'data-toggle':"tooltip"}
                    )

        if item.correo1:
            cuerpo.append(
                    TR(
                        TD(item.nit),
                        TD(nombre),
                        TD(item.correo1),
                        TD(DIV(btncorreo, "|" , DIV(btnactivo, _id=f"bntactivo_{item.id}", _name=f"bntactivo_{item.id}"), _class="row" ),
                            _align="right"),
                    ))

        else:

            cuerpo.append(
                    TR(
                        TD(item.nit),
                        TD(nombre),
                        TD("Sin Correo"),
                        TD(DIV(btncorreo, "|" , DIV(btnactivo, _id=f"bntactivo_{item.id}", _name=f"bntactivo_{item.id}"), _class="row" ),
                            _align="right"),
                        _class="alert alert-warning"
                    )

            )
    salida.append(encabezado)
    salida.append(cuerpo)
    return salida
#ajax
@auth.requires(lambda: auth.has_membership('Administradores') or auth.has_membership ('Super') )
def switcheActivar():
    id_usuario=request.vars.id_usuario
    consulta=db(db.tbl_cliente.id==id_usuario).select().first()
    salida="NADA --- {}".format(id_usuario)
    if consulta:
        estado = not (consulta.is_active)
        consulta.is_active=estado
        consulta.update_record()
        salida = fun_BotonActivo(estado, consulta.id)
        salida="$('#bntactivo_{}').html('{}');".format(consulta.id, XML(salida) )
    return salida

@auth.requires(lambda: auth.has_membership('Administradores') or auth.has_membership ('Super') )
def SubirPlano(archivo, proveedor,modulo):
    nrolinea=0
    archivo=open(archivo,"rb")
    inicio=True
    for linea in archivo.readlines():
        nrolinea +=1
        linea=linea.decode('latin-1')
        linea=linea.replace("\n","")
        linea=linea.replace("\r","")
        #partir campos
        if linea.find(',')>-1:
            linea=linea.split(",")
        elif linea.find(';')>-1:
            linea=linea.split(";")
        else:
            db.tbl_mensajes.insert(mensaje="Error achivo no es conpatible, No tiene los separadores de campo")
            break
        #Control lineas en blanco
        if len(linea[0].strip())==0:
            ##novedad.append([nrolinea,"Nombre en blanco", linea])
            continue
        #Control nit en blanco
        if len(linea[1].strip())==0:
            ##novedad.append([nrolinea,"NIT en blanco", linea])
            continue
        #Ajustar campos
        if len(linea)<6:
            for i in range(1,6-len(linea)):
                linea.append(None)
        #print (linea)
        if inicio and modulo==2:
            inicio=False
            continue    #oviar la primera linea.

        if modulo==2:   #empleados
            temp=linea[2].strip()
            temp=temp.split(" ")
            if len(temp)==4:
                apellido=f"{temp[0]} {temp[1]}"
                nombre=f"{temp[2]} {temp[3]}"
            elif len(temp)==3:
                apellido=f"{temp[0]} {temp[1]}"
                nombre=f"{temp[2]}"
            elif len(temp)==2:
                apellido=f"{temp[0]}"
                nombre=f"{temp[1]}"
            else:
                apellido=""
                nombre=linea[2]


            idusr=db(db.auth_user.username==linea[1].strip()).select(db.auth_user.id).first()
            if idusr:
                idusr=idusr.id
            else:   #Insertar Usuario
                idusr=db.auth_user.insert (first_name=nombre,
                                         last_name=apellido,
                                         username=linea[1].strip(),
                                         password=str(CRYPT(salt=True)(linea[1].strip())[0]),
                                         email=linea[3].strip()
                                         )
                #Adicion al grupo empleados
                db.auth_membership.insert(user_id=idusr,group_id=4)
            #Busca el cliente
            if db(db.tbl_cliente.nit==linea[1].strip()).isempty():
                db.tbl_cliente.insert(
                    id_usuario=idusr,
                    nombre=linea[2].strip(),
                    nit=linea[1].strip(),
                    correo1=linea[3].strip(),
                    proveedor=False,
                    tipodoc=linea[0].strip())
            else:
                consulta=db.tbl_cliente.nit==linea[1].strip()
                db(consulta).update(correo1=linea[3])
        else:
            if db(db.tbl_cliente.nit==linea[1]).isempty():
                idusr=db.auth_user.insert (first_name=linea[0],
                                         last_name=linea[1],
                                         username=linea[1],
                                         password=str(CRYPT(salt=True)(linea[1])[0]),
                                         email=linea[2]
                                         )
                db.tbl_cliente.insert(
                    id_usuario=idusr,
                    nombre=linea[0],
                    nit=linea[1],
                    correo1=linea[2],
                    correo2=linea[3],
                    correo3=linea[4],
                    proveedor=proveedor)
                #Adicion al grupo
                if proveedor:
                    db.auth_membership.insert(user_id=idusr,group_id=5)
                else:
                    db.auth_membership.insert(user_id=idusr,group_id=4)

            else:
                consulta=db.tbl_cliente.nit==linea[1]
                db(consulta).update(
                            correo1=linea[2],
                            correo2=linea[3],
                            correo3=linea[4],
                            )

                consulta=db(consulta).select(db.tbl_cliente.id_usuario).first()
                if consulta:
                    db(db.auth_user.id==consulta.id_usuario).update(email=linea[2])
                else:
                    db.tbl_mensajes.insert(mensaje="No actualiza usuario en login, por que no existe!!!", nivel=2)
    return

#ajax
@auth.requires(lambda: auth.has_membership('Administradores') or auth.has_membership ('Super') )
def guardarCorreo():
    idusuario = request.vars.id_usuario
    usuario = db(db.tbl_cliente.id==idusuario).select().first()
    if not usuario:
        return ("alert('no existe usuario!!!!');")

    salida=DIV()
    salida.append(fun_input("usuario","","idusr",'hidden',valor=usuario.id))
    salida.append(fun_input("correo1","Correo Pal.","usuario@dominio.com", valor=usuario.correo1))
    salida.append(fun_input("correo2","Copia Correo","usuario@dominio.com", valor=usuario.correo2))
    salida.append(fun_input("correo3","Copia Correo","usuario@dominio.com", valor=usuario.correo3))
    salida="$('#modalCuepo').html('{}');".format(XML(salida))
    salida+=f"$('#modalEncabezado').html('<CENTER>Correo de:<B>{usuario.nombre}</B></CENTER>');"
    botones =XML(A("Guardar",_class="btn btn-success text-white",
                _onclick="ajax('{}',['correo1','correo2','correo3'],':eval');".format(URL("GuardarCorreoFinal",vars=dict(idusr=usuario.id) ))
                ))
    botones +='<button type="button" id="bntcerrar" name=="bntcerrar" class="btn btn-secondary text-white" data-dismiss="modal">Cerrar</button>'
    salida+="$('#modalPie').html('{}');".format(botones)
    return salida
#ajax
@auth.requires(lambda: auth.has_membership('Administradores') or auth.has_membership ('Super') )
def GuardarCorreoFinal():
    correo1=request.vars.correo1
    correo2=request.vars.correo2
    correo3=request.vars.correo3
    idusr=request.vars.idusr
    print ("GuardarCorreoFinal",idusr)


    salida =None
    if not correo1:
        salida='''
                alert('Uno se ha ingresado el correo principal!!!');
                $('#correo1').focus();
                var p = $("#correo1").css("background-color", "yellow");
                p.hide(1500).show(1500);
                '''
    if salida: return salida
    #Valida correos
    if not es_correo_valido(correo1):
        salida='''
                alert('Correo no valido!!!');
                $('#correo1').focus();
                var p = $("#correo1").css("background-color", "yellow");
                p.hide(1500).show(1500);
                '''
    if salida: return salida
    if not es_correo_valido(correo2):
        salida='''
                $('#correo2').focus();
                var p = $("#correo2").css("background-color", "yellow");
                p.hide(1500).show(1500);
                '''
    elif not es_correo_valido(correo3):
        if salida:
            salida +='''var p = $("#correo3").css("background-color", "yellow");
                        p.hide(1500).show(1500);
                    '''
        else:
            salida='''
                $('#correo3').focus();
                var p = $("#correo3").css("background-color", "yellow");
                p.hide(1500).show(1500);
                '''

    usuario = db(db.tbl_cliente.id==idusr).select().first()
    salida=""
    if usuario:
        if correo1: usuario.correo1=correo1
        if correo2: usuario.correo2=correo2
        if correo3: usuario.correo3=correo3
        usuario.update_record()
        consulta  =db.tbl_recepcion.id_cliente==idusr
        consulta &=db.tbl_recepcion.estado=="C"
        recepcion=db(consulta).select().first()
        if recepcion:
            recepcion.update_record(estado="E")
        nit =usuario.nit
        nombre=usuario.nombre

        # datos='''['<input type="checkbox" name="selenvio" id="selenvio" value ="{}" checked />','{}','{}','{}','{}','{:,.0f}']'''.format(
        #         idusr, recepcion.nrodoc, recepcion.fecha, nit, nombre, recepcion.valor)
        salida='''
                $("#correo1").css("background-color", "white");
                $("#correo2").css("background-color", "white");
                $("#correo3").css("background-color", "white");
                $('#correo1').val("");
                $('#correo2').val("");
                $('#correo3').val("");
                $('#usuario').val("");
                $('#bntcerrar').click();
                alert('Modificacion realizada');
            '''
    else:
        salida="alert('Error no exite Proveedor !!!')"
    print (salida)
    return salida

#Ajax
@auth.requires(lambda: auth.has_membership('Administradores') or auth.has_membership ('Super') )
def formServer():
    id_server=request.vars.idserver or 0
    if int(id_server)==0:
        return DIV("No existe Configuracion!!", _class="alert alert-danger")
    consulta=db(db.tbl_parametros.id==id_server).select().first()
    salida=DIV(
            DIV(
                LABEL("Servidor",_class="form-control-label col-sm-1",_for="tbl_parametros_servidor_correo"),
                DIV(INPUT(_value=consulta.servidor_correo if consulta else "", _id="servidor_correo", _name="servidor_correo",_class="form-control string"),
                    _class="col-sm-5"),
                LABEL("Puerto",_class="form-control-label col-sm-1",_for="tbl_parametros_Puerto"),
                DIV(INPUT(_value=consulta.puerto if consulta else "", _id="puerto", _name="puerto",_class="form-control string"),
                    _class="col-sm-3"),
                DIV(INPUT(value=consulta.tls if consulta else False, _id="tls", _name="tls", _type="checkbox"),
                    LABEL("TLS",_class="form-control-label col-sm-1",_for="tbl_parametros_enviado_por"),
                    _class="col-sm-2"),
                _class="form-group row"),
            DIV(
                LABEL("Usuario",_class="form-control-label col-sm-1",_for="tbl_parametros_usuario"),
                DIV(INPUT(_value=consulta.usuario if consulta else "", _id="usuario", _name="usuario",_class="form-control string", requires=IS_NOT_EMPTY(error_message='¡Campo Requerido!')),
                    _class="col-sm-7"),
                LABEL("Password",_class="form-control-label col-sm-1",_for="tbl_parametros_password", requires=IS_NOT_EMPTY(error_message='¡Campo Requerido!')),
                DIV(INPUT(_value=consulta.password if consulta else "", _id="password", _name="password",_class="form-control string"),
                    _class="col-sm-3"),
                _class="form-group row"),
            DIV(
                LABEL("Enviado Por",_class="form-control-label col-sm-1",_for="tbl_parametros_enviado_por"),
                DIV(INPUT(_value=consulta.enviado_por if consulta else "", _id="enviado_por", _name="enviado_por",_class="form-control string", requires=IS_NOT_EMPTY(error_message='¡Campo Requerido!')),
                    _class="col-sm-4"),
                LABEL("Devolver",_class="form-control-label col-sm-2",_for="tbl_parametros_devolver"),
                DIV(INPUT(_value=consulta.devolver if consulta else "", _id="devolver", _name="devolver",_class="form-control string"),
                    _class="col-sm-5"),
                _class="form-group row"),
            DIV(
                LABEL("Asunto",_class="form-control-label col-sm-1",_for="tbl_parametros_asunto"),
                DIV(INPUT(_value=consulta.asunto if consulta else "", _id="asunto", _name="asunto",_class="form-control string", requires=IS_NOT_EMPTY(error_message='¡Campo Requerido!')),
                    _class="col-sm-11"),
                _class="form-group row"),
            DIV(
                LABEL("Cuerpo",_class="form-control-label col-sm-1",_for="tbl_parametros_cuerpo"),
                DIV(TEXTAREA( consulta.cuerpo if consulta else "", _id="cuerpo", _name="cuerpo",_class="form-control", requires=IS_NOT_EMPTY(error_message='¡Campo Requerido!')),
                    _class="col-sm-11"),
                _class="form-group row"),
            DIV(
                LABEL("Cuerpo HTML",_class="form-control-label col-sm-1",_for="tbl_parametros_cuerpohtml"),
                DIV(TEXTAREA( consulta.cuerpohtml if consulta else "", _id="cuerpohtml", _name="cuerpohtml",_class="form-control", requires=IS_NOT_EMPTY(error_message='¡Campo Requerido!')),
                    _class="col-sm-11"),
                _class="form-group row"),
            DIV(CENTER(A("Guardar",_class="btn btn-primary text-white",
                            _onclick="ajax('{}',['cuerpohtml','cuerpo','asunto','devolver','enviado_por','usuario','password','tls','puerto','servidor_correo'],':eval')".format(URL('GuardarServerCorreo',vars=dict(id_server=id_server)))))
                ),
            )
    return salida
# ajax desde formServer()
def GuardarServerCorreo():
    id_server=request.vars.id_server or None
    servidor_correo=request.vars.servidor_correo
    puerto=request.vars.puerto
    tls=request.vars.tls
    usuario=request.vars.usuario
    password=request.vars.password
    devolver=request.vars.devolver
    enviado_por=request.vars.enviado_por
    asunto=request.vars.asunto
    cuerpohtml=request.vars.cuerpohtml
    cuerpo=request.vars.cuerpo
    if id_server==None:        return('alert("Error grave idSever")')
    consulta=db(db.tbl_parametros.id==id_server).select().first()
    if consulta:
        consulta.servidor_correo=servidor_correo
        consulta.puerto=puerto
        consulta.tls=tls
        consulta.usuario=usuario
        consulta.password=password
        consulta.devolver=devolver
        consulta.enviado_por=enviado_por
        consulta.asunto=asunto
        consulta.cuerpohtml=cuerpohtml
        consulta.cuerpo=cuerpo
        consulta.update_record()
        salida="Registros Actualizados"
    else:
        db.tbl_parametros.insert(servidor_correo=servidor_correo,
                            puerto=puerto,
                            tls=tls,
                            usuario=usuario,
                            password=password,
                            devolver=devolver,
                            enviado_por=enviado_por,
                            asunto=asunto,
                            cuerpohtml=cuerpohtml,
                            cuerpo=cuerpo)
        salida="Registro Creado"

    return "alert('{}');".format(salida)

@auth.requires(lambda: auth.has_membership('Administradores') or auth.has_membership ('Super') )
def SubirEmpleados():
    subir_empleados = SQLFORM.factory(Field('archivo2', 'upload', label="Archivo de datos "))
    if subir_empleados.process().accepted:
        archivo=UNIR(request.folder,"uploads",subir_empleados.vars.archivo2)
        SubirPlano(archivo, False, modulo=2)
        redirect(URL("index.html",vars=dict(lugar=3)))
    return dict(subir_empleados=subir_empleados)

@auth.requires(lambda: auth.has_membership('Administradores') or auth.has_membership ('Super') )
def SubirProveedores():
    subir_formulario = SQLFORM.factory(Field('archivo1', 'upload', label="Archivo de datos"))
    if subir_formulario.process().accepted:
        archivo=UNIR(request.folder,"uploads",subir_formulario.vars.archivo1)
        novedad=SubirPlano(archivo, True, modulo=1)
        redirect(URL("index.html",vars=dict(lugar=2)))
    return dict(subir_formulario=subir_formulario)


#ajax
def funLstProveedores():
    proveedores=True#request.var.proveedores or True

    registrado  =db.tbl_cliente.id>0
    registrado &=db.tbl_cliente.proveedor==proveedores
    registrado=db(registrado).select(orderby=db.tbl_cliente.nombre)

    campos=[]
    for item in registrado:
        nombre=item.nombre

        btnactivo=fun_BotonActivo(item.is_active,item.id)
        btncorreo=SPAN(A(I(_class="fas fa-mail-bulk"), _class= "btn btn-sm btn-primary btn-circle btn text-white",
                        _onclick='''$('#DialModal').modal('show');
                                    ajax('{}',['usuario'],':eval');'''.format(URL("guardarCorreo",vars=dict(id_usuario=item.id))) ),
                    _class="d-inline-block", _tabindex="0",_title="Cambio Correo", **{'data-toggle':"tooltip"}
                    )

        campos.append((
                        item.nit,
                        nombre,
                        #item.tipodoc if item.tipodoc else "",
                        item.correo1 if item.correo1 else "",
                        #registro.correo2 if registro.correo2 else "" ,
                        #registro.correo3 if registro.correo3 else "",
                        (btnactivo,btncorreo)
                      )
                    )
    salida ={
                "data": campos,
                }
    return response.json(salida)

#ajax
def funLstEmpleados():
    proveedores=False
    registrado  =db.tbl_cliente.id>0
    registrado &=db.tbl_cliente.proveedor==proveedores
    registrado=db(registrado).select(orderby=db.tbl_cliente.nombre)

    campos=[]
    for item in registrado:
        nombre=item.nombre
        btnactivo=fun_BotonActivo(item.is_active,item.id)
        btncorreo=SPAN(A(I(_class="fas fa-mail-bulk"), _class= "btn btn-sm btn-primary btn-circle btn text-white",
                        _onclick='''$('#DialModal').modal('show');
                                    ajax('{}',['usuario'],':eval');'''.format(URL("guardarCorreo",vars=dict(id_usuario=item.id))) ),
                    _class="d-inline-block", _tabindex="0",_title="Cambio Correo", **{'data-toggle':"tooltip"}
                    )

        campos.append((
                        item.nit,
                        nombre ,
                        #item.tipodoc if item.tipodoc else "",
                        item.correo1 if item.correo1 else "",
                        #registro.correo2 if registro.correo2 else "" ,
                        #registro.correo3 if registro.correo3 else "",
                        (btnactivo,btncorreo)
                      )
                    )
    salida ={
                "data": campos,
                }
    return response.json(salida)
