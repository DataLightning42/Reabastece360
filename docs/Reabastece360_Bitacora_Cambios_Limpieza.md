# Reabastece360 — Bitácora de cambios y decisiones de limpieza de datos

**Proyecto:** Reabastece360  
**Módulo:** 4 — Big Data y MLOps  
**Idioma de documentación:** español  
**Última actualización de esta bitácora:** 28 de octubre de 2026  
**Estado:** revisión de códigos no estándar en curso; pendiente validar la ejecución completa del notebook después de aplicar los cambios.

---

## 1. Propósito de esta bitácora

Este documento registra qué se ha cambiado o propuesto en el notebook, por qué se hizo y qué evidencia tenemos. La idea es que el autor pueda volver a leerlo más adelante, comprender las decisiones y explicarlas durante la defensa del proyecto.

Se separan los **resultados observados en una ejecución** de las **expectativas pendientes de verificar**. No se consideran validados los resultados de una modificación hasta que el notebook completo se ejecute desde un kernel reiniciado y se comprueben las salidas.

## 2. Estado inicial y reproducibilidad

Se creó el repositorio local en:

`C:\Users\frank\Reabastece360`

Se copiaron estos archivos desde `D:\Python exercise\integrador-demanda\CHAT GPT SIDE\v2`:

- Notebook: `notebooks/Proyecto_Integrador_Reabastece360_HitoI.ipynb`
- Dataset: `data/raw/online_retail_II.xlsx`

Las copias se verificaron comparando sus hashes SHA-256 con los archivos originales. Ambos archivos coincidieron; los originales de la unidad D: no se modificaron.

El archivo de Excel está dentro de `data/raw/`, y `.gitignore` excluye esa carpeta. Se comprobó con `git check-ignore` que `data/raw/online_retail_II.xlsx` está ignorado por Git. El dataset no debe incorporarse al repositorio.

### Entorno verificado

- Python: 3.14.5 (64 bits)
- pandas: 3.0.3
- openpyxl: 3.1.5
- NumPy: 2.5.1
- PySpark: 4.2.0
- scikit-learn: 1.9.0
- VS Code se utiliza para editar y ejecutar el notebook.
- Directorio de trabajo reportado por el notebook: `C:\Users\frank\Reabastece360\notebooks`
- Ruta del dataset comprobada: `C:\Users\frank\Reabastece360\data\raw\online_retail_II.xlsx`

## 3. Línea base anterior a la modificación del filtro

La ejecución del notebook original desde la nueva carpeta terminó y mostró este resumen:

- Filas originales / limpias: **1,067,371 / 1,003,214**
- Valor bruto estimado de ventas en diciembre de 2010–noviembre de 2011: **£9,632,333.24**
- Productos (SKU) vendidos en esa ventana: **3,789**
- Facturas en la ventana: **18,957**
- Peso de facturas de al menos £500: **65.7 % del valor de ventas**
- Participación del Reino Unido: **84.6 %**; países presentes: **38**
- Líneas de cancelación en el período completo: **1.85 % de las filas deduplicadas**
- Valor de cancelaciones de SKU que cumplían el patrón anterior: **£716,426**
- Participación de ventas septiembre–noviembre: **37.2 %**
- Semana pico / mediana de semana completa: **2.20**
- Mes pico / promedio mensual: **1.81**, noviembre de 2011
- Clase A: **824 SKU (21.7 %)**; clase B: **963 (25.4 %)**; clase C: **2,002 (52.8 %)**
- Patrones de demanda de clase A: erratic 52.9 %, lumpy 25.4 %, smooth 12.5 %, intermittent 9.2 %

Estos datos son la salida observada del notebook antes de la nueva regla. La línea base debe conservarse para comparar los efectos del cambio.

**Importante:** el valor `cantidad × precio` se presenta como una **proxy de valor bruto de ventas**, no como utilidad ni como ingreso contable auditado. Las cancelaciones no se vinculan de forma fiable a una venta original, y los datos no contienen inventario histórico ni faltantes observados.

## 4. Problema detectado en el filtro de SKU

La regla inicial aceptaba códigos que coincidieran con:

```python
patron_producto = r"^\d{5}[A-Z]*$"
```

Esto acepta códigos de cinco dígitos con letras opcionales al final. Es una regla de formato, no una regla de negocio; por tanto, puede excluir productos reales cuyo código tenga letras al principio, guiones bajos u otra estructura.

La auditoría encontró **38 códigos no estándar distintos** y **4,699 filas positivas** que el filtro original eliminaba. Los códigos excluidos incluían categorías diferentes:

- Servicios y cargos: `DOT` (DOTCOM POSTAGE), `POST` (POSTAGE), `C2` (CARRIAGE).
- Transacciones manuales: `M` (Manual).
- Cargos y ajustes financieros: `AMAZONFEE`, `BANK CHARGES`, `B`, `ADJUST`, `ADJUST2`.
- Descuentos: `D`.
- Vales de regalo: `GIFT_0001_10`, `GIFT_0001_20`, y códigos similares.
- Productos físicos probables: varios códigos `DCGS...`, `DCGSSBOY`, `DCGSSGIRL`, `SP1002` y `PADS`.
- Productos de prueba: `TEST001` y `TEST002`.

