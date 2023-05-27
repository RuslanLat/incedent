# incident

[**Лидеры цифровой трансформации**](https://leaders2023.innoagency.ru/task_10)

Задача №10 "Сервис прогнозирования работ по содержанию и ремонту объектов городского хозяйства"

1. [Презентация](https://github.com/RuslanLat/incident/blob/main/presentation.pdf)
2. [WEB-приложение](https://incident.streamlit.app/)

![web](https://github.com/RuslanLat/green/blob/main/images/web.png)


Для локального использования WEB-приложения:
1. Загрузить все файлы репозитория **incident** \
    или выполнить команду в терминале bash ***"git clone https://github.com/RuslanLat/incident"***
2. Порядок запуска сервиса:

docker-compose up -d --build

docker-compose stop


2.1. **Frontend**  - веб-приложение с доступом к сервису прогозирования работ, с визуализацией даных в виде конструктора перечня.
* вызвать командную строку или в окне поиска ввести ***cmd***
* с помощью командной строки перейти в директорию ***cd incident\frontend***
* в командной строке выполнить команду ***docker build -t streamlit .*** (сборка образа контейнера)
* в командной строке выполнить команду ***docker run -p 5981:5981 streamlit*** (запуск контейнера в фоновом решиме)
* компонент сервиса будет доступен на локальном порту **5981**
* остановка работы базы ***docker stop <имя контейнера или id>***
* повторный запуск базы данных ***docker start <имя контейнера или id>***

2.2. **Backend** - компоненты сервиса сбора, анализа, исходных данных по событиям и объектам, на которых они происходят, рекомендация перечня работ
* вызвать командную строку или в окне поиска ввести ***cmd***
* с помощью командной строки перейти в директорию ***cd incident\backend***
* в командной строке выполнить команду ***docker build -t backend .*** (сборка образа контейнера)
* в командной строке выполнить команду ***docker run -d --name backend_app -p 8000:8000 backend*** (запуск контейнера в фоновом решиме)
* компонент сервиса будет доступен на локальном порту
***Пример:*** http://192.168.99.100/docs или http://127.0.0.1/docs
* остановка работы базы ****docker stop <имя контейнера или id>***
* повторный запуск базы данных ***docker start <имя контейнера или id>***

2.3. **Storage** - компоненты сервиса, обеспечивающие хранение и доступ к данным:
* вызвать командную строку или в окне поиска ввести ***cmd***
* с помощью командной строки перейти в директорию ***cd incident\storage***
* в командной строке выполнить команду ***docker-compose build*** (сборка образа контейнера)
* в командной строке выполнить команду ***docker-compose up -d*** (запуск контейнера в фоновом решиме)
* база данных Postgres SQL будет доступна на локальном порту 5432
* параметры доступа к базе данных указаны в docker-compoce.yml
* остановка работы базы ***docker stop <имя контейнера или id>*** или ***docker-compose stop <имя контейнера или id>***
* повторный запуск базы данных ***docker start <имя контейнера или id>*** \
***Примечание:*** в директории ***incident\storage*** создается папка ***pgdata*** с данными базы данных

Команда **"Extreme DS"** \
Руслан Латипов (капитан) <img src="https://github.com/RuslanLat/green/blob/main/images/telegram_icon.png" width="15"> @rus_lat116 \
Алексей Верт-Миллер <img src="https://github.com/RuslanLat/green/blob/main/images/telegram_icon.png" width="15"> @alexwert3 \
Юрий Дон <img src="https://github.com/RuslanLat/green/blob/main/images/telegram_icon.png" width="15"> @Yuriy_Nikitich \
Виталий Ерохин <img src="https://github.com/RuslanLat/green/blob/main/images/telegram_icon.png" width="15"> @warleagle \
Кирилл Ерохин <img src="https://github.com/RuslanLat/green/blob/main/images/telegram_icon.png" width="15"> @Kasdeja23