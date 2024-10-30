from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import mysql.connector

#Conect to database 
mydbProyecto = mysql.connector.connect(
    host="b82t0tp5jhudag9bplxj-mysql.services.clever-cloud.com",
    user="u4rury2dyfthr5ar",
    password="XINMiPV3FKruN6YgFPYE",
    database="b82t0tp5jhudag9bplxj",
    port=3306
)

#Create a cursor Object
cursor = mydbProyecto.cursor()

app = FastAPI()

class Empleado(BaseModel):
    id: int
    nombre: str
    rol: str
    informacion: str

@app.get("/empleados", status_code=status.HTTP_200_OK)
def get_empleados():
    select_query = "SELECT * FROM empleados"
    cursor.execute(select_query)
    results = cursor.fetchall()
    return results 

@app.get("/empleados/{id}", status_code=status.HTTP_200_OK)
def get_empleados_by_id(id:str):
    select_query = "SELECT * FROM empleados WHERE id = %s"
    cursor.execute(select_query, (id,))
    result = cursor.fetchone()
    if result:
        return result
    else: 
        raise HTTPException(status_code=404, detail="Empleado no encontrado")

@app.post("/empleados", status_code=status.HTTP_201_CREATED)
def insert_empleados(empleados: Empleado):
    insert_query = """
    INSERT INTO empleados (id, nombre, rol, informacion)
    VALUES (%s, %s, %s, %s)
    """
    values = (empleados.id, empleados.nombre, empleados.rol, empleados.informacion)

    try:
        cursor.execute(insert_query, values)
        mydbProyecto.commit()
    except mysql.connector.Error as error:
        raise HTTPException(status_code=400, detail=f"Error:{error}")