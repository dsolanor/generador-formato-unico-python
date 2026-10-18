"""Valores por defecto del envío para el Formato Único de Correos.

Se aplican a todos los paquetes y se pueden sobrescribir con los flags de
generar_formato_unico.py (--peso-kg, --alto-cm, --codigo-producto, ...).
"""

import iso_paises

PESO_KG_DEFECTO = 0.24
ALTO_CM_DEFECTO = 1
ANCHO_CM_DEFECTO = 29
PROFUNDO_CM_DEFECTO = 37
CODIGO_MERCANCIA_DEFECTO = "580"  # Anexo II: "Textiles - Algodón"
PAIS_ORIGEN_ADUANA_DEFECTO = iso_paises.CODIGO_ESPANA_ISO
CODIGO_PRODUCTO_DEFECTO = "S0360"  # Anexo I: PAQ LIGHT INTERNACIONAL
TIPO_ENVIO_DEFECTO = "2"  # Venta de Mercancías, obligatorio para envíos internacionales
INSTRUCCIONES_NO_ENTREGA_DEFECTO = "D"  # D: Devolver al remitente / A: Tratar como abandonado
