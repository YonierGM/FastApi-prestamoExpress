from fastapi import APIRouter, HTTPException, Response, status
from typing import List
from sqlalchemy import insert

from config.db import conn
from models.tipoprestamo import tipoprestamos
from schemas.tipoprestamo import TipoPrestamo

tipoPrestamoRoutes = APIRouter()

# Obtener todos los tipos de préstamo
@tipoPrestamoRoutes.get("/tiposprestamo", tags=["tiposprestamo"], response_model=List[TipoPrestamo], description="Get a list of all loan types")
def get_tipos_prestamo():
    return conn.execute(tipoprestamos.select()).fetchall()

# Obtener un tipo de préstamo por su ID
@tipoPrestamoRoutes.get("/tiposprestamo/{id}", tags=["tiposprestamo"], response_model=TipoPrestamo, description="Get a single loan type by ID")
def get_tipo_prestamo(id: int):
    existing_tipo_prestamo = conn.execute(tipoprestamos.select().where(tipoprestamos.c.tipoprestamoid == id)).first()
    if existing_tipo_prestamo:
        return existing_tipo_prestamo
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tipo de préstamo not found")

# Crear un nuevo tipo de préstamo
@tipoPrestamoRoutes.post("/tiposprestamo", tags=["tiposprestamo"], response_model=TipoPrestamo, description="Create a new loan type")
def create_tipo_prestamo(tipo_prestamo: TipoPrestamo):
    try:
        new_tipo_prestamo = {"descripcion": tipo_prestamo.descripcion}
        result = conn.execute(insert(tipoprestamos).values(new_tipo_prestamo))
        new_tipo_prestamo["tipoprestamoid"] = result.inserted_primary_key[0]
        conn.commit()
        return new_tipo_prestamo
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# Actualizar un tipo de préstamo por su ID
@tipoPrestamoRoutes.put("/tiposprestamo/{id}", tags=["tiposprestamo"], response_model=TipoPrestamo, description="Update a loan type by ID")
def update_tipo_prestamo(id: int, tipo_prestamo: TipoPrestamo):
    existing_tipo_prestamo = conn.execute(tipoprestamos.select().where(tipoprestamos.c.tipoprestamoid == id)).fetchone()
    if existing_tipo_prestamo:
        conn.execute(
            tipoprestamos.update()
            .values(descripcion=tipo_prestamo.descripcion)
            .where(tipoprestamos.c.tipoprestamoid == id)
        )
        conn.commit()
        return Response(status_code=status.HTTP_200_OK, content="Tipo de préstamo actualizado")
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tipo de préstamo not found")

# Eliminar un tipo de préstamo por su ID
@tipoPrestamoRoutes.delete("/tiposprestamo/{id}", tags=["tiposprestamo"])
def delete_tipo_prestamo(id: int):
    existing_tipo_prestamo = conn.execute(tipoprestamos.select().where(tipoprestamos.c.tipoprestamoid == id)).fetchone()
    if existing_tipo_prestamo:
        conn.execute(tipoprestamos.delete().where(tipoprestamos.c.tipoprestamoid == id))
        conn.commit()
        return Response(status_code=status.HTTP_200_OK, content="Tipo de préstamo eliminado")
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tipo de préstamo not found")
