from fastapi import FastAPI, HTTPException
from db import get_db_connection
from models import Recipie
import mysql.connector

app = FastAPI()

# Ruta para obtener todas las recetas
@app.get("/recipies", response_model=list[Recipie])
def get_recipies():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Recipies")
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows

# Ruta para obtener una receta por ID
@app.get("/recipies/{recipie_id}", response_model=Recipie)
def get_recipie(recipie_id: int):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Recipies WHERE id = %s", (recipie_id,))
    row = cursor.fetchone()
    cursor.close()
    connection.close()
    
    if row is None:
        raise HTTPException(status_code=404, detail="Recipie not found")
    return row

# Ruta para agregar una receta
@app.post("/recipies", response_model=Recipie)
def add_recipie(recipie: Recipie):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO Recipies (name, ingredients, instructions) VALUES (%s, %s, %s)",
        (recipie.name, recipie.ingredients, recipie.instructions)
    )
    connection.commit()
    cursor.close()
    connection.close()
    return recipie
