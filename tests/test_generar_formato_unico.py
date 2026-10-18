import pytest

import generar_formato_unico as g


# ---------- sanitize_filename ----------

@pytest.mark.parametrize("entrada,esperado", [
    ("United Kingdom", "United Kingdom"),
    ("", "SIN_PAIS"),
    ("   ", "SIN_PAIS"),
    ("A/B:C*D?", "A_B_C_D_"),
    ("País   con   espacios", "País con espacios"),
])
def test_sanitize_filename(entrada, esperado):
    assert g.sanitize_filename(entrada) == esperado


# ---------- _limpiar_telefono ----------

@pytest.mark.parametrize("entrada,esperado", [
    ("'+34600000000", "+34600000000"),
    (" +1 (555) 123-4567 ", "+15551234567"),
    ("", ""),
])
def test_limpiar_telefono(entrada, esperado):
    assert g._limpiar_telefono(entrada) == esperado


# ---------- _normalizar_tipografia ----------

def test_normalizar_tipografia_comillas_y_guiones():
    assert g._normalizar_tipografia("O’Prueba") == "O'Prueba"
    assert g._normalizar_tipografia("rango 1–2") == "rango 1-2"
    assert g._normalizar_tipografia("") == ""


# ---------- _sanear_direccion ----------

def test_sanear_direccion_sustituye_almohadilla():
    assert g._sanear_direccion("Carrera 1# 2-3") == "Carrera 1 Nº 2-3"
    assert g._sanear_direccion("#12") == "Nº 12"


def test_sanear_direccion_elimina_caracteres_no_permitidos():
    assert g._sanear_direccion("Calle 100% segura") == "Calle 100 segura"


def test_sanear_direccion_conserva_acentos_y_permitidos():
    direccion = "Calle Inventada 10 (dúplex 3)"
    assert g._sanear_direccion(direccion) == direccion


def test_sanear_direccion_vacia():
    assert g._sanear_direccion("") == ""


# ---------- construir_pedido_normalizado ----------

def test_pedido_internacional(args, square_header, fila_square):
    warnings = []
    pedido = g.construir_pedido_normalizado(square_header, fila_square(), args, warnings)

    assert pedido["es_internacional"] is True
    assert pedido["pais_iso"] == "AU"
    assert pedido["nombre"] == "Ana"
    assert pedido["apellido"] == "O'Prueba"
    assert pedido["telefono"] == "+61400000001"
    assert pedido["zip"] == "2000"
    assert pedido["peso_gramos"] == 240
    assert pedido["valor_neto_centimos"] == 6900
    assert pedido["codigo_producto"] == "S0360"
    assert pedido["instrucciones_no_entrega"] == "D"
    assert warnings == []


def test_pedido_nacional(args, square_header, fila_square):
    warnings = []
    fila = fila_square(**{"Shipping Country": "Spain", "Shipping Province": "B"})
    pedido = g.construir_pedido_normalizado(square_header, fila, args, warnings)

    assert pedido["es_internacional"] is False
    assert pedido["pais_iso"] == "ES"
    assert warnings == []


def test_pedido_pais_vacio_se_trata_como_nacional(args, square_header, fila_square):
    warnings = []
    fila = fila_square(**{"Shipping Country": ""})
    pedido = g.construir_pedido_normalizado(square_header, fila, args, warnings)

    assert pedido["es_internacional"] is False
    assert pedido["pais_iso"] == "ES"


def test_pedido_pais_desconocido_genera_aviso(args, square_header, fila_square):
    warnings = []
    fila = fila_square(**{"Shipping Country": "Narnia"})
    pedido = g.construir_pedido_normalizado(square_header, fila, args, warnings)

    assert pedido["es_internacional"] is True
    assert pedido["pais_iso"] == ""
    assert len(warnings) == 1
    assert "Narnia" in warnings[0]


def test_pedido_direccion_saneada(args, square_header, fila_square):
    warnings = []
    fila = fila_square(**{"Shipping Address2": "#12"})
    pedido = g.construir_pedido_normalizado(square_header, fila, args, warnings)
    assert pedido["direccion2"] == "Nº 12"


def test_pedido_nombre_una_sola_palabra(args, square_header, fila_square):
    warnings = []
    fila = fila_square(**{"Shipping Name": "Prince"})
    pedido = g.construir_pedido_normalizado(square_header, fila, args, warnings)
    assert pedido["nombre"] == "Prince"
    assert pedido["apellido"] == ""


# ---------- construir_fila_salida ----------

def _pedido_base(es_internacional=True):
    return {
        "codigo_producto": "S0360",
        "nombre": "Ana",
        "apellido": "O'Prueba",
        "direccion1": "1 Fake Street",
        "direccion2": "",
        "ciudad": "Sydney",
        "provincia": "NSW",
        "zip": "2000",
        "pais_iso": "AU",
        "telefono": "+61400000001",
        "email": "test@example.com",
        "order_id": "00001",
        "peso_gramos": 240,
        "largo_cm": 37,
        "alto_cm": 1,
        "ancho_cm": 29,
        "instrucciones_no_entrega": "D",
        "tipo_envio": "2",
        "es_internacional": es_internacional,
        "cantidad_mercancia": 1,
        "descripcion_mercancia_codigo": "580",
        "peso_neto_gramos": 240,
        "valor_neto_centimos": 6900,
        "pais_origen_aduana_iso": "ES",
    }


