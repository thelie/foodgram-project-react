# praktikum_new_diplom

![workflow](https://github.com/thelie/foodgram-project-react/actions/workflows/main.yml/badge.svg)

Foodgram - продуктовый помощник.

«Продуктовый помощник» - сайт, на котором пользователи будут публиковать рецепты,
добавлять чужие рецепты в избранное и подписываться на публикации других авторов.
Сервис «Список покупок» позволит пользователям создавать список продуктов,
которые нужно купить для приготовления выбранных блюд.

### Для доступа к серверу

ip: http://62.84.123.138/
test login: testuser
test password: qYi7FProPMnq-2Wru!m4
admin login: foodadmin
admin password: qYi7FProPMnq-2Wru!m4
 
### Для запуска проекта на удаленном сервере:

Склонируйте репозиторий  на локальный компьютер

В файле infra/nginx.conf укажите IP-адрес вашего сервера. Скопируйте файлы
infra/nginx.conf и infra/docker-compose.yml в корневую директорию сервера. Там
же создайте файл .env по шаблону .env.template.
На сервере должны быть установлены docker и docker-compose.

Для запуска контейнеров выполните
```
sudo docker-compose up -d --build
```
После успешного запуска на сервере выполните команды (только после первого деплоя):
```
sudo docker-compose exec foodgram_backend_1 python manage.py makemigrations
```
```
sudo docker-compose exec foodgram_backend_1 python manage.py migrate
```
```
sudo docker-compose exec foodgram_backend_1 python manage.py collectstatic
```
```
sudo docker-compose exec foodgram_backend_1 python manage.py loader_csv
```
```
sudo docker exec -it foodgram_backend_1 python manage.py loaddata data/dump.json
``` 
