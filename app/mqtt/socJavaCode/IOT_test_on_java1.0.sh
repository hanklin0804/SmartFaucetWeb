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
mkdir mqtt_client_project2
cd mqtt_client_project2

# 建立存放源碼檔案和類檔案的目錄
mkdir src  # java檔
mkdir bin  # byte code 檔
mkdir lib  # 建立存放第三方庫的目錄


# 下載並安裝 MQTT 客戶端庫，並將其放入 lib 目錄
wget -P lib https://repo1.maven.org/maven2/org/eclipse/paho/org.eclipse.paho.client.mqttv3/1.2.5/org.eclipse.paho.client.mqttv3-1.2.5.jar


# 創建 MqttClientDemo.java 源文件
cat <<EOF > src/MqttClientDemo.java
import org.eclipse.paho.client.mqttv3.*;

import java.util.Timer;
import java.util.TimerTask;

public class MqttClientDemo {
    private static final int MAX_RECONNECT_ATTEMPTS = 10;
    private static final int INITIAL_RECONNECT_DELAY_MS = 1000;
    private static final int MAX_RECONNECT_DELAY_MS = 60000;

    public static void main(String[] args) {
        String brokerUrl = "tcp://192.53.162.144:1883";
        String clientId = "JavaMqttClient";

        try {
            MqttClient client = new MqttClient(brokerUrl, clientId);
            MqttConnectOptions options = new MqttConnectOptions();
            options.setCleanSession(true);

            client.setCallback(new MqttCallback() {
                private int reconnectAttempts = 0;
                private int reconnectDelay = INITIAL_RECONNECT_DELAY_MS;

                @Override
                public void connectionLost(Throwable cause) {
                    System.out.println("Connection lost!");
                    // Attempt to reconnect with exponential backoff
                    while (!client.isConnected() && reconnectAttempts < MAX_RECONNECT_ATTEMPTS) {
                        try {
                            System.out.println("Attempting to reconnect...");
                            client.connect(options);
                            System.out.println("Reconnected!");
                            reconnectAttempts = 0;
                            reconnectDelay = INITIAL_RECONNECT_DELAY_MS;
                        } catch (MqttException e) {
                            reconnectAttempts++;
                            System.out.println("Reconnection attempt " + reconnectAttempts + " failed. Trying again in " + reconnectDelay/1000 + " seconds...");
                            try {
                                Thread.sleep(reconnectDelay);
                            } catch (InterruptedException ie) {
                                ie.printStackTrace();
                            }
                            // Increase delay for next try, but limit to max delay
                            reconnectDelay *= 2;
                            if (reconnectDelay > MAX_RECONNECT_DELAY_MS) {
                                reconnectDelay = MAX_RECONNECT_DELAY_MS;
                            }
                        }
                    }
                    if (reconnectAttempts >= MAX_RECONNECT_ATTEMPTS) {
                        System.out.println("Unable to reconnect after " + MAX_RECONNECT_ATTEMPTS + " attempts. Giving up.");
                    }
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

            for (Faucet faucet : FaucetDataGenerator.faucets) {
                client.subscribe("CompanyID/BuildingID/#");
            }

            Timer timer = new Timer();
            timer.schedule(new TimerTask() {
                @Override
                public void run() {
                    for (Faucet faucet : FaucetDataGenerator.faucets) {
                        try {
                            faucet.update();
                        } catch (Exception e) {
                            e.printStackTrace();
                            continue;
                        }

                        String data;
                        try {
                            data = faucet.getInfo();
                        } catch (Exception e) {
                            e.printStackTrace();
                            continue;
                        }

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
// 匯入 Java 內建的套件
import java.util.*;

// 定義 Faucet 類別來模擬水龍頭的資訊
class Faucet {
    // 定義水龍頭的各項屬性
    String deviceName; // 設備名稱
    String deviceModel; // 設備型號
    String deviceSN; // 設備序號
    String deviceID; // 設備 ID
    String fwVersion; // 韌體版本
    double accAmount; // 累計的水量
    int accFeedCount; // 累計的供水次數
    double accFeedTime; // 累計的供水時間
    String leakInfo; // 洩漏信息
    String topic; // MQTT 主題

    // Faucet 的建構子，用於初始化物件
    Faucet(String deviceName, String deviceModel, String deviceSN, String deviceID, String fwVersion, String topic) {
        this.deviceName = deviceName;
        this.deviceModel = deviceModel;
        this.deviceSN = deviceSN;
        this.deviceID = deviceID;
        this.fwVersion = fwVersion;
        this.topic = topic;
    }

    // 更新水龍頭的資訊
    void update() {
        Random rand = new Random();

        // 生成隨機的累計水量、供水次數、供水時間和洩漏信息
        this.accAmount = rand.nextDouble() * 1000;
        this.accFeedCount = rand.nextInt(100);
        this.accFeedTime = rand.nextDouble() * 100;
        this.leakInfo = rand.nextBoolean() ? "Leak Detected" : "No Leak";
    }

    // 獲取 MQTT 主題
    public String getTopic() {
        return this.topic;
    }

    // 獲取水龍頭的資訊
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

// 定義 FaucetDataGenerator 類別，用於生成和管理多個 Faucet 物件
public class FaucetDataGenerator {
    // 定義通用和特殊的 MQTT 主題
    static String commonTopic = "CompanyID/BuildingID/FloorID/Restroom";
    static String specialTopic = "CompanyID/BuildingID/FloorID/Kitchen";

    // 創建三個水龍頭的實例
    static Faucet faucet1 = new Faucet("Faucet1", "Model1", "SN1", "ID1", "Version1", commonTopic);
    static Faucet faucet2 = new Faucet("Faucet2", "Model2", "SN2", "ID2", "Version2", commonTopic);
    static Faucet faucet3 = new Faucet("Faucet3", "Model3", "SN3", "ID3", "Version3", specialTopic);

    // 將三個水龍頭實例放入一個列表中，方便管理和操作
    public static List<Faucet> faucets = Arrays.asList(faucet1, faucet2, faucet3);
}
EOF


# 編譯 Java 源文件，將結果放入 bin 目錄
javac -cp .:lib/*:src/ src/*.java -d bin

# 運行應用程序
java -cp .:bin/:lib/* MqttClientDemo
