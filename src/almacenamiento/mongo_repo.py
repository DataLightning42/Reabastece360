# Persistencia de pronósticos semanales en MongoDB.
# El almacenamiento admite pruebas con mongomock.

from pymongo import ASCENDING


def preparar_coleccion(base_datos):
    """Preparar una colección de pronósticos con índice único."""
    coleccion = base_datos["pronosticos_semanales"]

    coleccion.create_index(
        [
            ("sku", ASCENDING),
            ("semana", ASCENDING),
            ("modelo", ASCENDING),
        ],
        unique=True
    )

    return coleccion


def guardar_pronosticos(coleccion, documentos):
    """Guardar pronósticos sin duplicar registros existentes."""

    for documento in documentos:
        clave = {
            "sku": documento["sku"],
            "semana": documento["semana"],
            "modelo": documento["modelo"],
        }

        coleccion.update_one(
            clave,
            {"$set": documento},
            upsert=True
        )



def consultar_pronosticos(coleccion, sku):
    """Consultar pronósticos históricos de un producto."""
    return list(
        coleccion.find(
            {"sku": str(sku)},
            {"_id": 0}
        ).sort("semana", ASCENDING)
    )


# Pruebas de persistencia sin necesidad de un servidor MongoDB.

import mongomock

from src.almacenamiento.mongo_repo import (
    preparar_coleccion,
    guardar_pronosticos,
    consultar_pronosticos,
)


def test_guardar_y_consultar_pronosticos():
    cliente = mongomock.MongoClient()
    coleccion = preparar_coleccion(cliente["reabastece360"])

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

    # Repetir la carga no debe duplicar documentos.
    guardar_pronosticos(coleccion, documentos)

    assert coleccion.count_documents({}) == 1

    cliente.close()