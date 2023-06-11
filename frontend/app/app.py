# Modules

import streamlit as st
from streamlit_option_menu import option_menu
import streamlit_authenticator as stauth
import pandas as pd
from st_aggrid import AgGrid, GridUpdateMode, JsCode
from st_aggrid.grid_options_builder import GridOptionsBuilder
import json
import pickle
import requests
import os
import csv
import numpy as np
from PIL import Image
from pathlib import Path
import folium
import branca
from streamlit_folium import st_folium
from catboost import CatBoostClassifier

st.set_page_config(page_title="Департамент жилищно-коммунального хозяйства города Москвы",
                    page_icon="app/images/logo.ico",
                    layout = "wide") #layout = "wide"

col1, col2 = st.columns([1,5])
col1.markdown("""<p><img src="https://www.mos.ru/upload/iblock/ace/ace3fe6203ace8dc07a6d2b7e1e592d2.png" width="80" height="90" align="middle" /> </p>""", unsafe_allow_html=True)    
#col2.markdown("""<h6>ДЕПАРТАМЕНТ ЖИЛИЩНО-КОММУНАЛЬНОГО ХОЗЯЙСТВА ГОРОДА МОСКВЫ</h6>""", unsafe_allow_html=True)
col2.markdown("<p style='text-align: center; font-size:20px; color: blac;'><STRONG>ДЕПАРТАМЕНТ ЖИЛИЩНО-КОММУНАЛЬНОГО ХОЗЯЙСТВА ГОРОДА МОСКВЫ</STRONG></p>", unsafe_allow_html=True)
col2.markdown("<p style='text-align: center; color: blac;'> Сервис прогнозирования работ<br>по содержанию и ремонту объектов городского хозяйства </p>", unsafe_allow_html=True)


# --- USER AUTHENTICATION ---
names = ["Admin Name", "User Name"]
usernames = ["admin", "user"]
# load hashed passwords
file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)

#загрузка модели и вывод предсказание
file_path = Path(__file__).parent / "catboost_pred.pkl"
with file_path.open("rb") as file:
    model = pickle.load(file)

file_path = Path(__file__).parent / "work_name_key.json"
with file_path.open("r") as f:
    templates = json.load(f)


credentials = {
        "usernames":{
            usernames[0]:{
                "name":names[0],
                "password": hashed_passwords[0]
                },
            usernames[1]:{
                "name":names[1],
                "password": hashed_passwords[1]
                }            
            }
        }


authenticator = stauth.Authenticate(credentials, "sales_dashboard", "abcdef", cookie_expiry_days=30)

name, authentication_status, username = authenticator.login("Вход в систему", "main")

if authentication_status == False:
    st.error("Имя пользователя/пароль являются не верными")

if authentication_status == None:
    st.warning("Введите имя пользователя и пароль")

