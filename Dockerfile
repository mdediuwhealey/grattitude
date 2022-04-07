FROM python:3.8-alpine

COPY requirements.txt ./
# basic flask environment
RUN apk add --no-cache --update bash git nginx gcc libc-dev \
    && apk add --no-cache libffi-dev \
	&& pip install --upgrade pip \
	&& pip install -r requirements.txt 

# application folder
ENV APP_DIR /app

# app dir
RUN mkdir ${APP_DIR} \
	&& chown -R nginx:nginx ${APP_DIR} \
	&& chmod 777 /run/ -R \
	&& chmod 777 /root/ -R \
	&& chmod 777 ${APP_DIR} -R
VOLUME ${APP_DIR}
WORKDIR ${APP_DIR}

# expose web server port
# only http, for ssl use reverse proxy
EXPOSE 80

# copy config files into filesystem
COPY nginx.conf /etc/nginx/nginx.conf
COPY entrypoint.sh /entrypoint.sh 
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
