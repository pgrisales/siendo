cd /mnt/datos/marco/workspace/virtualenv3/web2py/applications/siendo/trabajo/ambientes
#python retencionanual_enterprice.py
python comprobante_enterprice.py
#python retencion_dian.py

cd /mnt/datos/marco/workspace/virtualenv3/web2py/applications/siendo/modules/SimpleSoft

#dian
#./F2S_filascol.py  -r /mnt/datos/marco/workspace/virtualenv3/web2py/applications/siendo/trabajo -f /home/marco/borrar/maquitodo/dian/cert_dian.txt -a retencion_dian.amb
#comprobante filas
#./F2S_filascol.py  -r /mnt/datos/marco/workspace/virtualenv3/web2py/applications/siendo/trabajo -f /home/marco/Clientes/maquitodo/trabajo/spools/Comprobantes_egreso.txt  -a comprobante.amb




#comprobante
./F2S_ExtraerPDF3.py "/home/marco/borrar/maquitodo/egresos2/PAGOS MAYO 25_pag_7.pdf" ../../trabajo comprobante_enterprice.amb /mnt/datos/marco/workspace/virtualenv3/web2py/applications/siendo 
#./F2S_ExtraerPDF3.py /home/marco/borrar/maquitodo/egresos2/error_may_24.pdf ../../trabajo comprobante_enterprice.amb /mnt/datos/marco/workspace/virtualenv3/web2py/applications/siendo --debug=True
#./F2S_ExtraerPDF3.py /home/marco/borrar/maquitodo/egresos2/error_may_24_pag_1.pdf ../../trabajo comprobante_enterprice.amb /mnt/datos/marco/workspace/virtualenv3/web2py/applications/siendo
#./F2S_ExtraerPDF3.py /home/marco/borrar/maquitodo/egresos2/error_may_24_pag_2.pdf ../../trabajo comprobante_enterprice.amb /mnt/datos/marco/workspace/virtualenv3/web2py/applications/siendo --debug=True
#./F2S_ExtraerPDF3.py /home/marco/borrar/maquitodo/egresos2/error_may_24_pag_3.pdf ../../trabajo comprobante_enterprice.amb /mnt/datos/marco/workspace/virtualenv3/web2py/applications/siendo --debug=True
#./F2S_ExtraerPDF3.py /home/marco/borrar/maquitodo/egresos2/error_may_24_pag_4.pdf ../../trabajo comprobante_enterprice.amb /mnt/datos/marco/workspace/virtualenv3/web2py/applications/siendo --debug=True
#./F2S_ExtraerPDF3.py /home/marco/borrar/maquitodo/egresos2/error_may_24_pag_5.pdf ../../trabajo comprobante_enterprice.amb /mnt/datos/marco/workspace/virtualenv3/web2py/applications/siendo --debug=True
#./F2S_ExtraerPDF3.py /home/marco/borrar/maquitodo/egresos2/error_may_24_pag_6.pdf ../../trabajo comprobante_enterprice.amb /mnt/datos/marco/workspace/virtualenv3/web2py/applications/siendo --debug=True
#./F2S_ExtraerPDF3.py /home/marco/borrar/maquitodo/egresos2/error_may_24_pag_7.pdf ../../trabajo comprobante_enterprice.amb /mnt/datos/marco/workspace/virtualenv3/web2py/applications/siendo --debug=True
#./F2S_ExtraerPDF3.py /home/marco/borrar/maquitodo/egresos2/error_may_24_pag_8.pdf ../../trabajo comprobante_enterprice.amb /mnt/datos/marco/workspace/virtualenv3/web2py/applications/siendo --debug=True
#./F2S_ExtraerPDF3.py /home/marco/borrar/maquitodo/egresos2/error_may_24_pag_9.pdf ../../trabajo comprobante_enterprice.amb /mnt/datos/marco/workspace/virtualenv3/web2py/applications/siendo --debug=True

