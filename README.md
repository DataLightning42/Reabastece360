# Reabastece360

**Pronóstico semanal de demanda y recomendaciones de reposición por producto.**

## 1. Problema y objetivo

Reabastece360 es un prototipo académico para ayudar a un mayorista
ficticio de artículos de regalo a planificar la reposición de productos
mediante pronósticos semanales de demanda.

El sistema busca proporcionar recomendaciones transparentes que una
persona responsable de compras pueda revisar.

## 2. Fuente de datos

Online Retail II — UCI Machine Learning Repository.

Fuente y licencia: https://doi.org/10.24432/C5CG6D

Licencia declarada: CC BY 4.0.

El archivo original se mantiene localmente y no debe subirse al
repositorio Git.

## 3. Alcance del proyecto

- Auditar y limpiar los datos transaccionales.
- Construir una serie de demanda semanal por producto.
- Procesar y validar agregaciones mediante PySpark.
- Comparar métodos de referencia y modelos de pronóstico con scikit-learn.
- Evaluar los resultados mediante una separación cronológica de entrenamiento, validación y prueba.
- Almacenar y consultar una muestra de pronósticos mediante una interfaz compatible con MongoDB, probada con mongomock.
- Demostrar una regla ilustrativa de reposición basada en supuestos explícitos.
- Documentar las decisiones técnicas, la evaluación financiera y las cinco etapas de Design Thinking.

## 4. Tecnologías utilizadas

El prototipo de Reabastece360 integra tres tecnologías principales, cada una con una función específica:

- **PySpark:** procesamiento de datos y agregación de ventas semanales por SKU. Los resultados se contrastaron con Pandas para verificar su consistencia.
- **scikit-learn:** entrenamiento y evaluación de modelos de pronóstico de demanda, incluyendo Ridge, KNeighborsRegressor e HistGradientBoostingRegressor.
- **MongoDB (interfaz compatible):** estructuración, actualización y consulta de pronósticos mediante PyMongo. Las operaciones se probaron con mongomock, sin desplegar un servidor MongoDB real.

**Herramientas complementarias:**

- **Pandas y NumPy:** limpieza, transformación y análisis de datos.
- **pytest:** ejecución de pruebas automatizadas.
- **Git y GitHub:** control de versiones y seguimiento del desarrollo.
- **Jupyter Notebook y VS Code:** desarrollo, ejecución y documentación de experimentos.

FastAPI y Docker no forman parte del alcance implementado en HITO II.

## 5. Limitaciones conocidas

El conjunto de datos no proporciona un historial fiable del inventario
disponible, los plazos de entrega de proveedores ni las roturas de stock
observadas.

Por tanto, cualquier evaluación de reposición que dependa de esos
elementos será una simulación basada en supuestos explícitos, no una
medición de resultados operativos reales.

## 6. Estado del proyecto

**Estado actual:** Prototipo académico funcional, desarrollado y validado localmente para HITO II.

**Resultados obtenidos:**

- Se procesaron y depuraron los datos históricos de ventas de Online Retail II.
- Se construyó una serie semanal de demanda para 4,691 productos (SKU), abarcando 103 semanas.
- Se validaron las agregaciones realizadas con PySpark mediante una comparación con Pandas, sin diferencias en las cantidades agregadas.
- Se evaluaron tres familias de modelos de aprendizaje automático y métodos de referencia, utilizando una separación cronológica de entrenamiento, validación y prueba.
- El promedio móvil de cuatro semanas obtuvo el menor WAPE en validación (**79.13%**) entre los métodos evaluados.
- Se prepararon 37,620 documentos históricos de pronóstico y se comprobó el almacenamiento de una muestra de 100 registros mediante mongomock.
- La prueba automatizada de persistencia se ejecutó correctamente con pytest (**1 prueba aprobada**).
- El notebook completo se ejecutó satisfactoriamente desde un kernel reiniciado.
- Se elaboraron las evaluaciones de viabilidad técnica, financiera y Design Thinking, incluyendo una consulta cualitativa con una persona experimentada en planificación de demanda.

**Limitaciones:** El prototipo no utiliza inventarios reales ni está desplegado en un entorno empresarial. Los beneficios económicos son escenarios hipotéticos y requieren validación mediante un piloto controlado.

## 7. Reproducibilidad

El proyecto fue desarrollado y probado localmente en Windows, utilizando Python 3.14.5 y Java OpenJDK 21 para PySpark.

### Preparación del entorno

1. Clonar el repositorio de Reabastece360 desde GitHub.
2. Abrir la carpeta del proyecto en VS Code.
3. Configurar un entorno de Python e instalar las dependencias necesarias: `pandas`, `numpy`, `pyspark`, `scikit-learn`, `pymongo`, `mongomock`, `pytest`, `openpyxl`, `jupyter` e `ipykernel`.
4. Descargar el conjunto de datos **Online Retail II** desde UCI Machine Learning Repository y colocar el archivo `online_retail_II.xlsx` en `data/raw/`.

El archivo original de datos no se distribuye dentro del repositorio.

### Ejecución del análisis

Abrir el notebook:

`notebooks/Proyecto_Integrador_Reabastece360_HitoI.ipynb`

Seleccionar el intérprete de Python correspondiente y ejecutar todas las celdas en orden, utilizando **Restart Kernel** y **Run All**.

El notebook contiene la preparación de datos, agregaciones con PySpark, evaluación de modelos, pruebas de persistencia compatibles con MongoDB y un ejemplo ilustrativo de reposición.

### Pruebas automatizadas

Desde la raíz del proyecto, ejecutar:

```powershell
python -m pytest -q tests/test_mongo_repo.py
```

En la validación final del 2 de noviembre de 2026 se obtuvo **1 prueba aprobada**. También se verificó la ejecución completa del notebook desde un kernel reiniciado.

### Resultados

Los archivos de resultados se encuentran en `reports/`, incluyendo las comparaciones de modelos, los pronósticos de validación y la evaluación financiera.

**Nota:** La persistencia se prueba utilizando mongomock. No es necesario ejecutar un servidor MongoDB real para reproducir las pruebas automatizadas del prototipo.

## 8. Uso de inteligencia artificial

La asistencia de IA se declarará en la documentación de la entrega.
El responsable del proyecto verificará los resultados y deberá
comprender y poder explicar el código utilizado.
