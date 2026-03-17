from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Libro(Base):
    __tablename__ = "libros"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(300), nullable=False)
    isbn = Column(String(13), unique=True, nullable=False)
    fecha_publicacion = Column(Date, nullable=False)
    copias_disponibles = Column(Integer, default=1)
    autor_id = Column(Integer, ForeignKey("autores.id"), nullable=False)
    categoria_id = Column(Integer, ForeignKey("categorias.id"), nullable=True)

    autor = relationship("Autor", back_populates="libros")
    categoria = relationship("Categoria", back_populates="libros")
    prestamos = relationship("Prestamo", back_populates="libro")