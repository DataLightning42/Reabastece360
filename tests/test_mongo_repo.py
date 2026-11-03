# Verificar el almacenamiento y la consulta de pronósticos.
# Se utiliza una base de datos simulada para realizar las pruebas.

import mongomock

from src.almacenamiento.mongo_repo import (
    preparar_coleccion,
    guardar_pronosticos,
    consultar_pronosticos,
)


def test_guardar_y_consultar_pronosticos():
    cliente = mongomock.MongoClient()
    coleccion = preparar_coleccion(cliente["reabastece360"])

    # Datos ficticios para comprobar el funcionamiento.
    documentos = [
        {
            "sku": "10002",
            "semana": "2011-06-13",
            "modelo": "media_movil_4",
            "pronostico_unidades": 25.5,
            "tipo_resultado": "validacion_historica",
        }
    ]

    guardar_pronosticos(coleccion, documentos)

    resultados = consultar_pronosticos(coleccion, "10002")

    assert len(resultados) == 1
    assert resultados[0]["pronostico_unidades"] == 25.5

    # Verificar que repetir la carga no duplica registros.
    guardar_pronosticos(coleccion, documentos)

    assert coleccion.count_documents({}) == 1

    cliente.close()