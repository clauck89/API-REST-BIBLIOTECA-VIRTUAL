from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.autor import Autor
from app.schemas.autor import AutorCreate, AutorUpdate, AutorOut
from app.dependencies import get_admin_user
from typing import List

router = APIRouter(prefix="/api/autores", tags=["Autores"])

@router.get("/", response_model=List[AutorOut])
def listar_autores(db: Session = Depends(get_db)):
    return db.query(Autor).all()

@router.get("/{id}", response_model=AutorOut)
def detalle_autor(id: int, db: Session = Depends(get_db)):
    autor = db.query(Autor).filter(Autor.id == id).first()
    if not autor:
        raise HTTPException(status_code=404, detail="Autor no encontrado")
    return autor

@router.post("/", response_model=AutorOut, status_code=201)
def crear_autor(
    autor_data: AutorCreate,
    db: Session = Depends(get_db),
    _: dict = Depends(get_admin_user)
):
    autor = Autor(**autor_data.model_dump())
    db.add(autor)
    db.commit()
    db.refresh(autor)
    return autor

@router.put("/{id}", response_model=AutorOut)
def actualizar_autor(
    id: int,
    autor_data: AutorUpdate,
    db: Session = Depends(get_db),
    _: dict = Depends(get_admin_user)
):
    autor = db.query(Autor).filter(Autor.id == id).first()
    if not autor:
        raise HTTPException(status_code=404, detail="Autor no encontrado")
    for key, value in autor_data.model_dump().items():
        setattr(autor, key, value)
    db.commit()
    db.refresh(autor)
    return autor

@router.delete("/{id}", status_code=204)
def eliminar_autor(
    id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(get_admin_user)
):
    autor = db.query(Autor).filter(Autor.id == id).first()
    if not autor:
        raise HTTPException(status_code=404, detail="Autor no encontrado")
    db.delete(autor)
    db.commit()