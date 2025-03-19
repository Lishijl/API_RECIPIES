from fastapi import FastAPI, HTTPException
from db import get_db_connection
from models import Recipe, RecipeUpdate

app = FastAPI()
# Endpoint para obtener todas las recetas
@app.get("/recipes/get")
def get_recipes():
    with get_db_connection() as conn:  # Cierra automáticamente al salir del bloque
        with conn.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT * FROM Recipe")
            recipes = cursor.fetchall()
    return recipes

# Endpoint para obtener una receta por su ID
@app.get("/recipes/get/{idRecipe}")
def get_recipe(idRecipe: int):
    with get_db_connection() as conn:
        with conn.cursor(dictionary=True) as cursor:
            # Consultar la base de datos para obtener la receta por ID
            cursor.execute("SELECT * FROM Recipe WHERE idRecipe = %s", (idRecipe,))
            recipe = cursor.fetchone()
             # Si no se encuentra la receta, lanzar un error 404
            if recipe is None:
                raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe

# Endpoint para crear una receta
@app.post("/recipes/crea")
def create_recipe(recipe: Recipe):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO Recipe (nombre, descripcion, tiempo, dificultad, raciones, imagen) VALUES (%s, %s, %s, %s, %s, %s)",
                (recipe.nombre, recipe.descripcion, recipe.tiempo, recipe.dificultad, recipe.raciones, recipe.imagen)
            )
            conn.commit()
    return {"message": "Recipe created successfully"}

# Endpoint para eliminar una receta
@app.delete("/recipes/delete/{idRecipe}")
def delete_recipe(idRecipe: int):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            # Verifica si la receta existe antes de intentar eliminarla
            cursor.execute("SELECT * FROM Recipe WHERE idRecipe = %s", (idRecipe,))
            recipe = cursor.fetchone()
            if recipe is None:
                raise HTTPException(status_code=404, detail="Recipe not found")
            # Elimina la receta
            cursor.execute("DELETE FROM Recipe WHERE idRecipe = %s", (idRecipe,))
            conn.commit()
    return {"message": f"Recipe with id {idRecipe} deleted successfully"}

# Endpoint para actualizar una receta
@app.put("/recipes/update/{idRecipe}")
def update_recipe(idRecipe: int, recipe_update: RecipeUpdate):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            # Verifica si la receta existe antes de intentar actualizarla
            cursor.execute("SELECT * FROM Recipe WHERE idRecipe = %s", (idRecipe,))
            recipe = cursor.fetchone()

            if recipe is None:
                raise HTTPException(status_code=404, detail="Recipe not found")

            # Preparamos la consulta de actualización
            update_fields = []
            update_values = []

            if recipe_update.nombre:
                update_fields.append("nombre = %s")
                update_values.append(recipe_update.nombre)
            if recipe_update.descripcion:
                update_fields.append("descripcion = %s")
                update_values.append(recipe_update.descripcion)
            if recipe_update.tiempo:
                update_fields.append("tiempo = %s")
                update_values.append(recipe_update.tiempo)
            if recipe_update.dificultad:
                update_fields.append("dificultad = %s")
                update_values.append(recipe_update.dificultad)
            if recipe_update.raciones:
                update_fields.append("raciones = %s")
                update_values.append(recipe_update.raciones)
            if recipe_update.imagen:
                update_fields.append("imagen = %s")
                update_values.append(recipe_update.imagen)

            # Si no hay campos para actualizar, retornar un error
            if not update_fields:
                raise HTTPException(status_code=400, detail="No fields to update")

            # Añadir el ID al final de los valores de actualización
            update_values.append(idRecipe)

            # Construimos la consulta SQL
            update_query = f"UPDATE Recipe SET {', '.join(update_fields)} WHERE idRecipe = %s"

            # Ejecutar la consulta de actualización
            cursor.execute(update_query, tuple(update_values))
            conn.commit()

    return {"message": f"Recipe with id {idRecipe} updated successfully"}
