from datetime import date, datetime
from typing import Annotated, List
import bcrypt
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import Model.model
from Setting_db.setting import settings_db
from Model.model import Table_user
from Responce_model.model_response import User_model, User_create, User_sort_date
import logging
import Model
from sqlalchemy import func

logging.basicConfig(level=logging.INFO)

app = FastAPI()


class UserCreate(BaseModel): # Модель создания пользователя 
    username: str
    email: str
    password: str



class Info_user:

    @app.post("/create_user/", response_model=User_create) # Модель ответа в формате json()
    async def create_user(
        user: UserCreate
        ): 

        with settings_db.Create_session() as db: # Cоздание сесси к базе 

            hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())

            # Поля должны соответствовать таблице Table_user

            # Создание объекта 
            user_create = Table_user(
                #cопостовление полей с Table_user
                username = user.username, 
                email = user.email,
                password_hash = hashed_password.decode('utf-8')
                
            )

            # проверка на то существует ли объект 
            if not user_create:

                raise HTTPException(status_code=404, detail="Пользователь не создан")
            
                
            db.add(user_create) # Добовления пользователя в базу
            db.commit() # сохранение 
            db.refresh(user_create) # перезапись

            user_create = {
                
                # Сопостовление полей с response_model

                "username" : user.username,
                "email" : user.email
            }

            return user_create # Создание пользователя , возвращение в json формате 

                        

    @app.get("/get_users/", response_model=list[User_model]) # Автоматическое преобразование в список объектов
    async def get_users():

        with settings_db.Create_session() as db:

            get_users = db.query(Table_user).order_by().all() # получение всех пользователей
      
            all_user = [] # Создание пустого листа

            for user in get_users:

                all_user.append({ # расширение списка 

                    "id" : user.id,
                    "username" : user.username,
                    "email" : user.email,
                    "created_at" : user.created_at
                   
                })

                
        return all_user   # возвращение всех пользователей




    @app.delete("/delete_by_id/{id}")
    async def delete_user_by_id(id: int):

        with settings_db.Create_session() as db: # Cоздание сесси к базе данных

            delete_user = db.query(Table_user).filter(Table_user.id == id).first() # Фильтрация в БД по ID пользователей

            if not delete_user: # проверка на ID 

                raise HTTPException(status_code=404, detail="ID пользователя не найдено") # вывод ошибки если ID не найден 

            

            db.delete(delete_user) # Удаление пользователя если id надено 
            db.commit() # сохранение бд
            

            return {"detail": f"Пользователь с ID : {id} \n username : {delete_user.username} \n был удален"} # Возвращение ID и имя пользователя который был удалён



    @app.get("/search_user/{id}", response_model=User_model)
    async def search_user_by_id(id: int):

        with settings_db.Create_session() as db:

            user_by_id = db.query(Table_user).filter(Table_user.id == id).first()

            if not user_by_id:

                raise HTTPException(status_code=404, detail="Пользователь с таким ID не найден")


            return ({ 
                "id" : user_by_id.id,
                "username" : user_by_id.username,
                "email" : user_by_id.email,
                "created_at" : user_by_id.created_at
            })

            
            


    @app.get("/sort_user_date/")
    async def sort_user_date(user_sort_by: date):

        with settings_db.Create_session() as db:
            

            # Первая реализация , с диапозонами по дате 
            """
            
            start_of_day = datetime.combine(user_sort_by, datetime.min.time())

            end_of_day = datetime.combine(user_sort_by, datetime.max.time())

            sort_user = db.query(Table_user).filter(Table_user.created_at >= start_of_day, Table_user.created_at <= end_of_day).all()

            """

            # Вторая по проще , используем func.date которое игнорирует время и сравнивает только дату

            sort_user = db.query(Table_user).filter(func.date(Table_user.created_at) == user_sort_by).all()


            return sort_user


 

                

          

            

            