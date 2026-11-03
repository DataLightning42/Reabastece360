# Reabastece360 — Evaluación de viabilidad técnica

**Proyecto:** Reabastece360  
**Hito:** II — Bitácora de avance y evaluación multidimensional  
**Fecha:** 2 de noviembre de 2026  
**Modalidad:** Proyecto individual — Business Case (PRINCE2)  
**Estado:** Evaluación del prototipo académico desarrollado

## 1. Objetivo de la evaluación

Determinar si la solución propuesta puede implementarse y ejecutarse técnicamente con los recursos disponibles, identificando las tecnologías utilizadas, sus contribuciones, las limitaciones encontradas y las condiciones necesarias para una futura aplicación empresarial.

Reabastece360 busca transformar transacciones históricas de ventas en estimaciones semanales por producto y recomendaciones orientativas de reposición.

El prototipo desarrollado no constituye un sistema empresarial en producción, ni realiza compras automáticamente.

## 2. Arquitectura del prototipo

El flujo implementado comprende las siguientes etapas:

1. **Preparación de datos:** lectura del archivo Online Retail II, depuración de transacciones y aplicación de reglas de elegibilidad de productos mediante Pandas.
2. **Procesamiento semanal:** agregación de cantidades vendidas por SKU y semana mediante PySpark, utilizando un archivo CSV intermedio.
3. **Pronóstico:** comparación de métodos de referencia y tres algoritmos de aprendizaje automático mediante scikit-learn.
4. **Persistencia de resultados:** generación de documentos de pronóstico y almacenamiento de una muestra mediante funciones compatibles con MongoDB, utilizando mongomock.
5. **Apoyo a reposición:** cálculo ilustrativo de un punto de reposición con plazo de entrega, factor de seguridad e inventario disponible hipotéticos.

Los datos de entrada corresponden a ventas históricas. No se dispone de inventarios verificados, plazos de proveedores, stock en tránsito ni registros observados de quiebres de inventario.

## 3. Tecnologías seleccionadas

### 3.1. PySpark — Procesamiento de datos

**Función:** realizar agregaciones semanales por producto y demostrar transformaciones reproducibles utilizando un motor de procesamiento de datos.

**Implementación comprobada:**

- Ejecución local con PySpark 4.2.0.
- Lectura de datos depurados desde CSV con esquema definido explícitamente.
- Transformación de fechas y agrupación de cantidades por SKU y semana.
- Comparación exhaustiva contra una implementación de referencia en Pandas.

Se obtuvieron 189,366 grupos SKU-semana y 10,642,073 unidades en ambos motores, sin diferencias en las cantidades agregadas.

**Limitación:** El volumen de datos no requiere necesariamente procesamiento distribuido. No se realizó una medición formal de rendimiento para demostrar que Spark sea más rápido que Pandas en este entorno.

### 3.2. scikit-learn — Pronóstico de demanda

**Función:** implementar y evaluar modelos predictivos sobre la demanda semanal histórica.

Se entrenaron tres familias de algoritmos:

- Regresión lineal regularizada mediante Ridge.
- Ensamble de árboles mediante HistGradientBoostingRegressor.
- Regresión por vecinos cercanos mediante KNeighborsRegressor.

Se compararon con un método de referencia basado en el promedio móvil de cuatro semanas.

El experimento utilizó una separación cronológica, variables históricas desplazadas para evitar el uso de la demanda de la semana objetivo y métricas MAE, RMSE, WAPE y sesgo.

El promedio móvil de cuatro semanas obtuvo el menor MAE y WAPE en validación, mientras que HistGradientBoosting presentó el menor RMSE.

**Limitaciones:** La demanda presenta intermitencia y variabilidad, con errores porcentuales elevados. Los modelos no incluyen disponibilidad histórica de inventario, promociones, precios futuros ni información comercial externa.

### 3.3. MongoDB — Modelo documental de almacenamiento

**Función:** estructurar registros de pronósticos identificados por producto, semana y modelo, permitiendo su almacenamiento, actualización y consulta.

Se desarrolló `src/almacenamiento/mongo_repo.py`, con funciones para preparar la colección, guardar pronósticos mediante operaciones `upsert` y recuperar documentos asociados a un SKU.

La prueba automatizada con pytest y mongomock finalizó correctamente. Adicionalmente, se prepararon 37,620 documentos procedentes de los resultados históricos de validación y se comprobó el almacenamiento de una muestra de 100 registros.

**Limitación fundamental:** Se utilizó mongomock como sustituto de una base de datos MongoDB durante las pruebas. No se comprobó una conexión con un servidor MongoDB real ni persistencia permanente de los documentos. Por lo tanto, la integración debe describirse como una implementación de interfaz compatible con MongoDB validada en memoria.

## 4. Tecnologías de apoyo

