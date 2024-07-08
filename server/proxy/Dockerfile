FROM nginx

ENV APP_HOST=asgi
ENV APP_PORT=9000
ENV LISTEN_PORT=80

COPY ./proxy_params /etc/nginx/
COPY ./default.conf.tpl /etc/nginx/

RUN touch /etc/nginx/conf.d/default.conf

RUN apt-get update && apt-get install -y gettext-base

CMD ["/bin/sh", "-c", "envsubst < /etc/nginx/default.conf.tpl > /etc/nginx/conf.d/default.conf && nginx -g 'daemon off;'"]
