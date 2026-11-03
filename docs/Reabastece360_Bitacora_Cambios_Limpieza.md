# Reabastece360 — Bitácora de cambios, decisiones y validación

**Proyecto:** Reabastece360  
**Módulo:** 4 — Big Data y MLOps  
**Fecha de actualización:** 2 de noviembre de 2026
**Responsable:** estudiante (proyecto individual)  
**Estado general:** prototipo académico HITO II desarrollado y validado localmente. Se completaron la preparación de demanda semanal, el procesamiento con PySpark, la comparación de modelos de pronóstico, las pruebas de persistencia compatibles con MongoDB, la demostración ilustrativa de reposición y las evaluaciones de Design Thinking, viabilidad técnica y financiera. El notebook se ejecutó satisfactoriamente desde un kernel reiniciado y la prueba automatizada de persistencia fue aprobada.

> **Cómo leer esta bitácora:** distingue los resultados observados en el notebook de las decisiones metodológicas y de las tareas todavía pendientes. No considerar una tarea finalizada solo porque se haya propuesto código: debe ejecutarse, revisarse y documentarse el resultado real.

---

## 1. Propósito

Esta bitácora registra los cambios hechos en el notebook, por qué se hicieron, qué evidencia los motivó y cómo se validaron. Su propósito es mantener la trazabilidad y ayudar al autor a comprender y defender las decisiones durante la evaluación académica.

Criterio de trabajo acordado: **implementar → explicar → validar → documentar → guardar en Git**.

La documentación del proyecto se redacta en español. Las explicaciones de mentoría se mantienen en inglés, salvo solicitud en contrario.

## 2. Contexto, alcance y limitaciones del negocio

Reabastece360 es un prototipo académico para pronosticar demanda semanal por producto y generar recomendaciones transparentes de reposición para un mayorista británico ficticio de artículos de regalo.

La fuente de datos es **Online Retail II**, del UCI Machine Learning Repository, publicada bajo licencia CC BY 4.0. La ventana anual de negocio empleada en el Business Case es del **1 de diciembre de 2010 al 30 de noviembre de 2011**.

El archivo contiene transacciones, pero no proporciona un historial fiable del inventario disponible, plazos de entrega de proveedores ni faltantes de stock observados. Por tanto:

- el cálculo `Quantity × Price` se denomina *proxy de valor bruto de ventas*, no utilidad ni ingreso contable auditado;
- las cancelaciones se analizan por separado si no es posible relacionarlas de forma fiable con la venta original;
- una prueba de reposición futura será una simulación basada en supuestos explícitos, no evidencia de ahorros, faltantes o excesos de inventario reales.

## 3. Entorno y estructura reproducible

### 3.1 Entorno comprobado

- Python: 3.14.5, 64 bits.
- Java: OpenJDK 21.0.12.1 LTS.
- Git: `2.56.0.windows.4`.
- pandas: 3.0.3.
- openpyxl: 3.1.5.
- NumPy: 2.5.1.
- PySpark: 4.2.0.
- scikit-learn: 1.9.0.
- VS Code se utiliza para editar y ejecutar el notebook. No se requiere instalar por separado la interfaz clásica de Jupyter Notebook o JupyterLab para continuar con este flujo.

El kernel de VS Code reportó el ejecutable `C:\Users\frank\AppData\Local\Programs\Python\Python314\python.exe` y el directorio de trabajo `C:\Users\frank\Reabastece360\notebooks`.

### 3.2 Archivos del proyecto

Raíz del repositorio local:

`C:\Users\frank\Reabastece360`

Archivos pertinentes:

- `notebooks/Proyecto_Integrador_Reabastece360_HitoI.ipynb`
- `data/raw/online_retail_II.xlsx`
- `docs/Reabastece360_Bitacora_Cambios_Limpieza.md`
- `.gitignore`
- `README.md`

El notebook y el archivo Excel se copiaron desde `D:\Python exercise\integrador-demanda\CHAT GPT SIDE\v2`. Las copias se verificaron mediante SHA-256 y coincidieron con los archivos fuente; los originales en D: no se modificaron.

La carpeta `data/` aparece ignorada por Git y se comprobó que la regla `.gitignore` protege `data/raw/online_retail_II.xlsx`. El Excel de aproximadamente 45.6 MB no se debe agregar al repositorio ni a sus commits.

### 3.3 Identidad y privacidad de Git

Git se configuró con un nombre de autor elegido por el usuario y el correo `noreply` de GitHub para evitar exponer el correo personal en los metadatos de los commits. El correo real no se registra en esta bitácora.

