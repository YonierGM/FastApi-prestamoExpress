from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from routes.cliente import clienteRoutes
from routes.rol import rolRoutes
from routes.administrador import administradorRoutes
from routes.estadoprestamo import estadoPrestamoRoutes
from routes.pago import pagoRoutes
from routes.prestamo import prestamoRoutes
from routes.tipoprestamo import tipoPrestamoRoutes
from routes.usuario import usuarioRoutes

backend = FastAPI()
# Configurar CORS
backend.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Reemplaza esto con el origen de tu aplicación React
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

backend.include_router(rolRoutes)
backend.include_router(clienteRoutes)
backend.include_router(administradorRoutes)
backend.include_router(estadoPrestamoRoutes)
backend.include_router(pagoRoutes)
backend.include_router(prestamoRoutes)
backend.include_router(tipoPrestamoRoutes)
backend.include_router(usuarioRoutes)