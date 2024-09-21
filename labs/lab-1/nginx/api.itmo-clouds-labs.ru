server {
    listen 80;
    server_name api.itmo-cloud-labs.ru;

    location / {
        proxy_pass http://localhost:8000;

        # CORS
        add_header 'Access-Control-Allow-Origin' '*';
        add_header 'Access-Control-Allow-Methods' 'GET, POST, HEAD, OPTIONS';
    }
}