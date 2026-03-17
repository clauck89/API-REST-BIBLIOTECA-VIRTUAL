from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.categoria import Categoria
from app.schemas.categoria import CategoriaCreate, CategoriaUpdate, CategoriaOut
from app.dependencies import get_admin_user
from typing import List

router = APIRouter(prefix="/api/categorias", tags=["Categorías"])

@router.get("/", response_model=List[CategoriaOut])
def listar_categorias(db: Session = Depends(get_db)):
    return db.query(Categoria).all()

@router.get("/{id}", response_model=CategoriaOut)
def detalle_categoria(id: int, db: Session = Depends(get_db)):
    categoria = db.query(Categoria).filter(Categoria.id == id).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return categoria

@router.post("/", response_model=CategoriaOut, status_code=201)
def crear_categoria(
    categoria_data: CategoriaCreate,
    db: Session = Depends(get_db),
    _: dict = Depends(get_admin_user)
):
    if db.query(Categoria).filter(Categoria.nombre == categoria_data.nombre).first():
        raise HTTPException(status_code=400, detail="La categoría ya existe")
    categoria = Categoria(**categoria_data.model_dump())
    db.add(categoria)
    db.commit()
    db.refresh(categoria)
    return categoria

@router.put("/{id}", response_model=CategoriaOut)
def actualizar_categoria(
    id: int,
    categoria_data: CategoriaUpdate,
    db: Session = Depends(get_db),
    _: dict = Depends(get_admin_user)
):
    categoria = db.query(Categoria).filter(Categoria.id == id).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    for key, value in categoria_data.model_dump().items():
        setattr(categoria, key, value)
    db.commit()
    db.refresh(categoria)
    return categoria

@router.delete("/{id}", status_code=204)
def eliminar_categoria(
    id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(get_admin_user)
):
    categoria = db.query(Categoria).filter(Categoria.id == id).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    db.delete(categoria)
    db.commit()