Los avisos de Git indicando que `LF` se convertirá a `CRLF` son advertencias de finales de línea en Windows; no impidieron los commits.

---

## 4. Historial de Git confirmado

| Commit | Mensaje | Alcance |
|---|---|---|
| `744fc01` | `chore: initialize Reabastece360 project` | Primer `README.md` y `.gitignore`; inicialización del repositorio en `main`. |
| `672023f` | `data: add exploratory notebook and product code audit` | Incorporación del notebook exploratorio y la primera auditoría de códigos de producto. |
| `1e8a07b` | `data: refine SKU eligibility and document cleaning results` | Notebook revisado y bitácora con la regla de elegibilidad revisada y los resultados reportados. |

El último commit reportado fue creado correctamente. El estado posterior no mostró archivos modificados sin guardar en la salida compartida. Para continuar, comprobar `git status --short` antes de realizar nuevos cambios o commits.

## 5. Línea base: resultados antes del cambio de elegibilidad

La ejecución del notebook original desde el nuevo directorio produjo el siguiente resumen:

| Indicador | Línea base reportada |
|---|---:|
| Filas originales / filas limpias | 1,067,371 / 1,003,214 |
| Proxy de valor bruto de ventas, dic. 2010–nov. 2011 | £9,632,333.24 |
| SKU vendidos en la ventana anual | 3,789 |
| Facturas en la ventana anual | 18,957 |
| Mediana del valor por factura | £302 |
| Facturas de al menos £500 / valor de ventas | 65.7 % |
| Participación del Reino Unido / países presentes | 84.6 % / 38 |
| Líneas de cancelación como porcentaje de filas deduplicadas, período completo | 1.85 % |
| Valor cancelado en SKU que cumplían el patrón anterior | aproximadamente £716,426 |
| Participación del valor de ventas en sep.–nov. | 37.2 % |
| Semana pico / mediana de semana completa | 2.20 |
| Mes pico / promedio mensual | 1.81 (noviembre de 2011) |
| Clase A / B / C | 824 / 963 / 2,002 SKU |
| Patrones de demanda en clase A | erratic 52.9 %; lumpy 25.4 %; smooth 12.5 %; intermittent 9.2 % |
| Mediana de semanas con venta en clase A | 49 de 53 |

Estos valores son la línea base reportada. Se conservan para comparar los efectos de los cambios. Los importes de cancelaciones corresponden al período completo disponible, no a la ventana anual del Business Case.

## 6. Cambio 1 — Auditoría de códigos de producto no estándar

### 6.1 Problema identificado

La regla original de elegibilidad era:

```python
patron_producto = r"^\d{5}[A-Z]*$"
mascara_producto = df_clean["StockCode"].str.match(patron_producto, na=False)
```

El patrón reconoce códigos con cinco dígitos seguidos de letras opcionales. Es una regla de formato, no una definición completa del significado comercial del código. Puede excluir productos físicos válidos y, al mismo tiempo, no decide por sí sola si una línea representa mercancía, un servicio, un descuento o un ajuste.

### 6.2 Evidencia de la auditoría

La auditoría identificó **38 códigos no estándar distintos** y **4,699 filas positivas** antes de aplicar la nueva política. La lista contenía varias categorías:

- servicios o cargos: `DOT` (DOTCOM POSTAGE), `POST` (POSTAGE), `C2` (CARRIAGE);
- transacciones manuales: `M` (Manual);
- comisiones y ajustes: `AMAZONFEE`, `BANK CHARGES`, `B`, `ADJUST`, `ADJUST2`;
- descuentos: `D`;
- vales de regalo: códigos `GIFT_0001_...`;
- productos de prueba: `TEST001`, `TEST002`;
- artículos con descripciones compatibles con mercancía física: varios códigos `DCGS...`, `DCGSSBOY`, `DCGSSGIRL`, `SP1002` y `PADS`.

Se concluyó que el formato del código por sí solo no era una regla suficiente para definir la elegibilidad para un pronóstico de demanda física.

### 6.3 Revisión de candidatos

Se inspeccionaron transacciones de ocho códigos candidatos dentro de la ventana anual:

| Código | Descripción |
|---|---|
| `DCGSSBOY` | BOYS PARTY BAG |
| `DCGSSGIRL` | GIRLS PARTY BAG |
| `DCGS0076` | SUNJAR LED NIGHT NIGHT LIGHT |
| `DCGS0004` | HAYNES CAMPER SHOULDER BAG |
| `DCGS0069` | OOH LA LA DOGS COLLAR |
| `DCGS0070` | CAMOUFLAGE DOG COLLAR |
| `DCGS0003` | BOXED GLASS ASHTRAY |
| `PADS` | PADS TO MATCH ALL CUSHIONS |

