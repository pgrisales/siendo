# -*- coding: utf-8 -*-
#
@auth.requires(lambda: auth.has_membership('Administradores') or auth.has_membership ('Super') )
def index():
	links = [
		lambda row: A(XML('<span class="glyphicon glyphicon-user" aria-hidden="true"></span>'),
						'Usuarios',
						_class='btn  btn-xs btn btn-success',
						_id="lst_usuarios",
						_href= URL('lst_usuarios',vars=dict(idgrupo=row.id), user_signature=True)
						#callback=URL('lst_usuarios',vars=dict(idgrupo=row.id), user_signature=True),
						#target="resultado"
					 )
		]
	db.auth_group.id.readable=False
	db.auth_group.role.writable=False
	formulario=SQLFORM.grid(db.auth_group.id>1,
						maxtextlength=120,
						deletable=False,
						editable=True,
						details=False,
						create=False,
						csv=False,
						links=links,
						user_signature=True
		)
	botones=DIV(A(I(_class="fas fa-user-plus  fa-2x"),"|","Adicionar Usuario",_class="btn btn-success text-white",
					_onclick="fun_llamar();"),"|",
				A(I(_class="fas fa-users-cog fa-2x"),"|","Administrar Usuario",_class="btn btn-primary text-white",
								_href="adminusers")
				 )

	return locals()

@auth.requires(lambda: auth.has_membership('Administradores') or auth.has_membership ('Super') )
def adminusers():
	db.auth_user.username.writable=False
	db.auth_user.id.readable=False

	consulta=db.auth_user.id>1
	formulario=SQLFORM.grid(consulta,
					maxtextlength=120,
					deletable=False,
					editable=True,
					details=False,
					create=False,
					csv=False,
					user_signature=True
	)
	return dict(formulario=formulario)

@auth.requires(lambda: auth.has_membership('Administradores') or auth.has_membership ('Super') )
def fun_Grupos(columnas=3):
	consulta=db(db.auth_group.id>1).select()
	salida=DIV(_class="row")

	for item in consulta:
		salida.append(DIV(INPUT (_id="grp_activos",_name="grp_activos",_type="checkbox",
									_value=item.id, value=False),
						  	item.role,
						  	_class="col-md-{}".format(12/columnas)))
	return salida

#ajax
@auth.requires(lambda: auth.has_membership('Administradores') or auth.has_membership ('Super') )
def AddUsuario():
	salida=DIV()
	salida.append(fun_input("nombres","Nombres","Nombres"))
	salida.append(fun_input("apellidos","Apellidos","Apellidos"))
	salida.append(fun_input("correo","correo","usuario@dominio.com"))
	salida.append(fun_input("usuario","Usuario","Nombre de usuario"))
	salida.append(fun_input("clave","Contraseña","","password"))
	salida.append(fun_Grupos())
	salida="$('#modalCuepo').html('{}');".format(XML(salida))
	salida+="$('#modalEncabezado').html('Nuevo Usuario');"

	botones =XML(A("Guardar",_class="btn btn-success text-white", _onclick="ajax('{}',['nombres','apellidos','correo','usuario','clave','grp_activos'],':eval');".format(URL("GuardarUsuario"))))
	botones +='<button type="button" id="bntcerrar" name=="bntcerrar" class="btn btn-secondary text-white" data-dismiss="modal">Cerrar</button>'
	salida+="$('#modalPie').html('{}');".format(botones)
	return salida

def errorCampo(campo, mensaje):
	salida=f'''
		alert('{mensaje}');
        $('#{campo}').focus();
    	var p = $('#{campo}').css('background-color', 'yellow');
        p.hide(1500).show(1500);
		'''
	return salida

