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
import numpy as np
from pathlib import Path
from PIL import Image
import folium
import branca
from streamlit_folium import st_folium

st.set_page_config(page_title="Департамент жилищно-коммунального хозяйства города Москвы",
                    page_icon="images/logo.ico",
                    layout = "wide") #layout = "wide"

col1, col2 = st.columns([1,5])
col1.markdown("""<p><img src="https://www.mos.ru/upload/iblock/ace/ace3fe6203ace8dc07a6d2b7e1e592d2.png" width="80" height="90" align="middle" /> </p>""", unsafe_allow_html=True)    
col2.markdown("<p style='text-align: center; font-size:20px; color: blac;'><STRONG>ДЕПАРТАМЕНТ ЖИЛИЩНО-КОММУНАЛЬНОГО ХОЗЯЙСТВА ГОРОДА МОСКВЫ</STRONG></p>", unsafe_allow_html=True)
col2.markdown("<p style='text-align: center; color: blac;'> Сервис прогнозирования работ<br>по содержанию и ремонту объектов городского хозяйства </p>", unsafe_allow_html=True)


@st.cache_data
def data_upload():
    df = pd.read_csv("data/addresses.csv")
    return df[:100]

df = data_upload()


def popup_html(row):

    i = row

    SIMPLE_ADDRESS=df['SIMPLE_ADDRESS'].iloc[i]
    ADM_AREA=df['ADM_AREA'].iloc[i]
    DISTRICT = df['DISTRICT'].iloc[i]
    unom=df['unom'].iloc[i]
    
    left_col_color = "#ff4040"
    right_col_color = "#FFFAFA"


    html = """<!DOCTYPE html><html>
    <head>
    <h4 style="margin-bottom:10"; width="200px">{}</h4>""".format(SIMPLE_ADDRESS) + """
    
    </head>
        <table style="height: 126px; width: 350px;">
    <tbody>
    <tr>
    <td style="background-color: """+ left_col_color +"""; text-align:center; border: 1px solid white;">Административный округ</td>
    <td style="width: 150px;background-color: """+ left_col_color +"""; text-align:center; border: 1px solid white;">{}</td>""".format(ADM_AREA) + """
    </tr>
    <tr>
    <td style="background-color: """+ right_col_color +"""; text-align:center; border: 1px solid white;">Административный район</td>
    <td style="width: 150px;background-color: """+ right_col_color +"""; text-align:center; border: 1px solid white;">{}</td>""".format(DISTRICT) + """
    </tr>
    <tr>
    <td style="background-color: """+ left_col_color +"""; text-align:center; border: 1px solid white;">id адреса</td>
    <td style="width: 150px;background-color: """+ left_col_color +"""; text-align:center; border: 1px solid white;">{}</td>""".format(unom) + """
    </tr>
    </tbody>
    </table>
    </html> """
    
    return html


location = df['LATITUDE'].mean(), df['LONGITUDE'].mean()
#Specify the center of the map by using the average of latitude and longitude coordinates
m = folium.Map(location=location,zoom_start=10)
#Create a empty folium map object #Color code the markers to show blue markers for public universities and brown colors for private universities
for i in range(0,len(df)):
    institution_type = df['CONTROL'].iloc[i]
    if institution_type == 0:
        color = 'darkblue'
    elif institution_type == 1:
        color = 'lightbrown'
    else: color = 'gray'
    html = popup_html(i)
    iframe = branca.element.IFrame(html=html,width=510,height=280)
    popup = folium.Popup(folium.Html(html, script=True), max_width=500)
    folium.Marker([df['LATITUDE'].iloc[i],df['LONGITUDE'].iloc[i]],
    popup=popup, icon=folium.Icon(color=color, icon='home')).add_to(m)

