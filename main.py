from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

from mysql.connector import MySQLConnection
from mysql.connector import Error

from fastapi.middleware.cors import CORSMiddleware

import datetime

#Conect to database 
mydbProyecto = MySQLConnection(
     host="beg3jcvse5jtip9hg9tj-mysql.services.clever-cloud.com",
     user="u2btrsl5fq4xslsn",
     password="9cxBWF6B9aAWy4Zjxqh1",
     database="beg3jcvse5jtip9hg9tj",
     port=3306
    )

#Create a cursor Object
cursor = mydbProyecto.cursor()


app = FastAPI()

#Configuracion de CORS
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
    
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Usuarios(BaseModel):
    email: str
    username: str
    password: str

@app.get("/usuarios", status_code=status.HTTP_200_OK)
def get_usuarios():
    select_query = "SELECT * FROM usuarios"
    cursor.execute(select_query)
    results = cursor.fetchall()
    return results 

@app.get("/usuarios/{id}", status_code=status.HTTP_200_OK)
def get_usuarios_by_id(id:int):
    select_query = "SELECT * FROM usuarios WHERE id = %s"
    cursor.execute(select_query, (id,))
    result = cursor.fetchone()
    if result:
        return result
    else: 
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

@app.post("/usuariosCrear", status_code=status.HTTP_201_CREATED)
async def insert_empleados(usuarios: Usuarios):
      insert_query = """
      INSERT INTO usuarios (email, username, password)
      VALUES (%s, %s, %s)
      """
      values = (usuarios.email, usuarios.username, usuarios.password)

      try:
          cursor.execute(insert_query, values)
          mydbProyecto.commit()
          return {"mensaje": "Usuario creado exitosamente"}
      except Error as error:
          raise HTTPException(status_code=400, detail=f"Error:{error}")

@app.put("/usuarios/{id}", status_code=status.HTTP_200_OK) 
def update_usuarios(id: int, usuarios: Usuarios): 
    update_query = """ 
    UPDATE usuarios SET nombreUsuario = %s, rol = %s, empleadoId = %s, fechaCreacion = %s WHERE id = %s """ 
    values = (usuarios.nombreUsuario, usuarios.rol, usuarios.empleadoId, usuarios.fechaCreacion, id) 
    try: 
        cursor.execute(update_query, values) 
        mydbProyecto.commit() 
        return {"message": "Usuario actualizado exitosamente"} 
    except mysql.connector.Error as error: 
        raise HTTPException(status_code=400, detail=f"Error: {error}") 
    

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

@app.post("/empleados", status_code=status.HTTP_201_CREATED) 
def insert_empleados(empleado: Empleado): 
    insert_query = """ 
    INSERT INTO empleados (id, nombre, rol, informacion_contacto) 
    VALUES (%s, %s, %s, %s) """ 
    values = (empleado.id, empleado.nombre, empleado.rol, empleado.informacion) 
    try: 
        cursor.execute(insert_query, values) 
        mydbProyecto.commit() 
        return {"message": "Empleado creado exitosamente"} 
    except mysql.connector.Error as error: 
        raise HTTPException(status_code=400, detail=f"Error:{error}") 
        
# Actualizar un empleado (Update) 
@app.put("/empleados/{id}", status_code=status.HTTP_200_OK) 
def update_empleados(id: int, empleado: Empleado): 
    update_query = """ 
    UPDATE empleados SET nombre = %s, rol = %s, informacion_contacto = %s WHERE id = %s """ 
    values = (empleado.nombre, empleado.rol, empleado.informacion, id) 
    try: 
        cursor.execute(update_query, values) 
        mydbProyecto.commit() return {"message": "Empleado actualizado exitosamente"} 
    except mysql.connector.Error as error: 
        raise HTTPException(status_code=400, detail=f"Error: {error}") 

