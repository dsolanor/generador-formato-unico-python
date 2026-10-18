#!/usr/bin/env python3
"""Genera un fichero "Formato Único" de Correos (carga masiva de envíos) a partir
de un export de pedidos Square/Squarespace.

Lee únicamente la primera fila de cada pedido (la que trae comprador y dirección
de envío completos) y descarta las filas de continuación que solo añaden
artículos. Sigue la especificación oficial "Definición del Formato de Fichero
Único para preparación de envíos a través de Mi Oficina" (versión 2018v002).

Solo exporta envíos INTERNACIONALES (destino distinto de España) — los
pedidos nacionales se omiten (se cuentan en el resumen) y se gestionan por
otra vía.

Datos de contrato/cuenta de Correos opcionales (código etiquetador, número de
contrato, número de cliente, etc.) y del remitente quedan vacíos — no son
obligatorios según la especificación y Correos los toma de la cuenta del
usuario si no se informan. El Código producto SÍ es obligatorio: usa
--codigo-producto (ver Anexo I de la guía de ayuda de Correos) si el valor
por defecto no corresponde a tu contrato.
"""

import argparse
import csv
import datetime
import re
import sys
from collections import OrderedDict
from pathlib import Path

import xlrd
import xlwt

sys.path.insert(0, str(Path(__file__).resolve().parent))
import iso_paises
from constantes import (
    PESO_KG_DEFECTO,
    ALTO_CM_DEFECTO,
    ANCHO_CM_DEFECTO,
    PROFUNDO_CM_DEFECTO,
    CODIGO_MERCANCIA_DEFECTO,
    PAIS_ORIGEN_ADUANA_DEFECTO,
    CODIGO_PRODUCTO_DEFECTO,
    TIPO_ENVIO_DEFECTO,
    INSTRUCCIONES_NO_ENTREGA_DEFECTO,
)

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
DEFAULT_PLANTILLA = REPO_ROOT / "vendor" / "template" / "PlantillaFicheroFormatoUnico.xls"

PLANTILLA_HOJA = "Hoja1"
PLANTILLA_FILA_CABECERA = 0

FORMATO_VERSION = "2018v002"  # campo 2, fijo según la especificación
FIN_DE_REGISTRO = "E"  # campo 186, fijo según la especificación
TOTAL_BULTOS = 1  # campo 14, obligatorio; un bulto por pedido
NUMERO_BULTO = 1  # campo 15, obligatorio

LIMITE_FILAS_XLS = 65535  # límite del formato .xls / xlwt

# Columnas por índice (0-based) de "Hoja1" en PlantillaFicheroFormatoUnico.xls.
# No se usa el texto de cabecera como clave porque varias cabeceras se repiten
# literalmente entre el bloque de destinatario y el bloque de remitente
# (p. ej. "Nombre", "Apellido 1", "Email", "Dirección"). Los valores del
# diccionario del pedido ya vienen en las unidades/formato que exige la
# especificación (gramos, céntimos, ISO-2, etc.) — ver construir_pedido_normalizado.
MAPEO_COLUMNAS = {
    2: "codigo_producto",
    18: "nombre",
    19: "apellido",
    25: "direccion1",
    26: "direccion2",
    33: "ciudad",
    34: "provincia",
    36: "zip",
    37: "pais_iso",
    41: "telefono",
    42: "email",
    45: "order_id",
    49: "peso_gramos",
    50: "largo_cm",
    51: "alto_cm",
    52: "ancho_cm",
    94: "instrucciones_no_entrega",
    110: "tipo_envio",
}

# Solo se rellenan si el pedido es internacional (declaración de aduana).
MAPEO_ADUANA_COLUMNAS = {
    114: "cantidad_mercancia",
    115: "descripcion_mercancia_codigo",
    116: "peso_neto_gramos",
    117: "valor_neto_centimos",
    120: "pais_origen_aduana_iso",
}

COLUMNA_POSICION = 0
COLUMNA_ANIO_VERSION = 1
COLUMNA_TOTAL_BULTOS = 13
COLUMNA_NUMERO_BULTO = 14


def sanitize_filename(name: str) -> str:
    name = name.strip() or "SIN_PAIS"
    name = re.sub(r'[\\/:*?"<>|]', "_", name)
    name = re.sub(r"\s+", " ", name).strip()
    return name or "SIN_PAIS"


