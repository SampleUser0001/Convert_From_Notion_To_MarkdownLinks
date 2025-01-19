# 任意のイメージを取得
FROM python:latest

RUN ln -sf /usr/share/zoneinfo/Asia/Tokyo /etc/localtime

RUN python -m pip install --upgrade pip
RUN pip install python-dotenv

WORKDIR /opt/app

COPY app /opt/app

RUN chmod 755 /opt/app/start.sh

RUN python --version

# ENTRYPOINT [ "/opt/app/start.sh" ]
