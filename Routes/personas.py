# routes/personas.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from Config.DatabaseConn import get_db
from Models.Persona import Persona, PersonaCreate, PersonaRead

router = APIRouter()

@router.post("/personas/", response_model=PersonaRead)
def crear_persona(persona: PersonaCreate, db: Session = Depends(get_db)):
    db_persona = Persona(**persona.model_dump())
    db.add(db_persona)
    db.commit()
    db.refresh(db_persona)
    return db_persona

@router.get("/personas/{persona_id}", response_model=PersonaRead)
def obtener_persona(persona_id: int, db: Session = Depends(get_db)):
    persona = db.query(Persona).filter(Persona.id == persona_id).first()
    if not persona:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    return persona

@router.get("/personas/", response_model=list[PersonaRead])
def listar_personas(db: Session = Depends(get_db)):
    return db.query(Persona).all()

@router.put("/personas/{persona_id}", response_model=PersonaRead)
def modificar_persona(persona_id: int, persona: PersonaCreate, db: Session = Depends(get_db)):
    db_persona = db.query(Persona).filter(Persona.id == persona_id).first()
    if not db_persona:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    for key, value in persona.model_dump().items():
        setattr(db_persona, key, value)
    db.commit()
    db.refresh(db_persona)
    return db_persona

@router.delete("/personas/{persona_id}")
def eliminar_persona(persona_id: int, db: Session = Depends(get_db)):
    db_persona = db.query(Persona).filter(Persona.id == persona_id).first()
    if not db_persona:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    db.delete(db_persona)
    db.commit()
    return {"ok": True}