# Eliminar un empleado (Delete) 
@app.delete("/empleados/{id}", status_code=status.HTTP_200_OK) 
def delete_empleados(id: int): 
    delete_query = "DELETE FROM empleados WHERE id = %s" 
    try: 
        cursor.execute(delete_query, (id,)) 
        mydbProyecto.commit() 
        return {"message": "Empleado eliminado exitosamente"} 
    except mysql.connector.Error as error: 
        raise HTTPException(status_code=400, detail=f"Error: {error}"

#Tabla Cliente 
class Cliente(BaseModel):
    id: int
    nombre: str
    informacion_contacto: str = None
    direccion: str = None

@app.get("/clientes", status_code=status.HTTP_200_OK)
def get_clientes():
    select_query = "SELECT * FROM clientes"
    cursor.execute(select_query)
    results = cursor.fetchall()
    return results

@app.get("/clientes/{id}", status_code=status.HTTP_200_OK)
def get_cliente_by_id(id: int):
    select_query = "SELECT * FROM clientes WHERE id = %s"
    cursor.execute(select_query, (id,))
    result = cursor.fetchone()
    if result:
        return result
    else:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

@app.post("/clientes", status_code=status.HTTP_201_CREATED)
def insert_cliente(cliente: Cliente):
    insert_query = """
    INSERT INTO clientes (id, nombre, informacion_contacto, direccion)
    VALUES (%s, %s, %s, %s)
    """
    values = (cliente.id, cliente.nombre, cliente.informacion_contacto, cliente.direccion)
    try:
        cursor.execute(insert_query, values)
        mydbProyecto.commit()
        return {"message": "Cliente creado exitosamente"}
    except mysql.connector.Error as error:
        raise HTTPException(status_code=400, detail=f"Error:{error}")

@app.put("/clientes/{id}", status_code=status.HTTP_200_OK)
def update_cliente(id: int, cliente: Cliente):
    update_query = """
    UPDATE clientes SET nombre = %s, informacion_contacto = %s, direccion = %s WHERE id = %s
    """
    values = (cliente.nombre, cliente.informacion_contacto, cliente.direccion, id)
    try:
        cursor.execute(update_query, values)
        mydbProyecto.commit()
        return {"message": "Cliente actualizado exitosamente"}
    except mysql.connector.Error as error:
        raise HTTPException(status_code=400, detail=f"Error: {error}")

@app.delete("/clientes/{id}", status_code=status.HTTP_200_OK)
def delete_cliente(id: int):
    delete_query = "DELETE FROM clientes WHERE id = %s"
    try:
        cursor.execute(delete_query, (id,))
        mydbProyecto.commit()
        return {"message": "Cliente eliminado exitosamente"}
    except mysql.connector.Error as error:
        raise HTTPException(status_code=400, detail=f"Error: {error}")


#Tabla Materias_Primas 

class MateriaPrima(BaseModel):
    id: int
    nombre: str
    proveedor_id: int = None
    cantidad: float
    unidad: str
    fecha_expiracion: str = None
    umbral_alerta: float

@app.get("/materias_primas", status_code=status.HTTP_200_OK)
def get_materias_primas():
    select_query = "SELECT * FROM materias_primas"
    cursor.execute(select_query)
    results = cursor.fetchall()
    return results

@app.get("/materias_primas/{id}", status_code=status.HTTP_200_OK)
def get_materia_prima_by_id(id: int):
    select_query = "SELECT * FROM materias_primas WHERE id = %s"
    cursor.execute(select_query, (id,))
    result = cursor.fetchone()
    if result:
        return result
    else:
        raise HTTPException(status_code=404, detail="Materia prima no encontrada")

@app.post("/materias_primas", status_code=status.HTTP_201_CREATED)
def insert_materia_prima(materia_prima: MateriaPrima):
    insert_query = """
    INSERT INTO materias_primas (id, nombre, proveedor_id, cantidad, unidad, fecha_expiracion, umbral_alerta)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    values = (materia_prima.id, materia_prima.nombre, materia_prima.proveedor_id, materia_prima.cantidad, materia_prima.unidad, materia_prima.fecha_expiracion, materia_prima.umbral_alerta)
    try:
        cursor.execute(insert_query, values)
        mydbProyecto.commit()
        return {"message": "Materia prima creada exitosamente"}
    except mysql.connector.Error as error:
        raise HTTPException(status_code=400, detail=f"Error:{error}")

@app.put("/materias_primas/{id}", status_code=status.HTTP_200_OK)
def update_materia_prima(id: int, materia_prima: MateriaPrima):
    update_query = """
    UPDATE materias_primas SET nombre = %s, proveedor_id = %s, cantidad = %s, unidad = %s, fecha_expiracion = %s, umbral_alerta = %s WHERE id = %s
    """
    values = (materia_prima.nombre, materia_prima.proveedor_id, materia_prima.cantidad, materia_prima.unidad, materia_prima.fecha_expiracion, materia_prima.umbral_alerta, id)
    try:
        cursor.execute(update_query, values)
        mydbProyecto.commit()
        return {"message": "Materia prima actualizada exitosamente"}
    except mysql.connector.Error as error:
        raise HTTPException(status_code=400, detail=f"Error: {error}")

@app.delete("/materias_primas/{id}", status_code=status.HTTP_200_OK)
def delete_materia_prima(id: int):
    delete_query = "DELETE FROM materias_primas WHERE id = %s"
    try:
        cursor.execute(delete_query, (id,))
        mydbProyecto.commit()
        return {"message": "Materia prima eliminada exitosamente"}
    except mysql.connector.Error as error:
        raise HTTPException(status_code=400, detail=f"Error: {error}")





