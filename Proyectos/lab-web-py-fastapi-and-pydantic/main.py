from fastapi import FastAPI, HTTPException
from datetime import datetime
from models.tarea import TareaEntrada, TareaActualizacion

app = FastAPI()
tareas = []
contador_id = 1

# POST /tareas - Crear tarea
@app.post("/tareas")
def crear_tarea(tarea: TareaEntrada):
    global contador_id

    nueva_tarea = {
        "id": contador_id,
        "titulo": tarea.titulo,
        "descripcion": tarea.descripcion,
        "prioridad": tarea.prioridad,
        "completada": False,
        "creada_en": datetime.now(),
        "completada_en": None,
        "fecha_limite": tarea.fecha_limite
    }

    tareas.append(nueva_tarea)
    contador_id += 1

    return nueva_tarea

# GET /tareas - Listar todas (filtrar por ?completada=true/false&prioridad=alta)
@app.get("/tareas")
def listar_tareas(completada: bool = None, prioridad: str = None):
    resultado = tareas

    if completada is not None:
        resultado = [
            tarea for tarea in resultado
            if tarea["completada"] == completada
        ]

    if prioridad is not None:
        resultado = [
            tarea for tarea in resultado
            if tarea["prioridad"] == prioridad
        ]

    return resultado

# GET /tareas/{id} - Obtener una tarea
@app.get("/tareas/{id}")
def obtener_tarea(id: int):
    for tarea in tareas:
        if tarea["id"] == id:
            return tarea

    raise HTTPException(status_code=404, detail="Tarea no encontrada")

# PATCH /tareas/{id} - Actualizar campos concretos
@app.patch("/tareas/{id}")
def actualizar_tarea(id: int, datos: TareaActualizacion):
    for tarea in tareas:
        if tarea["id"] == id:

            if datos.titulo is not None:
                tarea["titulo"] = datos.titulo

            if datos.descripcion is not None:
                tarea["descripcion"] = datos.descripcion

            if datos.prioridad is not None:
                tarea["prioridad"] = datos.prioridad

            if datos.completada is not None:
                tarea["completada"] = datos.completada

            if datos.fecha_limite is not None:
                tarea["fecha_limite"] = datos.fecha_limite

            return tarea

    raise HTTPException(status_code=404, detail="Tarea no encontrada")

# DELETE /tareas/{id} - Eliminar
@app.delete("/tareas/{id}")
def eliminar_tarea(id: int):
    for tarea in tareas:
        if tarea["id"] == id:
            tareas.remove(tarea)
            return {"mensaje": "Tarea eliminada"}

    raise HTTPException(status_code=404, detail="Tarea no encontrada")

# POST /tareas/{id}/completar - Marcar como completada (registrar timestamp)
@app.post("/tareas/{id}/completar")
def completar_tarea(id: int):
    for tarea in tareas:
        if tarea["id"] == id:
            tarea["completada"] = True
            tarea["completada_en"] = datetime.now()

            return tarea

    raise HTTPException(status_code=404, detail="Tarea no encontrada")

# GET /tareas/estadisticas - Resumen: total, completadas, pendientes por prioridad
@app.get("/tareas/estadisticas")
def estadisticas():
    total = len(tareas)

    completadas = len([
        tarea for tarea in tareas
        if tarea["completada"]
    ])

    pendientes = total - completadas

    prioridad_alta = len([
        tarea for tarea in tareas
        if tarea["prioridad"] == "alta"
    ])

    prioridad_media = len([
        tarea for tarea in tareas
        if tarea["prioridad"] == "media"
    ])

    prioridad_baja = len([
        tarea for tarea in tareas
        if tarea["prioridad"] == "baja"
    ])

    return {
        "total": total,
        "completadas": completadas,
        "pendientes": pendientes,
        "por_prioridad": {
            "alta": prioridad_alta,
            "media": prioridad_media,
            "baja": prioridad_baja
        }
    }
