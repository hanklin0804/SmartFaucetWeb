#!/bin/bash
# Create a new directory for the project
mkdir -p mqtt_webserver
mkdir -p mqtt_webserver/logs
mkdir -p mqtt_webserver/mongodb
cd mqtt_webserver

# 啟動 MongoDB、Mysql 容器並掛載資料夾
docker stop mongodb && docker rm -f mongodb
docker run -d -p 27017:27017 --name mongodb -v ./mongodb:/data/db mongo


# Install the necessary Python packages
pip install paho-mqtt pymongo

# Write the Python script to a file
cat > mqtt_client.py <<EOF
import paho.mqtt.client as mqtt
import json
import concurrent.futures
import threading
import logging
import logging.handlers
import time
from pymongo import MongoClient, errors

# Create a logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.handlers.TimedRotatingFileHandler('logs/mqtt_client.log', when="d", interval=1, backupCount=7)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Create a semaphore to limit the number of concurrent MQTT message processing
msg_semaphore = threading.Semaphore(500)

def connect_mongo():
    # MongoDB client setup
    mongo_client = MongoClient("mongodb://localhost:27017/")
    db = mongo_client["mqtt_data"]
    collection = db["device_data"]

    # Create unique index for "Device SN"
    collection.create_index("Device SN", unique=True)
    return collection

collection = connect_mongo()

def handle_message(collection, msg):
    try:
        # Ensure we release the semaphore even if an error occurs
        with msg_semaphore:
            payload = json.loads(msg.payload)

            # Make sure payload has the keys we need
            if "Device SN" not in payload:
                if "Device ID" not in payload:
                    logger.warning("Invalid message: Missing 'Device SN' and 'Device ID'")
                    return
                else:
                    payload["Device SN"] = payload["Device ID"]

            # Retry MongoDB operation on failure
            for _ in range(3):
                try:
                    collection.update_one({"Device SN": payload["Device SN"]}, {"$set": payload}, upsert=True)
                    print(123)
                    break
                except errors.PyMongoError as e:
                    print(3)
                    logger.error(f"An error occurred: {e}")
                    collection = connect_mongo()
    finally:
        msg_semaphore.release()

def on_connect(client, userdata, flags, rc):
    logger.info("Connected with result code "+str(rc))
    client.subscribe("CompanyID/#")

def on_message(client, userdata, msg):
    logger.debug(msg.topic+" "+str(msg.payload))
    msg_semaphore.acquire()
    executor.submit(handle_message, collection, msg)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Create a thread pool with 10 threads
executor = concurrent.futures.ThreadPoolExecutor(max_workers=10)

# Retry connection on failure
while True:
    try:
        client.connect("192.53.162.144", 1883, 60)
        client.loop_forever()
        break
    except Exception as e:
        logger.error(f"Failed to connect MQTT server: {e}")
        time.sleep(1)
EOF

python mqtt_client.py
