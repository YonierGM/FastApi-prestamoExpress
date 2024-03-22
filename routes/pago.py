from fastapi import APIRouter, HTTPException, Response, status
from typing import List
from sqlalchemy import insert

from config.db import conn
from models.pago import pagos
from schemas.pago import Pago

pagoRoutes = APIRouter()

# Obtener todos los pagos
@pagoRoutes.get("/pagos", tags=["pagos"], response_model=List[Pago], description="Get a list of all payments")
def get_pagos():
    return conn.execute(pagos.select()).fetchall()

# Obtener un pago por su ID
@pagoRoutes.get("/pagos/{id}", tags=["pagos"], response_model=Pago, description="Get a single payment by ID")
def get_pago(id: int):
    return conn.execute(pagos.select().where(pagos.c.pagoid == id)).first()

# Crear un nuevo pago
@pagoRoutes.post("/pagos", tags=["pagos"], response_model=Pago, description="Create a new payment")
def create_pago(pago: Pago):
    try:
        new_pago = {"fechapago": pago.fechapago, "monto": pago.monto, "prestamoid": pago.prestamoid}
        result = conn.execute(insert(pagos).values(new_pago))
        new_pago["pagoid"] = result.inserted_primary_key[0]
        return new_pago
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Actualizar un pago por su ID
@pagoRoutes.put("/pagos/{id}", tags=["pagos"], response_model=Pago, description="Update a payment by ID")
def update_pago(id: int, pago: Pago):
    conn.execute(
        pagos.update()
        .values(fechapago=pago.fechapago, monto=pago.monto, prestamoid=pago.prestamoid)
        .where(pagos.c.pagoid == id)
    )
    conn.commit()
    return pago

# Eliminar un pago por su ID
@pagoRoutes.delete("/pagos/{id}", tags=["pagos"])
def delete_pago(id: int):
    pago = conn.execute(pagos.select().where(pagos.c.pagoid == id)).fetchone()
    if pago:
        conn.execute(pagos.delete().where(pagos.c.pagoid == id))
        conn.commit()
        return Response(status_code=status.HTTP_200_OK, content="Pago eliminado")
    else:
        return Response(status_code=status.HTTP_404_NOT_FOUND, content="Pago no encontrado")
