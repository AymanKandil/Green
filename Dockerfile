FROM ubuntu:latest
RUN apt-get update -y && \
    apt-get install -y python3-pip python3
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip3 install -r requirements.txt
COPY . /app
CMD ["gunicorn", "-w 4", "-b", "0.0.0.0:5000", "app:app"]
