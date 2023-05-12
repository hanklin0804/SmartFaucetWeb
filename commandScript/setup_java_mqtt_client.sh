#!/bin/bash

# install java se 17
sudo apt update
sudo apt install openjdk-17-jdk -y
java -version

# add java path to environment variables
JAVA_PATH=$(dirname $(readlink -f $(which java)))
echo "Java installed in $JAVA_PATH"
echo "export PATH=\$PATH:$JAVA_PATH" >> ~/.bashrc
source ~/.bashrc


# 創建專案目錄
mkdir javaExample
cd javaExample

# 下載並安裝 MQTT 客戶端庫
wget https://repo1.maven.org/maven2/org/eclipse/paho/org.eclipse.paho.client.mqttv3/1.2.5/org.eclipse.paho.client.mqttv3-1.2.5.jar

# 創建 Java 源文件
cat <<EOF > MqttClientDemo.java
import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.MqttCallback;
import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttConnectOptions;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.MqttMessage;

import java.util.Timer;
import java.util.TimerTask;

public class MqttClientDemo {

    public static void main(String[] args) {
        String brokerUrl = "tcp://45.79.128.168:1883";
        String clientId = "JavaMqttClient";
        String topic = "temperature";

        try {
            MqttClient client = new MqttClient(brokerUrl, clientId);
            MqttConnectOptions options = new MqttConnectOptions();
            options.setCleanSession(true);

            client.setCallback(new MqttCallback() {
                @Override
                public void connectionLost(Throwable cause) {
                    System.out.println("Connection lost!");
                }

                @Override
                public void messageArrived(String topic, MqttMessage message) {
                    System.out.println("Received message: " + new String(message.getPayload()));
                }

                @Override
                public void deliveryComplete(IMqttDeliveryToken token) {
                }
            });

            client.connect(options);
            client.subscribe(topic);

            Timer timer = new Timer();
            timer.schedule(new TimerTask() {
                @Override
                public void run() {
                    String data = "{ \"ip\": \"140.118.122.123\", \"COMMAND\": \"deviceSN\", \"MODE\": \"SINGLE\", \"id\": \"562bf9a4d\", \"PARA\": \"-1\", }";
                    MqttMessage message = new MqttMessage(data.getBytes());
                    try {
                        client.publish(topic, message);
                        System.out.println("Message sent: " + data);
                    } catch (MqttException e) {
                        e.printStackTrace();
                    }
                }
            }, 0, 5000);

        } catch (MqttException e) {
            e.printStackTrace();
        }
    }
}
EOF

# 編譯 Java 源文件
javac -cp org.eclipse.paho.client.mqttv3-1.2.5.jar MqttClientDemo.java

# 運行應用程序
java -cp .:org.eclipse.paho.client.mqttv3-1.2.5.jar MqttClientDemo
