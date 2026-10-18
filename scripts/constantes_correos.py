"""Constantes fijas para el fichero "Formato Único" de Correos: datos de
remitente y de contrato/cuenta, iguales en todas las filas del fichero.

Los valores se leen de variables de entorno (CORREOS_REMITENTE_<CAMPO> y
CORREOS_CONTRATO_<CAMPO>) para no guardar datos personales en el repositorio.
Copia .env.example a .env y rellénalo; `make` carga .env automáticamente.
Las variables no definidas quedan vacías.
"""

import os

CAMPOS_REMITENTE = (
    "nombre", "apellido1", "apellido2", "nif", "empresa", "persona_contacto",
    "tipo_direccion", "direccion", "numero", "portal", "bloque", "escalera",
    "piso", "puerta", "localidad", "provincia", "cp", "zip", "pais",
    "telefono", "email",
)

# Datos de contrato/cuenta Correos — no aparecen en una etiqueta individual,
# los asigna Correos a tu cuenta.
CAMPOS_CONTRATO = (
    "anio_estructura_version", "codigo_producto", "tipo_franqueo",
    "codigo_etiquetador", "numero_contrato", "numero_cliente",
    "numero_maquina_franquear", "modalidad_entrega", "tipo_envio",
)


def _leer_entorno(prefijo: str, campos: tuple[str, ...]) -> dict[str, str]:
    return {campo: os.environ.get(f"{prefijo}{campo.upper()}", "").strip() for campo in campos}


REMITENTE = _leer_entorno("CORREOS_REMITENTE_", CAMPOS_REMITENTE)
CONTRATO = _leer_entorno("CORREOS_CONTRATO_", CAMPOS_CONTRATO)
