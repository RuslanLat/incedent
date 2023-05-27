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
from pathlib import Path

st.set_page_config(page_title="Департамент жилищно-коммунального хозяйства города Москвы",
                    page_icon="../images/logo.ico") #layout = "wide"

col1, col2 = st.columns([1,5])
col1.markdown("""<p><img src="https://www.mos.ru/upload/iblock/ace/ace3fe6203ace8dc07a6d2b7e1e592d2.png" width="80" height="90" align="middle" /> </p>""", unsafe_allow_html=True)    
col2.markdown("""<h6>ДЕПАРТАМЕНТ ЖИЛИЩНО-КОММУНАЛЬНОГО ХОЗЯЙСТВА ГОРОДА МОСКВЫ</h6>""", unsafe_allow_html=True)
col2.markdown("<p style='text-align: center; color: blac;'> Сервис прогнозирования работ<br>по содержанию и ремонту объектов городского хозяйства </p>", unsafe_allow_html=True)


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
        selected = option_menu(None, ["Задача", "Аналитика",  "Прогнозирование", "О приложении"], 
            icons=['house', 'graph-up-arrow', "building-up", 'gear'], 
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

    oprions = st.selectbox("Выбирите способ загрузки файла", 
                          ("База данных", "API", "Загрузка файла"))

    @st.cache_data
    def data_upload():
        #df = pd.read_csv('./../data/cars_moldova.csv')
        df = pd.DataFrame([[1, 2, 3, 6], [4, 5, 6, 7]], columns=["datd", "data", "ffff", "dsfds"])
        return df

    if selected == "Задача":
        st.write("Сервис прогнозирования работ по содержанию и ремонту объектов городского хозяйства")


    if selected == "Аналитика":

        st.write("Здесь будет какой нибудь дашборд")

        if oprions == "Загрузка файла":
            
            uploaded_file = st.file_uploader("Окно загрузки файла", type=None,
                            help="Загрузите файл или переташите файл в окно загрузки")
            if uploaded_file is not None:
                filename, file_extension = os.path.splitext(uploaded_file.name)

                if (file_extension in [".xlsx", ".csv"]) is True:
                    st.success("Файл загружен")
                    if file_extension == ".csv":
                        df = pd.read_csv(uploaded_file)
                    else:
                        df = pd.read_excel(uploaded_file)
                    st.write(df.head())
                else:
                    st.error('Не верное расширение файла')
            else:
                st.warning("Загрузите файл или переташите файл в окно загрузки")
        if oprions == "API":
            if st.button("API"):
                res = requests.post(url = "http://api:8000/events",)
                df = pd.DataFrame(res.json())
                st.write(df)

    #with open("./css/AG_GRID_LOCALE_RU.txt", 'w') as f:
    #    json.dump(AG_CRID_LOCALE_RU, f)
    with open("app/css/AG_GRID_LOCALE_RU.txt", 'r') as f:
        AG_CRID_LOCALE_RU = json.load(f)

    if selected == "Прогнозирование":

        # Data

        df = data_upload()

        st.header("This is AgGrid Table")

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
        gd.configure_column("Фильтр даты", floatingFilter= True, filter = "agDateColumnFilter") 
        gridoptions = gd.build()
        grid_table = AgGrid(df, gridOptions=gridoptions,
                            update_mode=GridUpdateMode.SELECTION_CHANGED,
                            allow_unsafe_jscode=True,
                            theme="alpine")
        
    if selected == "О приложении":

        st.write("Лидеры цифровой трансформации")

st.write("##")
st.markdown("<h5 style='text-align: center; color: blac;'> ©️ Команда Extreme DS </h5>", unsafe_allow_html=True)
st.markdown("<h5 style='text-align: center; color: blac;'> Лидеры цифровой трансформации 2023 </h5>", unsafe_allow_html=True)