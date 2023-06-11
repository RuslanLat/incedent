from fastapi import FastAPI
from typing import List, Dict
import psycopg2
from pathlib import Path
import pickle
from catboost import CatBoostClassifier
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


file_path = Path(__file__).parent / "catboost_pred.pkl"
with file_path.open("rb") as file:
    model = pickle.load(file)



@app.get("/")
def read_root():
    return {"incidents": "Сервис прогнозирования работ по содержанию и ремонту объектов городского хозяйства"}


@app.post("/items")
def read_item(data:List[Dict]): #data:List[Dict]
    
    return {"data" : data, "predict" : "Победа!"}
    

@app.post("/incidents")
def load_incidents():
    cursor.execute("""SELECT project_series, floor_value, entrance_value,
                    total_area, total_area_res, total_area_non_res,
                    wall_material, num_elevator, num_carco_elevator, status_mcd,
                    num_freight_elevastor, unom, calls_laste_month,
                    calls_aver_month, year
                    FROM incidents
                    INNER JOIN houses USING(unom);""")
    rows = cursor.fetchall()

    colnames = ['Серия проекта', 'Количество этажей', 'Количество подъездов',
        'Общая площадь', 'Общая площадь жилых помещений',
        'Общая площадь нежилых помещений', 'Материал стен',
        'Количество пассажирских лифтов', 'Количество грузопассажирских лифтов',
        'Статус МКД', 'Количество грузовых лифтов', 'Месяц создания во внешней системе',
        'Количество обращений за последний месяц',
        'Среднемесячное количество обращений', 'Возраст дома']
    

    # colnames = ["Количество обращений за последний месяц",
    #             "Среднее количество обращений за месяц", "Год постройки",
    #             'Серия проекта', 'Количество этажей',
    #             'Количество подъездов', 'Общая площадь',
    #             'Общая площадь жилых помещений', 'Общая площадь нежилых помещений',
    #             'Материал стен', 'Количество пассажирских лифтов',
    #             'Количество грузопассажирских лифтов', 'Статус МКД',
    #             'Количество грузовых лифтов']
    res = [dict(zip(colnames, row)) for row in rows]
    return res


@app.post("/addresses")
def load_addresses():
    cursor.execute("""SELECT unom, adm_area_name, district_area_name, addresse_title
                    FROM addresses
                    INNER JOIN adm_areas USING(id_adm_area)
                    INNER JOIN district_areas USING(id_district_area);""")
    rows = cursor.fetchall()
    colnames = ["Индефикатор адреса", "Административный округ", "Административный район", "Адрес"]
    res = [dict(zip(colnames, row)) for row in rows]
    return res

@app.post("/geo")
def load_geo():
    cursor.execute("""SELECT unom, latitude, longitude
                    FROM addresses;""")
    rows = cursor.fetchall()
    colnames = ["Индефикатор адреса", "latitude", "longitude"]
    res = [dict(zip(colnames, row)) for row in rows]

    return res

@app.post("/work_facts")
def load_work_fact():
    cursor.execute("""SELECT unom, adm_area_name, district_area_name,
                    addresse_title, work_name_example, period, plan_date_start, plan_date_end, latitude,
                    longitude
                    FROM work_facts
                    INNER JOIN work_types USING(id_work)
                    INNER JOIN addresses USING(unom)
                    INNER JOIN adm_areas USING(id_adm_area)
                    INNER JOIN district_areas USING(id_district_area)
                    LIMIT 200;""")
    rows = cursor.fetchall()
    

    colnames = ["Индефикатор адреса", "Административный округ", "Административный район",
                "Адрес", "Наименование работ", "Период", "Плановая дата начала работ",
                "Плановая дата завершения работ", "latitude", "longitude"]
    
    res = [dict(zip(colnames, row)) for row in rows]

    return res