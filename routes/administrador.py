from fastapi import APIRouter, HTTPException, Response, status
from typing import List
from sqlalchemy import insert

from config.db import conn
from models.administrador import administradores
from schemas.administrador import Administrador

administradorRoutes = APIRouter()

# Obtener todos los administradores
@administradorRoutes.get("/administradores", tags=["administradores"], response_model=List[Administrador], description="Get a list of all administrators")
def get_administradores():
    return conn.execute(administradores.select()).fetchall()

# Obtener un administrador por su ID
@administradorRoutes.get("/administradores/{id}", tags=["administradores"], response_model=Administrador, description="Get a single administrator by ID")
def get_administrador(id: int):
    return conn.execute(administradores.select().where(administradores.c.administradorid == id)).first()

# Crear un nuevo administrador
@administradorRoutes.post("/administradores", tags=["administradores"], response_model=Administrador, description="Create a new administrator")
def create_administrador(administrador: Administrador):
    try:
        new_administrador = {"nombre": administrador.nombre, "apellido": administrador.apellido, "documento": administrador.documento, "email": administrador.email, "celular": administrador.celular, "rolid": administrador.rolid}
        result = conn.execute(insert(administradores).values(new_administrador))
        new_administrador["administradorid"] = result.inserted_primary_key[0]
        return new_administrador
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Actualizar un administrador por su ID
@administradorRoutes.put("/administradores/{id}", tags=["administradores"], response_model=Administrador, description="Update an administrator by ID")
def update_administrador(id: int, administrador: Administrador):
    conn.execute(
        administradores.update()
        .values(nombre=administrador.nombre, apellido=administrador.apellido, documento=administrador.documento, email=administrador.email, celular=administrador.celular, rolid=administrador.rolid)
        .where(administradores.c.administradorid == id)
    )
    conn.commit()
    return administrador

# Eliminar un administrador por su ID
@administradorRoutes.delete("/administradores/{id}", tags=["administradores"])
def delete_administrador(id: int):
    administrador = conn.execute(administradores.select().where(administradores.c.administradorid == id)).fetchone()
    if administrador:
        conn.execute(administradores.delete().where(administradores.c.administradorid == id))
        conn.commit()
        return Response(status_code=status.HTTP_200_OK, content="Administrador eliminado")
    else:
        return Response(status_code=status.HTTP_404_NOT_FOUND, content="Administrador no encontrado")