@auth.requires(lambda: auth.has_membership('Administradores') or auth.has_membership ('Super') )
def GuardarUsuario():
	nombre=request.vars.nombres
	apellidos=request.vars.apellidos
	correo=request.vars.correo
	usuario=request.vars.usuario
	clave=request.vars.clave
	grupos=request.vars.grp_activos
	usuario=usuario.strip() if usuario != None else ""

	if not nombre:		return errorCampo ('nombres', "Falta nombre!!")
	if not apellidos:	return errorCampo ('apellidos', "Falta apellido!!")
	if not correo:		return errorCampo ('correo', "Falta correo!!")
	if not usuario:		return errorCampo ('usuario', "Falta usuario!!")
	if not clave:		return errorCampo ('clave', "Falta clave!!")

	consulta=db(db.auth_user.username==usuario).select()
	if consulta:
		return errorCampo ('usuario', "Usuario ya fue registrado!!!!")

	idusr=db.auth_user.insert(first_name=nombre,
						last_name=apellidos,
						email=correo,
						username=usuario,
						password=str(CRYPT(salt=True)(clave)[0])

						)

	if isinstance(grupos,str):
		grupos=[grupos]

	for grupo in grupos:
		db.auth_membership.insert(user_id=idusr, group_id=grupo)

	return "alert('Usuario regisrado..');$('#bntcerrar').click();"

@auth.requires(lambda: auth.has_membership('Administradores') or auth.has_membership ('Super') )
def lst_usuarios():
	idgrupo= request.vars.idgrupo or redirect(URL("index"))
	nombregrupo=db(db.auth_group.id==idgrupo).select(db.auth_group.role).first()
	consulta=db(db.auth_membership.group_id==idgrupo).select()
	db.auth_membership.id.readable=False
	db.auth_membership.group_id.readable=False

	formulario=TABLE(THEAD(TR(TH("Nombre (apellido o Nit)"),TH("Nombre Usuario"),TH("Control"))),
						_class="table", _name="tabla_grupo", _id="tabla_grupo")
	cuerpo=TBODY()
	for item in consulta:
		cuerpo.append( TR( 	TD(f"{item.user_id.first_name} {item.user_id.last_name}"),
							TD(item.user_id.username),
							TD(A(SPAN("",_class="icon trash icon-trash glyphicon glyphicon-trash"),
								"Remover",_class="btn btn-warning text-white",
								_onclick="ajax('{}',['idusr'],':eval');".format(URL('GrupoRemover',vars=dict(idgrupo=item.id)))
								),
							),
							_id=f"f_grupo-{item.id}",_name=f"f_grupo-{item.id}"
							))
	formulario.append(cuerpo)

	#consulta =db.auth_membership.group_id!=idgrupo
	#consulta &=db.auth_user.id == db.auth_membership.user_id
	#consulta=db(consulta).select(db.auth_user.id, db.auth_user.first_name,db.auth_user.last_name,db.auth_user.email)
	sql=f"SELECT id, first_name, last_name, email FROM auth_user  WHERE id not in (SELECT user_id FROM auth_membership where group_id={idgrupo})"
	consulta = db.executesql(sql)
	usuarios_reg=TABLE(THEAD(TR(TH(""),TH("Nombre (apellido o Nit)"),TH("Correo"))),
						_class="table", _name="tabla_usuarios", _id="tabla_usuarios")
	cuerpo=TBODY()
	for item in consulta:
		if item[0]==1: continue
		cuerpo.append( TR( TD(INPUT(_type="checkbox", _value=item[0], _id="id_usuario", _name="id_usuario")),
							TD(f"{item[1]} {item[2]}"),TD(item[3]),
							_id=f"f_entrada-{item[0]}",_name=f"f_entrada-{item[0]}"
							))
	usuarios_reg.append(cuerpo)
	usuarios_reg=DIV(P(A("Adicionar", _class="btn btn-success text-white",_id="btn_adicionar",
	 					_onclick="$('#btn_adicionar').text('Procesando...');ajax('{}',['id_usuario'],':eval');".format(URL('GrupoAdd',vars=dict(idgrupo=idgrupo))))),
					usuarios_reg)

	return locals();
#AJAX
@auth.requires(lambda: auth.has_membership('Administradores') or auth.has_membership ('Super') )
def GrupoRemover():
	usuario = request.vars.idgrupo or None
	if usuario ==None : return "alert('Usuario(s) no seleccionado(s)');"

	consulta =db.auth_membership.id==usuario

	datos=db(consulta).select().first()
	selector=XML(INPUT(_type="checkbox", _value=datos.user_id, _id="id_usuario", _name="id_usuario"))
	nombre=f"{datos.user_id.first_name} {datos.user_id.last_name}"

	salida ='''tabla_grupo.row( $('#f_grupo-{}') ).remove().draw();tabla_usuarios.row.add(['{}','{}','{}']).node().id = 'f_entrada-{}';
				tabla_usuarios.draw(false);
	'''.format(usuario, selector, nombre, datos.user_id.email,datos.user_id)

	db(consulta).delete()
	return (salida)
