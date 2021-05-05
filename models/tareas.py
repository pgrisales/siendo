# -*- coding: utf-8 -*-
from os.path import join as JOIN
from os import remove as REMOVE
IDMODULO=""
def VerificarModulo(modulo):
    #Anterior mente el modulo se verifica con el id pero se cambia al
    #nombre del ambiente para buscar el id
    if isinstance( modulo,(int,float)):return modulo
    if not isinstance(modulo, str):return None
    #Busca el nombre del modulo por el ambiente:
    buscar = db(db.tbl_modulo.ambiente==modulo).select(db.tbl_modulo.id).first()
    salida=None
    if buscar: salida = buscar.id
    return salida

def VerificarCliente(nit, nombre):
    cliente =db(db.tbl_cliente.nit==nit).select().first()
    correo=None
    if not cliente:#no Existe el Nit se crea el usuario y Cliente
        print("se crear por que no exites nit")
        user_id=db.auth_user.insert(first_name=nombre,
                last_name=nit,
               username=nit,
               password=str(CRYPT(salt=True)(nit)[0])
                )
        db.commit()
        id_cliente=db.tbl_cliente.insert(  nit=nit,
                            nombre=nombre,
                            id_usuario=user_id,
                            proveedor=False
                        )
        db.commit()
    else:   #Datos del cliente
        id_cliente=cliente.id
        correo=cliente.correo1

    print("id_cliente:",id_cliente)
    return id_cliente, correo

def RegistroRecepcion (idcliente, nrodoc, valor, fecha, correo, nombrepdf,modulo):
    #Si tiene correo lo coloca en estado para enviar= E
    estado= 'E' if correo  else "C"
    print (f"crear recepcion en estado {estado}")
    #si el nrodoc esta registrado no se actualiza.
    if not  db(db.tbl_recepcion.nrodoc==nrodoc).isempty():
        #Falta borrar el pdf creado
        ruta=JOIN(request.folder,'static','PDF',nombrepdf)
        print ('borrar', ruta)
        try:
            REMOVE(ruta)
        except Exception as e:
            print (e)
        return True

    print (valor)

    #Esta ruta no tiene la direccion de la app
    db.tbl_recepcion.insert(id_cliente=idcliente,
                        nrodoc=nrodoc,
                        valor=valor,
                        rutapdf='PDF/'+nombrepdf,
                        fecha=fecha,
                        #fecha_hasta=campo["Fecha_Hasta"] if "Fecha_Hasta" in campo else "" ,
                        estado=estado,
                        tipdoc=modulo,
                    )
    db.commit()




