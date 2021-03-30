# -*- coding: utf-8 -*-
db.define_table("tblfac_tipocampo",
    Field("tipo"),
    Field("descripcion"),
    format="%(descripcion)s"
)