def test_construir_fila_salida_internacional():
    num_columnas = 186
    fila = g.construir_fila_salida(_pedido_base(), num_columnas)

    assert len(fila) == num_columnas
    assert fila[g.COLUMNA_ANIO_VERSION] == g.FORMATO_VERSION
    assert fila[g.COLUMNA_TOTAL_BULTOS] == g.TOTAL_BULTOS
    assert fila[g.COLUMNA_NUMERO_BULTO] == g.NUMERO_BULTO
    assert fila[2] == "S0360"
    assert fila[18] == "Ana"
    assert fila[19] == "O'Prueba"
    assert fila[37] == "AU"
    assert fila[94] == "D"
    assert fila[114] == 1
    assert fila[117] == 6900
    assert fila[-1] == g.FIN_DE_REGISTRO


def test_construir_fila_salida_sin_aduana_si_no_es_internacional():
    fila = g.construir_fila_salida(_pedido_base(es_internacional=False), 186)
    for col in g.MAPEO_ADUANA_COLUMNAS:
        assert fila[col] == ""


# ---------- aplicar_posiciones ----------

def test_aplicar_posiciones_un_solo_pedido():
    filas = [[None, "x"]]
    g.aplicar_posiciones(filas)
    assert filas[0][0] == "U"


def test_aplicar_posiciones_varios_pedidos():
    filas = [[None], [None], [None], [None]]
    g.aplicar_posiciones(filas)
    assert [f[0] for f in filas] == ["C", "R", "R", "F"]


def test_aplicar_posiciones_lista_vacia():
    filas = []
    g.aplicar_posiciones(filas)
    assert filas == []


# ---------- leer_pedidos ----------

def _escribir_csv(tmp_path, contenido, nombre="pedidos.csv"):
    csv_path = tmp_path / nombre
    csv_path.write_text(contenido, encoding="utf-8")
    return csv_path


def test_leer_pedidos_deduplica_por_order_id(tmp_path):
    contenido = (
        "Order ID,Email,Shipping Address1,Shipping Country\n"
        '"00001","a@a.com","Calle 1","Spain"\n'
        '"00001","","",""\n'
        '"00002","b@b.com","Calle 2","Germany"\n'
    )
    csv_path = _escribir_csv(tmp_path, contenido)
    header, rows, warnings = g.leer_pedidos(csv_path)

    assert header == ["Order ID", "Email", "Shipping Address1", "Shipping Country"]
    assert len(rows) == 2
    assert [r[0] for r in rows] == ["00001", "00002"]
    assert warnings == []


def test_leer_pedidos_omite_order_id_vacio(tmp_path):
    contenido = (
        "Order ID,Email,Shipping Address1,Shipping Country\n"
        '"","a@a.com","Calle 1","Spain"\n'
    )
    csv_path = _escribir_csv(tmp_path, contenido)
    header, rows, warnings = g.leer_pedidos(csv_path)

    assert rows == []
    assert len(warnings) == 1
    assert "Order ID" in warnings[0]


def test_leer_pedidos_omite_filas_con_columnas_incorrectas(tmp_path):
    contenido = (
        "Order ID,Email,Shipping Address1,Shipping Country\n"
        '"00001","a@a.com","Calle 1"\n'
    )
    csv_path = _escribir_csv(tmp_path, contenido)
    header, rows, warnings = g.leer_pedidos(csv_path)

    assert rows == []
    assert len(warnings) == 1


def test_leer_pedidos_formato_no_soportado(tmp_path):
    contenido = "Name,Price\nCamiseta,10\n"
    csv_path = _escribir_csv(tmp_path, contenido)

    with pytest.raises(ValueError, match="Big Cartel"):
        g.leer_pedidos(csv_path)


def test_leer_pedidos_fichero_vacio(tmp_path):
    csv_path = _escribir_csv(tmp_path, "", nombre="vacio.csv")

    with pytest.raises(ValueError):
        g.leer_pedidos(csv_path)


def test_leer_pedidos_fixture_square_completo(orders_square_csv):
    header, rows, warnings = g.leer_pedidos(orders_square_csv)

    assert len(header) == 47
    assert [r[0] for r in rows] == ["10001", "10002", "10003", "10004", "10005", "10006", "10007"]
    assert warnings == []


def test_leer_pedidos_fixture_square_conserva_fila_con_datos_de_envio(orders_square_csv):
    header, rows, _ = g.leer_pedidos(orders_square_csv)
    fila = dict(zip(header, rows[0]))

    assert fila["Order ID"] == "10001"
    assert fila["Email"] == "cliente10001@example.com"
    assert fila["Shipping Country"] == "Australia"
    assert fila["Lineitem name"] == "Producto de prueba A"
