from fastapi import APIRouter, HTTPException, Response, status
from typing import List
from sqlalchemy import select, join, insert

from config.db import conn

from schemas.prestamo import Prestamo
from models.estadoprestamo import estadoprestamos
from models.prestamo import prestamos
from models.cliente import clientes
from models.tipoprestamo import tipoprestamos

from fastapi import Query
prestamoRoutes = APIRouter()

# Obtener todos los préstamos
from collections import namedtuple

@prestamoRoutes.get("/prestamos", tags=["prestamos"], description="Get a list of all loans")
def get_prestamos():
    query = (
        select(
            prestamos.c.prestamoid,
            prestamos.c.fechaprestamo,
            prestamos.c.fechaestimadapago,
            prestamos.c.monto,
            prestamos.c.cuotas,
            prestamos.c.valorcuota,
            clientes.c.nombre.label('nombre_cliente'),
            clientes.c.apellido.label('apellido_cliente'),
            estadoprestamos.c.descripcion.label('descripcion_estadoPrestamo'),
            tipoprestamos.c.descripcion.label('descripcion_tipoprestamo')
        )
        .select_from(
            prestamos.join(clientes, prestamos.c.clienteid == clientes.c.clienteid)
            .join(tipoprestamos, prestamos.c.tipoprestamoid == tipoprestamos.c.tipoprestamoid)
            .join(estadoprestamos, prestamos.c.estadoid == estadoprestamos.c.estadoid   )
        )
    )

    # Obtener los nombres de las columnas
    columns = query.columns.keys()

    # Ejecutar la consulta y obtener los resultados
    result_temporal = conn.execute(query).fetchall()

    # Construir una lista de diccionarios a partir del resultado
    result_final = [dict(zip(columns, row)) for row in result_temporal]

    return result_final


# Obtener un préstamo por su ID
@prestamoRoutes.get("/prestamos/{id}", tags=["prestamos"], response_model=Prestamo, description="Get a single loan by ID")
def get_prestamo(id: int):
    existing_prestamo = conn.execute(prestamos.select().where(prestamos.c.prestamoid == id)).first()
    if existing_prestamo:
        return existing_prestamo
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Préstamo not found")

# Crear un nuevo préstamo
@prestamoRoutes.post("/prestamos", tags=["prestamos"], response_model=Prestamo, description="Create a new loan")
def create_prestamo(prestamo: Prestamo):
    try:
        new_prestamo = {"fechaprestamo": prestamo.fechaprestamo, "fechaestimadapago": prestamo.fechaestimadapago,
                        "monto": prestamo.monto, "cuotas": prestamo.cuotas, "valorcuota": prestamo.valorcuota,
                        "clienteid": prestamo.clienteid, "estadoid": prestamo.estadoid, "tipoprestamoid": prestamo.tipoprestamoid}
        result = conn.execute(insert(prestamos).values(new_prestamo))
        new_prestamo["prestamoid"] = result.inserted_primary_key[0]
        conn.commit()
        return new_prestamo
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# Actualizar un préstamo por su ID
@prestamoRoutes.put("/prestamos/{id}", tags=["prestamos"], response_model=Prestamo, description="Update a loan by ID")
def update_prestamo(id: int, prestamo: Prestamo):
    existing_prestamo = conn.execute(prestamos.select().where(prestamos.c.prestamoid == id)).fetchone()
    if existing_prestamo:
        conn.execute(
            prestamos.update()
            .values(fechaprestamo=prestamo.fechaprestamo, fechaestimadapago=prestamo.fechaestimadapago,
                    monto=prestamo.monto, cuotas=prestamo.cuotas, valorcuota=prestamo.valorcuota,
                    clienteid=prestamo.clienteid, estadoid=prestamo.estadoid, tipoprestamoid=prestamo.tipoprestamoid)
            .where(prestamos.c.prestamoid == id)
        )
        conn.commit()
        return Response(status_code=status.HTTP_200_OK, content="Préstamo actualizado")
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Préstamo not found")

# Eliminar un préstamo por su ID
@prestamoRoutes.delete("/prestamos/{id}", tags=["prestamos"])
def delete_prestamo(id: int):
    existing_prestamo = conn.execute(prestamos.select().where(prestamos.c.prestamoid == id)).fetchone()
    if existing_prestamo:
        conn.execute(prestamos.delete().where(prestamos.c.prestamoid == id))
        conn.commit()
        return Response(status_code=status.HTTP_200_OK, content="Préstamo eliminado")
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Préstamo not found")
