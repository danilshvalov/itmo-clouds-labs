# Лабораторная работа №1

## Обязательное задание

### Введение

В данной лабораторной работе в качестве двух пет-проектов используются два скрипта на Python. Первый представляет из себя сервер, реализующий фронтенд, второй — реализующий бэкенд. Фронтенд возвращает HTML страницу, в которую встроен JS-скрипт. Этот скрипт запрашивает данные от бэкенда и выводит их на экран. Исходный код фронтенда и бэкенда находятся [здесь](frontend/server.py) и [здесь](backend/server.py) соответственно.

Для развертывания был арендован VDS-сервер, а также доменное имя `itmo-clouds-labs.ru`. Далее сервер и домен будут использоваться при настройке и развертывании Nginx.

Для доставки конфигурационных файлов до сервера использовался Git. С помощью утилиты командной строки данный репозиторий был склонирован на сервер. Все дальнейшие операции с файлами используют копию репозитория на сервере.

### Получение сертификатов

Лабораторная работа предполагает использование HTTPS-протокола для взаимодействия с сервером. Для использования HTTPS необходимо получить сертификаты.

Для получения сертификатов использовался certbot — утилита для получения сертификатов от Let's Encrypt. Let's Encrypt — это центр сертификации от некоммерческой организации ISRG, существующий при поддержке EFF и многих компаний, взявшей на себя миссию дать людям бесплатные SSL/TLS сертификаты для сайтов и серверов.

certbot был установлен следующим образом:

1. Установлены необходимые зависимости:

   ```bash
   sudo apt install python3 python3-venv libaugeas0 python3-certbot-nginx
   ```

2. Создано виртуальное окружение:

   ```bash
   sudo python3 -m venv /opt/certbot/
   sudo /opt/certbot/bin/pip install --upgrade pip
   ```

3. Установлен certbox:

   ```bash
   sudo /opt/certbot/bin/pip install certbot
   ```

4. Создан алиас для утилиты:

   ```bash
   ln -s /opt/certbot/bin/certbot /usr/bin/certbot
   ```

После установки certbot, были выписаны сертификаты с помощью следующей команды:

```bash
sudo certbot certonly --nginx
```

После выполнения команды и ввода необходимых данных, утилита вывела пути к созданным сертификатам:

```
Successfully received certificate.
Certificate is saved at: /etc/letsencrypt/live/itmo-clouds-labs.ru/fullchain.pem
Key is saved at:         /etc/letsencrypt/live/itmo-clouds-labs.ru/privkey.pem
```

Далее они будут использоваться при настройке Nginx.

### Настройка Nginx

Для настройки Nginx использовался конфиг, исходных код которого находится [здесь](nginx/nginx.conf). В нем можно выделить две части: конфигурация для фронтенда и для бэкенда. Рассмотрим каждую из них.

Конфигурация для фронтенда выглядит следующим образом:

```nginx
# frontend
server {
    server_name itmo-clouds-labs.ru;

    listen 443 ssl;
    ssl_certificate /etc/letsencrypt/live/itmo-clouds-labs.ru/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/itmo-clouds-labs.ru/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    location / {
        proxy_pass http://localhost:3000;
    }
}

# https redirect
server {
    listen 80;
    server_name itmo-clouds-labs.ru;
    return 301 https://itmo-clouds-labs.ru$request_uri;
}
```

В данном конфиге представлены две конфигурации `server`. Первая отвечает за HTTPS запросы и перенаправление их фронтенд серверу. Вторая отвечает за перенаправление HTTP запросов на HTTPS (т. е. к первой конфигурации).

Далее перечислены директивы и их назначения:

- `server_name` — указывается, на запросы с каким заголовком `Host` действуют далее описанные правила;
- `listen` — указывается, для какого порта действуют далее описанные правила;
- `ssl_certificate`, `ssl_certificate_key` и `ssl_dhparam` — настройка сертификатов;
- `location` — указывается, для каких HTTP-запросов действуют далее описанные правила (в данном случае для всех);
- `proxy_pass` — проксирование запроса (в данном случае фронтенд серверу).

Конфигурация для бэкенда выглядит похожим образом:

```nginx
# backend
server {
    server_name api.itmo-clouds-labs.ru;

    listen 443 ssl;
    ssl_certificate /etc/letsencrypt/live/itmo-clouds-labs.ru/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/itmo-clouds-labs.ru/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    location / {
        proxy_pass http://localhost:8000;

        # CORS
        add_header 'Access-Control-Allow-Origin' '*';
        add_header 'Access-Control-Allow-Methods' 'GET, POST, HEAD, OPTIONS';
    }
}

# https redirect
server {
    listen 80;
    server_name api.itmo-clouds-labs.ru;
    return 301 https://api.itmo-clouds-labs.ru$request_uri;
}
```

Единственное отличие, за исключением измененного хоста (вместо `itmo-clouds-labs.ru` теперь `api.itmo-clouds-labs.ru`), — это наличие директив `add_header`, которые разрешают кросс-доменные запросы (чтобы фронтенд мог ходить в бэкенд).

После того, как конфиг был дописан, его было необходимо переместить в папку конфигураций Nginx. Это было сделано следующими командами:

1. Удалены предыдущие файлы конфигураций:

   ```bash
   sudo rm /etc/nginx/sites-{available,enabled}/default
   ```

2. Созданы символические ссылки на ранее представленную конфигурацию:

   ```bash
   sudo ln -s ~/itmo-clouds-labs/labs/lab-1/nginx/nginx.conf /etc/nginx/sites-available/default
   sudo ln -s ~/itmo-clouds-labs/labs/lab-1/nginx/nginx.conf /etc/nginx/sites-enabled/default
   ```

После этого Nginx был перезагружен с помощью следующей команды:

```bash
sudo systemctl restart nginx
```

### Тестирование

При переходе по ссылке <https://itmo-clouds-labs.ru> открывается сайт с действительным сертификатом:

![](images/certificate.png)

При обновлении страницы фраза, выводимая на экран, меняется:

![](images/example-1.png)

![](images/example-2.png)

Это свидетельствует о том, что фронтенд и бэкенд работают, при этом у фронтенда получается доставить свой запрос до бэкенда.

### Заключение

В данной лабораторной работе был настроен Nginx для обслуживания фронтенда и бэкенда по протоколу HTTPS. Для реализации фронтенда и бэкенда использовались скрипты на Python, а для получения сертификатов использовался certbot.
