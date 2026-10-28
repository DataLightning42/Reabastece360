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
- Comparar un método de referencia con modelos de pronóstico.
- Evaluar los resultados mediante una separación cronológica.
- Simular y comparar políticas de reposición.
- Documentar las decisiones técnicas, financieras y de diseño.
- Preparar un servicio local reproducible.

## 4. Tecnologías previstas

- PySpark: procesamiento y agregación de datos.
- scikit-learn: entrenamiento y evaluación de modelos.
- MongoDB: persistencia de resultados.
- FastAPI: servicio REST.
- Docker: ejecución reproducible.
- pytest y Git: pruebas y control de versiones.

## 5. Limitaciones conocidas

El conjunto de datos no proporciona un historial fiable del inventario
disponible, los plazos de entrega de proveedores ni las roturas de stock
observadas.

Por tanto, cualquier evaluación de reposición que dependa de esos
elementos será una simulación basada en supuestos explícitos, no una
medición de resultados operativos reales.

## 6. Estado del proyecto

En desarrollo. Los resultados, las métricas y las pruebas se incorporarán
después de ejecutar y validar el código correspondiente.

## 7. Reproducibilidad

Las instrucciones de instalación, ejecución, configuración y pruebas
se completarán una vez verificado el entorno y fijadas las dependencias.

## 8. Uso de inteligencia artificial

La asistencia de IA se declarará en la documentación de la entrega.
El responsable del proyecto verificará los resultados y deberá
comprender y poder explicar el código utilizado.
