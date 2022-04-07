FROM ubuntu:20.04

RUN apt-get update \
    && apt-get install -y net-tools \
    && apt-get install -y apt-utils \
	&& apt-get install -y python3 \
	&& apt-get install -y python3-pip \
	&& apt-get install -y iputils-ping \
    && apt-get install -y curl \
    && apt-get install -y systemctl

WORKDIR /app
COPY ./deploy.sh ./
RUN chmod u+x ./deploy.sh

CMD ["./deploy.sh"]e