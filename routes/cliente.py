from fastapi import APIRouter, HTTPException, Response, status
from typing import List

from sqlalchemy import insert

from config.db import conn
from models.cliente import clientes
from models.prestamo import prestamos
from schemas.cliente import Cliente

clienteRoutes = APIRouter()

@clienteRoutes.get("/clientes", tags=["clientes"], response_model=list[Cliente], description="Get a list of allclients")
def get_clientes():
    return conn.execute(clientes.select()).fetchall()

# Obtener todos los clientes
@clienteRoutes.get("/login_cliente", tags=["clientes"], response_model=Cliente, description="Get a clients")
def login(username: str, passw: str):
    existing_cliente = conn.execute(clientes.select().where(clientes.c.username == username and clientes.c.passw == passw)).first()
    if existing_cliente:
        return existing_cliente
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente not found")

# Obtener un cliente por su ID
@clienteRoutes.get("/clientes/{id}", tags=["clientes"], response_model=Cliente, description="Get a single client by ID")
def get_cliente(id: int):
    existing_cliente = conn.execute(clientes.select().where(clientes.c.clienteid == id)).first()
    if existing_cliente:
        return existing_cliente
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente not found")

# Crear un nuevo cliente
@clienteRoutes.post("/clientes", tags=["clientes"], response_model=Cliente, description="Create a new client")
def create_cliente(cliente: Cliente):
    try:
        new_cliente = {"nombre": cliente.nombre,
                       "apellido": cliente.apellido,
                       "documento": cliente.documento,
                       "fecha_nac": cliente.fecha_nac,
                       "direccion": cliente.direccion,
                       "celular": cliente.celular,
                       "email": cliente.email,
                       "username": cliente.username,
                       "passw": cliente.passw,
                       "rolid": cliente.rolid}
        result = conn.execute(insert(clientes).values(new_cliente))
        new_cliente["clienteid"] = result.inserted_primary_key[0]
        conn.commit()
        return new_cliente

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# Actualizar un cliente por su ID
@clienteRoutes.put("/clientes/{id}", tags=["clientes"], response_model=Cliente, description="Update a client by ID")
def update_cliente(id: int, cliente: Cliente):
    existing_cliente = conn.execute(clientes.select().where(clientes.c.clienteid == id)).fetchone()
    if existing_cliente:
        conn.execute(
            clientes.update()
            .values(nombre=cliente.nombre,
                    apellido=cliente.apellido,
                    documento=cliente.documento,
                    fecha_nac=cliente.fecha_nac,
                    direccion=cliente.direccion,
                    celular=cliente.celular,
                    email=cliente.email,
                    username=cliente.username,
                    passw=cliente.passw,
                    rolid=cliente.rolid)
            .where(clientes.c.clienteid == id)
        )
        conn.commit()
        return existing_cliente
    else:
         return status.HTTP_404_NOT_FOUND

# Eliminar un cliente por su ID
@clienteRoutes.delete("/clientes/{id}", tags=["clientes"])
def delete_cliente(id: int):
    existing_cliente = conn.execute(clientes.select().where(clientes.c.clienteid == id)).fetchone()
    if existing_cliente:
        print("cliente existe")

        prestamo_cliente = conn.execute(prestamos.select().where(prestamos.c.clienteid == existing_cliente.clienteid)).fetchall()

        if prestamo_cliente:
            print("hola")

            return HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail= "El cliente tiene prestamos activos")
        else:

            conn.execute(clientes.delete().where(clientes.c.clienteid == id))
            conn.commit()
            return status.HTTP_200_OK
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente not found")