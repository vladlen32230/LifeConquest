FROM nginx:latest

COPY default.conf /etc/nginx/conf.d/default.conf
COPY .letsencrypt /etc/letsencrypt

WORKDIR /front

EXPOSE 80 443
