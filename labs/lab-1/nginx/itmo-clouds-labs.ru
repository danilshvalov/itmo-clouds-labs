server {
    listen 80;
    server_name itmo-cloud-labs.ru;

    location / {
        proxy_pass http://localhost:3000;
    }
}
