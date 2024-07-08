FROM node:18

WORKDIR /app

COPY . /app/

RUN npm install

RUN npm run build

WORKDIR /app/dist

COPY ../start.sh /start.sh

RUN chmod +x /start.sh

CMD ["/start.sh"]
