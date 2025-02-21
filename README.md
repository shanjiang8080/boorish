Boorish is a simple booru-like image gallery created in django.  
Demoserver available here: [https://boorishdemo.shanjiang.ca](https://boorishdemo.shanjiang.ca)
***
![main page](https://raw.githubusercontent.com/shanjiang8080/boorish/refs/heads/main/preview_1.png)
![detail view](https://raw.githubusercontent.com/shanjiang8080/boorish/refs/heads/main/preview_2.png)
![filter view](https://raw.githubusercontent.com/shanjiang8080/boorish/refs/heads/main/preview_3.png)
## Installation:   
Install via docker: [https://hub.docker.com/r/shanjiang8080/boorish](https://hub.docker.com/r/shanjiang8080/boorish)    
Boorish is a simple booru-like image gallery created in django.   
# Installation   
To install, include a docker-compose.yml and two files called .web\_env and .db\_env in the same directory.
Your docker-compose.yml should look like this:   
```
services:
  web:
    container_name: boorish_gallery
    image: shanjiang8080/boorish
    volumes:
      - static_volume:/home/boorish/web/staticfiles
      - media_volume:/home/boorish/web/mediafiles
    expose:
      - 7999
    environment:
      - DJANGO_SUPERUSER_PASSWORD=defaultpassword
      - TRUSTED_ORIGINS="https://gallery.shanjiang.ca"
      - ALLOWED_HOSTS="gallery.shanjiang.ca"
      - SQL_PORT=3306
      # these should match those found in db
      - SQL_DATABASE=gallery_database
      - SQL_USER=gallery_user
      - SQL_PASSWORD=gallery_password
    restart: on-failure
    depends_on:
      - db

  db:
    container_name: boorish_db
    image: mariadb
    restart: always
    volumes:
      - mariadb_data:/var/lib/mysql/data
    environment:
      - MYSQL_PORT=5431
      - MYSQL_ROOT_PASSWORD=mariadb
      - MYSQL_ROOT_HOST=%
      # should match those found in web
      - MYSQL_DATABASE=gallery_database
      - MYSQL_USER=gallery_user
      - MYSQL_PASSWORD=gallery_password
    ports:
      - "5431:3306"
  nginx:
    container_name: boorish_nginx
    image: nginx
    volumes:
      - static_volume:/home/boorish/web/staticfiles
      - media_volume:/home/boorish/web/mediafiles
    configs:
    - source: nginx.conf
      target: /etc/nginx/conf.d/default.conf
    ports:
      - 1337:80
    restart: always
    depends_on:
      - web

volumes:
  mariadb_data:
  static_volume:
  media_volume:

configs:
  nginx.conf:
    content: |
      upstream boorish {
        server web:7999;
      }
      server {
        listen 80;
        location / {
          proxy_pass http://boorish;
          proxy_set_header X-Forwarded-For $$proxy_add_x_forwarded_for;
          proxy_set_header Host $$host;
          proxy_redirect off;
          client_max_body_size 1G;
        }
        location /static/ {
          alias /home/boorish/web/staticfiles/;
        }
        location /media/ {
          alias /home/boorish/web/mediafiles/;
        }
      }
```
The .db_env file should look like this:
```
MYSQL_ROOT_PASSWORD=[root_password]
MYSQL_ROOT_HOST=%
MYSQL_DATABASE=[mysql_database]
MYSQL_USER=[mysql_user]
MYSQL_PASSWORD=[mysql_password]
```
The .web_env file should look like this:
```
SQL_DATABASE=[mysql_database]
SQL_USER=[mysql_user]
SQL_PASSWORD=[mysql_password]
```
Note that `[mysql_database]`, `[mysql_user]`, and `[mysql_password]` should be identical across both files.
   
By default, the site is accessible on port 1337. To change the port, change the port in the docker compose file.   
   
# Usage:   
To add images, you must log in, which you can do in the top right corner. To add images, click the + icon. To add tags, click on the tag icon and add tags. There are four types of tags: Normal, Character, Artist, and Series.   
To add/remove users or remove images, use the admin panel, accessible at `localhost:1337/admin/` (or whatever the domain and port is).    
   
