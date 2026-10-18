import csv
import shutil
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

# Datos 100% ficticios con el mismo formato que el export de Square
# (data/orders-square.csv). Nunca usar data/ en los tests: contiene datos reales.
FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"
ORDERS_SQUARE_FIXTURE = FIXTURES_DIR / "orders-square.csv"


@pytest.fixture
def orders_square_csv(tmp_path):
    """Copia del CSV ficticio en tmp_path, para que ningún test modifique el original."""
    destino = tmp_path / ORDERS_SQUARE_FIXTURE.name
    shutil.copy(ORDERS_SQUARE_FIXTURE, destino)
    return destino


@pytest.fixture
def square_header():
    with ORDERS_SQUARE_FIXTURE.open(encoding="utf-8", newline="") as f:
        return next(csv.reader(f))


@pytest.fixture
def fila_square(square_header):
    """Factoría de filas completas del export de Square con valores ficticios.

    Uso: fila_square(**{"Shipping Country": "Spain"})
    """
    def _crear(**overrides):
        valores = dict.fromkeys(square_header, "")
        valores.update({
            "Order ID": "00001",
            "Email": "test@example.com",
            "Financial Status": "PAID",
            "Currency": "EUR",
            "Subtotal": "69.00",
            "Shipping Name": "Ana O’Prueba",
            "Shipping Address1": "1 Fake Street",
            "Shipping City": "Sydney",
            "Shipping Province": "NSW",
            "Shipping Zip": "2000",
            "Shipping Country": "Australia",
            "Shipping Phone": "'+61400000001",
            "Lineitem quantity": "1",
            "Lineitem name": "Producto de prueba A",
        })
        desconocidas = set(overrides) - set(square_header)
        if desconocidas:
            raise KeyError(f"columnas que no existen en el export de Square: {desconocidas}")
        valores.update(overrides)
        return [valores[campo] for campo in square_header]
    return _crear


@pytest.fixture
def escribir_csv_square(tmp_path, square_header):
    """Escribe en tmp_path un CSV con la cabecera completa de Square y las filas dadas."""
    def _escribir(filas, nombre="pedidos.csv"):
        csv_path = tmp_path / nombre
        with csv_path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f, quoting=csv.QUOTE_ALL)
            writer.writerow(square_header)
            writer.writerows(filas)
        return csv_path
    return _escribir


@pytest.fixture
def args():
    return SimpleNamespace(
        peso_kg=0.24,
        alto_cm=1,
        ancho_cm=29,
        profundo_cm=37,
        codigo_mercancia="580",
        pais_origen_aduana="ES",
        codigo_producto="S0360",
        tipo_envio="2",
        instrucciones_no_entrega="D",
    )
