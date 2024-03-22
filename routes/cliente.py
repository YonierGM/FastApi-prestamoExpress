from fastapi import APIRouter, HTTPException, Response, status
from typing import List
from sqlalchemy import insert

from config.db import conn
from models.cliente import clientes
from schemas.cliente import Cliente

clienteRoutes = APIRouter()

# Obtener todos los clientes
@clienteRoutes.get("/clientes", tags=["clientes"], response_model=List[Cliente], description="Get a list of all clients")
def get_clientes():
    return conn.execute(clientes.select()).fetchall()

# Obtener un cliente por su ID
@clienteRoutes.get("/clientes/{id}", tags=["clientes"], response_model=Cliente, description="Get a single client by ID")
def get_cliente(id: int):
    return conn.execute(clientes.select().where(clientes.c.clienteid == id)).first()

# Crear un nuevo cliente
@clienteRoutes.post("/clientes", tags=["clientes"], response_model=Cliente, description="Create a new client")
def create_cliente(cliente: Cliente):
    try:
        new_cliente = {"nombre": cliente.nombre, "apellido": cliente.apellido, "documento": cliente.documento, "fecha_nac": cliente.fecha_nac, "direccion": cliente.direccion, "celular": cliente.celular, "email": cliente.email, "rolid": cliente.rolid}
        result = conn.execute(insert(clientes).values(new_cliente))
        new_cliente["clienteid"] = result.inserted_primary_key[0]
        return new_cliente
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Actualizar un cliente por su ID
@clienteRoutes.put("/clientes/{id}", tags=["clientes"], response_model=Cliente, description="Update a client by ID")
def update_cliente(id: int, cliente: Cliente):
    conn.execute(
        clientes.update()
        .values(nombre=cliente.nombre, apellido=cliente.apellido, documento=cliente.documento, fecha_nac=cliente.fecha_nac, direccion=cliente.direccion, celular=cliente.celular, email=cliente.email, rolid=cliente.rolid)
        .where(clientes.c.clienteid == id)
    )
    conn.commit()
    return cliente

# Eliminar un cliente por su ID
@clienteRoutes.delete("/clientes/{id}", tags=["clientes"])
def delete_cliente(id: int):
    cliente = conn.execute(clientes.select().where(clientes.c.clienteid == id)).fetchone()
    if cliente:
        conn.execute(clientes.delete().where(clientes.c.clienteid == id))
        conn.commit()
        return Response(status_code=status.HTTP_200_OK, content="Cliente eliminado")
    else:
        return Response(status_code=status.HTTP_404_NOT_FOUND, content="Cliente no encontrado")
