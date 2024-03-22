from fastapi import APIRouter, HTTPException
from starlette.status import HTTP_404_NOT_FOUND
from typing import List
from sqlalchemy import insert

from config.db import conn
from models.rol import roles
from schemas.rol import Rol

rolRoutes = APIRouter()

# Obtener todos los roles
@rolRoutes.get(
    "/roles",
    tags=["roles"],
    response_model=List[Rol],
    description="Get a list of all roles",
)
def get_roles():
    return conn.execute(roles.select()).fetchall()

# Obtener un rol por su ID
@rolRoutes.get(
    "/roles/{id}",
    tags=["roles"],
    response_model=Rol,
    description="Get a single rol by Id",
)
def get_rol(id: int):
    rol = conn.execute(roles.select().where(roles.c.rolid == id)).first()
    if rol:
        return rol
    else:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Rol not found")

# Crear un nuevo rol
@rolRoutes.post("/", tags=["roles"], response_model=Rol, description="Create a new rol")
def create_rol(rol: Rol):
    new_rol = {"descripcion": rol.descripcion}
    result = conn.execute(insert(roles).values(new_rol))
    new_rol["rolid"] = result.inserted_primary_key[0]
    return new_rol

# Actualizar un rol por su ID
@rolRoutes.put("/roles/{id}", tags=["roles"], response_model=Rol, description="Update a Rol by Id")
def update_rol(id: int, rol: Rol):
    conn.execute(
        roles.update()
        .values(descripcion=rol.descripcion)
        .where(roles.c.rolid == id)
    )
    return rol

# Eliminar un rol por su ID
@rolRoutes.delete("/{id}", tags=["roles"])
def delete_rol(id: int):
    rol = conn.execute(roles.select().where(roles.c.rolid == id)).fetchone()
    if rol:
        conn.execute(roles.delete().where(roles.c.rolid == id))
        return "Rol eliminado"
    else:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Rol not found")
