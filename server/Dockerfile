FROM python
LABEL author="chene2000"
ENV PYTHONIOENCODING=utf-8

RUN mkdir -p /app
WORKDIR /app
COPY requirements.txt /app
RUN pip3 install -r requirements.txt -i https://pypi.doubanio.com/simple --trusted-host pypi.doubanio.com

COPY . /app

CMD bash start-server.sh