Resultado observado en la auditoría: **35 filas**, **8 códigos distintos** y **£395.163** de valor bruto. Las descripciones son compatibles con artículos físicos, aunque `PADS` tiene un precio unitario de £0.001 y debe conservarse como anomalía de precio. Otros códigos tipo mercancía incluidos en la lista de excepciones aparecen fuera de la ventana anual y podrían ser relevantes para el histórico completo.

## 7. Cambio 2 — Regla revisada de elegibilidad de SKU

Se sustituyó la decisión basada únicamente en el patrón por una regla auditable que acepta:

1. códigos que cumplen el patrón estándar; **o**
2. códigos incluidos explícitamente en una lista de excepciones de mercancía revisada a partir de la auditoría.

La lista utilizada en el notebook es:

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

El código normaliza los valores del `StockCode` para la comparación (espacios externos y mayúsculas), construye la tabla de auditoría, acepta el patrón estándar o una excepción y calcula las filas excluidas comparando el tamaño del DataFrame antes y después del filtro.

Los servicios, cargos, ajustes, descuentos, vales de regalo y códigos de prueba no incluidos en la lista siguen fuera del conjunto para demanda física. La clasificación es una regla de negocio documentada y revisable, no una prueba de inventario real. `PADS` se retiene para análisis de unidades y queda marcado para revisión del precio nominal.

### 7.1 Salida observada inmediatamente después del Paso 4 revisado

| Indicador | Resultado reportado |
|---|---:|
| Códigos no estándar distintos auditados | 38 |
| Filas excluidas por elegibilidad | 4,556 |
| Filas del DataFrame limpio | 1,003,357 |
| Proxy de valor bruto de ventas positivas, todos los períodos | £19,643,861.64 |

La nueva regla conserva **143 filas adicionales** respecto a la línea base anterior (`1,003,357 − 1,003,214`).

## 8. Cambio 3 — Coherencia entre ventas positivas y cancelaciones

La máscara anterior de cancelaciones aceptaba solo códigos del patrón estándar y `Price > 0`, lo que daba una población diferente de la empleada para las ventas positivas después de añadir las excepciones.

Se actualizó la lógica propuesta/aplicada en la celda de perfil del negocio para normalizar `StockCode` y aceptar el patrón estándar o la lista `codigos_excepcion_producto`. Se conservó la condición `Price > 0` para el indicador descriptivo del valor cancelado.

Reglas de interpretación:

- las cancelaciones se reportan como indicador separado;
- no se emparejan automáticamente con ventas originales;
- el valor no equivale a pérdidas reales, devoluciones físicas demostradas ni roturas de stock;
- el porcentaje de cancelaciones corresponde al período completo disponible y se debe distinguir del valor bruto anual.

## 9. Resultados reportados después de ejecutar el notebook completo

El usuario compartió el siguiente resumen tras aplicar los cambios. La tabla reproduce resultados reportados desde VS Code; no representa una ejecución independiente en este entorno.

| Indicador | Resultado actualizado |
|---|---:|
| Filas originales / limpias | 1,067,371 / 1,003,357 |
| Proxy de valor bruto anual (dic. 2010–nov. 2011) | £9,632,728.40 |
| SKU vendidos en la ventana anual | 3,797 |
| Facturas en la ventana anual | 18,957 |
| Mediana por factura | £302 |
| Peso de facturas de al menos £500 en el valor | 65.7 % |
| Reino Unido / países presentes | 84.6 % / 38 |
| Cancelaciones como porcentaje de filas deduplicadas, período completo | 1.85 % |
| Valor cancelado en SKU elegibles, período completo | aproximadamente £716,463 |
| Valor cancelado / ventas brutas elegibles | aproximadamente 3.6 % |
| Participación de sep.–nov. en ventas anuales | 37.2 % |
| Semana pico / mediana semanal | 2.20 |
| Mes pico / promedio mensual | 1.81 (noviembre de 2011) |
| Clase A / B / C | 824 (21.7 %) / 964 (25.4 %) / 2,009 (52.9 %) |
| Patrones de demanda clase A | erratic 52.9 %; lumpy 25.4 %; smooth 12.5 %; intermittent 9.2 % |
| Mediana de semanas con venta clase A | 49 de 53 |

### 9.1 Conciliación con la línea base

