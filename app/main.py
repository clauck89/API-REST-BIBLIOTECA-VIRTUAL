from fastapi import FastAPI
from app.routers import autores, categorias, libros, prestamos, auth

app = FastAPI(
    title="Biblioteca Virtual API",
    description="API REST para gestionar una Biblioteca Virtual",
    version="1.0.0"
)

app.include_router(auth.router)
app.include_router(autores.router)
app.include_router(categorias.router)
app.include_router(libros.router)
app.include_router(prestamos.router)

@app.get("/")
def root():
    return {"message": "Bienvenido a la API de Biblioteca Virtual"}