Pandas se utilizó para preparación, limpieza y validación de datos; NumPy para operaciones numéricas; pytest para pruebas automatizadas; Git y GitHub para seguimiento de cambios; y VS Code/Jupyter Notebook como entorno de desarrollo y experimentación.

Estas herramientas apoyan el prototipo, pero no se presentan como sustitutos de la justificación funcional de las tres tecnologías principales.

## 5. Recursos técnicos y viabilidad de ejecución

El trabajo se desarrolló en un equipo personal con Windows, Python 3.14.5 y Java OpenJDK 21, utilizando PySpark en modo local.

Los componentes de preparación semanal, agregación en Spark, entrenamiento de modelos y pruebas de almacenamiento se ejecutaron en dicho entorno.

La evidencia demuestra viabilidad de ejecución local para el alcance ensayado, aunque no permite establecer requisitos mínimos universales de memoria o procesador.

No se contrató infraestructura de nube ni se desplegó una aplicación empresarial.

## 6. Riesgos técnicos

| Riesgo | Impacto posible | Mitigación propuesta |
|---|---|---|
| Ausencia de inventario histórico | Imposibilidad de verificar quiebres y excedentes reales | Incorporar información operativa durante un piloto |
| Productos sin actividad continua | Sesgo en modelos por semanas registradas como cero | Validar ciclo de vida, rotación y disponibilidad de SKU |
| Pronósticos imprecisos | Recomendaciones de reposición poco confiables | Supervisión humana, monitoreo de errores y reglas conservadoras |
| Incompatibilidad entre librerías | Fallos de ejecución o mantenimiento | Fijar versiones y ejecutar pruebas de regresión |
| Persistencia simulada | Pérdida de datos al reiniciar el entorno | Probar servidor MongoDB real antes de una implantación |
| Carga masiva lenta en mongomock | Tiempo excesivo durante pruebas | Utilizar muestras de prueba y validar rendimiento en una base real |
| Ausencia de datos comerciales externos | Pronósticos sin contexto de promociones o eventos | Incorporar revisión del responsable comercial |
| Dependencia del notebook | Dificultad para reutilizar o automatizar componentes | Modularizar progresivamente el código y documentar su ejecución |

## 7. Pertinencia del alcance tecnológico

La selección de PySpark, scikit-learn y MongoDB responde a tres necesidades diferentes: procesar datos históricos, generar estimaciones de demanda y estructurar resultados consultables.

El docente confirmó que el proyecto requiere al menos tres tecnologías con una función justificada, sin obligación de implementar todas las herramientas mencionadas en la guía general.

Por ello, se excluyeron del alcance del HITO II Dask, S3 simulado, aprendizaje profundo, una API REST y el despliegue con Docker.

Esta decisión busca evitar duplicidad técnica y concentrar el esfuerzo en resultados verificables, dentro del plazo académico disponible.

## 8. Evaluación de viabilidad empresarial

La viabilidad técnica del prototipo local es favorable para fines académicos y de exploración, dado que se ha demostrado la ejecución de sus principales componentes analíticos.

Sin embargo, trasladar la solución a un entorno empresarial requiere validar aspectos que no pudieron comprobarse con el conjunto público:

- Disponibilidad y actualización de inventario físico y en tránsito.
- Calidad y oportunidad de la información de ventas.
- Plazos reales de abastecimiento.
- Integración con los procesos de compras y revisión comercial.
- Precisión del pronóstico en condiciones operativas.
- Rendimiento y persistencia de la base de datos real.
- Seguridad, acceso, mantenimiento y respaldo de la información.

La consulta cualitativa realizada a una persona con experiencia en planificación comercial reforzó la importancia de estos elementos, especialmente la revisión humana de pronósticos y la visibilidad del inventario.

## 9. Conclusión y recomendación

**Reabastece360 es técnicamente viable como prototipo académico local, pero no se considera validado para una implementación empresarial inmediata.**

Se recomienda realizar un piloto controlado con una selección de productos y datos operativos reales. Dicho piloto debería medir el error de pronóstico, los quiebres de inventario, el exceso y obsolescencia de existencias, el capital de trabajo y el tiempo dedicado a la planificación.

La decisión de ampliar la solución deberá basarse en los resultados observados durante el piloto y en una evaluación financiera actualizada, no únicamente en las proyecciones hipotéticas del Business Case.

## 10. Transparencia metodológica

La implementación, las verificaciones y las limitaciones aquí descritas se basan en los resultados de ejecución compartidos durante el desarrollo del proyecto.

Se utilizó asistencia de inteligencia artificial para apoyar decisiones técnicas, generar propuestas de código, revisar riesgos y estructurar la documentación. La ejecución de pruebas y experimentos se realizó en el entorno local del estudiante.

Este documento distingue las funcionalidades implementadas de las mejoras propuestas y no atribuye a Reabastece360 capacidades que todavía no han sido demostradas.