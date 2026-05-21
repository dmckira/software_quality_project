"""
src/routers/estudiantes.py
Endpoints para gestión de estudiantes.

DEUDA TÉCNICA:
  - [MEDIA] Sin validación de formato de email con EmailStr
  - [MEDIA] Código de respuesta HTTP hardcodeado como magic number
  - [BAJA]  Sin paginación en el endpoint de listado
"""
from fastapi import APIRouter, HTTPException
from src.models.schemas import EstudianteCreate, EstudianteResponse
from src.models.database import get_estudiantes

router = APIRouter(prefix="/estudiantes", tags=["Estudiantes"])


@router.post("/", response_model=EstudianteResponse, status_code=201, responses={
    400: {"description": "codigo duplicado, email invalido, o el semestra esta fuera del rango (1-10)"}
})
def crear_estudiante(estudiante: EstudianteCreate):
    db = get_estudiantes()
    codigo = estudiante.codigo.strip().upper()

    if codigo in db:
        raise HTTPException(status_code=400, detail="El código ya existe")

    if "@" not in estudiante.email:
        raise HTTPException(status_code=400, detail="Email inválido")

    if not (1 <= estudiante.semestre <= 10):
        raise HTTPException(status_code=400, detail="Semestre debe estar entre 1 y 10")

    db[codigo] = {
        "codigo": codigo,
        "nombre": estudiante.nombre.strip(),
        "email": estudiante.email.strip().lower(),
        "semestre": estudiante.semestre,
        "activo": True,
    }
    return db[codigo]


@router.get("/", response_model=list[EstudianteResponse])
def listar_estudiantes():
    # [DEUDA] Sin paginación — podría retornar miles de registros
    return list(get_estudiantes().values())


@router.get("/{codigo}", response_model=EstudianteResponse, responses={
    404: {"description": "Estudiante no encontrado"}
})
def obtener_estudiante(codigo: str):
    db = get_estudiantes()
    codigo = codigo.upper()
    if codigo not in db:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    return db[codigo]


@router.delete("/{codigo}", status_code=204,  responses={
    404: {"description": "Estudiante no encontrado"}
})
def eliminar_estudiante(codigo: str):
    db = get_estudiantes()
    codigo = codigo.upper()
    if codigo not in db:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    del db[codigo]


@router.put("/{codigo}/desactivar", response_model=EstudianteResponse, responses={
    404: {"description": "Estudiante no encontrado"}
})
def desactivar_estudiante(codigo: str):
    db = get_estudiantes()
    codigo = codigo.upper()
    if codigo not in db:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    db[codigo]["activo"] = False
    return db[codigo]
