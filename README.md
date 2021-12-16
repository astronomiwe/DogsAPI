# Проект API для сайта с обьявлениями по продаже щенков

### Стек технологий (полностью описан в [requirements.txt](requirements.txt))
* Python 3.8
* Django, DRF
* JWT
* Swagger
* Для локальной разработки используется СУБД MySQL
* Docker-compose

### Документацию проекта можно посмотреть после развертывания проекта на локальной машине: http://127.0.0.1:8000/swagger

Для того, чтобы запустить проект, потребуется:
1. Собрать и запустить докер-контейнер (по инструкции ниже)
2. Создать супер-пользователя для входа в админку (также можно найти ниже)

Все команды выполняются из корневой папки проекта.

## Запуск docker-контейнера для локальной разработки
0. Пункт-разъяснение только для бэкэнд-разработчиков:
Для создания файлов миграции необходима следующая последовательность команд:
> source ACTIVATE_vars_for_example.sh
> python manage.py makemigrations
> source DEACTIVATE.sh

1. Собрать контейнер
> docker-compose -f docker-compose.example.yml build

2. Запустить контейнер
> docker-compose -f docker-compose.example.yml up
* при первом запуске может возникнуть ошибка сервиса web - 
> web_1  | django.db.utils.OperationalError: (2002, "Can't connect to MySQL server on 'db' (115)")
> 
лечится следующим образом:
дожидаетесь, пока db_1 загрузится и в логе db_1 будет: 
> "/usr/sbin/mysqld: ready for connections."

нажимаете 1 раз ctrl+c, дожидаетесь остановки сервиса:
> Stopping %CONTAINERNAME% ... done 

> Stopping %CONTAINERNAME%  ... done 

Снова запускаете контейнер (п.2)

#### Остановка контейнера (можно повторно запустить):
> docker-compose -f docker-compose.example.yml stop

#### Остановка контейнера с удалением контейнера
> docker-compose -f docker-compose.example.yml down

#### Добавить суперпользователя (для захода в админку):
1. Смотрим список запущенных контейнеров командой:
> docker-compose ps
2. Находим контейнер с "web" в имени. Добавляем суперпользователя командой (%CONTAINERNAME% - имя контейнера из п.1):
> docker exec -it %CONTAINERNAME% python manage.py createsuperuser
