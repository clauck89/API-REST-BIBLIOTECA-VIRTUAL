from pydantic import BaseModel
from datetime import date

class AutorBase(BaseModel):
    nombre: str
    biografia: str | None = None
    fecha_nacimiento: date

class AutorCreate(AutorBase):
    pass

class AutorUpdate(AutorBase):
    pass

class AutorOut(AutorBase):
    id: int

    class Config:
        from_attributes = True