FROM python:3.13

WORKDIR /app

RUN apt-get update && apt-get install -y iputils-ping mosquitto-clients

COPY agents.py requirements.txt zigbee0_zgb_packets_db.csv .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "agents.py"]