from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import get_db
from app.models.prestamo import Prestamo
from app.models.libro import Libro
from app.schemas.prestamo import PrestamoCreate, PrestamoOut
from app.dependencies import get_current_active_user, get_admin_user
from app.models.user import User
from typing import List

router = APIRouter(prefix="/api", tags=["Préstamos"])

@router.get("/prestamos", response_model=List[PrestamoOut])
def listar_prestamos(
    db: Session = Depends(get_db),
    _: User = Depends(get_admin_user)
):
    return db.query(Prestamo).all()

@router.get("/mis-prestamos", response_model=List[PrestamoOut])
def mis_prestamos(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return db.query(Prestamo).filter(Prestamo.usuario_id == current_user.id).all()

@router.post("/prestamos", response_model=PrestamoOut, status_code=201)
def crear_prestamo(
    prestamo_data: PrestamoCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # Validar que el libro existe
    libro = db.query(Libro).filter(Libro.id == prestamo_data.libro_id).first()
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")

    # Validar copias disponibles
    if libro.copias_disponibles < 1:
        raise HTTPException(status_code=400, detail="No hay copias disponibles")

    # Validar máximo 3 préstamos activos
    prestamos_activos = db.query(Prestamo).filter(
        Prestamo.usuario_id == current_user.id,
        Prestamo.devuelto == False
    ).count()
    if prestamos_activos >= 3:
        raise HTTPException(status_code=400, detail="Ya tienes 3 préstamos activos")

    # Validar que no tenga el mismo libro sin devolver
    prestamo_existente = db.query(Prestamo).filter(
        Prestamo.usuario_id == current_user.id,
        Prestamo.libro_id == prestamo_data.libro_id,
        Prestamo.devuelto == False
    ).first()
    if prestamo_existente:
        raise HTTPException(status_code=400, detail="Ya tienes este libro prestado")

    # Crear préstamo y reducir copias
    prestamo = Prestamo(
        usuario_id=current_user.id,
        libro_id=prestamo_data.libro_id
    )
    libro.copias_disponibles -= 1
    db.add(prestamo)
    db.commit()
    db.refresh(prestamo)
    return prestamo

@router.post("/prestamos/{id}/devolver", response_model=PrestamoOut)
def devolver_libro(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    prestamo = db.query(Prestamo).filter(
        Prestamo.id == id,
        Prestamo.usuario_id == current_user.id
    ).first()
    if not prestamo:
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")
    if prestamo.devuelto:
        raise HTTPException(status_code=400, detail="Este libro ya fue devuelto")

    prestamo.devuelto = True
    prestamo.fecha_devolucion = datetime.utcnow()
    prestamo.libro.copias_disponibles += 1
    db.commit()
    db.refresh(prestamo)
    return prestamo