#ajax
@auth.requires(lambda: auth.has_membership('Administradores') or auth.has_membership ('Super') )
def GrupoAdd():
	usuario = request.vars.id_usuario or None
	idgrupo=request.vars.idgrupo or None
	if usuario==None: return "$('#btn_adicionar').text('Adicionar');alert('No se ha seleccionado Usuario!!!');"
	if idgrupo==None: return "$('#btn_adicionar').text('Adicionar');alert('Error Grave no existe grupo!!!');"
	grupoadd=db.auth_membership.insert(group_id=idgrupo, user_id=usuario)
	consulta=db(db.auth_user.id==usuario).select().first()


	nombre=f'{consulta.first_name} {consulta.last_name}'
	bntremover=XML(A(SPAN("",_class="icon trash icon-trash glyphicon glyphicon-trash"),
					"Remover",_class="btn btn-warning text-white",
					_onclick="ajax('{}',['idusr'],':eval');".format(URL('GrupoRemover',vars=dict(idgrupo=grupoadd)))
					))

	salida ='''tabla_usuarios.row( $('#f_entrada-{}') ).remove().draw();
                tabla_grupo.row.add(['{}','{}']).node().id = 'f_grupo-{}';
                tabla_grupo.draw(false);
				$('#btn_adicionar').text('Adicionar');
				'''.format(usuario,nombre,bntremover,grupoadd.id)
	return salida

@auth.requires(lambda: auth.has_membership('Administradores') or auth.has_membership ('Super') )
def controlusuario():
	import f2s_paginador
	if not request.vars.f2s_orden_arriba :request.vars.f2s_orden_arriba=1
	if not request.vars.f2s_ordenar :request.vars.f2s_ordenar="auth_user.username"
	campos=[
		db.auth_user.id,
		db.auth_user.first_name,
		db.auth_user.last_name,
		db.auth_user.email,
		db.auth_user.username,
		db.auth_user.is_active
	  ]
	db.auth_user.is_active.represent=lambda r: "Activo" if r else "Inactivo"

	titulos=["Nombre","apellidos",
			"correo","Usuario","activo"]

	links = [
               lambda registro: A (SPAN(" ",_class="icon pen icon-pencil glyphicon glyphicon-pencil"),
               							"Editar",_href=URL("EditarUsuario",
               												vars= dict(usuario=registro.id)),
               						_class="btn btn-primary"),
               ]

	pagina_actual=request.vars.pagina or 1
	consulta=db.auth_user.id>1
	formulario=DIV()
	vertodos=None
	formulario.append( f2s_paginador.Fun_Grilla(db,consulta,campos = campos,
												  titulos= titulos,
												  #ordenar= ["auth_user.username"],
												links=links,
											  	busqueda=[ 	{"ayuda":"Nombres","campo":db.auth_user.first_name},
                                                        	{"ayuda":"Apellidos","campo":db.auth_user.last_name},
                                                        	{"ayuda":"Nombre Usuario","campo":db.auth_user.username},

                                                              ],
												  )
	)

	return dict(formulario=formulario)

