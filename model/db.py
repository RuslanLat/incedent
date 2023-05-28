import pandas as pd
from pony.orm import *
from models import db

def get_data():
    df_train = pd.read_csv("model/df_train.csv")
    df = df_train.iloc[:,:-1]
    df.columns = ["Источник", "Адрес", "Год постройки", "Серия проекта",
        "Количество этажей", "Количество подъездов",
        "Общая площадь", "Общая площадь жилых помещений",
        "Общая площадь нежилых помещений", "Материал стен",
        "Количество пассажирских лифтов",
        "Количество грузопассажирских лифтов", "Статус МКД",
        "Количество грузовых лифтов"]
    data_train = df.values
    return data_train

@db_session
def add_train(source, address, year, project_series, floors,
            entrance, area, area_residential, area_non_residential,
            material, elevator, cargo, status, freight):

    """ функуия записи адресов в таблицу - 'trais' """
    
    db.Train(source=source, address=address, year=year,
            project_series=project_series, floors=floors,
            entrance=entrance, area=area, area_residential=area_residential,
            area_non_residential=area_non_residential,
            material=material, elevator=elevator, cargo=cargo,
            status=status, freight=freight)
    # commit() will be done automatically
    # database session cache will be cleared automatically
    # database connection will be returned to the pool



def insert_data(data_train):
    for source, address, year, project_series, floors, \
        entrance, area, area_residential, area_non_residential, \
        material, elevator, cargo, status, freight in data_train:
        add_train(source=source, address=address, year=year,
                project_series=project_series, floors=floors,
                entrance=entrance, area=area, area_residential=area_residential,
                area_non_residential=area_non_residential,
                material=material, elevator=elevator, cargo=cargo,
                status=status, freight=freight)
        
def main():
    data_train = get_data()
    insert_data(data_train)

if __name__ == "__main__":
    main()