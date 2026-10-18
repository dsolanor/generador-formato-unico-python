# Generador de Formato Único de Correos

Genera un fichero `.xls` listo para la carga masiva de envíos de Correos a
partir del export de pedidos de Square/Squarespace.

## Qué hace

Toma el CSV de pedidos que le indiques, se queda con una única
fila por pedido (la que trae los datos completos de comprador y dirección de
envío; ignora las líneas de producto) y genera un `.xls` con exactamente las
mismas columnas, en el mismo orden, que la plantilla oficial
`vendor/template/PlantillaFicheroFormatoUnico.xls`, listo para subir al
portal de Correos. Sigue la especificación oficial del Formato Único
(versión 2018v002, ver `GuiadeAyuda`): marca correctamente los campos
obligatorios (Posición C/F/R/U, Año de versión, Total Bultos, Fin de
registro...), usa código ISO-2 de país, peso en gramos y valor en céntimos
donde la especificación lo exige.

**Solo exporta envíos internacionales** (destino distinto de España). Los
pedidos nacionales se detectan y se omiten del fichero — se cuentan en el
resumen de la ejecución (con sus `Order ID`), pero hay que gestionarlos por
otra vía.

## CSV de entrada

El CSV de entrada es **obligatorio** y debe ser el export de pedidos de
la tienda de **Squarespace**, sin modificar: una
cabecera con 47 columnas (`Order ID`, `Email`, `Financial Status`, …,
`Shipping Name`, `Shipping Address1`, `Shipping Country`, `Shipping Phone`,
…, `Payment Reference`) y una fila por cada artículo del pedido. Solo la
primera fila de cada `Order ID` trae los datos del comprador y del envío;
las siguientes solo añaden artículos y se ignoran.

Ejemplo (datos ficticios, se muestran solo 2 de las N columnas):

| Order ID | Email | … |
|---|---|---|
| 10001 | cliente10001@example.com | … |
| 10001 | | … |
| 10002 | cliente10002@example.com | … |
| … | … | … |

Las columnas imprescindibles son `Order ID`, `Email` y `Shipping Address1`.
Si faltan, el script se detiene con un error. El export de Big Cartel no es
compatible.

Hay un ejemplo completo con datos ficticios en
`tests/fixtures/orders-square.csv`.

> Los CSV reales contienen datos personales de clientes: guárdalos en
> `data/`, que está en `.gitignore`, y no los subas nunca al repositorio.

## Instalación y uso con Make

```bash
make install            # crea el entorno virtual e instala dependencias
make generar CSV=data/orders-square.csv            # genera el .xls de envíos internacionales (fichero único)
make generar-por-pais CSV=data/orders-square.csv   # genera un .xls por país de envío
make clean              # borra el entorno virtual y los __pycache__
make help                # lista los targets disponibles
```

`make generar`/`make generar-por-pais` crean e instalan el entorno virtual
automáticamente si no existe — no hace falta ejecutar `make install` antes.
Si no se pasa `CSV=<ruta>`, fallan con un error.

## Instalación manual (alternativa, sin Make)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Uso básico (manual)

```bash
source .venv/bin/activate
python3 scripts/generar_formato_unico.py data/orders-square.csv
```

Genera `data/<DD-MM-YYYY>/envios-correos_<DD-MM-YYYY_HHMMSS>.xls` con todos
los pedidos (el nombre lleva fecha y hora para no pisar ficheros de
ejecuciones anteriores el mismo día).

## Agrupar por país

```bash
python3 scripts/generar_formato_unico.py data/orders-square.csv --agrupar-por-pais
```

Genera un `.xls` por país de envío en
`data/<DD-MM-YYYY>/<País>_<DD-MM-YYYY_HHMMSS>.xls`, en vez de un único
fichero.

## Opciones

| Flag | Por defecto | Descripción |
|---|---|---|
| `csv_path` (posicional, **obligatorio**) | — | Ruta al CSV de pedidos exportado de Squarespace |
| `--plantilla` | `vendor/template/PlantillaFicheroFormatoUnico.xls` | Ruta a la plantilla .xls |
| `-o`, `--salida` | `data/<DD-MM-YYYY>/envios-correos_<DD-MM-YYYY_HHMMSS>.xls` | Ruta del .xls de salida (solo si no se usa `--agrupar-por-pais`) |
| `--agrupar-por-pais` | desactivado | Genera un .xls por país en vez de un único fichero |
| `--peso-kg` | `0.24` | Peso fijo por paquete (kg) |
| `--alto-cm` | `1` | Alto fijo (cm) |
| `--ancho-cm` | `29` | Ancho fijo (cm) |
| `--profundo-cm` | `37` | Profundo/largo fijo (cm) |
| `--codigo-mercancia` | `580` (Textiles - Algodón) | Código de mercancía (Anexo II) para la declaración de aduana |
| `--pais-origen-aduana` | `ES` | Código ISO-2 del país de origen declarado en aduana |
| `--codigo-producto` | `S0360` (Paq Light Internacional) | Código de producto (Anexo I) — ajústalo si no corresponde a tu contrato |
| `--tipo-envio` | `2` (Venta de Mercancías) | Tipo de envío (campo 111) |
| `--instrucciones-no-entrega` | `D` (Devolver al remitente) | Instrucciones si no hay entrega: `D` Devolver al remitente / `A` Tratar como abandonado |

Los valores por defecto de peso, medidas y códigos de Correos están en
`scripts/constantes.py`: edítalos ahí si cambian para todos los envíos, o
usa los flags para una ejecución concreta.

Ejemplo cambiando el peso:

```bash
python3 scripts/generar_formato_unico.py data/otro-export.csv --peso-kg 0.5
```

## Datos que quedan sin rellenar

El código de producto y el tipo de envío ya se rellenan automáticamente con
valores por defecto razonables (ver tabla de opciones arriba) — ajústalos con
los flags si no corresponden a tu contrato real con Correos.

Quedan sin rellenar, porque no vienen en el CSV y son opcionales según la
especificación (Correos los toma de tu cuenta si no se informan):

- **Datos de contrato** (tipo de franqueo, código etiquetador, número de
  contrato, número de cliente, número de máquina de franquear).
- **Datos del remitente** (tu nombre, dirección, localidad, CP, provincia,
  país, teléfono, email) — se repetirían igual en todas las filas.

El fichero se puede subir así: Correos usa los datos de remitente y de
contrato de la cuenta con la que lo cargas.

## Tests

```bash
make test               # instala pytest (si falta) y ejecuta toda la suite
```

Los tests viven en `tests/` y cubren las funciones puras (saneado de texto,
teléfono, resolución de país ISO-2, deduplicación del CSV, construcción de
filas) y el flujo completo (`main()` de principio a fin, incluyendo el
filtrado de pedidos nacionales y el modo `--agrupar-por-pais`), usando la
plantilla real de `vendor/template/` y ficheros temporales — no tocan
`data/` ni generan ficheros reales del proyecto.

Los datos de prueba son ficticios: `tests/fixtures/orders-square.csv` imita
el export de Squarespace, y `tests/conftest.py` expone las fixtures
`orders_square_csv`, `square_header`, `fila_square(**overrides)`,
`escribir_csv_square(filas)` y `args`. No uses nunca datos de `data/` en los
tests.

## Reutilización

El script no necesita cambios para volver a usarse: cada vez que haya un
nuevo export de pedidos, basta con ejecutarlo de nuevo apuntando al CSV
correspondiente.
