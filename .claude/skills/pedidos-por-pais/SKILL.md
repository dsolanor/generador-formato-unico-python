---
name: pedidos-por-pais
description: Agrupa las filas de un CSV de export de pedidos Square/Squarespace (p.ej. data/orders-square.csv) por "Shipping Country", quedándose solo con la primera fila de cada "Order ID" (la que trae los datos completos del comprador y envío) y descartando las filas siguientes del mismo pedido que solo añaden artículos. Genera un CSV por país, con todas las columnas originales, dentro de una carpeta data/<DD-MM-YYYY>/. Usar cuando se pida separar/agrupar pedidos de Correos por país, generar CSV por país de envío, o se invoque "/pedidos-por-pais". No sirve para el formato de export de Big Cartel (columnas distintas, sin "Order ID").
---

# Pedidos por país

Prepara los pedidos de Square/Squarespace para el envío por Correos, agrupándolos por país de destino.

## Invocación

- `/pedidos-por-pais` — usa `data/orders-square.csv` por defecto.
- `/pedidos-por-pais ruta/al/export.csv` — usa el CSV indicado.

## Qué hace

1. Lee el CSV y, para cada `Order ID`, se queda solo con la primera fila (la cabecera del pedido, con email, total y dirección de envío completos) — descarta las filas siguientes del mismo pedido, que solo añaden artículos y vienen con el resto de campos vacíos.
2. Agrupa esas filas por el valor de `Shipping Country`.
3. Escribe un CSV por país (con la cabecera y las 47 columnas originales intactas) en `data/<DD-MM-YYYY>/<Pais>.csv`, usando la fecha de hoy.
4. Si se re-ejecuta el mismo día, sobrescribe los ficheros de esa carpeta con los datos actuales del CSV de origen (no hace merge ni versiona).

Pedidos sin país de envío informado se agrupan en `SIN_PAIS.csv`.

Este formato (columnas `Order ID` y `Shipping Country`) es el de Square/Squarespace. No soporta el export de Big Cartel (p.ej. `data/orders-partially_shipped-*.csv`), que tiene columnas distintas (`Number`, `Shipping country` en minúscula, artículos empaquetados en un solo campo) — el script fallará con un error claro si se le pasa un fichero así.

## Ejecución

Ejecutar:

```
python3 .claude/skills/pedidos-por-pais/scripts/group_orders_by_country.py [ruta_csv_opcional]
```

Reportar al usuario el resumen que imprime el script: número de pedidos distintos, ficheros generados por país con su recuento, avisos (filas omitidas, pedidos sin país) y la carpeta de salida.
