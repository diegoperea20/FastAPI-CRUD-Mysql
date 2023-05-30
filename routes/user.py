from fastapi import APIRouter
from config.db import conn
from models.user import users
from schemas.user import User

#part of encrypt password
from cryptography.fernet import Fernet
key = Fernet.generate_key()
f=Fernet(key)
#---------------------------------------


user= APIRouter()

from sqlalchemy import select



@user.get("/users")
def get_users():
    result = conn.execute(select(users.c.id, users.c.name, users.c.email, users.c.password))
# Specify the columns to select
    users_list = [dict(row._asdict()) for row in result.fetchall()]
    return users_list


@user.post("/users")
def create_user(user:User):
    new_user={"name":user.name,"email":user.email}
    new_user["password"]=f.encrypt(user.password.encode("utf-8"))
    result=conn.execute(users.insert().values(new_user))
    # Confirmar los cambios en la base de datos
    conn.commit()
    return "User created"


@user.get("/users/{id}")
def get_user(id: int):
    # Realizar la consulta a la base de datos para obtener el usuario con el ID especificado
    user = conn.execute(users.select().where(users.c.id == id)).fetchone()

    if user:
        # Si se encontró el usuario, devolver los datos correspondientes
        user_data = {
            "id": user.id,
            "name": user.name,
            "email": user.email,
        }
        return user_data
    else:
        # Si no se encontró el usuario, devolver un mensaje de error o el código de respuesta adecuado
        return {"error": "User not found"}

@user.put("/users/{id}")
def update_user(user: User, id: int):
    conn.execute(
        users.update()
        .values(name=user.name, email=user.email, password=user.password)
        .where(users.c.id == id)
    )
    result = conn.execute(users.select().where(users.c.id == id)).fetchone()
    user_dict = {
        "id": result.id,
        "name": result.name,
        "email": result.email,
        "password": result.password,
    } 
    conn.commit() 
    return user_dict

@user.delete("/users/{id}")
def delete_user(id: int):
    # Realizar la consulta a la base de datos para eliminar el usuario con el ID especificado
    result = conn.execute(users.delete().where(users.c.id == id))
    if result.rowcount > 0:
        # Si se eliminó el usuario, devolver los datos correspondientes
        user_data = {
            "id": id,
        }
        conn.commit() 
        return user_data
    else:
        # Si no se encontró el usuario, devolver un mensaje de error o el código de respuesta adecuado
        return {"error": "User not found"}



