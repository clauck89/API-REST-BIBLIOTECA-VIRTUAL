from sqlalchemy import Column, Integer, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Prestamo(Base):
    __tablename__ = "prestamos"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    libro_id = Column(Integer, ForeignKey("libros.id"), nullable=False)
    fecha_prestamo = Column(DateTime, server_default=func.now())
    fecha_devolucion = Column(DateTime, nullable=True)
    devuelto = Column(Boolean, default=False)

    usuario = relationship("User")
    libro = relationship("Libro", back_populates="prestamos")