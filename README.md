# Сервис по сокращению ссылок
> В соответствии с договором об оказании услуг [удалено] от 30 сентября 2024 года

Сервис представляет собой набор Python скриптов для запуска сервиса для сокращения ссылок. Пользователи могут регистрироваться, создавать, удалять, добавлять в избранное ссылки, генерировать QR код.

## Стек разработки
* Python 3.11.8
* PostgreSQL 16
* Django 5.1
* Docker

## Быстрый старт

Скачать исходник :
* Скачайте [релизную версию](https://github.com/DogNellaf/link-operator-pro/releases)
* Или склонируйте репозиторий из ветки master путем выполнения команды `git clone https://github.com/DogNellaf/link-operator-pro`

Установка зависимостей :
* Скачайте PostgreSQL 16 с [официального сайта](https://www.postgresql.org/download/) для вашей операционной системы
* Скачайте Python:
    * Набор команд для ubuntu: 
       * `sudo apt update`
       * `sudo apt install python3.11 -y`
       * `sudo apt install python3-pip -y`
    * Python для windows можно скачать [здесь](https://www.python.org/downloads/release/python-3118/)
* Установите docker и docker-compose:
    * Набор команд для ubuntu: 
       * `sudo apt update`
       * `sudo apt install curl software-properties-common ca-certificates apt-transport-https -y`
       * `wget -O- https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor | sudo tee /etc/apt/keyrings/docker.gpg > /dev/null`
       * `echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu jammy stable"| sudo tee /etc/apt/sources.list.d/docker.list > /dev/null`
       * `sudo apt update`
       * `sudo apt install docker-ce -y`
       * `sudo apt-get install docker-compose`
    * Для windows на [официальном сайте](https://www.docker.com/products/docker-desktop/)

Запуск в докере:
* В папке проекта выполните команды:
    * `docker compose build`
    * `docker compose up -d`

## Эндпоинты

* 
* 
* 
* 

## Лицензия

Все права принадлежат ИП [удалено] ([удалено] от 01.09.2021)
