from fastapi import APIRouter, HTTPException, Response, status
from typing import List
from sqlalchemy import insert

from config.db import conn
from models.estadoprestamo import estadoprestamos
from schemas.estadoprestamo import EstadoPrestamo

estadoPrestamoRoutes = APIRouter()

# Obtener todos los estados de préstamo
@estadoPrestamoRoutes.get("/estados-prestamo", tags=["estados_prestamo"], response_model=List[EstadoPrestamo], description="Get a list of all loan statuses")
def get_estados_prestamo():
    return conn.execute(estadoprestamos.select()).fetchall()

# Obtener un estado de préstamo por su ID
@estadoPrestamoRoutes.get("/estados-prestamo/{id}", tags=["estados_prestamo"], response_model=EstadoPrestamo, description="Get a single loan status by ID")
def get_estado_prestamo(id: int):
    existing_estado_prestamo = conn.execute(estadoprestamos.select().where(estadoprestamos.c.estadoid == id)).first()
    if existing_estado_prestamo:
        return existing_estado_prestamo
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Estado de préstamo not found")

# Crear un nuevo estado de préstamo
@estadoPrestamoRoutes.post("/estados-prestamo", tags=["estados_prestamo"], response_model=EstadoPrestamo, description="Create a new loan status")
def create_estado_prestamo(estado_prestamo: EstadoPrestamo):
    try:
        new_estado_prestamo = {"descripcion": estado_prestamo.descripcion}
        result = conn.execute(insert(estadoprestamos).values(new_estado_prestamo))
        new_estado_prestamo["estadoid"] = result.inserted_primary_key[0]
        conn.commit()
        return new_estado_prestamo
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# Actualizar un estado de préstamo por su ID
@estadoPrestamoRoutes.put("/estados-prestamo/{id}", tags=["estados_prestamo"], response_model=EstadoPrestamo, description="Update a loan status by ID")
def update_estado_prestamo(id: int, estado_prestamo: EstadoPrestamo):
    existing_estado_prestamo = conn.execute(estadoprestamos.select().where(estadoprestamos.c.estadoid == id)).fetchone()
    if existing_estado_prestamo:
        conn.execute(
            estadoprestamos.update()
            .values(descripcion=estado_prestamo.descripcion)
            .where(estadoprestamos.c.estadoid == id)
        )
        conn.commit()
        return Response(status_code=status.HTTP_200_OK, content="Estado de préstamo actualizado")
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Estado de préstamo not found")

# Eliminar un estado de préstamo por su ID
@estadoPrestamoRoutes.delete("/estados-prestamo/{id}", tags=["estados_prestamo"])
def delete_estado_prestamo(id: int):
    existing_estado_prestamo = conn.execute(estadoprestamos.select().where(estadoprestamos.c.estadoid == id)).fetchone()
    if existing_estado_prestamo:
        conn.execute(estadoprestamos.delete().where(estadoprestamos.c.estadoid == id))
        conn.commit()
        return status.HTTP_200_OK
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Estado de préstamo not found")