# --- USER AUTHENTICATION ---
names = ["Admin Name", "User Name"]
usernames = ["admin", "user"]
# load hashed passwords
file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)

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

    # As sidebar menu CSS style definitions
    with st.sidebar:
        # ---- SIDEBAR ----
        st.sidebar.title(f"Добро пожаловать\n{name}!")
        authenticator.logout("Выйти", "sidebar")
        st.write("##")
        selected = option_menu(None, ["Задача", "Прогнозирование", "О приложении"], 
            icons=['house', "building-up", 'gear'], 
            menu_icon="cast", default_index=1,
            styles={
                "container": {"padding": "0!important", "background-color": "#fafafa"},
                "icon": {"color": "#a31b1b", "font-size": "30px", "--hover-color": "#ffffff"},
                "nav-link": {"color": "black", "font-size": "20px", "text-align": "left", "margin":"0px", "--hover-color": "#ff4040"},
                "nav-link-selected": {"color": "#ffffff",
                                    "background-color": "#ff0000"}
            }
        )


    # Functions

    

    if selected == "Задача":
        st.subheader(""" Задча 10: "Сервис прогнозирования работ по содержанию и ремонту объектов городского хозяйства" """)
        st.markdown("""**АКТУАЛЬНОСТЬ**

В управление «Объединенная диспетчерская служба Департамента жилищно-коммунального хозяйства города Москвы» и на портал «Наш город» ежегодно поступает более 7.5 млн обращений граждан по вопросам ЖКХ.

В целях снижения трудозатрат на их анализ необходимо создать автоматизированный сервис с использованием алгоритмов машинного обучения для формирования предложений по планированию работ по ремонту и содержанию объектов Комплекса городского хозяйства города Москвы

**ОПИСАНИЕ ЗАДАЧИ**

Разработайте сервис прогнозирования работ по содержанию и ремонту объектов городского хозяйства на основании анализа событий с применением технологии машинного обучения и возможностью корректировки итогового результата пользователем.""")

    if selected == "Прогнозирование":
        #with open("./css/AG_GRID_LOCALE_RU.txt", 'w') as f:
        #    json.dump(AG_CRID_LOCALE_RU, f)
        with open("css/AG_GRID_LOCALE_RU.txt", 'r') as f:
            AG_CRID_LOCALE_RU = json.load(f)

        oprions = st.selectbox("Выбирите способ загрузки файла", 
                          ("База данных", "Пользовательский ввод"))
        
        # Data
        if oprions == "База данных":
            
            

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
            gd.configure_grid_options(stopEditingWhenCellsLoseFocus=True, rowHeight=80)
            gd.configure_grid_options(localeText=AG_CRID_LOCALE_RU)
            gd.configure_default_column(editable=True, groupable=True)
            gd.configure_selection(selection_mode="multiple", use_checkbox=True)
            gd.configure_grid_options(onRowSelected = js, pre_selected_rows = [])
            gridoptions = gd.build()
            grid_table = AgGrid(df, gridOptions=gridoptions,
                                update_mode=GridUpdateMode.SELECTION_CHANGED,
                                allow_unsafe_jscode=True,
                                theme="alpine")
                       
            st.subheader("Предлагаемый план работ")
            st_data = st_folium(m, width=1600)
            
        if oprions == "Пользовательский ввод":

            st.subheader("Выбирете параметры")
            source_list = st.selectbox(
            'Выбирете источник', df.iloc[:,0].unique())
            year_list = st.selectbox(
            'Выбирете год постройки', df.iloc[:,2].unique())
            project_list = st.selectbox(
            'Выбирете серию проекта', df.iloc[:,3].unique())
            
            index_list = np.where((df.iloc[:,0] == source_list) &
                    (df.iloc[:,2] == year_list) &
                    (df.iloc[:,3] == project_list))
            
            df_new = df.iloc[index_list]
            st.subheader("Предлагаемый план работ")

            js = JsCode("""
            function(e) {
                let api = e.api;     
                let sel = api.getSelectedRows();
                api.applyTransaction({remove: sel});
            };
            """)

            gd = GridOptionsBuilder.from_dataframe(df_new)
            gd.configure_pagination(enabled=True,
                                    paginationAutoPageSize=False,
                                    paginationPageSize=10)
            gd.configure_grid_options(stopEditingWhenCellsLoseFocus=True, rowHeight=80)
            gd.configure_grid_options(localeText=AG_CRID_LOCALE_RU)
            gd.configure_default_column(editable=True, groupable=True)
            gd.configure_selection(selection_mode="multiple", use_checkbox=True)
            gd.configure_grid_options(onRowSelected = js, pre_selected_rows = [])
            gridoptions = gd.build()
            grid_table = AgGrid(df_new, gridOptions=gridoptions,
                                update_mode=GridUpdateMode.SELECTION_CHANGED,
                                allow_unsafe_jscode=True,
                                theme="alpine")
            
    if selected == "О приложении":

        image_1 = Image.open("images/1.png")
        image_2 = Image.open("images/2.png")
        image_3 = Image.open("images/3.png")
        image_4 = Image.open("images/4.png")
        image_5 = Image.open("images/5.png")
        image_6 = Image.open("images/6.png")

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