# Проект API для сайта с обьявлениями по продаже щенков

### Стек технологий (полностью описан в [requirements.txt](requirements.txt))
* Python 3.8
* Django, DRF
* JWT
* Swagger
* Для локальной разработки используется СУБД MySQL

### Документацию проекта можно посмотреть после развертывания проекта на локальной машине: http://127.0.0.1/swagger

# Варианты запуска проекта:
1. Запуск для локальной разработки
2. Запуск на сервере для разработки
3. Запуск на прод сервере

## В любом из этих вариантов, для того, чтобы запустить проект, потребуется:
1. Собрать и запустить докер-контейнер (по инструкции ниже)
2. Создать супер-пользователя для входа в админку (также можно найти ниже)

Все команды выполняются из папки /backend_v2


## 1. Запуск docker-контейнера для локальной разработки
0. Пункт-разъяснение только для бэкэнд-разработчиков:
Для создания файлов миграции необходима следующая последовательность команд:
> source ACTIVATE_vars_for_dev.sh
> python manage.py makemigrations
> source DEACTIVATE.sh

1. Собрать контейнер
> docker-compose -f docker-compose.localdev.yml build

2. Запустить контейнер
> docker-compose -f docker-compose.localdev.yml up
* при первом запуске может возникнуть ошибка сервиса web - 
> web_1  | django.db.utils.OperationalError: (2002, "Can't connect to MySQL server on 'db' (115)")
> 
лечится следующим образом:
дожидаетесь, пока db_1 загрузится и в логе db_1 будет: 
> "/usr/sbin/mysqld: ready for connections."

нажимаете 1 раз ctrl+c, дожидаетесь остановки сервиса:
> Stopping backend_v2_web_1 ... done 

> Stopping backend_v2_db_1  ... done 

Снова запускаете контейнер (п.2)

#### Остановка контейнера (можно повторно запустить):
> docker-compose -f docker-compose.localdev.yml stop

#### Остановка контейнера с удалением контейнера
> docker-compose -f docker-compose.localdev.yml down

#### Добавить суперпользователя (для захода в админку):
1. Смотрим список запущенных контейнеров командой:
> docker-compose ps
2. Находим контейнер с "web" в имени. Добавляем суперпользователя командой (backend_v2_web_1 - имя контейнера из п.1):
> docker exec -it backend_v2_web_1 python manage.py createsuperuser


## 2. Запуск docker-контейнера на сервере для разработки

1. Собрать контейнер
> docker-compose -f docker-compose.srvdev.yml build

2. Запустить контейнер
> docker-compose -f docker-compose.srvdev.yml up

#### Остановка контейнера (можно повторно запустить):
> docker-compose -f docker-compose.srvdev.yml stop

#### Остановка контейнера с удалением контейнера (volume остаются, база тоже)
> docker-compose -f docker-compose.srvdev.yml down

#### Комментарий
В отличие от формата запуска "1. Запуск docker-контейнера для локальной разработки", при запуске "2. Запуск docker-контейнера на сервере для разработки" будет использоваться СУБД Amazon RDS.


## 3. Запуск на прод сервере

1. Собрать контейнер
> docker-compose -f docker-compose.srvprod.yml build

2. Запустить контейнер
> docker-compose -f docker-compose.srvprod.yml up

#### Остановка контейнера (можно повторно запустить):
> docker-compose -f docker-compose.srvprod.yml stop

#### Остановка контейнера с удалением контейнера (volume остаются, база тоже)
> docker-compose -f docker-compose.srvprod.yml down

#### Комментарий
Формат запуска "2. Запуск docker-контейнера на сервере для разработки" отличается от "3. Запуск на прод сервере" тем, что используются тестовая и прод СУБД Amazon RDS.
