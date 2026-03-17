from pydantic import BaseModel
from datetime import date
from app.schemas.autor import AutorOut
from app.schemas.categoria import CategoriaOut

class LibroBase(BaseModel):
    titulo: str
    isbn: str
    fecha_publicacion: date
    copias_disponibles: int = 1
    autor_id: int
    categoria_id: int | None = None

class LibroCreate(LibroBase):
    pass

class LibroUpdate(LibroBase):
    pass

class LibroOut(LibroBase):
    id: int
    autor: AutorOut
    categoria: CategoriaOut | None = None

    class Config:
        from_attributes = True