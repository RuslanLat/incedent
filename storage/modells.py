from datetime import date
from datetime import datetime
from pony.orm import *
import os
from dotenv import load_dotenv
load_dotenv()


DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

db = Database()


db.bind(provider="postgres",
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        database=DB_NAME)

class Train(db.Entity):
    id = PrimaryKey(int, column='id', auto=True)  # id идентификатор события
    source = Required(str, column='source')  # источник
    address = Required(str, column='address')  # адрес
    year = Required(int, column='year')  # год постройки 
    project_series = Required(str, column='project_series')  # серия проекта  
    floors = Required(int, column='floors')  # количество этажей
    entrance = Required(int, column='entrance')  # количество подъездов
    area = Required(int, column='area')  # oбщая площадь 
    area_residential = Required(int, column='area_residential')  # общая площадь жилых помещений 
    area_non_residential = Required(int, column='area_non_residential')  # общая площадь нежилых помещений
    material = Required(str, column='material')  # материал стен
    elevator = Required(int, column='elevator')  # количество пассажирских лифтов
    cargo = Required(int, column='cargo')  # количество грузопассажирских лифтов
    status = Required(str, column='status')  # статус МКД 
    freight = Required(int)  # количество грузовых лифтов 
    work = Required(int, column='work')  # класс перечня работ


db.generate_mapping(create_tables=True)