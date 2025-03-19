from pydantic import BaseModel
from typing import Optional

# Modelo de Recipe para crear o mostrar la receta
class Recipe(BaseModel):
    idRecipe: int
    nombre: str
    descripcion: str
    tiempo: int
    dificultad: str
    raciones: int
    imagen: str

# Modelo de Recipe para actualizar, con campos opcionales
class RecipeUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    tiempo: Optional[int] = None
    dificultad: Optional[str] = None
    raciones: Optional[int] = None
    imagen: Optional[str] = None