- Valor bruto anual: `£9,632,728.40 − £9,632,333.24 = £395.16` de diferencia redondeada a dos decimales, coherente con las filas candidatas auditadas (`£395.163`).
- SKU vendidos en la ventana anual: `3,797 − 3,789 = 8` SKU adicionales.
- Filas limpias: `1,003,357 − 1,003,214 = 143` filas adicionales retenidas.
- Valor cancelado elegible: el resumen lo presenta como aproximadamente £716,463, frente al valor anterior aproximado de £716,426; ambos están redondeados a libras en las salidas compartidas.
- ABC: `824 + 964 + 2,009 = 3,797` SKU, coherente con el total de SKU anuales.

La diferencia del valor bruto anual es coherente con el valor de las excepciones. El indicador de cancelaciones se ha actualizado, pero sigue siendo un indicador descriptivo de todo el período y no debe interpretarse como una medición de pérdidas.

### 9.2 Etiqueta del indicador de cancelaciones

La etiqueta anterior «Valor cancelado en SKU de patrón aceptado» quedó desactualizada tras añadir excepciones. Se debe usar una etiqueta descriptiva como:

`Valor cancelado en SKU elegibles (patrón estándar + excepciones auditadas)`

El cambio de etiqueta solo mejora la descripción; no modifica la fórmula. La salida completa compartida por el usuario se produjo antes de que se informara el cambio de etiqueta. Confirmar que el texto se guardó en el notebook actualizado si se necesita comprobarlo; el cálculo de cancelaciones sí fue reportado como actualizado.

## 10. Diagnóstico de calidad después de la limpieza

El usuario ejecutó un diagnóstico de `df_clean` y reportó:

- forma del DataFrame: `(1,003,357, 9)`;
- columnas: `Invoice`, `StockCode`, `Description`, `Quantity`, `InvoiceDate`, `Price`, `Customer ID`, `Country`, `Revenue`;
- `Quantity`: `int64`; `InvoiceDate`: `datetime64[us]`; `Price` y `Revenue`: `float64`; `Invoice` y `StockCode`: texto; `Description`: objeto; `Customer ID`: `float64`; `Country`: texto;
- cobertura de fecha: `2009-12-01 07:45:00` a `2011-12-09 12:50:00`;
- fechas ausentes: 0; códigos de producto ausentes: 0; cantidades no positivas: 0; precios no positivos: 0;
- SKU distintos en todo el historial limpio: 4,725;
- suma de cantidades: 11,188,061 unidades.

Los 4,725 SKU corresponden al historial completo limpio, mientras que 3,797 es el número de SKU vendidos en la ventana anual del Business Case. Son poblaciones y períodos diferentes, por lo que no se deben tratar como cifras contradictorias.

La ausencia de cantidades y precios no positivos es consistente con el filtro actual; no implica que el origen no contuviera filas inválidas, sino que esas filas ya se retiraron antes de este diagnóstico.

## 11. Planificación inicial de la agregación semanal SKU-semana

**Estado histórico (28 de octubre de 2026):** En esta etapa se definieron los requisitos y las comprobaciones necesarias para construir el conjunto semanal de demanda. La implementación todavía estaba pendiente en ese momento.

**Estado actualizado (2 de noviembre de 2026):** La agregación semanal fue implementada y validada. Se obtuvieron 4,691 SKU, 103 semanas y 483,173 combinaciones SKU-semana. La comparación entre Pandas y PySpark confirmó 189,366 grupos con ventas registradas, sin diferencias en las cantidades agregadas. Los resultados y las validaciones se detallan en las secciones 14.2 y 14.3.

Objetivo: construir una tabla de demanda semanal por producto para usarla como base de evaluación de pronósticos. Se propuso crear `df_weekly_demand` sin sobrescribir `df_clean`, con las siguientes columnas:

- `StockCode`
- `WeekStart`
- `Description`
- `DemandUnits`
- `GrossSalesValue`
- `TransactionLines`

El diseño propuesto es:

1. filtrar una ventana de modelado con semanas completas de lunes a domingo, propuesta desde el 7 de diciembre de 2009 hasta el 27 de noviembre de 2011;
2. determinar el lunes de cada semana usando semanas que terminan en domingo;
3. agregar las transacciones por `StockCode` y `WeekStart`, sumando unidades y valor bruto y contando líneas;
4. rellenar con demanda cero únicamente los huecos entre la primera y la última semana observada de cada SKU, sin extender automáticamente la serie antes de la primera venta o después de la última;
5. comprobar que no haya duplicados SKU-semana, que `WeekStart` caiga en lunes y que las unidades sean no negativas.

### Supuestos que deben revisarse antes de aprobar el código

