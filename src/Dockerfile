FROM python:3.8

WORKDIR /usr/src/app

COPY ./ ./

RUN apt update && apt upgrade -y
RUN pip3 install -r requirements.txt

CMD ["python3", "main.py"]
