# -*- coding: utf-8 -*-
# ---
MODULO=2


@auth.requires(lambda: auth.has_membership ('Gerencia') or auth.has_membership('Administradores') or auth.has_membership ('Super') )
def index():
    if len(request.args)>0:
        MODULO=request.args[0]
    print('Modulo:', MODULO)
    posicion_tab=request.vars.posicion_tab or 1
    tarea=0
    modulos=db(db.tbl_modulo.id==MODULO).select().first()
    if modulos==None:
        raise HTTP(400)
    bntEnvio=DIV(A("Envio Correo",_class="btn btn-success",
                _onclick="ajax('{}',['selenvio'],':eval');".format(URL(('enviocorreo')))
            ),"|",A("No Envio",_class="btn btn-danger",
                _onclick="ajax('{}',['selenvio'],':eval');".format(URL(('noenviocorreo'))))
            )

    pendientes=fun_pendiente("C","Pendientes sin Correo","bg-danger", "tabla_sincorreo")
    envios=fun_pendiente("E","Pendientes para envio Correo","bg-primary","tabla_pendiente", bntEnvio)
    BtnGuardar=A("Guardar", _class="btn btn-primary",
                _onclick="ajax('{}',['btnusr','correo1', 'correo2', 'correo3'],':eval');$('#cmbMail').modal('hide');".format(URL('guardarCorreo') )
                )

    form_enviados=(DIV(   LABEL("Fecha Inicial", _class="col-sm-1 col-form-label"),
                                DIV(INPUT(_type="date",_class="form-control", _id="fecha_inicio",
                                _name="fecha_inicio"),_class="col-sm-2"),
                                LABEL("Fecha Final", _class="col-sm-1 col-form-label"),
                                DIV(INPUT(_type="date",_class="form-control", _id="fecha_final",
                                _name="fecha_final"),_class="col-sm-2"),
                                LABEL("NIT/Proveedor", _class="col-sm-1 col-form-label"),
                                DIV(INPUT(_class="form-control", _id="nit_correo",
                                _name="nit_correo"),_class="col-sm-2"),
                                A("Buscar",_class="btn btn-success",
                                _onclick="ajax('{}',['fecha_inicio','fecha_final','nit_correo'],'resultenviados');".format(URL("BuscarCorreoEnviado"))
                                ),
                        _class="form-group row")
                        )

    formulario = SQLFORM.factory(Field('archivo', 'upload', label="Archivo de datos"))
    if formulario.process().accepted:
        response.flash = 'formulario aceptado'

        verificar,msgerror =Verificar(formulario.vars.archivo)

        if verificar:
            tarea=db.tbl_control_maestro.insert(
                descripcion="Subir Archivo de Nomina",
                funcion="Crear Pdf",
                args="{" + f"'archivo': '{formulario.vars.archivo}','modulo':{MODULO}, " + "}",
                estado= 'I')

    elif formulario.errors:
        response.flash = 'el formulario tiene errores'


    return locals() #dict(formulario=formulario)

def Verificar(archivo):
    from os.path import join as UNIR
    archivo=UNIR(request.folder,"uploads",archivo)
    print ('Verificar:', archivo)
    msgerror=False
    arch=open(archivo,"rb")
    datos=arch.read(500)
    arch.close()
    salida=False
    datos=datos.decode("latin-1")
    #Modificacion lectura de PDF
    if datos.find ('%PDF')==0: return True, None
    #######----####

    if MODULO==1:       #Comprobantes de ingresos
        control=['|    PAGO ELECTRONICO   |', "|COMPROBANTES DE EGRESOS|"]
        for item in control:
            if datos.find(item)>-1:
                salida=True
            else:
                db.tbl_mensajes.insert(mensaje=f"Archivo:[{formulario.vars.archivo}] no es un Comprobante de egreso!")
                msgerror=f"Archivo:[{formulario.vars.archivo}] no es un Comprobante de egreso!"




    return salida, msgerror

#ajax
def BuscarCorreoEnviado():
    return (BuscarEnClientes(1))


def guardarCorreo():
    correo1=request.vars.correo1
    correo2=request.vars.correo2
    correo3=request.vars.correo3
    idusr  =request.vars.btnusr
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

    recepcion = db(db.tbl_recepcion.id==idusr).select().first()
    salida=""
    if recepcion:
        cliente=db(db.tbl_cliente.id==recepcion.id_cliente).select().first()

        print (recepcion,cliente)

        if not cliente : return("alert('error grave no existe cliente!!!!');")
        if correo1: cliente.correo1=correo1
        if correo2: cliente.correo2=correo2
        if correo3: cliente.correo3=correo3
        cliente.update_record()
        recepcion.estado="E"
        recepcion.update_record()
        db(db.auth_user.id==cliente.id_usuario).update(email=correo1)
        nit =cliente.nit
        nombre=cliente.nombre

        boton=SPAN ( A(I(" ",_class="far fa-file-pdf"),_class="btn btn-sm btn-danger btn-circle  text-white",
                    _onclick="ajax('{}',['superid'],':eval');$('#visorPDF').modal('show');".format(URL("verpdf",vars=dict(idpdf=idusr)))),
                _class="d-inline-block", _tabindex="0",_title="Ver Docmento", **{'data-toggle':"tooltip", "data-placement":"top"})

        datos='''['<input type="checkbox" name="selenvio" id="selenvio" value ="{}" checked />','{}','{}','{}','{}','{:,.0f}','{}']'''.format(
                idusr, recepcion.nrodoc, recepcion.fecha, nit, nombre, recepcion.valor,boton)
        salida='''
                $("#correo1").css("background-color", "white");
                $("#correo2").css("background-color", "white");
                $("#correo3").css("background-color", "white");
                $('#correo1').val("");
                $('#correo2').val("");
                $('#correo3').val("");
                tabla_sincoreo.row( $('#fila_c-{0}') ).remove().draw();
                tabla_pendiente.row.add({1}).node().id = 'fila_e-{0}';
                tabla_pendiente.draw(false);
            '''.format(idusr,datos)

    else:
        salida="alert('Error no exite Proveedor !!!')"
    return salida

def fun_pendiente(estado,titulo,color="bg-primary",idtabla="",botones=None):
    consulta=db.tbl_recepcion.estado==estado
    consulta&=db.tbl_recepcion.tipdoc==1

    consulta = db(consulta).select(orderby=db.tbl_recepcion.estado)
    if consulta==None:
        return ""

    tabla=TABLE(_class="table table-striped table-bordered",_name=idtabla, _id=idtabla)

    if estado == "E":
        tabla.append (THEAD(TR(
                        TH(),TH("Nro.Doc"),TH("Fecha"),TH("NIT"),TH("Nombre Proveedor"),TH("Valor"),TH("Accion")
                        )))
    elif estado == "C":
        tabla.append (THEAD(TR(
                    TH("Nro.Doc"),TH("Fecha"),TH("NIT"),TH("Nombre Proveedor"),TH("Valor"),
                    TH("Accion")
                    )))

    cuerpo=TBODY()
    for item in consulta:
        if item.estado == "E":
            cuerpo.append(TR(
                            TD(INPUT(_type='checkbox', _name='selenvio', _id="selenvio", _value=item.id, value=True)),
                            TD(item.nrodoc),
                            TD(item.fecha),
                            TD(item.id_cliente.nit),
                            TD(item.id_cliente.nombre),
                            TD("{:,.0f}".format(item.valor),_align="right"),
                            TD(
                                SPAN (
                                        A(  I(" ",_class="far fa-file-pdf"),
                                            _class="btn btn-sm btn-danger btn-circle  text-white",
                                            _onclick='''ajax('{}',['superid'],':eval');
                                                    $('#visorPDF').modal('show');'''.format(URL("verpdf",vars=dict(idpdf=item.id)))
                                        ),
                                        _class="d-inline-block", _tabindex="0",_title="Ver Docmento",
                                        **{'data-toggle':"tooltip", "data-placement":"top"})
                            ),
                            _id=f"fila_e-{item.id}", _name=f"fila_e-{item.id}",_align="center"
                            ))
        elif item.estado =="C":
            cuerpo.append(TR(
                    TD(item.nrodoc),
                    TD(item.fecha),
                    TD(item.id_cliente.nit),
                    TD(item.id_cliente.nombre),
                    TD("{:,.0f}".format(item.valor),_align="right"),
                    TD(
                        SPAN (
                                A(  I(" ",_class="far fa-file-pdf"),
                                    _class="btn btn-sm btn-danger btn-circle  text-white",
                                    _onclick='''ajax('{}',['superid'],':eval');
                                            $('#visorPDF').modal('show');'''.format(URL("verpdf",vars=dict(idpdf=item.id)))
                                ),
                                _class="d-inline-block", _tabindex="0",_title="Ver Docmento",
                                **{'data-toggle':"tooltip", "data-placement":"top"}),
                        "|",
                        A(I(_class="fas fa-envelope-open-text"),"Adicionar Correo", _class="btn btn-warning",
                         _onclick= "instertarmail('{}', '{}');".format(item.id, item.id_cliente.nombre)
                        ),
                    ),
                    _id=f"fila_c-{item.id}", _name=f"fila_c-{item.id}",)
                )
    tabla.append(cuerpo)
    tabla=DIV(DIV(H4(CENTER(titulo), botones if botones else "",_class="text-white"), _class="card-header {}".format(color)),
            DIV(tabla, _class="card-body"),
                _class="card table-responsive")
    salida =XML(tabla)
    return salida

#ajax
def ReenvioCorreo():
    idrecepcion=request.vars.id_recepcion or None
    if not idrecepcion: return "alert('Error ReenvioCorreo, No se ingreso indice');"
    consulta=db(db.tbl_recepcion.id==idrecepcion).select().first()
    if not consulta: return "alert('Error, registro no encontrado');"
    salida=DIV()
    salida.append(fun_input("remail1","Email Principal","email@domininio.com",tipo="email", valor=consulta.id_cliente.correo1))
    salida.append(fun_input("remail2","Email Copia"    ,"email@domininio.com",tipo="email", valor=consulta.id_cliente.correo2))
    salida.append(fun_input("remail3","Email Copia","email@domininio.com",tipo="email", valor=consulta.id_cliente.correo3))
    salida.append(fun_input("cambiar","Modificar el correos?",tipo="checkbox"))
    salida="$('#modalCuepo').html('{}');".format(XML(salida))
    salida+="$('#modalEncabezado').html('Reenvio Correo');"
    botones =XML(A("Reenviar",_class="btn btn-success text-white", _onclick="ajax('{}',['remail1','remail2','remail3','cambiar'],':eval');".format(URL("ReenvioCorreoGuadar",vars=dict(idrecepcion=idrecepcion)))))
    botones +='<button type="button" id="bntcerrar" name=="bntcerrar" class="btn btn-secondary text-white" data-dismiss="modal">Cerrar</button>'
    salida+="$('#modalPie').html('{}');".format(botones)
    return salida

#ajax ^
def ReenvioCorreoGuadar():
    idrecepcion=request.vars.idrecepcion or None
    correo1=request.vars.remail1 or None
    correo2=request.vars.remail2 or None
    correo3=request.vars.remail3 or None
    cambiar=request.vars.cambiar or  None
    salida=""

    if correo1==None or es_correo_valido(correo1)==False:
        salida= '''alert('Uno se ha ingresado el correo principal !!!');
                        $('#remail').focus();
                        var p = $('#remail').css("background-color", 'yellow');
                        p.hide(1500).show(1500);'''

    consulta=db(db.tbl_recepcion.id==idrecepcion).select().first()
    if cambiar:
        cliente=db(db.tbl_cliente.id==consulta.id_cliente).select().first()
        cliente.update_record(correo1=correo1)
        if es_correo_valido(correo2):            cliente.update_record(correo2=correo2)
        if es_correo_valido(correo3):            cliente.update_record(correo3=correo3)
        db.commit()

    paraserver=VerificarModulo("comprobante.amb")
    tarea = planificador.queue_task(fun_EnviarCorreo,
                                    pvars=dict(envio = idrecepcion, correo=correo1, paraserver=paraserver),#paraserver = Parametro servidor o Modulo...!
                                    timeout = 360)


    if tarea:
        consulta.tarea=tarea.id
        consulta.update_record()
        salida+=f"alert('Proceso encolado:{tarea.id}');"

    return XML(salida)
#ajax
def enviocorreo():
    envios=request.vars.selenvio
    if isinstance(envios,str):
        envios=[envios]
    salida =""
    for envio in envios:
        tarea = planificador.queue_task(fun_EnviarCorreo,
                                        pvars=dict(envio = envio),
                                        timeout = 360)
        salida +='''tabla_pendiente.row( $('#fila_e-{}') ).remove().draw();'''.format(envio)
        consulta=db(db.tbl_recepcion.id==envio).select().first()
        #print ("compegreso.enviocorreo:",consulta)
        if consulta:
            print ("Tarea:", tarea)
            consulta.tarea=tarea.id
            consulta.update_record()
    return salida


#ajax
def estadosubir():
    tarea=request.vars.tarea or None
    salida = F2s_Estado(tarea)
    return salida


#ajax
def verpdf():
    '''verpdf entrega el archivo pdf en stream para se visualido en pantalla'''
    id_recepccion=request.vars.idpdf
    salida = F2s_VerPDF(id_recepccion)
    return salida

#ajax
def noenviocorreo():
    envios=request.vars.selenvio
    if isinstance(envios,str):
        envios=[envios]
    salida =""
    if envios==None: return("alert('No se ha Seleccionado documento');")
    #return("alert('{}');".format(envios[0]))

    for envio in envios:
        db(db.tbl_recepcion.id==envio).update(estado="T",fechaenvio=request.now)
        salida +='''tabla_pendiente.row( $('#fila_e-{}') ).remove().draw();'''.format(envio)
    return salida
