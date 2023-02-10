FROM node:17.5.0
RUN mkdir -p /home/Service
WORKDIR /home/Service
COPY ./ /home/Service
RUN npm install pm2 --global  \
        && npm install
EXPOSE 3000
CMD pm2 start ./bin/www --no-daemon
