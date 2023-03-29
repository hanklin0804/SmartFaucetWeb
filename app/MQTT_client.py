# MQTT subscriber
import paho.mqtt.client as mqtt
from pymongo import MongoClient

# MQTT 連接和主題設置
broker = "10.140.0.2"
port = 1883
topic = "faucet_data/+"  # 訂閱所有水龍頭的數據

# MongoDB 連接設置
mongo_uri = "mongodb://hanklin:hanklin@172.17.0.2:27017"
database_name = "faucets"
collection_name = "faucets123"

# 創建 MongoDB 客戶端並連接到指定的集合
mongo_client = MongoClient(mongo_uri)
db = mongo_client[database_name]
collection = db[collection_name]

# 定義 MQTT 消息處理函數
def on_message(client, userdata, message):
    data = message.payload.decode()
    topic = message.topic

    # # 解析數據，例如將其轉換為字典
    # parsed_data = parse_data(data)  # 根據您的數據格式實現此函數

    # # 將數據儲存到 MongoDB
    # collection.insert_one(parsed_data)
    print(f"Stored data: {data}")

# 初始化 MQTT 客戶端
client = mqtt.Client()
client.on_message = on_message

# 連接到 MQTT Broker 並訂閱主題
client.connect(broker, port)
client.subscribe(topic)

# 啟動 MQTT 客戶端循環
client.loop_forever()