def GenerarPDF(archivo, modulo, fecha_arreglo=None):
    #gGuarda la generacion de pdf en Web2py
    from os import makedirs
    from os.path import isdir
    from os.path import isfile
    from os import remove as BORRAR
    from os.path import join as UNIR
    from os.path import split as PARTIR
    from shutil import move as MOVER

    from SimpleSoft.Facil 			import ObjFacil
    from SimpleSoft.F2S_filascol 	import ObjFilas

    modulo = VerificarModulo(modulo)

    #print (f"modulo {modulo}")
    #print (f'archivo {archivo}')

    novedad=[]

    idmodulo=db(db.tbl_modulo.id==modulo).select().first()
    rutarecursos=UNIR(request.folder,"trabajo")
    archivo=UNIR(request.folder,"uploads",archivo)

    ob=ObjFacil( rutarecursos )
    ob.AbrirAmbiente(idmodulo.ambiente)
    print (ob.encabezado['modo'],archivo,rutarecursos)


    if ob.encabezado['modo']==4:
        docuementos  = ProcesarEntradaPDF(rutarecursos, archivo, ob.encabezado)
        print ('siguiente')
        for campo in docuementos:
            print (campo)
            idcliente, correo =VerificarCliente(campo['nit'] ,campo['entregadoa'])
            RegistroRecepcion (idcliente, campo['nrodoc'], campo['valor_total'],
                         campo['fecha'], correo, campo['nombrepdf'] ,idmodulo)


        return 'Generando pdf'


    obFilasCol=ObjFilas(ob, rutarecursos)
    campos = obFilasCol.Procesar(archivo)

    if not isinstance(campos, list):  return False
    print ('Web2py campos:',campos)
    totalE=0
    totalC=0
    if fecha_arreglo:
        fecha=fecha_arreglo
    else:
        fecha=request.now
    ruta_pdf=UNIR(request.folder,"static/PDF/{}/{:%Y}/{:%m}".format(idmodulo.carpeta,fecha,fecha) )
    ruta_db =UNIR("PDF/{}/{:%Y}/{:%m}".format(idmodulo.carpeta,fecha,fecha) )

    if not isdir(ruta_pdf):
        print (f"Crear Nueva Ruta : {ruta_pdf}")
        makedirs(ruta_pdf)



    for campo in campos:
        #Si el nit no viene, se da el nombre de usuario..... Esto se debe a Comprobante de pago Para Cliente Dian si nit()!!!!
        if len(campo['nit'].strip())==0:            campo['nit']=campo['nombre']
        #Busca el nit si esta registrado en la tabla de Clientes
        cliente =db(db.tbl_cliente.nit==campo["nit"]).select().first()

        if not cliente:#no Existe el Nit se crea el usuario y Cliente
            print("se crear por que no exites nit")
            user_id=db.auth_user.insert(first_name=campo["nombre"],
                    last_name=campo["nit"],
                   username=campo["nit"],
                   password=str(CRYPT(salt=True)(campo["nit"])[0])
                    )
            db.commit()
            id_cliente=db.tbl_cliente.insert(  nit=campo["nit"],
                                nombre=campo["nombre"],
                                id_usuario=user_id,
                                proveedor=False
                            )
            db.commit()
        else:   #Datos del cliente
            id_cliente=cliente.id
        print("id_cliente:",id_cliente)
        #Verificar si el nro del documento existe
        consulta=db.tbl_recepcion.nrodoc==campo["nrodoc"]
        #adicional exite en el caso de nomina el mismo numero de documento para todos,
        #por ese motivo se mira el id del cliente.
        consulta &=db.tbl_recepcion.id_cliente==id_cliente
        documento=db(consulta).select().first()
        if documento:   #Si existe el documento no lo inserta
            print (f"Existe Registro del {id_cliente} - {campo['nrodoc']} para el usuario id {campo['nit']}")
            buscar_archivo=UNIR("/home/www-data/web2py",request.folder,"static",documento.rutapdf)#ruta_Destino
            print (f"ruta en base:{buscar_archivo}")
            if not isfile(buscar_archivo):
                print (f"no exite archivo se Reemplaza por el campo: {campo['pdf']}")
                MOVER(campo["pdf"], buscar_archivo)
            else:
                print("Borrar por que existe!!")
                try:
                    BORRAR(campo["pdf"])#ruta_de_ubicacion_PDF_cuando_se_Genera...
                except:
                    pass

            continue
        #Mover el pdf al sitio de web2py
        #1 Craar si no existe la ruta
        tempo=PARTIR(campo["pdf"])

        nuevaruta=UNIR(ruta_pdf,"{}".format(tempo[-1]) )
        #Eliminar Espacion en blanco
        nuevaruta=nuevaruta.replace(" ","_")
        print (f"origen:{campo['pdf']}")
        MOVER(campo["pdf"], nuevaruta)
        #Verificar Correo
        estado="C"
        #Si tiene correo lo coloca en estado para enviar= E
        if cliente:
            print ("cliente.correo1",cliente.correo1)
            if cliente.correo1:
                estado="E"
                totalE =+1
            else:
                totalC=+1

        print (f"crear recepcion en estado {estado}")
        #Esta ruta no tiene la direccion de la app
        nuevaruta=UNIR(ruta_db,"{}".format(tempo[-1]) )
        nuevaruta=nuevaruta.replace(" ","_")

        db.tbl_recepcion.insert(id_cliente=id_cliente,
                            nrodoc=campo["nrodoc"],
                            valor=campo["valor"],
                            rutapdf=nuevaruta,
                            fecha=campo ["Fecha"],
                            fecha_hasta=campo["Fecha_Hasta"] if "Fecha_Hasta" in campo else "" ,
                            estado=estado,
                            tipdoc=modulo,
                        )
        db.commit()
    print(f"Total con Coreo:{totalE}")
    print(f"Total sin Coreo:{totalC}")
    return novedad


