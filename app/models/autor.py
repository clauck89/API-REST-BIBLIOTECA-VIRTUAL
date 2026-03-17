from sqlalchemy import Column, Integer, String, Date, Text
from sqlalchemy.orm import relationship
from app.database import Base

class Autor(Base):
    __tablename__ = "autores"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(200), nullable=False)
    biografia = Column(Text, nullable=True)
    fecha_nacimiento = Column(Date, nullable=False)

    libros = relationship("Libro", back_populates="autor")