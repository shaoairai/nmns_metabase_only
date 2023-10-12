FROM python:3.7.2-stretch

RUN apt-get update
RUN apt-get install -y openssh-server

WORKDIR /app

ADD ./ /app

RUN pip install -r requirements.txt

# EXPOSE 5000

# docker build -t shaoairai/iseek:latest .  docker push shaoairai/iseek:latest

# docker run -d -p 5328:5000 -it  --restart=always -v C:\project\iseek:/app  --name flaktest2 shaoairai/test bash -c "flask run --no-debugger --port 5012 --host 0.0.0.0"

