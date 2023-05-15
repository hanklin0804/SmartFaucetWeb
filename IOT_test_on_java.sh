#!/bin/bash

# 安裝 Java SE 17
sudo apt update
sudo apt install openjdk-17-jdk -y
java -version

# 把 Java 路徑加入環境變數
JAVA_PATH=$(dirname $(readlink -f $(which java)))
echo "Java installed in $JAVA_PATH"
echo "export PATH=\$PATH:$JAVA_PATH" >> ~/.bashrc

# 讀取新的環境變數
source ~/.bashrc
echo "Java path added to PATH variable."

# 建立專案目錄
mkdir mqtt_client_project
cd mqtt_client_project

# 建立存放源碼檔案和類檔案的目錄
mkdir src  # java檔
mkdir bin  # byte code 檔
mkdir lib  # 建立存放第三方庫的目錄


# 下載並安裝 MQTT 客戶端庫，並將其放入 lib 目錄
wget -P lib https://repo1.maven.org/maven2/org/eclipse/paho/org.eclipse.paho.client.mqttv3/1.2.5/org.eclipse.paho.client.mqttv3-1.2.5.jar


# 創建 MqttClientDemo.java 源文件
cat <<EOF > src/MqttClientDemo.java
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
        String brokerUrl = "tcp://192.53.162.144:1883";
        String clientId = "JavaMqttClient";

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

            // 訂閱所有水龍頭的主題
            for (Faucet faucet : FaucetDataGenerator.faucets) {
                client.subscribe("CompanyID/BuildingID/#");
            }

            Timer timer = new Timer();
            timer.schedule(new TimerTask() {
                @Override
                public void run() {
                    for (Faucet faucet : FaucetDataGenerator.faucets) {
                        faucet.update();
                        String data = faucet.getInfo();
                        MqttMessage message = new MqttMessage(data.getBytes());
                        try {
                            client.publish(faucet.getTopic(), message);
                            System.out.println("Message sent: " + data);
                        } catch (MqttException e) {
                            e.printStackTrace();
                        }
                    }
                }
            }, 0, 5000);

        } catch (MqttException e) {
            e.printStackTrace();
        }
    }
}
EOF

# 創建 FaucetDataGenerator.java 源文件
cat <<EOF > src/FaucetDataGenerator.java
import java.util.*;

class Faucet {
    String deviceName;
    String deviceModel;
    String deviceSN;
    String deviceID;
    String fwVersion;
    double accAmount;
    int accFeedCount;
    double accFeedTime;
    String leakInfo;
    String topic;

    Faucet(String deviceName, String deviceModel, String deviceSN, String deviceID, String fwVersion, String topic) {
        this.deviceName = deviceName;
        this.deviceModel = deviceModel;
        this.deviceSN = deviceSN;
        this.deviceID = deviceID;
        this.fwVersion = fwVersion;
        this.topic = topic;
    }

    void update() {
        Random rand = new Random();

        this.accAmount = rand.nextDouble() * 1000;  // Generate random water consumption between 0 and 1000
        this.accFeedCount = rand.nextInt(100);  // Generate random feed count between 0 and 100
        this.accFeedTime = rand.nextDouble() * 100;  // Generate random feed time between 0 and 100
        this.leakInfo = rand.nextBoolean() ? "Leak Detected" : "No Leak";  // Generate random leak info
    }

    public String getTopic() {
        return this.topic;
    }

    public String getInfo() {
        return "Device Name: " + this.deviceName + "\n" +
                "Device Model: " + this.deviceModel + "\n" +
                "Device SN: " + this.deviceSN + "\n" +
                "Device ID: " + this.deviceID + "\n" +
                "Firmware Version: " + this.fwVersion + "\n" +
                "Accumulated Water Amount: " + this.accAmount + "\n" +
                "Accumulated Feed Count: " + this.accFeedCount + "\n" +
                "Accumulated Feed Time: " + this.accFeedTime + "\n" +
                "Leak Information: " + this.leakInfo + "\n";
    }
}

public class FaucetDataGenerator {
    static String commonTopic = "CompanyID/BuildingID/FloorID/Restroom";
    static String specialTopic = "CompanyID/BuildingID/FloorID/Kitchen";

    static Faucet faucet1 = new Faucet("Faucet1", "Model1", "SN1", "ID1", "Version1", commonTopic);
    static Faucet faucet2 = new Faucet("Faucet2", "Model2", "SN2", "ID2", "Version2", commonTopic);
    static Faucet faucet3 = new Faucet("Faucet3", "Model3", "SN3", "ID3", "Version3", specialTopic);

    public static List<Faucet> faucets = Arrays.asList(faucet1, faucet2, faucet3);
}
EOF


# 編譯 Java 源文件，將結果放入 bin 目錄
javac -cp .:lib/*:src/ src/*.java -d bin

# 運行應用程序
java -cp .:bin/:lib/* MqttClientDemo
