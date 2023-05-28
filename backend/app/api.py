from fastapi import FastAPI
import psycopg2
import pandas as pd
import os
from dotenv import load_dotenv
load_dotenv()


DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

app = FastAPI()


connect = psycopg2.connect(database=DB_NAME,
                            user=DB_USER,
                            password=DB_PASSWORD,
                            host=DB_HOST,
                            port=DB_PORT)
cursor = connect.cursor()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id):
    if item_id != "data":
        return item_id
    else:
        data = {"item_id": 
                    {"id" : 2,
                    "source" : "ASUPR",
                    "address" : "Дом по адресу Сиреневый бульв., д.73, к.1",
                    "year" : 2022,
                    "project_series" : "П-29",
                    "floors" : 9,
                    "entrance" : 4,
                    "area" : 6718,
                    "area_residential" : 5639,
                    "area_non_residential" : 1079,
                    "material" : "кирпичные",
                    "elevator" : 4,
                    "cargo" : 0,
                    "status" : "в эксплуатации",
                    "freight" : 0}
                }
        return data       

@app.post("/train")
def load_train():
    cursor.execute("""SELECT * FROM train;""")
    train_data = cursor.fetchall()
    colnames = ["id", "Источник", "Адрес", "Год постройки", "Серия проекта",
    "Количество этажей", "Количество подъездов",
    "Общая площадь", "Общая площадь жилых помещений",
    "Общая площадь нежилых помещений", "Материал стен",
    "Количество пассажирских лифтов",
    "Количество грузопассажирских лифтов", "Статус МКД",
    "Количество грузовых лифтов"] 
    df = pd.DataFrame(train_data, columns=colnames)
    df = df.iloc[:,1:] #, columns=colnames
    return df.to_dict()