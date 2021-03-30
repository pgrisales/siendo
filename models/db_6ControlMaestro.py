# -*- coding: utf-8 -*-
db.define_table("tbl_control_maestro",
    Field("descripcion"),
    Field("funcion"),
    Field("args"),
    Field('estado',requires = IS_IN_SET({'I':'Encolado',
                                          'A':"asignado",
                                         'E':'Error',
                                         'P':'Procesando',
                                         'F':'Finalizados'})),
    auth.signature,
    format="%(descripcion)s"
)

db.define_table("tbl_control_procg",
	Field("idmaestro","reference tbl_control_maestro"),
	Field("resultado")
	)