#renta
#./F2S_ExtraerPDF3.py /home/marco/borrar/maquitodo/renta/LCertificadoRenta_pag_1.pdf ../../trabajo retencionanual_enterprice.amb /mnt/datos/marco/workspace/virtualenv3/web2py/applications/siendo
#./F2S_ExtraerPDF2.py /home/marco/borrar/maquitodo/renta/LCertificadoRenta_pag_4.pdf ../../trabajo retencionanual_enterprice.amb /mnt/datos/marco/workspace/virtualenv3/web2py/applications/siendo
#./F2S_ExtraerPDF2.py /home/marco/borrar/maquitodo/renta/LCertificadoRenta_pag_2.pdf ../../trabajo retencionanual_enterprice.amb /mnt/datos/marco/workspace/virtualenv3/web2py/applications/siendo
#./F2S_ExtraerPDF2.py /home/marco/borrar/maquitodo/renta/LCertificadoRenta_pag_3.pdf ../../trabajo retencionanual_enterprice.amb /mnt/datos/marco/workspace/virtualenv3/web2py/applications/siendo
#./F2S_ExtraerPDF2.py /home/marco/borrar/maquitodo/renta/LCertificadoRenta_pag_5.pdf ../../trabajo retencionanual_enterprice.amb /mnt/datos/marco/workspace/virtualenv3/web2py/applications/siendo
#./F2S_ExtraerPDF2.py /home/marco/borrar/maquitodo/renta/LCertificadoRenta_pag_6.pdf ../../trabajo retencionanual_enterprice.amb /mnt/datos/marco/workspace/virtualenv3/web2py/applications/siendo
#./F2S_ExtraerPDF2.py /home/marco/borrar/maquitodo/renta/LCertificadoRenta_pag_8.pdf ../../trabajo retencionanual_enterprice.amb /mnt/datos/marco/workspace/virtualenv3/web2py/applications/siendo
#./F2S_ExtraerPDF2.py /home/marco/borrar/maquitodo/renta/LCertificadoRenta_pag_9.pdf ../../trabajo retencionanual_enterprice.amb /mnt/datos/marco/workspace/virtualenv3/web2py/applications/siendo
#./F2S_ExtraerPDF2.py /home/marco/borrar/maquitodo/renta/LCertificadoRenta_pag_10.pdf ../../trabajo retencionanual_enterprice.amb /mnt/datos/marco/workspace/virtualenv3/web2py/applications/siendo
#./F2S_ExtraerPDF2.py /home/marco/borrar/maquitodo/renta/LCertificadoRenta_pag_11.pdf ../../trabajo retencionanual_enterprice.amb /mnt/datos/marco/workspace/virtualenv3/web2py/applications/siendo
#./F2S_ExtraerPDF2.py /home/marco/borrar/maquitodo/renta/LCertificadoRenta_pag_12.pdf ../../trabajo retencionanual_enterprice.amb /mnt/datos/marco/workspace/virtualenv3/web2py/applications/siendo
#./F2S_ExtraerPDF2.py /home/marco/borrar/maquitodo/renta/LCertificadoRenta_pag_13.pdf ../../trabajo retencionanual_enterprice.amb /mnt/datos/marco/workspace/virtualenv3/web2py/applications/siendo
#./F2S_ExtraerPDF2.py /home/marco/borrar/maquitodo/renta/LCertificadoRenta_pag_15.pdf ../../trabajo retencionanual_enterprice.amb /mnt/datos/marco/workspace/virtualenv3/web2py/applications/siendo
#./F2S_ExtraerPDF2.py /home/marco/borrar/maquitodo/renta/LCertificadoRenta_pag_16.pdf ../../trabajo retencionanual_enterprice.amb /mnt/datos/marco/workspace/virtualenv3/web2py/applications/siendo
#./F2S_ExtraerPDF2.py /home/marco/borrar/maquitodo/renta/LCertificadoRenta_pag_17.pdf ../../trabajo retencionanual_enterprice.amb /mnt/datos/marco/workspace/virtualenv3/web2py/applications/siendo
#./F2S_ExtraerPDF2.py /home/marco/borrar/maquitodo/renta/LCertificadoRenta_pag_18.pdf ../../trabajo retencionanual_enterprice.amb /mnt/datos/marco/workspace/virtualenv3/web2py/applications/siendo
#./F2S_ExtraerPDF2.py /home/marco/borrar/maquitodo/renta/LCertificadoRenta_pag_19.pdf ../../trabajo retencionanual_enterprice.amb /mnt/datos/marco/workspace/virtualenv3/web2py/applications/siendo
#./F2S_ExtraerPDF2.py /home/marco/borrar/maquitodo/renta/LCertificadoRenta_pag_20.pdf ../../trabajo retencionanual_enterprice.amb /mnt/datos/marco/workspace/virtualenv3/web2py/applications/siendo
#./F2S_ExtraerPDF2.py /home/marco/borrar/maquitodo/renta/LCertificadoRenta_pag_21.pdf ../../trabajo retencionanual_enterprice.amb /mnt/datos/marco/workspace/virtualenv3/web2py/applications/siendo
#./F2S_ExtraerPDF2.py /home/marco/borrar/maquitodo/renta/LCertificadoRenta_pag_22.pdf ../../trabajo retencionanual_enterprice.amb /mnt/datos/marco/workspace/virtualenv3/web2py/applications/siendo
#./F2S_ExtraerPDF2.py /home/marco/borrar/maquitodo/renta/LCertificadoRenta_pag_23.pdf ../../trabajo retencionanual_enterprice.amb /mnt/datos/marco/workspace/virtualenv3/web2py/applications/siendo
#./F2S_ExtraerPDF2.py /home/marco/borrar/maquitodo/renta/LCertificadoRenta_pag_24.pdf ../../trabajo retencionanual_enterprice.amb /mnt/datos/marco/workspace/virtualenv3/web2py/applications/siendo
#./F2S_ExtraerPDF2.py /home/marco/borrar/maquitodo/renta/LCertificadoRenta_pag_25.pdf ../../trabajo retencionanual_enterprice.amb /mnt/datos/marco/workspace/virtualenv3/web2py/applications/siendo
#./F2S_ExtraerPDF2.py /home/marco/borrar/maquitodo/renta/LCertificadoRenta_pag_26.pdf ../../trabajo retencionanual_enterprice.amb /mnt/datos/marco/workspace/virtualenv3/web2py/applications/siendo
#./F2S_ExtraerPDF2.py /home/marco/borrar/maquitodo/renta/LCertificadoRenta_pag_27.pdf ../../trabajo retencionanual_enterprice.amb /mnt/datos/marco/workspace/virtualenv3/web2py/applications/siendo
#./F2S_ExtraerPDF2.py /home/marco/borrar/maquitodo/renta/LCertificadoRenta_pag_28.pdf ../../trabajo retencionanual_enterprice.amb /mnt/datos/marco/workspace/virtualenv3/web2py/applications/siendo
#./F2S_ExtraerPDF2.py /home/marco/borrar/maquitodo/renta/LCertificadoRenta_pag_29.pdf ../../trabajo retencionanual_enterprice.amb /mnt/datos/marco/workspace/virtualenv3/web2py/applications/siendo
