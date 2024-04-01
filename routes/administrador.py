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

@administradorRoutes.get("/login_admin", tags=["administradores"], response_model=Administrador, description="Get a administrador")
def login(username: str, passw: str):
    existing_admin = conn.execute(administradores.select().where(administradores.c.username == username and administradores.c.passw == passw)).first()
    if existing_admin:
        return existing_admin
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Admin not found")

# Obtener un administrador por su ID
@administradorRoutes.get("/administradores/{id}", tags=["administradores"], response_model=Administrador, description="Get a single administrator by ID")
def get_administrador(id: int):
    existing_administrador = conn.execute(administradores.select().where(administradores.c.administradorid == id)).first()
    if existing_administrador:
        return existing_administrador
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Administrador not found")

# Crear un nuevo administrador
@administradorRoutes.post("/administradores", tags=["administradores"], response_model=Administrador, description="Create a new administrator")
def create_administrador(administrador: Administrador):
    try:
        new_administrador = {"nombre": administrador.nombre,
                             "apellido": administrador.apellido,
                             "documento": administrador.documento,
                             "email": administrador.email,
                             "celular": administrador.celular,
                             "username": administrador.username,
                             "passw": administrador.passw,
                             "rolid": administrador.rolid}
        result = conn.execute(insert(administradores).values(new_administrador))
        new_administrador["administradorid"] = result.inserted_primary_key[0]
        conn.commit()
        return new_administrador
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# Actualizar un administrador por su ID
@administradorRoutes.put("/administradores/{id}", tags=["administradores"], response_model=Administrador, description="Update an administrator by ID")
def update_administrador(id: int, administrador: Administrador):
    existing_administrador = conn.execute(administradores.select().where(administradores.c.administradorid == id)).fetchone()
    if existing_administrador:
        conn.execute(
            administradores.update()
            .values(nombre=administrador.nombre,
                    apellido=administrador.apellido,
                    documento=administrador.documento,
                    email=administrador.email,
                    celular=administrador.celular,
                    username=administrador.username,
                    passw=administrador.passw,
                    rolid=administrador.rolid)
            .where(administradores.c.administradorid == id)
        )
        conn.commit()
        return Response(status_code=status.HTTP_200_OK, content="Administrador actualizado")
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Administrador not found")

# Eliminar un administrador por su ID
@administradorRoutes.delete("/administradores/{id}", tags=["administradores"])
def delete_administrador(id: int):
    existing_administrador = conn.execute(administradores.select().where(administradores.c.administradorid == id)).fetchone()
    if existing_administrador:
        conn.execute(administradores.delete().where(administradores.c.administradorid == id))
        conn.commit()
        return status.HTTP_200_OK
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Administrador not found")