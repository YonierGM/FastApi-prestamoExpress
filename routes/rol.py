from fastapi import APIRouter, HTTPException, Response
from starlette import status
from starlette.status import HTTP_404_NOT_FOUND, HTTP_200_OK
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
    existing_rol = conn.execute(roles.select().where(roles.c.rolid == id)).first()
    if existing_rol:
        return existing_rol
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rol not found")

# Crear un nuevo rol
@rolRoutes.post("/", tags=["roles"], response_model=Rol, description="Create a new rol")
def create_rol(rol: Rol):
    try:
        new_rol = {"descripcion": rol.descripcion}
        result = conn.execute(insert(roles).values(new_rol))
        new_rol["rolid"] = result.inserted_primary_key[0]
        conn.commit()
        return new_rol
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# Actualizar un rol por su ID
@rolRoutes.put("/roles/{id}", tags=["roles"], response_model=Rol, description="Update a Rol by Id")
def update_rol(id: int, rol: Rol):
    existing_rol=conn.execute(roles.select().where(roles.c.rolid == id)).fetchone()
    if existing_rol:
        conn.execute(
            roles.update()
            .values(descripcion=rol.descripcion)
            .where(roles.c.rolid == id)
        )
        conn.commit()
        return Response(status_code=status.HTTP_200_OK, content="Rol actualizado")
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rol not found")

# Eliminar un rol por su ID
@rolRoutes.delete("/{id}", tags=["roles"])
def delete_rol(id: int):
    existing_rol = conn.execute(roles.select().where(roles.c.rolid == id)).fetchone()
    if existing_rol:
        conn.execute(roles.delete().where(roles.c.rolid == id))
        conn.commit()
        return status.HTTP_200_OK
    else:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Rol not found")