- Que no haya transacciones registradas en una semana no demuestra que el producto estuviera en stock y disponible; el cero es una convención de demanda observada.
- Debe validarse que la suma de `DemandUnits` en la tabla semanal sea igual a la suma de cantidades de las transacciones incluidas en la misma ventana.
- El día de inicio y final y las semanas completas deben explicarse claramente; no se debe mezclar esta ventana con la ventana anual de negocio.
- Se deben revisar productos de demanda intermitente y cantidades inusualmente elevadas antes de entrenar modelos.
- Las variables futuras o los promedios móviles que incluyan la semana objetivo no deben usarse como predictores; se debe prevenir fuga de datos.
- Esta primera agregación se propuso en pandas para validar la lógica. La transformación reutilizable para el pipeline debe implementarse después en PySpark, si procede, y validarse contra una referencia equivalente.

No se debe decir que `df_weekly_demand` existe ni que la agregación semanal ha pasado pruebas hasta que el usuario ejecute el código y comparta la salida.

## 12. Resumen breve para la defensa académica

> Se detectó que un filtro basado exclusivamente en el formato del código de stock excluía algunos artículos cuyas descripciones eran compatibles con mercancía física. Se auditaron 38 códigos no estándar y se revisaron transacciones de ocho candidatos dentro de la ventana anual, con 35 filas y £395.163 de valor bruto. Se aplicó una lista explícita y revisable de excepciones para mercancía, manteniendo fuera servicios, cargos, descuentos, vales, ajustes y productos de prueba. Según el resumen del notebook compartido después de los cambios, el conjunto limpio contiene 1,003,357 filas; el proxy del valor bruto anual es £9,632,728.40 y se identifican 3,797 SKU vendidos. El valor cancelado elegible, aproximadamente £716,463, corresponde al período completo y es descriptivo; no mide pérdidas reales ni demuestra faltantes. El conjunto no contiene un historial fiable de inventario o roturas de stock. La siguiente fase será crear y validar la demanda semanal por SKU.

## 13. Checklist de seguimiento

### Completado según la evidencia compartida

- [x] Inicializar el repositorio local y crear `README.md` y `.gitignore`.
- [x] Configurar Git con correo privado de GitHub.
- [x] Copiar notebook y Excel y verificar sus hashes SHA-256.
- [x] Confirmar que `data/raw/online_retail_II.xlsx` está ignorado por Git.
- [x] Ejecutar el notebook original desde el nuevo directorio.
- [x] Auditar 38 códigos no estándar.
- [x] Revisar las transacciones de ocho códigos candidatos.
- [x] Implementar la lista de excepciones de mercancía en Paso 4.
- [x] Aplicar la regla de elegibilidad revisada al cálculo de cancelaciones, según la salida que compartió el usuario.
- [x] Obtener el resumen anual revisado y comprobar la conciliación básica de filas, valor anual y SKU.
- [x] Guardar commits `744fc01`, `672023f` y `1e8a07b`.
- [x] Guardar la bitácora en `docs/` y registrar el resumen de resultados revisados.
- [x] Construir la matriz `demanda_semanal` y conciliar las unidades con las transacciones de la misma ventana temporal.
- [x] Revisar ejemplos de series SKU-semana y semanas sin ventas registradas.
- [x] Implementar la agregación en PySpark y verificar su equivalencia con Pandas: 189,366 grupos y cero diferencias.
- [x] Evaluar tres métodos de referencia y tres modelos de aprendizaje automático mediante separación cronológica.
- [x] Implementar y verificar una regla ilustrativa de punto de reposición con parámetros hipotéticos y redondeo a unidades enteras.

### Pendiente

- [ ] Confirmar que la etiqueta de cancelaciones en el notebook guardado refleja la regla de elegibilidad actualizada.
- [x] Ejecutar el notebook completo desde un kernel reiniciado, sin errores.
- [x] Confirmar el estado del repositorio mediante `git status --short`.
- [x] Implementar una regla ilustrativa de reposición con supuestos explícitos. No se desarrolló una simulación integral de políticas de inventario.
- [x] Completar la documentación de Design Thinking, incluyendo una consulta cualitativa con una persona experimentada en planificación de demanda.
- [x] Completar la evaluación de viabilidad técnica y los escenarios financieros con análisis del punto de equilibrio.
- [x] Ejecutar las pruebas automatizadas de persistencia: 1 prueba aprobada mediante pytest.
- [ ] Revisar los archivos que se incorporarán al commit y sincronizar el repositorio con GitHub.
- [ ] Confirmar la entrega académica en los espacios correspondientes a HITO II y HITO III.

---