def fun_EnviarCorreo(envio, correo=None, paraserver=1):
    '''Arg: correo, si tiene texto este es el correo a enviar...'''
    from gluon.tools import Mail
    from os.path import join as UNIR

    print (correo, paraserver)

    mail = Mail()
    servercorreo=db(db.tbl_parametros.id_modulo==paraserver).select().first()
    if not servercorreo:
        print ("Error no esta especificado en parametros el modulo {}".format(paraserver))
        return 0

    # print ("EnviarCorreo")
    # print ("Servidor", servercorreo)
    # print ("Sitio",envio)
    # print ("="*80)
    mail.settings.server = '{}:{}'.format(servercorreo.servidor_correo,servercorreo.puerto)    #'smtp.gmail.com:587'
    mail.settings.login  = '{}:{}'.format(servercorreo.usuario, servercorreo.password)         #'maquitodosel@gmail.com:Maquitodo2019'
    mail.settings.tls    = servercorreo.tls                                                     #True
    mail.settings.sender = servercorreo.enviado_por                                             #'maquitodosel@gmail.com'
    consulta=db(db.tbl_recepcion.id==envio).select().first()
    print ("fun_EnviarCorreo",envio,consulta)
    if not consulta:    return 0
    consulta.estado="Q"
    consulta.fechaenvio=request.now
    consulta.update_record()
    db.commit()
    copia=[]
    if correo:
        correo=[correo]
    else:
        correo=[consulta.id_cliente.correo1]
        if consulta.id_cliente.correo2:
            copia.append(consulta.id_cliente.correo2)
        if consulta.id_cliente.correo3:
            copia.append(consulta.id_cliente.correo3)

    archpdf=UNIR(request.folder,"static",consulta.rutapdf)
    #Arreglo a Windows
    archpdf=archpdf.replace("\\","/")
    print ("envio:",correo,archpdf)




    ennvio = mail.send(  to=correo,
                cc=copia,
                subject= servercorreo.asunto,                                               #'comporbante de pago',
                reply_to=servercorreo.devolver if servercorreo.devolver else "",            #'soportesimplesoft@gmail.com',
                message=(servercorreo.cuerpo.format(consulta.valor),
                    servercorreo.cuerpohtml.format(consulta.valor)),
                attachments = [
                    mail.Attachment(archpdf),
                    # mail.Attachment('/home/marco/workspace/virtualenv3/web2py/web2py/applications/siendo/static/images/logo.png',
                    #                 content_id='foto')
                    ]
                )

    if ennvio:
        consulta.estado="T"
        consulta.fechaenvio=request.now
        consulta.update_record()
        db.commit()
    return ennvio

