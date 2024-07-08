# proxy/default.conf.tpl

server {
    listen 80;
  
    client_max_body_size 100M;
    
    location /static {
        alias /vol/static;
    }

    location /media {
        alias /vol/media;
    }

    location / {
        proxy_pass http://localhost:9000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        include /etc/nginx/proxy_params;
    }


    location /ws/ {
        proxy_pass http://localhost:9000;
        proxy_http_version 1.1;

    }
}