**Fin de la bitácora, versión actualizada al 28 de octubre de 2026.** La próxima sesión debe continuar por la validación de la agregación semanal SKU-semana, no repetir la configuración del entorno ni la auditoría ya documentada.


## 14. Avance técnico del HITO II — 2 de noviembre de 2026

### 14.1. Actualización del alcance académico

El docente confirmó que el proyecto debe implementar al menos tres tecnologías, seleccionadas por su utilidad para la solución propuesta. También informó que el HITO III y la defensa oral fueron cancelados. La entrega final del HITO II deberá cargarse en ambos espacios de entrega antes del 3 de noviembre de 2026 a medianoche.

En consecuencia, se priorizó la construcción y validación del prototipo analítico, evitando desarrollar componentes adicionales como API REST, Docker o almacenamiento S3 que no resultan indispensables bajo las instrucciones actualizadas.

### 14.2. Preparación de demanda semanal

Se construyó una matriz de ventas semanales por producto a partir de las transacciones positivas elegibles, utilizando semanas completas comprendidas entre diciembre de 2009 y noviembre de 2011.

**Resultados de la ejecución:**

| Indicador | Resultado |
|---|---:|
| SKU identificados | 4,691 |
| Semanas completas | 103 |
| Registros SKU-semana | 483,173 |
| Combinaciones con ventas registradas | 189,366 |
| Combinaciones sin ventas registradas | 293,807 |
| Unidades vendidas agregadas | 10,642,073 |

Las semanas sin transacciones se representaron mediante cero. Esta decisión permite construir series temporales regulares, aunque no demuestra que la demanda real fuera nula, puesto que se desconoce la disponibilidad histórica de los productos.

Se comprobaron la ausencia de combinaciones duplicadas de SKU y semana, la no negatividad de las cantidades y la conciliación del total de unidades contra las transacciones utilizadas.

### 14.3. Procesamiento con PySpark

Se implementó una transformación de ventas semanales mediante PySpark 4.2.0 en modo local.

El procesamiento utiliza un archivo CSV intermedio generado a partir de los datos previamente depurados en Pandas. PySpark realiza la lectura con un esquema explícito, determina la semana correspondiente y agrupa las cantidades vendidas por producto.

La comparación entre Pandas y PySpark produjo:

- 189,366 combinaciones SKU-semana en ambos motores.
- 10,642,073 unidades agregadas en ambos motores.
- Cero diferencias en las cantidades al comparar cada combinación.
- Cero filas con campos nulos detectadas en la lectura de Spark.

Con ello se verificó la equivalencia de la agregación semanal observada entre ambas implementaciones. El resultado no constituye una medición comparativa de velocidad ni demuestra una ventaja de rendimiento de PySpark frente a Pandas.

### 14.4. Experimento de pronóstico

Para evaluar métodos de predicción semanal se seleccionaron 3,135 SKU mediante criterios calculados exclusivamente con datos anteriores al inicio de la validación: al menos 12 semanas con ventas positivas y 30 unidades acumuladas.

Se estableció una separación cronológica de 79 semanas de entrenamiento, 12 semanas de validación y 12 semanas de prueba. El pronóstico evaluado corresponde a un horizonte móvil de una semana, utilizando observaciones históricas anteriores a cada semana objetivo.

Se generaron variables de rezago de una, dos, cuatro y ocho semanas, promedios móviles de cuatro y ocho semanas y representaciones cíclicas de la semana del año.

**Resultados de validación:**

| Método | MAE | RMSE | WAPE | Sesgo |
|---|---:|---:|---:|---:|
| Promedio móvil de 4 semanas | 18.610 | 66.742 | 79.131% | 0.172 |
| HistGradientBoosting | 19.252 | 62.304 | 81.858% | 1.859 |
| KNN | 20.530 | 70.327 | 87.295% | 1.539 |
| Ridge | 24.074 | 63.855 | 102.362% | 5.352 |

Se verificó que los modelos fueron comparados sobre las mismas 37,620 observaciones de validación.

El promedio móvil de cuatro semanas obtuvo los menores valores de MAE y WAPE, mientras que HistGradientBoosting presentó el menor RMSE. Se seleccionó provisionalmente el promedio móvil como método de referencia para la siguiente etapa del prototipo.

Los resultados no demuestran que los algoritmos de aprendizaje automático sean inferiores en cualquier contexto, sino que, con las características, parámetros y período utilizados, no mejoraron el error absoluto del método sencillo.

Como limitación metodológica, los resultados de prueba de los métodos de referencia fueron inspeccionados antes de finalizar la selección de modelos. Por ello, no se describirá el conjunto de prueba como completamente ciego.