def leer_pedidos(csv_path: Path):
    """Deduplica por 'Order ID', quedándose con la primera fila de cada pedido."""
    warnings = []
    with csv_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            raise ValueError(f"'{csv_path}' está vacío")

        try:
            order_id_idx = header.index("Order ID")
            email_idx = header.index("Email")
            shipping_address1_idx = header.index("Shipping Address1")
        except ValueError:
            raise ValueError(
                f"'{csv_path}' no tiene el formato esperado "
                "(faltan columnas 'Order ID', 'Email' y/o 'Shipping Address1'). "
                "Este script no soporta el formato de export de Big Cartel."
            )

        kept = OrderedDict()
        for line_no, row in enumerate(reader, start=2):
            if not row or all(cell == "" for cell in row):
                continue
            if len(row) != len(header):
                warnings.append(
                    f"línea {line_no}: {len(row)} columnas, se esperaban {len(header)} — omitida"
                )
                continue
            order_id = row[order_id_idx]
            if order_id == "":
                warnings.append(f"línea {line_no}: 'Order ID' vacío — omitida")
                continue
            if not row[email_idx] and not row[shipping_address1_idx]:
                continue  # fila de continuación (solo artículos), no trae dirección
            if order_id not in kept:
                kept[order_id] = row

    return header, list(kept.values()), warnings


def leer_cabeceras_plantilla(plantilla_path: Path) -> list[str]:
    wb = xlrd.open_workbook(str(plantilla_path))
    sh = wb.sheet_by_name(PLANTILLA_HOJA)
    return [str(v) for v in sh.row_values(PLANTILLA_FILA_CABECERA)]


def _limpiar_telefono(telefono: str) -> str:
    telefono = telefono.strip().lstrip("'")
    return re.sub(r"[\s()\-]", "", telefono)


# Caracteres especiales que Correos acepta en Nombre/Dirección, según el
# mensaje de validación del portal: letras, números y ". · - ( ) ' çÇ ! ¡ ¿ ?
# ~ , : ; & / @ _ ª $ € º + * ="
_CARACTERES_ESPECIALES_PERMITIDOS = ".·-()'çÇ!¡¿?~,:;&/@_ª$€º+*="
_PATRON_CARACTERES_NO_PERMITIDOS = re.compile(
    r"[^A-Za-zÀ-ÖØ-öø-ÿ0-9 " + re.escape(_CARACTERES_ESPECIALES_PERMITIDOS) + r"]"
)


def _normalizar_tipografia(texto: str) -> str:
    """Convierte comillas/guiones tipográficos de Unicode a sus equivalentes
    ASCII permitidos por Correos (p. ej. ’ -> ', – -> -)."""
    if not texto:
        return texto
    for origen, destino in (("’", "'"), ("‘", "'"), ("´", "'"), ("–", "-"), ("—", "-")):
        texto = texto.replace(origen, destino)
    return texto


def _sanear_direccion(texto: str) -> str:
    """Normaliza tipografía y elimina caracteres no permitidos en campos de
    dirección (p. ej. '#', que Correos no acepta — se sustituye por 'Nº')."""
    if not texto:
        return texto
    texto = _normalizar_tipografia(texto)
    texto = re.sub(r"\s*#\s*", " Nº ", texto).strip()
    return _PATRON_CARACTERES_NO_PERMITIDOS.sub("", texto)


def construir_pedido_normalizado(header: list[str], row: list[str], args, warnings: list) -> dict:
    fila = dict(zip(header, row))
    order_id = fila.get("Order ID", "")

    nombre_completo = _normalizar_tipografia((fila.get("Shipping Name") or "").strip())
    partes = nombre_completo.split()
    nombre = partes[0] if partes else ""
    apellido = " ".join(partes[1:])

    pais_nombre = (fila.get("Shipping Country") or "").strip()
    provincia = (fila.get("Shipping Province") or "").strip()
    shipping_zip = fila.get("Shipping Zip") or ""

    if not pais_nombre:
        pais_iso = iso_paises.CODIGO_ESPANA_ISO
        es_internacional = False
    else:
        resuelto = iso_paises.resolver_iso_pais(pais_nombre)
        if resuelto is None:
            warnings.append(
                f"pedido {order_id}: país '{pais_nombre}' no reconocido — "
                "código ISO dejado en blanco, revisar a mano antes de subir el fichero"
            )
            pais_iso = ""
            es_internacional = True
        else:
            pais_iso = resuelto
            es_internacional = resuelto != iso_paises.CODIGO_ESPANA_ISO

    peso_gramos = round(args.peso_kg * 1000)
    valor_neto_centimos = round(float(fila.get("Subtotal") or 0) * 100)

    return {
        "order_id": order_id,
        "nombre": nombre,
        "apellido": apellido,
        "email": fila.get("Email", ""),
        "telefono": _limpiar_telefono(fila.get("Shipping Phone") or ""),
        "direccion1": _sanear_direccion(fila.get("Shipping Address1", "")),
        "direccion2": _sanear_direccion(fila.get("Shipping Address2", "")),
        "ciudad": fila.get("Shipping City", ""),
        "provincia": provincia,
        "zip": shipping_zip,
        "pais_iso": pais_iso,
        "pais_nombre": pais_nombre or "SIN_PAIS",
        "es_internacional": es_internacional,
        "codigo_producto": args.codigo_producto,
        "tipo_envio": args.tipo_envio,
        "instrucciones_no_entrega": args.instrucciones_no_entrega,
        "peso_gramos": peso_gramos,
        "largo_cm": round(args.profundo_cm),
        "alto_cm": round(args.alto_cm),
        "ancho_cm": round(args.ancho_cm),
        "cantidad_mercancia": 1,
        "descripcion_mercancia_codigo": args.codigo_mercancia,
        "peso_neto_gramos": peso_gramos,
        "valor_neto_centimos": valor_neto_centimos,
        "pais_origen_aduana_iso": args.pais_origen_aduana,
    }


