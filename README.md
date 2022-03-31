# hiphop-bot

![Deploy on Heroku](https://github.com/mshat/hiphop-bot/actions/workflows/docker-image.yml/badge.svg)


## Описание
Учебный проект: рекомендательная система для подбора музыкантов в жанре русского хип-хопа. 
Имеет разговорный интерфейс, то есть анализирует не заранее заданные команды, а сообщения на естественном языке. 
Работает через консоль или как телеграм-бот.

## Возможности
1. Подбор списка музыкантов, похожих на заданного (можно сразу с фильтрами, например: найди **соло** исполнителей **мужского пола** похожих на **касту** в возрасте **от 18 до 45 лет**).
2. Подбор списка рекомендаций по предпочтениям (по лайкам и дизлайкам).
3. Фильтрация артистов по полу, возрасту или количеству участников коллектива.
4. Поиск артистов по полу, возрасту, в определенном жанре
5. Просмотр списка всех артистов, дерева жанров
6. ...
7. Графическая админка для добавления артистов
![image](https://user-images.githubusercontent.com/37267798/161043989-37f45f25-337b-4848-a77a-21a6f14bc640.png)

## Особенности
* Алгоритм определения схожести артистов базируется на обобщающей мере близости, включающей расчёт близости жанров музыки артистов (по дереву жанров), пола и возраста музыкантов, количеству участников коллектива и преобладающему антуражу песен исполнителей.
* Распознавание фразы на естественном языке разговорным интерфейсом реализовано при помощи системы шаблонов фраз, которые сопоставляются с входным сообщением после токенизации и нормализации последнего. Для более удобной настройки шаблонов релазизована система проверки логических условий.
* Для системы сопоставления шаблонов и системы проверки логических условий написаны юнит и интеграционные тесты.
* Автоматическая сборка и деплой телеграм-бота на Heroku при помощи Github Actions. Проект обёрнут в Docker и может быть развёрнут с локальной БД (docker-compose.yml)
* Использутеся база данных PostgreSQL для хранения списка пользователей, истории их запросов к боту и данных рекомендательной системы (список артистов, жанров и тд).
* Для взаимодействия с данными в базе для каждой таблицы созданы классы-модели, наподобие ORM моделей в Django.
* Модуль разговорного бота имеет MVC архитектуру и два интерфейса: консольный и в виде телеграм-бота.
* Взаимодействие с Postgres организовано через пул соединений ThreadedConnectionPool модуля psycopg2.
* Используется паттерн синглтон для обеспечения единой точки доступа к данным рекомендательной системы и исключения многократной заргузки её данных.
* Админка на PySimpleGui с возможностью добавления, обновлнния и удаления артистов из базы

## Локальный запуск телеграм-бота
``` docker-compose up ```

**Нужно добавить файл hiphop_bot/hiphop_bot/env** со следующим содержанием: TG_TOKEN=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX, где вместо Х **токен вашего бота**.

Инструкция по регистрации бота: https://core.telegram.org/bots#6-botfather

## Пример
![Без имени-1](https://user-images.githubusercontent.com/37267798/161091163-400ebd2d-2eb2-487c-be09-24941def2191.jpg)