### 14.5. Persistencia compatible con MongoDB

Se desarrolló el módulo `src/almacenamiento/mongo_repo.py`, con funciones para preparar una colección, almacenar pronósticos y consultarlos por producto.

Se implementó un índice único compuesto por SKU, semana y modelo, así como operaciones de actualización con `upsert=True` para evitar registros duplicados.

La prueba automatizada `tests/test_mongo_repo.py` finalizó satisfactoriamente:

**Resultado: 1 prueba aprobada mediante pytest.**

Posteriormente se prepararon 37,620 documentos correspondientes a los pronósticos históricos de validación.

Un primer intento de cargar la totalidad de los documentos mediante operaciones individuales en `mongomock` presentó un rendimiento inadecuado y fue interrumpido. Se modificó la estrategia de prueba y se almacenó exitosamente una muestra de 100 documentos procedentes de los resultados reales del experimento.

La prueba confirmó el número de registros insertados. La persistencia se realizó en memoria mediante `mongomock`, sin una conexión a un servidor MongoDB real. Por lo tanto, se considera validada la interfaz de almacenamiento compatible, pero no la persistencia permanente en MongoDB.

### 14.6. Demostración de reposición

Se implementó una regla ilustrativa que combina el pronóstico semanal, un plazo de entrega supuesto y una reserva de seguridad porcentual.

El punto de reposición se calcula como:

**Punto de reposición = techo[Pronóstico semanal × Plazo de entrega × (1 + Factor de seguridad)]**

En una ejecución de ejemplo para el SKU 10120 se obtuvieron los siguientes resultados:

| Parámetro | Valor |
|---|---:|
| Pronóstico semanal | 0.5 unidades |
| Plazo de entrega supuesto | 2 semanas |
| Factor de seguridad supuesto | 25% |
| Inventario disponible supuesto | 100 unidades |
| Punto de reposición calculado | 2 unidades |
| Recomendación | No revisar reposición |

La regla fue comprobada mediante ejecución, pero no se ha realizado una simulación retrospectiva de inventario con costos operativos ni se ha demostrado una reducción de faltantes, excesos de inventario o gastos.

### 14.7. Uso de asistencia de inteligencia artificial

Durante esta fase se utilizó ChatGPT como apoyo técnico para proponer y generar partes del código de procesamiento semanal, validaciones entre Pandas y PySpark, construcción de variables históricas, experimentos con scikit-learn, funciones de almacenamiento y pruebas automatizadas.

El estudiante participó en la configuración y ejecución del entorno, la revisión de resultados, la resolución de errores, la comprobación de decisiones y la integración del código dentro del proyecto.

La asistencia también se utilizó para identificar riesgos metodológicos, explicar conceptos y proponer ajustes de implementación. Las salidas numéricas documentadas corresponden a ejecuciones realizadas en el entorno local del proyecto, no a resultados inventados


## 15. Revisión crítica de la viabilidad financiera — 2 de noviembre de 2026

Durante la revisión de los escenarios financieros, se cuestionó la razonabilidad de los retornos proyectados, especialmente los ROI de 521.54% y 770.85% a 24 meses.

Aunque los cálculos resultaron matemáticamente consistentes, se identificó que los beneficios dependen de supuestos no verificados sobre ventas perdidas, recuperación de ventas, inventario promedio, reducción de existencias y horas de trabajo ahorradas.

Como alternativa, se calculó el punto de equilibrio económico del proyecto. Con una inversión inicial de £6,400 y costos operativos anuales de £2,640, el beneficio mínimo necesario para recuperar los costos durante 24 meses es de **£5,840 anuales**, equivalente al **16.09% del beneficio anual hipotético del escenario base**.

Este umbral supone beneficios constantes e inmediatos, sin considerar descuentos financieros, impuestos, retrasos de implementación ni variaciones de costos.

**Decisión del responsable del proyecto:** recomendar un piloto controlado antes de cualquier implementación empresarial completa. El piloto deberá medir inventario disponible, plazos de entrega, faltantes, tiempo dedicado a planificación y costos reales, para evaluar si existen beneficios económicos suficientes.

Los ROI originales se conservarán únicamente como escenarios ilustrativos de sensibilidad, no como rentabilidad esperada ni como evidencia de ahorros alcanzados.

Esta revisión fue impulsada por el cuestionamiento del estudiante sobre la plausibilidad económica de los resultados iniciales, con apoyo de IA para analizar la sensibilidad y calcular el umbral de equilibrio.

## 16. Evaluación exploratoria con usuario de referencia — Design Thinking

