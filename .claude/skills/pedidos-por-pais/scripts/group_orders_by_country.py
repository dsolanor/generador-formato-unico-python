#!/usr/bin/env python3
"""Agrupa pedidos Square/Squarespace por país de envío en CSV separados."""

import argparse
import csv
import datetime
import re
import sys
from collections import OrderedDict
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[3]
DEFAULT_CSV = REPO_ROOT / "data" / "orders-square.csv"


def sanitize_filename(name: str) -> str:
    name = name.strip() or "SIN_PAIS"
    name = re.sub(r'[\\/:*?"<>|]', "_", name)
    name = re.sub(r"\s+", " ", name).strip()
    return name or "SIN_PAIS"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Agrupa un CSV de pedidos Square/Squarespace por país de envío."
    )
    parser.add_argument(
        "csv_path",
        nargs="?",
        default=None,
        help=f"Ruta al CSV de pedidos (por defecto: {DEFAULT_CSV})",
    )
    args = parser.parse_args()

    csv_path = Path(args.csv_path).resolve() if args.csv_path else DEFAULT_CSV

    if not csv_path.exists():
        print(f"Error: no existe el fichero '{csv_path}'", file=sys.stderr)
        return 1

    with csv_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            print(f"Error: '{csv_path}' está vacío", file=sys.stderr)
            return 1

        try:
            order_id_idx = header.index("Order ID")
            shipping_country_idx = header.index("Shipping Country")
        except ValueError:
            print(
                f"Error: '{csv_path}' no tiene el formato esperado "
                "(faltan las columnas 'Order ID' y/o 'Shipping Country'). "
                "Esta skill no soporta el formato de export de Big Cartel.",
                file=sys.stderr,
            )
            return 1

        kept = OrderedDict()
        warnings = []
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
            if order_id not in kept:
                kept[order_id] = row

    groups = OrderedDict()
    for row in kept.values():
        country = row[shipping_country_idx].strip()
        if not country:
            warnings.append(
                f"pedido {row[order_id_idx]}: 'Shipping Country' vacío — agrupado en SIN_PAIS"
            )
            country = "SIN_PAIS"
        groups.setdefault(country, []).append(row)

    date_str = datetime.date.today().strftime("%d-%m-%Y")
    out_dir = REPO_ROOT / "data" / date_str
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"Pedidos distintos encontrados: {len(kept)}")
    for country, rows in groups.items():
        filename = sanitize_filename(country) + ".csv"
        out_path = out_dir / filename
        with out_path.open("w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f, quoting=csv.QUOTE_ALL, lineterminator="\n")
            writer.writerow(header)
            writer.writerows(rows)
        print(f"  {country}: {len(rows)} pedido(s) -> {out_path}")

    if warnings:
        print("\nAvisos:")
        for w in warnings:
            print(f"  - {w}")

    print(f"\nCarpeta de salida: {out_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
