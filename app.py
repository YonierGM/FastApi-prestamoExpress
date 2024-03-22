from fastapi import FastAPI
from routes.cliente import clienteRoutes
from routes.rol import rolRoutes
from routes.administrador import administradorRoutes
from routes.estadoprestamo import estadoPrestamoRoutes
from routes.pago import pagoRoutes
from routes.prestamo import prestamoRoutes
from routes.tipoprestamo import tipoPrestamoRoutes
from routes.usuario import usuarioRoutes

backend = FastAPI()

backend.include_router(rolRoutes)
backend.include_router(clienteRoutes)
backend.include_router(administradorRoutes)
backend.include_router(estadoPrestamoRoutes)
backend.include_router(pagoRoutes)
backend.include_router(prestamoRoutes)
backend.include_router(tipoPrestamoRoutes)
backend.include_router(usuarioRoutes)