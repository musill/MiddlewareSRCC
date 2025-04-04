from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

app = FastAPI()
DATABASE_URL = "sqlite:///./estudiantes.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# MODELOS

class Estudiante(Base):
    __tablename__ = "estudiantes"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    matriculas = relationship("Matricula", back_populates="estudiante")

class Matricula(Base):
    __tablename__ = "matriculas"
    id = Column(Integer, primary_key=True, index=True)
    estudiante_id = Column(Integer, ForeignKey("estudiantes.id"))
    asignatura = Column(String)
    nota1 = Column(Float)
    nota2 = Column(Float)
    nota_supletorio = Column(Float)
    estudiante = relationship("Estudiante", back_populates="matriculas")

Base.metadata.create_all(bind=engine)

# SCHEMAS

class EstudianteCreate(BaseModel):
    nombre: str

class MatriculaCreate(BaseModel):
    estudiante_id: int
    asignatura: str
    nota1: float
    nota2: float
    nota_supletorio: float

# ENDPOINTS

@app.post("/estudiantes/")
def crear_estudiante(est: EstudianteCreate):
    db = SessionLocal()
    nuevo = Estudiante(nombre=est.nombre)
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@app.post("/matriculas/")
def crear_matricula(mat: MatriculaCreate):
    db = SessionLocal()
    estudiante = db.query(Estudiante).filter_by(id=mat.estudiante_id).first()
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    nueva = Matricula(**mat.dict())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

@app.get("/matriculas/")
def listar_matriculas():
    db = SessionLocal()
    return db.query(Matricula).all()
