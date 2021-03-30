# -*- coding: utf-8 -*-
db.define_table("tbl_modulo",
    Field("descripcion"),
    Field("ambiente"),
    Field("carpeta"),
    Field("busqueda",label="Texto de busqueda"),
    format="%(descripcion)s"
)
db.define_table('tbl_mensajes',
            Field('mensaje'),
            Field('visto','boolean',default=False),
            Field('nivel','integer',default=1),
            auth.signature
)

db.define_table('tbl_cliente',
            Field("id_usuario","reference auth_user"),
            Field('nombre'),
            Field('nit',unique=True),
            Field('correo1'),
            Field('correo2'),
            Field('correo3'),
            Field('proveedor','boolean',default=True),
            Field("tipodoc"),
            auth.signature,
            format="%(nombre)s"
)

db.define_table('tbl_recepcion',
            Field('id_cliente', 'reference tbl_cliente'),
            Field('nrodoc'),
            Field('valor', 'float', ),
            Field('estado',requires = IS_IN_SET({'C':'No Tiene Correo',
                                                'E':'Enviar',
                                                'Q':'Tarea SEgundo Plano',
                                                'F':'Finalizados',
                                                'T':"Finalizados Ver2"},
                                                zero=None)),
            Field('rutapdf'),
            Field("fecha","date"),
            Field("pagado","boolean"),
            Field("tipdoc","reference tbl_modulo"),#comporbante de egreso
            Field("fechaenvio","datetime"),
            Field("tarea","reference scheduler_task"),
            Field("fecha_hasta","date"),

            )

db.define_table("tbl_parametros",
                Field("servidor_correo",requires=IS_NOT_EMPTY(error_message='¡Campo Requerido!' )),
                Field("puerto","integer",requires=IS_NOT_EMPTY(error_message='¡Campo Requerido!') ),
                Field("usuario",requires=IS_NOT_EMPTY(error_message='¡Campo Requerido!') ),
                Field("password",requires=IS_NOT_EMPTY(error_message='¡Campo Requerido!') ),
                Field("tls","boolean",default=True),
                Field("enviado_por",requires=IS_NOT_EMPTY(error_message='¡Campo Requerido!') ),
                Field("asunto"),
                Field("devolver"),
                Field("cuerpo","text"),
                Field("cuerpohtml","text"),#,widget=ckeditor.widget),
                Field("id_modulo", "reference tbl_modulo"),
                )

# db.define_table("tbl_mensatareas",
#         Field("servidor_correo",requires=IS_NOT_EMPTY(error_message='¡Campo Requerido!' )),
#
#
# )
