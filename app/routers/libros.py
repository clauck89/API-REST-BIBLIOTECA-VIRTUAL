from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.libro import Libro
from app.schemas.libro import LibroCreate, LibroUpdate, LibroOut
from app.dependencies import get_admin_user
from typing import List, Optional

router = APIRouter(prefix="/api/libros", tags=["Libros"])

@router.get("/", response_model=List[LibroOut])
def listar_libros(
    db: Session = Depends(get_db),
    search: Optional[str] = Query(None, description="Buscar por título o ISBN"),
    categoria_id: Optional[int] = Query(None),
    autor_id: Optional[int] = Query(None),
    order_by: Optional[str] = Query(None, description="titulo o fecha_publicacion")
):
    query = db.query(Libro)
    if search:
        query = query.filter(
            Libro.titulo.ilike(f"%{search}%") | Libro.isbn.ilike(f"%{search}%")
        )
    if categoria_id:
        query = query.filter(Libro.categoria_id == categoria_id)
    if autor_id:
        query = query.filter(Libro.autor_id == autor_id)
    if order_by == "titulo":
        query = query.order_by(Libro.titulo)
    elif order_by == "fecha_publicacion":
        query = query.order_by(Libro.fecha_publicacion)
    return query.all()

@router.get("/{id}", response_model=LibroOut)
def detalle_libro(id: int, db: Session = Depends(get_db)):
    libro = db.query(Libro).filter(Libro.id == id).first()
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return libro

@router.post("/", response_model=LibroOut, status_code=201)
def crear_libro(
    libro_data: LibroCreate,
    db: Session = Depends(get_db),
    _: dict = Depends(get_admin_user)
):
    if db.query(Libro).filter(Libro.isbn == libro_data.isbn).first():
        raise HTTPException(status_code=400, detail="El ISBN ya existe")
    libro = Libro(**libro_data.model_dump())
    db.add(libro)
    db.commit()
    db.refresh(libro)
    return libro

@router.put("/{id}", response_model=LibroOut)
def actualizar_libro(
    id: int,
    libro_data: LibroUpdate,
    db: Session = Depends(get_db),
    _: dict = Depends(get_admin_user)
):
    libro = db.query(Libro).filter(Libro.id == id).first()
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    for key, value in libro_data.model_dump().items():
        setattr(libro, key, value)
    db.commit()
    db.refresh(libro)
    return libro

@router.delete("/{id}", status_code=204)
def eliminar_libro(
    id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(get_admin_user)
):
    libro = db.query(Libro).filter(Libro.id == id).first()
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    db.delete(libro)
    db.commit()