**Fecha:** 2 de noviembre de 2026  
**Modalidad:** Consulta cualitativa mediante revisión del documento de Reabastece360.  
**Participante:** Persona con experiencia práctica en elaboración de pronósticos de ventas y planificación de necesidades.  
**Evidencia:** Notas tomadas por el responsable del proyecto a partir de los comentarios del participante.  
**Alcance:** Una consulta exploratoria; no constituye una prueba formal de usabilidad ni una validación representativa del mercado.

### 16.1. Empatizar

Se consultó a una persona con experiencia en procesos de pronóstico y planificación comercial para conocer cómo se desarrollaban estas actividades en un entorno empresarial.

El participante describió un proceso de extracción mensual de ventas desde SAP, utilizando información de SKU, descripción del material, fecha de facturación, cantidades, importes y países de destino.

Según su experiencia, el análisis empleaba históricos de aproximadamente 36 meses y combinaba suavización exponencial triple (Holt-Winters), regresión y promedios históricos.

Los resultados estadísticos se revisaban con responsables comerciales para incorporar condiciones que los modelos no capturaban directamente, como promociones, licitaciones, eventos climáticos y otras situaciones excepcionales.

### 16.2. Definir

La consulta permitió identificar necesidades relevantes para una herramienta de planificación:

- Contar con información histórica consolidada y depurada.
- Reconocer tendencias, estacionalidad y comportamientos atípicos por producto.
- Incorporar revisión humana de situaciones comerciales extraordinarias.
- Considerar existencias disponibles e inventario en tránsito antes de recomendar reposiciones.
- Clasificar productos según su rotación para priorizar las decisiones.

Estas necesidades permiten precisar el problema de negocio: no se trata únicamente de producir un pronóstico, sino de facilitar decisiones de abastecimiento con información actualizada, interpretación comercial y visibilidad de inventario.

### 16.3. Idear

A partir de los comentarios recibidos se identificaron oportunidades para futuras versiones del prototipo:

1. Incorporar inventario disponible e inventario en tránsito.
2. Añadir una etapa de revisión y ajuste comercial de los pronósticos.
3. Comparar métodos de pronóstico orientados a series con estacionalidad, como Holt-Winters, cuando exista suficiente historial.
4. Incorporar segmentación por mercado o país cuando el caso de negocio lo requiera.
5. Clasificar productos por niveles de rotación y riesgo de obsolescencia.
6. Medir la utilidad mediante indicadores de disponibilidad, capital de trabajo y eficiencia del proceso de planificación.

Estas propuestas constituyen oportunidades de mejora, no funcionalidades implementadas en HITO II.

### 16.4. Prototipar

El prototipo académico desarrollado prepara ventas semanales por producto, compara métodos de pronóstico y demuestra una regla de revisión de reposición con parámetros supuestos.

Se implementaron transformaciones en PySpark, experimentos con scikit-learn y una interfaz de persistencia compatible con MongoDB, probada mediante mongomock.

El prototipo no dispone de información verificada de inventario disponible, existencias en tránsito ni plazos de entrega. Tampoco ofrece actualmente un flujo de aprobación comercial o una interfaz gráfica destinada a usuarios finales.

### 16.5. Evaluar

El participante manifestó que considera aplicable la solución, especialmente en el contexto de una empresa mediana, y reconoció como razonable el horizonte temporal planteado, aunque contrastó el enfoque con su experiencia utilizando series históricas más extensas.

También destacó que el valor de una solución de este tipo debería evaluarse principalmente por su contribución a una planificación más ágil, menor riesgo de quiebres y excedentes de inventario, control del capital de trabajo y reducción de productos obsoletos o de baja rotación.

Estos comentarios respaldan la relevancia del problema abordado y ayudan a identificar requisitos funcionales que podrían mejorar el prototipo.

**Limitaciones de la evaluación:** La consulta se realizó sobre la documentación conceptual. No se ejecutó una prueba de tareas con el participante, no se midieron tiempos de uso y no se validó la precisión del pronóstico en su entorno empresarial.

### 16.6. Decisiones derivadas

Se conservará el alcance técnico actual para completar HITO II, sin incorporar nuevas tecnologías o modelos únicamente por haber surgido durante la consulta.

Las recomendaciones sobre inventario en tránsito, revisión comercial, clasificación por rotación y uso de históricos más extensos se documentarán como oportunidades de evolución.

En la evaluación financiera se mantendrá la recomendación de un piloto controlado, durante el cual puedan medirse indicadores operativos y económicos reales antes de justificar una inversión empresarial completa.