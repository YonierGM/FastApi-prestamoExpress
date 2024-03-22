from fastapi import APIRouter, HTTPException, Response, status
from typing import List
from sqlalchemy import insert

from config.db import conn
from models.prestamo import prestamos
from schemas.prestamo import Prestamo

prestamoRoutes = APIRouter()

# Obtener todos los préstamos
@prestamoRoutes.get("/prestamos", tags=["prestamos"], response_model=List[Prestamo], description="Get a list of all loans")
def get_prestamos():
    return conn.execute(prestamos.select()).fetchall()

# Obtener un préstamo por su ID
@prestamoRoutes.get("/prestamos/{id}", tags=["prestamos"], response_model=Prestamo, description="Get a single loan by ID")
def get_prestamo(id: int):
    return conn.execute(prestamos.select().where(prestamos.c.prestamoid == id)).first()

# Crear un nuevo préstamo
@prestamoRoutes.post("/prestamos", tags=["prestamos"], response_model=Prestamo, description="Create a new loan")
def create_prestamo(prestamo: Prestamo):
    try:
        new_prestamo = {"fechaprestamo": prestamo.fechaprestamo, "fechaestimadapago": prestamo.fechaestimadapago,
                        "monto": prestamo.monto, "cuotas": prestamo.cuotas, "valorcuota": prestamo.valorcuota,
                        "clienteid": prestamo.clienteid, "estadoid": prestamo.estadoid, "tipoprestamoid": prestamo.tipoprestamoid}
        result = conn.execute(insert(prestamos).values(new_prestamo))
        new_prestamo["prestamoid"] = result.inserted_primary_key[0]
        return new_prestamo
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Actualizar un préstamo por su ID
@prestamoRoutes.put("/prestamos/{id}", tags=["prestamos"], response_model=Prestamo, description="Update a loan by ID")
def update_prestamo(id: int, prestamo: Prestamo):
    conn.execute(
        prestamos.update()
        .values(fechaprestamo=prestamo.fechaprestamo, fechaestimadapago=prestamo.fechaestimadapago,
                monto=prestamo.monto, cuotas=prestamo.cuotas, valorcuota=prestamo.valorcuota,
                clienteid=prestamo.clienteid, estadoid=prestamo.estadoid, tipoprestamoid=prestamo.tipoprestamoid)
        .where(prestamos.c.prestamoid == id)
    )
    conn.commit()
    return prestamo

# Eliminar un préstamo por su ID
@prestamoRoutes.delete("/prestamos/{id}", tags=["prestamos"])
def delete_prestamo(id: int):
    prestamo = conn.execute(prestamos.select().where(prestamos.c.prestamoid == id)).fetchone()
    if prestamo:
        conn.execute(prestamos.delete().where(prestamos.c.prestamoid == id))
        conn.commit()
        return Response(status_code=status.HTTP_200_OK, content="Préstamo eliminado")
    else:
        return Response(status_code=status.HTTP_404_NOT_FOUND, content="Préstamo no encontrado")
