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
        proxy_pass      http://${APP_HOST}:${APP_PORT};
        include         /etc/nginx/proxy_params;
    }

}