@auth.requires(lambda: auth.has_membership('Administradores') or auth.has_membership ('Super') )
def EditarUsuario():
	iduser=request.vars.usuario
	grupos=formGrupos(iduser)
	formulario=DIV(DIV(	DIV(
							DIV(SPAN(" ",_class="glyphicon glyphicon-user", _style="font-size: 18pt"),
								" Informacion Usuario",_class="panel-heading"),
							DIV(formUsuario(iduser),_class="panel-body"),
							_class="panel panel-primary"),
						_class="col-md-7"),
					_class="row")
	formulario.append(DIV(DIV(DIV(SPAN(" ",_class="glyphicon glyphicon-th-list", _style="font-size: 18pt"),
								" Grupos Seleccionados",_class="panel-heading"),
								DIV(formGrupos(iduser),_class="panel-body"),
							_class="panel panel-primary"),
						_class="col-md-5"))
	formulario=FORM(formulario,
					#INPUT(_value=iduser, _hidden=True, _name="iduser"),
					INPUT(_type="submit", _value="Modificar"),
					#_action=URL('modificarusr')
					)
	formulario.add_button('Volver', URL('ctlusuario'))
	if formulario.process().accepted:
		grupos    = request.vars.grp_activos
		nombre    = request.vars.nombre
		apellido  = request.vars.apellido
		correo    = request.vars.correo
		usuario   = request.vars.nomusuario
		habilitado= request.vars.habilitado
		db(db.auth_user.id==iduser).update(first_name=nombre,
										last_name=apellido,
										username=usuario,
										email=correo,
										)
		#Borrar el asocio de los usuarios y grupo
		db(db.auth_membership.user_id==iduser).delete()
		#registration_key="disabled"
		if habilitado==None:
			db(db.auth_user.id==iduser).update(is_active=False, registration_key="disabled")
		else:
			db(db.auth_user.id==iduser).update(is_active=True, registration_key="")
			#Registar el nuevo grupo
			if not isinstance (grupos,list):grupos=[grupos]
			for id_grupo in grupos:
				if id_grupo:
					db.auth_membership.insert(user_id=iduser, group_id=id_grupo)

		session.flash="Usuario Modifcado"
		redirect(URL(EditarUsuario,vars=dict(usuario=iduser)))

	return dict(formulario=formulario,var_desarrollo=False)

@auth.requires(lambda: auth.has_membership('Administradores') or auth.has_membership ('Super') )
def formGrupos(iduser):
	columnas=3
	consulta=db(db.auth_membership.user_id==iduser).select()
	selecciones=[]
	encontrado=[]
	for item in consulta:

		selecciones.append(DIV(INPUT (_id="grp_activos",_name="grp_activos",_type="checkbox",
									_value=item.group_id, value=True),
						  	item.group_id.role,
						  	_class="col-md-{}".format(12/columnas)))
		encontrado.append(item.group_id)
	consulta1=db(db.auth_group.id>0).select()
	for item in consulta1:
		if item.id==1:continue
		if item.id in encontrado:continue
		selecciones.append(DIV(INPUT (_id="grp_activos",_name="grp_activos",_type="checkbox",
									_value=item.id, value=False),
						  	item.role,
						  	_class="col-md-{}".format(12/columnas)))


	salida=DIV()
	fila=DIV(_class="row")
	columna=0
	for item in selecciones:
		columna+=1
		fila.append(item)
		if columna ==columnas:
			columna=0
			salida.append(fila)
			fila=DIV(_class="row")

	return salida

@auth.requires(lambda: auth.has_membership('Administradores') or auth.has_membership ('Super') )
def formUsuario(iduser):
	consulta=db(db.auth_user.id==iduser).select().first()
	contenido=TABLE(_class="table")
	contenido.append(TR(TD("Creado por:"),TD(consulta.created_by.username if consulta.created_by else ""),
						TD("Fecha Creación"),TD(consulta.created_on if consulta.created_on else "" )))
	contenido.append(TR(TD("Modificado por:"),TD(consulta.modified_by.username if consulta.modified_by else "" ),
						TD("Fecha Modificación"),TD(consulta.modified_on if consulta.modified_on else "")))
	contenido.append(TR(TD("Nombres"),TD(INPUT(_id="nombre", _name="nombre", _value=consulta.first_name,  requires=IS_NOT_EMPTY())),
						TD("Apellidos",TD(INPUT(_id="apellido",_name="apellido",_value=consulta.last_name,  requires=IS_NOT_EMPTY())))))
	contenido.append(TR(TD("Correo"),TD(INPUT(_id="correo",_name="correo",_value=consulta.email,  		requires=IS_NOT_EMPTY()),
						TD("Usuario"),TD(INPUT(_id="nomusuario",_name="nomusuario",_value=consulta.username, 	requires=IS_NOT_EMPTY())))))
	contenido.append(TR(TD("Cambio de Clave"),TD(INPUT(_value="", _id="nuevaclave", _name="nuevaclave", requires=IS_NOT_EMPTY()))))
	contenido.append(TR(TD("Habilitado"),TD(INPUT(_id="habilitado",_name="habilitado",_type="checkbox",value=consulta.is_active))))

	return contenido