La auditoría de todos los códigos es evidencia de que el patrón de código, por sí solo, no es suficiente para definir un producto elegible para pronóstico de demanda física.

## 5. Auditoría de excepciones de mercancía

Se inspeccionaron las filas de ocho códigos candidatos durante la ventana del negocio (1 de diciembre de 2010 hasta antes del 1 de diciembre de 2011):

- `DCGSSBOY` — BOYS PARTY BAG
- `DCGSSGIRL` — GIRLS PARTY BAG
- `DCGS0076` — SUNJAR LED NIGHT NIGHT LIGHT
- `DCGS0004` — HAYNES CAMPER SHOULDER BAG
- `DCGS0069` — OOH LA LA DOGS COLLAR
- `DCGS0070` — CAMOUFLAGE DOG COLLAR
- `DCGS0003` — BOXED GLASS ASHTRAY
- `PADS` — PADS TO MATCH ALL CUSHIONS

Resultado observado:

- Filas candidatas: **35**
- Códigos candidatos: **8**
- Valor bruto exacto: **£395.163**

Las descripciones de esos códigos son compatibles con artículos físicos, aunque `PADS` tiene un precio unitario nominal de £0.001 y debe marcarse como una anomalía para revisión. Los códigos `DCGS...` y `DCGSS...` son ejemplos de artículos cuyo formato no cumple el patrón original, pero cuyas descripciones parecen corresponder a mercancía.

Además, se incluyeron en la lista de excepciones auditadas otros códigos de mercancía que aparecen fuera de la ventana anual, para no excluirlos automáticamente de todo el historial si posteriormente se usa esa historia para entrenar modelos.

## 6. Nueva regla propuesta para elegibilidad de productos

La regla propuesta acepta:

1. Códigos que cumplen el patrón estándar, **o**
2. Códigos incluidos de forma explícita en una lista de excepciones revisada.

Lista de excepciones incluida en el código propuesto:

```python
codigos_excepcion_producto = {
    "DCGS0066N",
    "DCGS0041",
    "DCGS0044",
    "DCGS0058",
    "DCGS0062",
    "DCGS0037",
    "DCGS0068",
    "DCGS0075",
    "DCGS0072",
    "DCGS0003",
    "DCGS0004",
    "DCGS0069",
    "DCGS0070",
    "DCGS0076",
    "DCGSSBOY",
    "DCGSSGIRL",
    "PADS",
    "SP1002",
}
```

El propósito de la lista es hacer las excepciones visibles y auditables, en vez de ampliar el patrón hasta aceptar indiscriminadamente códigos que pueden representar cargos, ajustes o transacciones de prueba.

Los códigos que no están en el patrón estándar ni en la lista de excepciones siguen excluidos de la demanda física. Las razones y categorías de exclusión deben quedar documentadas para que se puedan revisar en el futuro.

### Código aplicado en el Paso 4

Se actualizó el Paso 4 para:

- Normalizar temporalmente los códigos (quitar espacios y convertir a mayúsculas) al evaluarlos.
- Generar una tabla de auditoría de códigos no estándar con conteos, descripción y decisión preliminar.
- Aceptar el patrón estándar o una excepción aprobada.
- Calcular las filas excluidas comparando el número de filas antes y después del filtro, en lugar de depender de una resta de contadores anteriores.
- Imprimir el tamaño final del conjunto limpio y la proxy bruta para todos los períodos.

### Salida observada después de aplicar el nuevo Paso 4

La ejecución del Paso 4 modificado mostró:

- Códigos no estándar distintos: **38**
- Filas excluidas por elegibilidad: **4,556**
- Tamaño final de los datos limpios: **(1,003,357, 8)**
- Proxy de ventas positivas brutas en todos los períodos: **£19,643,861.64**

La diferencia de filas respecto de la línea base es de **143 filas adicionales retenidas** (1,003,357 − 1,003,214). Esto es coherente con la inclusión de las excepciones, pero la validación completa requiere ejecutar el notebook desde un kernel reiniciado y revisar el resumen anual posterior.

La salida del Paso 4, por sí sola, **no demuestra aún** que todos los cálculos posteriores estén actualizados ni que la cifra anual final sea la esperada.

## 7. Coherencia en el cálculo de cancelaciones

El código anterior filtraba las líneas de cancelación únicamente con el patrón estándar y `Price > 0`. Eso generaría una población distinta de la usada ahora para ventas positivas, porque las excepciones de mercancía serían aceptadas para las ventas, pero no para las cancelaciones.

Se propuso sustituir esa máscara para que las cancelaciones usen la misma política:

- Código estándar o código incluido en `codigos_excepcion_producto`.
- Precio positivo para el indicador descriptivo de valor cancelado, manteniendo la decisión previa del notebook.
- No se intenta asociar una cancelación con una venta específica.

El código que se propuso para la celda de perfil de negocio es:

```python
# Normalizar los códigos de cancelación para la comparación.
stockcode_canc_norm = (
    df_canc["StockCode"]
    .astype("string")
    .str.strip()
    .str.upper()
)

mascara_canc_codigo = (
    stockcode_canc_norm.str.match(
        patron_producto, na=False
    )
    | stockcode_canc_norm.isin(
        codigos_excepcion_producto
    )
)

mascara_canc_producto = (
    mascara_canc_codigo
    & df_canc["Price"].gt(0)
)

df_canc_producto = df_canc.loc[
    mascara_canc_producto
].copy()

valor_cancelado = -(
    df_canc_producto["Quantity"]
    * df_canc_producto["Price"]
).sum()

peso_canc_valor = (
    valor_cancelado / ventas_brutas
    if ventas_brutas
    else np.nan
)
```

**Estado de esta modificación:** código propuesto para sustituir la lógica de la celda, pero todavía pendiente confirmar una ejecución completa desde kernel reiniciado después de introducirlo. No se debe declarar la nueva cifra de cancelaciones como validada hasta revisar el resultado real.

## 8. Por qué no se emparejan automáticamente las cancelaciones

Los datos no permiten establecer de manera fiable qué cancelación corresponde a cada venta original utilizando únicamente el código de producto, el cliente, la cantidad y el precio. Por esa razón:

- Las ventas positivas elegibles se conservan según las reglas documentadas.
- Las líneas de cancelación se presentan como un indicador separado.
- El valor cancelado se describe como una medida transaccional, no como una medición de pérdidas reales.
- No se afirma que el conjunto de datos demuestre cuántas roturas de stock, ventas perdidas o unidades físicamente devueltas ocurrieron.

## 9. Resultados que siguen pendientes de verificar

Después de guardar las modificaciones y reiniciar el kernel en VS Code, hay que ejecutar **Run All** y revisar:

- [ ] Que el notebook completo finaliza sin errores desde un kernel limpio.
- [ ] Que la tabla de códigos no estándar muestra las decisiones esperadas.
- [ ] Que el tamaño final del conjunto limpio y el conteo de filas son reproducibles.
- [ ] Que el valor bruto anual y el número de SKU se recalculan con el filtro nuevo.
- [ ] Que la clasificación ABC y los patrones de demanda se recalculan sobre la población revisada.
- [ ] Que la cifra de cancelaciones se obtiene usando la misma regla de elegibilidad.
- [ ] Que las cifras de ventas, cancelaciones y proporciones comparan ventanas temporales consistentes o identifican claramente cuando no lo hacen.
- [ ] Que las salidas del informe se actualizan a partir de la ejecución validada.

La cifra aproximada de **£9,632,728.40** para el valor bruto anual se mencionó como expectativa bajo la hipótesis de que la única adición al período anual sea el valor auditado de £395.163. **No es todavía un resultado validado.** Debe confirmarse en el resumen de la ejecución completa.

## 10. Historial de Git

Se han confirmado estos commits locales:

| Commit | Mensaje | Contenido |
|---|---|---|
| `744fc01` | `chore: initialize Reabastece360 project` | Primer `README.md` y `.gitignore`. |
| `672023f` | `data: add exploratory notebook and product code audit` | Notebook exploratorio con la auditoría añadida hasta ese momento. |

El código modificado del Paso 4 y la celda de cancelaciones se trabajaron después de esos commits. **No considerar que esos cambios posteriores están guardados en Git hasta que se confirme su guardado en VS Code y se cree un nuevo commit.**

Las advertencias de Git acerca de convertir LF a CRLF son mensajes de normalización de finales de línea en Windows; no son por sí mismos un error de commit.

## 11. Próximas acciones

1. Guardar el notebook con `Ctrl + S`.
2. Confirmar que el nuevo Paso 4 y la celda de cancelaciones están en las celdas correctas.
3. Reiniciar el kernel y ejecutar **Run All**.
4. Comparar el nuevo resumen anual con la línea base de la sección 3.
5. Revisar las cifras de cancelaciones y de SKU; explicar toda diferencia material.
6. Si todo cuadra, registrar un nuevo commit de Git con un mensaje que describa el cambio de elegibilidad de productos.
7. Con la población de productos validada, construir la matriz semanal SKU-semana y comenzar el pronóstico con un baseline.

---

## 12. Resumen breve para la defensa

> Se detectó que un filtro basado exclusivamente en el formato del código de stock excluía algunos artículos que parecen ser mercancía física. Se auditaron 38 códigos no estándar y se revisaron las transacciones de ocho candidatos presentes en la ventana anual, con 35 filas y £395.163 de valor bruto. Se propuso una lista explícita de excepciones de mercancía, manteniendo fuera cargos, servicios, descuentos, vales, ajustes y productos de prueba. El objetivo es que la regla sea transparente y reproducible. La salida del Paso 4 modificado conserva 1,003,357 filas y una proxy bruta de £19,643,861.64 para todos los períodos; los resultados finales anuales y la coherencia de cancelaciones siguen pendientes de validación mediante una ejecución completa del notebook.