if authentication_status:

    st.markdown(f'''
    <style>
        section[data-testid="stSidebar"] .css-ng1t4o {{width: 18rem;}}
        section[data-testid="stSidebar"] .css-1d391kg {{width: 18rem;}}
    </style>
''',unsafe_allow_html=True)

    # As sidebar menu CSS style definitions
    with st.sidebar:
        # ---- SIDEBAR ----
        st.sidebar.title(f"Добро пожаловать\n{name}!")
        authenticator.logout("Выйти", "sidebar")
        st.write("##")
        selected = option_menu(None, ["Задача", "Прогнозирование", "О приложении"], 
            icons=['house', "building-up", 'gear'], 
            menu_icon="cast", default_index=0,
            styles={
                "container": {"padding": "0!important", "background-color": "#fafafa"},
                "icon": {"color": "#a31b1b", "font-size": "20px", "--hover-color": "#ffffff"},
                "nav-link": {"color": "black", "font-size": "15px", "text-align": "left", "margin":"0px", "--hover-color": "#ff4040"},
                "nav-link-selected": {"color": "#ffffff",
                                    "background-color": "#ff0000"}
            }
        )


    # Functions

    @st.cache_data
    def load_incident_count(unom):

        file_path = Path(__file__).parent / "incidents_count.csv"
        with file_path.open() as f:
            rows = csv.reader(f)
            i = 0
        
            data = []
            colnames = None

            for row in rows:
                if i != 0:
                    data.append(row)
                else:
                    colnames = row
                    i = 1

            df = pd.DataFrame(data, columns=colnames)

            df = df[df["unom"].isin(unom)]
                
        return df

    
    @st.cache_data
    def data_upload_work_facts():

        res = requests.post(url = "http://api:8000/work_facts",)
        df = pd.DataFrame(res.json())

        return df
    
    @st.cache_data
    def data_upload_incidents():

        res = requests.post(url = "http://api:8000/incidents",)
        df = pd.DataFrame(res.json())

        return df
    
    @st.cache_data
    def data_upload_addresses():

        res = requests.post(url = "http://api:8000/addresses",)
        df = pd.DataFrame(res.json())

        return df
    
    @st.cache_data
    def data_upload_geo():

        res = requests.post(url = "http://api:8000/geo",)
        df = pd.DataFrame(res.json())

        return df
    
    @st.cache_data
    def creat_predict_proba(pred_proba, df_new, templates):
        df_pred_proba = pd.DataFrame(data=pred_proba)
        pred_list = []
        for j in range(len(df_pred_proba)):
            for i in df_pred_proba.columns:
                data = {"umon" : df_new['Месяц создания во внешней системе'][j],
                        "Вероятность" : df_pred_proba[i][j].round(3),
                        "Наименование работ" : templates[str(i)]}
                pred_list.append(data)

        return pred_list

    @st.cache_data
    def popup_html(row):

        i = row

        unom=df_group['Индефикатор адреса'].iloc[i]
        adm_area_name=df_group['Административный округ'].iloc[i]
        district_area_name = df_group['Административный район'].iloc[i]
        addresse_title = df_group['Адрес'].iloc[i]
        incidents = df_group["Период"].iloc[i]

    
        left_col_color = "#ff4040"
        right_col_color = "#FFFAFA"


        html = """<!DOCTYPE html><html>
        <head>
        <h4 style="margin-bottom:10"; width="200px">{}</h4>""".format(unom) + """
        
        </head>
            <table style="height: 126px; width: 400px;">
        <tbody>
        <tr>
        <td style="background-color: """+ left_col_color +"""; text-align:center; border: 2px solid white;">Административный округ</td>
        <td style="width: 220px;background-color: """+ left_col_color +"""; text-align:center; border: 2px solid white;">{}</td>""".format(adm_area_name) + """
        </tr>
        <tr>
        <td style="background-color: """+ right_col_color +"""; text-align:center; border: 2px solid white;">Административный район</td>
        <td style="width: 220px;background-color: """+ right_col_color +"""; text-align:center; border: 2px solid white;">{}</td>""".format(district_area_name) + """
        </tr>
        <tr>
        <td style="background-color: """+ left_col_color +"""; text-align:center; border: 2px solid white;">Адрес</td>
        <td style="width: 220px;background-color: """+ left_col_color +"""; text-align:center; border: 2px solid white;">{}</td>""".format(addresse_title) + """
        </tr>
        <tr>
        <td style="background-color: """+ right_col_color +"""; text-align:center; border: 2px solid white;">Количество обращений</td>
        <td style="width: 220px;background-color: """+ right_col_color +"""; text-align:center; border: 2px solid white;">{}</td>""".format(incidents) + """
        </tr>
        </tbody>
        </table>
        </html> """
        
        return html




    if selected == "Задача":
        st.subheader(""" Задача 10: "Сервис прогнозирования работ по содержанию и ремонту объектов городского хозяйства" """)
        st.markdown("""**АКТУАЛЬНОСТЬ**

В управление «Объединенная диспетчерская служба Департамента жилищно-коммунального хозяйства города Москвы» и на портал «Наш город» ежегодно поступает более 7.5 млн обращений граждан по вопросам ЖКХ.

В целях снижения трудозатрат на их анализ необходимо создать автоматизированный сервис с использованием алгоритмов машинного обучения для формирования предложений по планированию работ по ремонту и содержанию объектов Комплекса городского хозяйства города Москвы

**ОПИСАНИЕ ЗАДАЧИ**

Разработайте сервис прогнозирования работ по содержанию и ремонту объектов городского хозяйства на основании анализа событий с применением технологии машинного обучения и возможностью корректировки итогового результата пользователем.""")

    if selected == "Прогнозирование":
        #with open("./css/AG_GRID_LOCALE_RU.txt", 'w') as f:
        #    json.dump(AG_CRID_LOCALE_RU, f)
        with open("app/css/AG_GRID_LOCALE_RU.txt", 'r') as f:
            AG_CRID_LOCALE_RU = json.load(f)

        oprions = st.selectbox("Выбирите способ загрузки файла", 
                            ("База данных", "Пользовательский ввод", "Локальная загрузка", "Передать по API"))
        
        # Data
        if oprions == "База данных":
            
            df = data_upload_work_facts()

            st.subheader("Предлагаемый план работ")

            js = JsCode("""
            function(e) {
                let api = e.api;     
                let sel = api.getSelectedRows();
                api.applyTransaction({remove: sel});
            };
            """)

            gd = GridOptionsBuilder.from_dataframe(df)
            gd.configure_pagination(enabled=True,
                                    paginationAutoPageSize=False,
                                    paginationPageSize=10)
            gd.configure_grid_options(stopEditingWhenCellsLoseFocus=True) #, rowHeight=80
            gd.configure_grid_options(localeText=AG_CRID_LOCALE_RU)
            gd.configure_default_column(editable=True, groupable=True)
            gd.configure_selection(selection_mode="multiple", use_checkbox=True)
            gd.configure_grid_options(onRowSelected = js, pre_selected_rows = [])
            gridoptions = gd.build()
            grid_table = AgGrid(df, gridOptions=gridoptions,
                                update_mode=GridUpdateMode.SELECTION_CHANGED,
                                allow_unsafe_jscode=True,
                                theme="alpine")

            
            df_group = df.groupby(["Индефикатор адреса", "Административный округ",
                                    "Административный район", "Адрес", "latitude", "longitude"], as_index=False)["Период"].count()


            location = df_group['latitude'].mean(), df_group['longitude'].mean()
            #Specify the center of the map by using the average of latitude and longitude coordinates
            m = folium.Map(location=location,zoom_start=12)
            #Create a empty folium map object #Color code the markers to show blue markers for public universities and brown colors for private universities
            for i in range(0,len(df_group)):
                institution_type = df_group["Период"].iloc[i]
                if institution_type < df_group["Период"].quantile(0.35):
                    color = 'green'
                elif institution_type < df_group["Период"].quantile(0.75):
                    color = 'darkblue'
                else: color = 'red'
                html = popup_html(i)
                iframe = branca.element.IFrame(html=html,width=510,height=280)
                popup = folium.Popup(folium.Html(html, script=True), max_width=500)
                folium.Marker([df_group['latitude'].iloc[i],df_group['longitude'].iloc[i]],
                popup=popup, icon=folium.Icon(color=color, icon='home')).add_to(m)

                
            st.subheader("Визуализация результатов")
            st_data = st_folium(m, width=1620)
            
        if oprions == "Пользовательский ввод":

            df = data_upload_incidents()

            with st.form("Выбирете параметры"):
                year = st.multiselect('Возраст дома', options=df['Возраст дома'].unique(),
                                        default=df['Возраст дома'].unique()[:4])
                project_series = st.multiselect('Серия проекта',
                                                options=df['Серия проекта'].unique(),
                                                default=df['Серия проекта'].unique()[:5])
                wall_material = st.multiselect('Материал стен',
                                                options=df['Материал стен'].unique(),
                                                default=df['Материал стен'].unique()[:2])
                submitted = st.form_submit_button("Спланировать работы")

            if submitted:
                
                index_list = np.where((df['Возраст дома'].isin(year)) & 
                                        (df['Серия проекта'].isin(project_series)) &
                                        (df['Материал стен'].isin(wall_material)))
                
                df_new = df.iloc[index_list]

                df_new = df_new.reset_index(drop=True)
                pred_proba = model.predict_proba(df_new)
                pred_df = creat_predict_proba(pred_proba, df_new, templates)
                pred_plot =pd.DataFrame(pred_df)
                pred_plot = pred_plot.sort_values(by="Вероятность", ascending=False)[:10]

                pred_plot["umon"] = pred_plot["umon"].astype("str")
                
                unom = pred_plot["umon"].unique()    
                
                df_whie = load_incident_count(unom)


                col1, col2 = st.columns(2)

                with col1:
                    st.subheader("ТОП-10 работ в плане")
                    st.write(pred_plot)

                with col2:
                    st.subheader("Почему модель так считает")
                    st.write(df_whie)

                

        if oprions == "Локальная загрузка":
            uploaded_file = st.file_uploader("Загрузите файл", type=["csv", "xlsx"])

            if uploaded_file:
                if uploaded_file.name.split(".")[-1] == "csv":
                    df = pd.read_csv(uploaded_file)
                    st.write(df)
                else:
                    df = pd.read_excel(uploaded_file)
                    st.write(df)

        if oprions == "Передать по API":

            st.subheader("POST метод API")

            st.code("data = [\n{\n'unom' : 2023,\n'incident_name' : 'Финал ЛЦТ',\n'date' : '11.06.2023'\n}\n]\n\nrequests.post(url = 'http://api:8000/items/', data=json.dump(data)",
                    line_numbers=True)
                    
            data = st.text_area("Введите данные", value="""[{"unom" : 2023, "incident_name" : "Финал ЛЦТ", "date" : "11.06.2023"}]""")
            
            if type(eval(data)) == list:
                res = requests.post(url = "http://api:8000/items", data=json.dumps(eval(data))) # 
                st.subheader("Результат запроса")
                st.write(res.json())
            else:
                st.error("Не верный формат данных")

    if selected == "О приложении":

        image_1 = Image.open("app/images/1.png")
        image_2 = Image.open("app/images/2.png")
        image_3 = Image.open("app/images/3.png")
        image_4 = Image.open("app/images/4.png")
        image_5 = Image.open("app/images/5.png")
        image_6 = Image.open("app/images/6.png")

        st.subheader('Элемент авторизации')
        st.image(image_1, caption='Элемент авторизации')
        st.subheader('Сохранение предсказания в файл')
        st.image(image_2, caption='Сохранение предсказания в файл')
        st.subheader('Фильтрация данных')
        st.image(image_3, caption='Фильтрация данных')
        st.subheader('Отбор признаков в выводе данных')
        st.image(image_4, caption='Отбор признаков в выводе данных')
        st.subheader('Группировка данных')
        st.image(image_5, caption='Группировка данных')
        st.subheader('Изменения порядка вывода признаков')
        st.image(image_6, caption='Изменения порядка вывода признаков')

st.write("##")
st.markdown("<h5 style='text-align: center; color: blac;'> ©️ Команда Extreme DS </h5>", unsafe_allow_html=True)
st.markdown("<h5 style='text-align: center; color: blac;'> Лидеры цифровой трансформации 2023 </h5>", unsafe_allow_html=True)