from fastapi import APIRouter, HTTPException, Response, status
from typing import List
from sqlalchemy import insert

from config.db import conn
from models.usuario import usuarios
from schemas.usuario import Usuario

usuarioRoutes = APIRouter()

# Obtener todos los usuarios
@usuarioRoutes.get("/usuarios", tags=["usuarios"], response_model=List[Usuario], description="Get a list of all users")
def get_usuarios():
    return conn.execute(usuarios.select()).fetchall()

# Obtener un usuario por su ID
@usuarioRoutes.get("/usuarios/{id}", tags=["usuarios"], response_model=Usuario, description="Get a single user by ID")
def get_usuario(id: int):
    return conn.execute(usuarios.select().where(usuarios.c.usuarioid == id)).first()

# Crear un nuevo usuario
@usuarioRoutes.post("/usuarios", tags=["usuarios"], response_model=Usuario, description="Create a new user")
def create_usuario(usuario: Usuario):
    try:
        new_usuario = {"username": usuario.username, "passw": usuario.passw, "rolid": usuario.rolid}
        result = conn.execute(insert(usuarios).values(new_usuario))
        new_usuario["usuarioid"] = result.inserted_primary_key[0]
        return new_usuario
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Actualizar un usuario por su ID
@usuarioRoutes.put("/usuarios/{id}", tags=["usuarios"], response_model=Usuario, description="Update a user by ID")
def update_usuario(id: int, usuario: Usuario):
    conn.execute(
        usuarios.update()
        .values(username=usuario.username, passw=usuario.passw, rolid=usuario.rolid)
        .where(usuarios.c.usuarioid == id)
    )
    conn.commit()
    return usuario

# Eliminar un usuario por su ID
@usuarioRoutes.delete("/usuarios/{id}", tags=["usuarios"])
def delete_usuario(id: int):
    usuario = conn.execute(usuarios.select().where(usuarios.c.usuarioid == id)).fetchone()
    if usuario:
        conn.execute(usuarios.delete().where(usuarios.c.usuarioid == id))
        conn.commit()
        return Response(status_code=status.HTTP_200_OK, content="Usuario eliminado")
    else:
        return Response(status_code=status.HTTP_404_NOT_FOUND, content="Usuario no encontrado")