FROM python:3.8.10

ENV PYTHONUNBUFFERED=1
ENV TZ=Asia/Seoul
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

WORKDIR /app

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt