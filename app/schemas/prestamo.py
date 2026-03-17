from pydantic import BaseModel
from datetime import datetime
from app.schemas.user import UserOut
from app.schemas.libro import LibroOut

class PrestamoBase(BaseModel):
    libro_id: int

class PrestamoCreate(PrestamoBase):
    pass

class PrestamoOut(BaseModel):
    id: int
    libro_id: int
    usuario_id: int
    fecha_prestamo: datetime
    fecha_devolucion: datetime | None = None
    devuelto: bool
    libro: LibroOut

    class Config:
        from_attributes = True