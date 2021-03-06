### Telegram-Бот для сервиса Intraservice.ru

Предназначен для запуска через docker-compose (или просто docker).
Для запуска потребуется следующая информация:
* токен вашего telegram-бота
* имя сайта в Intraservice (если полная ссылка на ваш сайт https://mysite.intraservice.ru, то имя сайта будет mysite)
* логин и пароль к пользователю, от имени которого будет осуществляться вход в Intraservice
* id фильтра, через который бот будет смотреть новые заявки (если в браузере ссылка на страницу фильтра javascript:loadState(112), то id будет 112)
* указанные через запятую пользователи (логин в телеграм), которые могут пользоваться ботом

#### Пример docker-compose.yml:

```yml
version: '2'
services:
  bot_intraservice:
    image: mydockerhub/bot_intraservice
    container_name: Bot_Intraservice
    command: --botToken токен_бота --site имя_сайта --siteLogin логин_в_интрасервис --sitePass пароль_в_интрасервис --filterId ид_фильтра
    volumes:
    - /etc/localtime:/etc/localtime:ro
    - /home/user/botData:/usr/src/app/data      # путь к папке data, в /home/user/botData положить файл users.list
    restart: unless-stopped
```