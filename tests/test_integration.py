import datetime
import sys

import pytest
import xlrd

import generar_formato_unico as g

PLANTILLA_REAL = g.DEFAULT_PLANTILLA

requiere_plantilla = pytest.mark.skipif(
    not PLANTILLA_REAL.exists(), reason="plantilla real de Correos no disponible"
)

@requiere_plantilla
def test_leer_cabeceras_plantilla_real():
    cabeceras = g.leer_cabeceras_plantilla(PLANTILLA_REAL)
    assert len(cabeceras) == 186
    assert cabeceras[0] == "Posición"
    assert cabeceras[-1] == "Fin De registro"


@requiere_plantilla
def test_escribir_xls_roundtrip(tmp_path):
    cabeceras = g.leer_cabeceras_plantilla(PLANTILLA_REAL)

    pedido = {
        "codigo_producto": "S0360", "nombre": "Ana", "apellido": "O'Prueba",
        "direccion1": "1 Fake Street", "direccion2": "", "ciudad": "Sydney",
        "provincia": "NSW", "zip": "2000", "pais_iso": "AU",
        "telefono": "+61400000001", "email": "test@example.com", "order_id": "00001",
        "peso_gramos": 240, "largo_cm": 37, "alto_cm": 1, "ancho_cm": 29,
        "instrucciones_no_entrega": "D", "tipo_envio": "2", "es_internacional": True,
        "cantidad_mercancia": 1, "descripcion_mercancia_codigo": "580",
        "peso_neto_gramos": 240, "valor_neto_centimos": 6900, "pais_origen_aduana_iso": "ES",
    }
    filas = [g.construir_fila_salida(pedido, len(cabeceras))]
    out_path = tmp_path / "salida.xls"
    g.escribir_xls(cabeceras, filas, out_path)

    wb = xlrd.open_workbook(str(out_path))
    sh = wb.sheet_by_name(g.PLANTILLA_HOJA)

    assert sh.nrows == 2  # cabecera + 1 fila
    assert sh.row_values(0) == cabeceras

    fila_leida = sh.row_values(1)
    assert fila_leida[0] == "U"  # único registro del fichero
    assert fila_leida[2] == "S0360"
    assert fila_leida[37] == "AU"
    assert fila_leida[-1] == "E"
    for celda in sh.row(1):
        assert celda.ctype in (xlrd.XL_CELL_TEXT, xlrd.XL_CELL_EMPTY)


@requiere_plantilla
def test_main_filtra_nacionales_y_genera_fichero(
    tmp_path, monkeypatch, capsys, fila_square, escribir_csv_square
):
    csv_path = escribir_csv_square([
        fila_square(**{"Order ID": "00001", "Email": "intl@example.com"}),
        fila_square(**{
            "Order ID": "00002", "Email": "nacional@example.com",
            "Shipping Name": "Carla Ficticia", "Shipping Address1": "Calle Inventada 1",
            "Shipping City": "Madrid", "Shipping Zip": "28001", "Shipping Province": "M",
            "Shipping Country": "Spain", "Shipping Phone": "+34600000000",
        }),
    ])
    salida = tmp_path / "salida.xls"

    monkeypatch.setattr(g, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(sys, "argv", [
        "generar_formato_unico.py", str(csv_path),
        "--plantilla", str(PLANTILLA_REAL),
        "-o", str(salida),
    ])

    assert g.main() == 0

    captura = capsys.readouterr()
    assert "Internacionales (exportados): 1" in captura.out
    assert "Nacionales (omitidos" in captura.out
    assert "00002" in captura.out

    wb = xlrd.open_workbook(str(salida))
    sh = wb.sheet_by_name(g.PLANTILLA_HOJA)
    assert sh.nrows == 2  # cabecera + 1 pedido internacional
    assert sh.row_values(1)[42] == "intl@example.com"


@requiere_plantilla
def test_main_agrupa_por_pais(tmp_path, monkeypatch, orders_square_csv):
    csv_path = orders_square_csv

    monkeypatch.setattr(g, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(sys, "argv", [
        "generar_formato_unico.py", str(csv_path),
        "--plantilla", str(PLANTILLA_REAL),
        "--agrupar-por-pais",
    ])

    assert g.main() == 0

    hoy = datetime.date.today().strftime("%d-%m-%Y")
    out_dir = tmp_path / "data" / hoy
    ficheros = sorted(p.name for p in out_dir.glob("*.xls"))
    paises = sorted(n.rsplit("_", 2)[0] for n in ficheros)
    # Spain (pedido 10003) es nacional y no genera fichero
    assert paises == ["Australia", "Colombia", "Germany", "United Kingdom", "United States"]

    [fichero_au] = [out_dir / n for n in ficheros if n.startswith("Australia_")]
    wb = xlrd.open_workbook(str(fichero_au))
    sh = wb.sheet_by_name(g.PLANTILLA_HOJA)
    assert sh.nrows == 3  # cabecera + 2 pedidos de Australia


@requiere_plantilla
def test_main_sin_pedidos_internacionales(
    tmp_path, monkeypatch, capsys, fila_square, escribir_csv_square
):
    csv_path = escribir_csv_square([
        fila_square(**{"Shipping Country": "Spain", "Shipping City": "Madrid"}),
    ])

    monkeypatch.setattr(g, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(sys, "argv", [
        "generar_formato_unico.py", str(csv_path),
        "--plantilla", str(PLANTILLA_REAL),
    ])

    assert g.main() == 0
    captura = capsys.readouterr()
    assert "No hay pedidos internacionales" in captura.out


def test_main_csv_inexistente(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", [
        "generar_formato_unico.py", str(tmp_path / "no-existe.csv"),
    ])
    assert g.main() == 1
    captura = capsys.readouterr()
    assert "no existe" in captura.err.lower()


def test_main_sin_csv_es_error(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["generar_formato_unico.py"])
    with pytest.raises(SystemExit) as exc:
        g.main()
    assert exc.value.code == 2
    assert "csv_path" in capsys.readouterr().err
