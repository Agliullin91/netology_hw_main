FROM ubuntu

RUN apt-get update

RUN apt-get install -y nginx

RUN echo "daemon off;" >> /etc/nginx/nginx.conf

COPY . /usr/share/nginx/html

WORKDIR /

CMD ["nginx"]

EXPOSE 80