def F2s_Estado(tarea):
    '''Mira el esado de la tarea genereada'''
    detener=False
    if tarea == None:
        salida = '<div class="progress">'
        detener=True
    else:
        buscar=db(db.tbl_control_maestro.id==tarea).select(db.tbl_control_maestro.estado).first()
        if buscar.estado == "I":
            salida='<div class="progress">'
            salida += '<div class="progress-bar text-dark progress-bar-striped bg-warning" role="progressbar" style="width: 25%" aria-valuenow="25" aria-valuemin="0" aria-valuemax="100"><b>CARGANDO</b></div>'
            salida += '</div>'
        elif buscar.estado == "A":
            salida='<div class="progress">'
            salida += '<div class="progress-bar progress-bar-striped bg-success" role="progressbar" style="width: 25%" aria-valuenow="25" aria-valuemin="0" aria-valuemax="100"></div>'
            salida += '<div class="progress-bar text-dark progress-bar-striped bg-warning" role="progressbar" style="width: 25%" aria-valuenow="5" aria-valuemin="0" aria-valuemax="100"><b>PROCESANDO</b></div>'
            salida += '</div>'
        elif buscar.estado == "P":
            salida  = '<div class="progress">'
            salida += '<div class="progress-bar progress-bar-striped progress-bar-animated  bg-success" role="progressbar" style="width: 25%" aria-valuenow="25" aria-valuemin="0" aria-valuemax="100"></div>'
            salida += '<div class="progress-bar progress-bar-striped progress-bar-animated bg-success" role="progressbar" style="width: 25%" aria-valuenow="50" aria-valuemin="0" aria-valuemax="100"></div>'
            salida += '<div class="progress-bar text-dark progress-bar-striped progress-bar-animated bg-warning" role="progressbar bg-warning" style="width: 25%" aria-valuenow="25" aria-valuemin="0" aria-valuemax="100"><b>GRABANDO</b></div>'
            salida += '</div>'
        if buscar.estado == "F":
            detener=True
            salida  ='<div class="progress">'
            salida +='<div class="progress-bar progress-bar-animated progress-bar-striped bg-success" role="progressbar" style="width: 25%" aria-valuenow="25" aria-valuemin="0" aria-valuemax="100"></div>'
            salida +='<div class="progress-bar progress-bar-animated progress-bar-striped bg-success" role="progressbar" style="width: 25%" aria-valuenow="50" aria-valuemin="0" aria-valuemax="100"></div>'
            salida +='<div class="progress-bar progress-bar-animated progress-bar-striped bg-success" role="progressbar" style="width: 25%" aria-valuenow="75" aria-valuemin="0" aria-valuemax="100"></div>'
            salida +='<div class="progress-bar text-dark progress-bar-animated progress-bar-striped bg-success" role="progressbar" style="width: 25%" aria-valuenow="25" aria-valuemin="0" aria-valuemax="100"><B>FINALIZADO</B></div>'
            salida +='</div>'
            salida +='<br>'
        if buscar.estado == "E":
            detener=True
            salida  ='<div class="progress">'
            salida +='<div class="progress-bar text-dark progress-bar-animated progress-bar-striped bg-danger" role="progressbar" style="width: 100%" aria-valuenow="25" aria-valuemin="0" aria-valuemax="100"><B>Error!!</B></div>'
            salida +='</div>'
            salida +='<br>'

    salida="$('#progreso').html('{}');".format(XML(salida))
    if detener:    salida +="Detener();"
    return salida

def F2s_VerPDF(id_recepccion):
    if id_recepccion==None:    return "alert ('No se ha entregado el id del pdf');"
    #Consultas
    recepcion=db(db.tbl_recepcion.id==id_recepccion).select().first()
    print ('queso',id_recepccion)
    print ('aquii',recepcion)
    if not recepcion: return "alert ('No se encuentra id del pdf');"
    salida='var f2s_options = {'
    salida+='height: "500px",'
    salida+="pdfOpenParams: { view: 'FitV', page: '1' }"
    salida+='};'
    salida += "PDFObject.embed('{}',viewpdf,f2s_options);\n".format(URL("static",recepcion.rutapdf));
    salida=salida.replace("\\","/") #Por si viene desde windows!!
    return salida

def ProcesarEntradaPDF(rutarecursos, archivo, ambiente):
    '''Lee los datos de un pdf, y los envia al ambiente. '''
    from SimpleSoft.F2S_ExtraerPDF2 import ObjPDF
    ob=ObjPDF(  archpdf = archivo,
                    ruta_recursos=rutarecursos,
                    ambiente = ambiente,
                    ruta_app=request.folder,
                    debug= False
                )
    if ob.error:
        print ('eeeeeerrrrrooooorrr')
        return

    ob.VistaPdf()
    print ('*'*50)
    salida =ob.Procesar()
    # print (ob.Procesar())
    salida=[]
    for i in ob.documentos:
        #print (ob.documentos[i]['camposweb2py'])
        salida.append(ob.documentos[i]['camposweb2py'])
    # print (ob.documentos['1']['datos'].campos)
    # print (ob.documentos['10']['datos'].campos)
    return salida
