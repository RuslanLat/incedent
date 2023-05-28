# incident

[**Лидеры цифровой трансформации**](https://leaders2023.innoagency.ru/task_10)

Задача №10 "Сервис прогнозирования работ по содержанию и ремонту объектов городского хозяйства"

1. [Презентация](https://github.com/RuslanLat/incedent/blob/main/presentation.pdf)
2. [WEB-приложение](https://incedent.streamlit.app/)

![web](https://github.com/RuslanLat/incedent/blob/main/images/web.png)


Для локального использования WEB-приложения:
1. Загрузить все файлы репозитория **incident** \
    или выполнить команду в терминале bash ***"git clone https://github.com/RuslanLat/incident"***
2. Порядок запуска сервиса:

* в директории с проектом в терминале выполнить команду ***docker-compose up -d --build*** (сборка контейнеров и запуск их в работе в фоновом режиме)
* сервис будет доступен на локальном порту **5981**
* для остановки работы сервера в директории с проектом в терминале выполнить команду ***docker-compose stop***
* для повторного запуска в дирктории с проектом в терминале выполнить команду ***docker-compose start*** 

***Примечание:*** в директории с проектом (incident) создается папка ***pgdata*** с данными базы данных

Команда **"Extreme DS"** \
Руслан Латипов (капитан) <img src="https://github.com/RuslanLat/green/blob/main/images/telegram_icon.png" width="15"> @rus_lat116 \
Алексей Верт-Миллер <img src="https://github.com/RuslanLat/green/blob/main/images/telegram_icon.png" width="15"> @alexwert3 \
Юрий Дон <img src="https://github.com/RuslanLat/green/blob/main/images/telegram_icon.png" width="15"> @Yuriy_Nikitich \
Виталий Ерохин <img src="https://github.com/RuslanLat/green/blob/main/images/telegram_icon.png" width="15"> @warleagle \
Кирилл Ерохин <img src="https://github.com/RuslanLat/green/blob/main/images/telegram_icon.png" width="15"> @Kasdeja23