def construir_fila_salida(pedido: dict, num_columnas: int) -> list:
    fila_salida = [""] * num_columnas
    fila_salida[COLUMNA_ANIO_VERSION] = FORMATO_VERSION
    fila_salida[COLUMNA_TOTAL_BULTOS] = TOTAL_BULTOS
    fila_salida[COLUMNA_NUMERO_BULTO] = NUMERO_BULTO

    for col, clave in MAPEO_COLUMNAS.items():
        fila_salida[col] = pedido[clave]

    if pedido["es_internacional"]:
        for col, clave in MAPEO_ADUANA_COLUMNAS.items():
            fila_salida[col] = pedido[clave]

    fila_salida[num_columnas - 1] = FIN_DE_REGISTRO
    return fila_salida


def aplicar_posiciones(filas: list[list]) -> None:
    """Rellena el campo 'Posición' (columna 0): C/F/R/U según la especificación."""
    n = len(filas)
    for i, fila in enumerate(filas):
        if n == 1:
            fila[COLUMNA_POSICION] = "U"
        elif i == 0:
            fila[COLUMNA_POSICION] = "C"
        elif i == n - 1:
            fila[COLUMNA_POSICION] = "F"
        else:
            fila[COLUMNA_POSICION] = "R"


def escribir_xls(headers_plantilla: list[str], filas: list[list], out_path: Path) -> None:
    if 1 + len(filas) > LIMITE_FILAS_XLS:
        raise ValueError(
            f"Demasiadas filas ({len(filas)}) para un único .xls "
            f"(límite {LIMITE_FILAS_XLS}). Usa --agrupar-por-pais."
        )

    aplicar_posiciones(filas)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    wb = xlwt.Workbook(encoding="utf-8")
    sh = wb.add_sheet(PLANTILLA_HOJA)

    for col, valor in enumerate(headers_plantilla):
        sh.write(0, col, valor)

    for row_idx, fila in enumerate(filas, start=1):
        for col, valor in enumerate(fila):
            # Todas las celdas como texto: varios portales de carga masiva
            # leen el fichero asumiendo que toda celda es texto y fallan si
            # encuentran una celda numérica de Excel.
            sh.write(row_idx, col, "" if valor == "" else str(valor))

    wb.save(str(out_path))


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Genera un .xls en 'Formato Único' de Correos a partir de un CSV "
            "de pedidos Square/Squarespace, listo para carga masiva de envíos."
        )
    )
    parser.add_argument(
        "csv_path",
        help="Ruta al CSV de pedidos exportado de Squarespace (obligatorio)",
    )
    parser.add_argument(
        "--plantilla",
        default=None,
        help=f"Ruta a la plantilla .xls de Correos (por defecto: {DEFAULT_PLANTILLA})",
    )
    parser.add_argument(
        "-o", "--salida",
        default=None,
        help="Ruta del .xls de salida (solo si no se usa --agrupar-por-pais; "
             "por defecto: data/<DD-MM-YYYY>/envios-correos_<DD-MM-YYYY_HHMMSS>.xls)",
    )
    parser.add_argument(
        "--agrupar-por-pais",
        action="store_true",
        help="Genera un .xls por país de envío en vez de un único fichero",
    )
    parser.add_argument("--peso-kg", type=float, default=PESO_KG_DEFECTO,
                         help=f"Peso fijo por paquete en kg (por defecto: {PESO_KG_DEFECTO})")
    parser.add_argument("--alto-cm", type=float, default=ALTO_CM_DEFECTO,
                         help=f"Alto fijo en cm (por defecto: {ALTO_CM_DEFECTO})")
    parser.add_argument("--ancho-cm", type=float, default=ANCHO_CM_DEFECTO,
                         help=f"Ancho fijo en cm (por defecto: {ANCHO_CM_DEFECTO})")
    parser.add_argument("--profundo-cm", type=float, default=PROFUNDO_CM_DEFECTO,
                         help=f"Profundo/largo fijo en cm (por defecto: {PROFUNDO_CM_DEFECTO})")
    parser.add_argument("--codigo-mercancia", default=CODIGO_MERCANCIA_DEFECTO,
                         help="Código de mercancía (Anexo II de la guía de Correos) para la "
                              "declaración de aduana en envíos internacionales "
                              f"(por defecto: {CODIGO_MERCANCIA_DEFECTO} = Textiles - Algodón)")
    parser.add_argument("--pais-origen-aduana", default=PAIS_ORIGEN_ADUANA_DEFECTO,
                         help="Código ISO-2 del país de origen declarado en aduana "
                              f"(por defecto: {PAIS_ORIGEN_ADUANA_DEFECTO}, España)")
    parser.add_argument("--codigo-producto", default=CODIGO_PRODUCTO_DEFECTO,
                         help="Código de producto (Anexo I) para los envíos internacionales "
                              f"(por defecto: {CODIGO_PRODUCTO_DEFECTO})")
    parser.add_argument("--tipo-envio", default=TIPO_ENVIO_DEFECTO,
                         help="Tipo de envío (campo 111): "
                              "1 Documentos / 2 Venta de Mercancías / 3 Regalo / "
                              "4 Muestra Comercial / 5 Mercancía Devuelta / 6 Otro "
                              f"(por defecto: {TIPO_ENVIO_DEFECTO})")
    parser.add_argument("--instrucciones-no-entrega", default=INSTRUCCIONES_NO_ENTREGA_DEFECTO,
                         choices=["D", "A"],
                         help="Instrucciones si no hay entrega: D Devolver al remitente / "
                              f"A Tratar como abandonado (por defecto: {INSTRUCCIONES_NO_ENTREGA_DEFECTO})")
    args = parser.parse_args()

    csv_path = Path(args.csv_path).resolve()
    plantilla_path = Path(args.plantilla).resolve() if args.plantilla else DEFAULT_PLANTILLA

    if not csv_path.exists():
        print(f"Error: no existe el fichero '{csv_path}'", file=sys.stderr)
        return 1
    if not plantilla_path.exists():
        print(f"Error: no existe la plantilla '{plantilla_path}'", file=sys.stderr)
        return 1

    try:
        header, rows, warnings = leer_pedidos(csv_path)
        headers_plantilla = leer_cabeceras_plantilla(plantilla_path)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    todos_los_pedidos = [construir_pedido_normalizado(header, row, args, warnings) for row in rows]
    pedidos = [p for p in todos_los_pedidos if p["es_internacional"]]
    nacionales_omitidos = [p for p in todos_los_pedidos if not p["es_internacional"]]

    ahora = datetime.datetime.now()
    date_str = ahora.strftime("%d-%m-%Y")
    timestamp_str = ahora.strftime("%d-%m-%Y_%H%M%S")
    out_dir = REPO_ROOT / "data" / date_str

    print(f"Pedidos distintos encontrados: {len(todos_los_pedidos)}")
    print(f"  Internacionales (exportados): {len(pedidos)}")
    if nacionales_omitidos:
        ids = ", ".join(p["order_id"] for p in nacionales_omitidos)
        print(f"  Nacionales (omitidos, gestionar aparte): {len(nacionales_omitidos)} -> {ids}")

    if not pedidos:
        print("No hay pedidos internacionales que exportar.")
        return 0

    if args.agrupar_por_pais:
        grupos = OrderedDict()
        for pedido in pedidos:
            grupos.setdefault(pedido["pais_nombre"], []).append(pedido)

        for pais_nombre, pedidos_pais in grupos.items():
            filas = [construir_fila_salida(p, len(headers_plantilla)) for p in pedidos_pais]
            out_path = out_dir / f"{sanitize_filename(pais_nombre)}_{timestamp_str}.xls"
            escribir_xls(headers_plantilla, filas, out_path)
            print(f"  {pais_nombre}: {len(pedidos_pais)} pedido(s) -> {out_path}")
    else:
        filas = [construir_fila_salida(p, len(headers_plantilla)) for p in pedidos]
        out_path = Path(args.salida).resolve() if args.salida else out_dir / f"envios-correos_{timestamp_str}.xls"
        escribir_xls(headers_plantilla, filas, out_path)
        print(f"  -> {out_path}")

    if warnings:
        print("\nAvisos:")
        for w in warnings:
            print(f"  - {w}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
