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
mkdir src  # 存放 .java 檔
mkdir bin  # 存放 byte code 檔
mkdir lib  # 存放第三方套件庫
mkdir resources # 存放設定檔案
mkdir logs # 存放日誌檔案
mkdir tmp
touch logs/receiver.log
touch logs/sender.log


# 下載並安裝 MQTT 客戶端庫，並將其放入 lib 目錄
# 使用 wget 指令從 Maven 倉庫下載 MQTT 客戶端庫
wget -O lib/org.eclipse.paho.client.mqttv3-1.2.5.jar https://repo1.maven.org/maven2/org/eclipse/paho/org.eclipse.paho.client.mqttv3/1.2.5/org.eclipse.paho.client.mqttv3-1.2.5.jar
wget -O lib/gson-2.10.1.jar https://repo1.maven.org/maven2/com/google/code/gson/gson/2.10.1/gson-2.10.1.jar

# 創建設定檔案 (config.properties)，並寫入 MQTT 代理伺服器的 URL 和客戶端 ID
cat <<EOF > resources/config.properties
brokerUrl=tcp://10.182.0.2:48755
topic=SOC/loadData
clientId=JavaMqttClient9
EOF

# 創建 Subscriber.java 源文件
cat <<'EOF' > src/Receiver.java
import java.io.FileInputStream;
import java.io.IOException;
import java.io.PrintWriter;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Properties;
import java.nio.file.StandardOpenOption;


import org.eclipse.paho.client.mqttv3.*;

public class Receiver implements MqttCallback {

    private static final Path LOG_PATH = Paths.get("logs/receiver.log");
    private static final long LOG_MAX_SIZE = 5 * 1024 * 1024; // 5 MB
    private static PrintWriter logWriter;

    public static void main(String[] args) throws MqttException, IOException {
        Properties props = new Properties();
        props.load(new FileInputStream("resources/config.properties"));

        String brokerUrl = props.getProperty("brokerUrl");
        String topic = props.getProperty("topic");

        MqttConnectOptions options = new MqttConnectOptions();
        options.setAutomaticReconnect(true);

        MqttClient client = new MqttClient(brokerUrl, MqttClient.generateClientId());
        client.setCallback(new Receiver());
        client.connect(options);

        logWriter = new PrintWriter(Files.newBufferedWriter(LOG_PATH, StandardOpenOption.APPEND));
        
        client.subscribe(topic);
    }

    @Override
    public void connectionLost(Throwable cause) {
        logWriter.println("Connection lost");
        logWriter.flush();
    }

    @Override
    public void messageArrived(String topic, MqttMessage message) throws IOException {
        manageLogFile();
        logWriter.println("Received message: " + new String(message.getPayload()));
        logWriter.flush();
    }

    @Override
    public void deliveryComplete(IMqttDeliveryToken token) {
        // Nothing to do here for this example
    }

    private static void manageLogFile() throws IOException {
        if (Files.size(LOG_PATH) > LOG_MAX_SIZE) {
            Files.move(LOG_PATH, Paths.get("logs/receiver.log.old"));
            logWriter.close();
            logWriter = new PrintWriter(Files.newBufferedWriter(LOG_PATH, StandardOpenOption.APPEND));

        }
    }
}
EOF

# 創建 Publisher.java 源文件
cat <<'EOF' > src/Sender.java
import java.io.FileInputStream;
import java.io.IOException;
import java.io.PrintWriter;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Properties;
import java.nio.file.StandardOpenOption;


import org.eclipse.paho.client.mqttv3.*;

public class Sender {

    private static final Path LOG_PATH = Paths.get("logs/sender.log");
    private static final long LOG_MAX_SIZE = 5 * 1024 * 1024; // 5 MB
    private static MqttClient client;
    private static PrintWriter logWriter;

    public static void main(String[] args) throws MqttException, IOException {
        Properties props = new Properties();
        props.load(new FileInputStream("resources/config.properties"));

        String brokerUrl = props.getProperty("brokerUrl");
        String topic = props.getProperty("topic");

        MqttConnectOptions options = new MqttConnectOptions();
        options.setAutomaticReconnect(true);

        client = new MqttClient(brokerUrl, MqttClient.generateClientId());
        client.connect(options);

        logWriter = new PrintWriter(Files.newBufferedWriter(LOG_PATH, StandardOpenOption.APPEND));

        new FaucetDataGenerator().startGenerating(); // This assumes FaucetDataGenerator has a no-arg constructor and startGenerating method
    }

    public static void sendData(String data) throws MqttException, IOException {
        manageLogFile();
        logWriter.println("Sending data: " + data);
        logWriter.flush();

        MqttMessage message = new MqttMessage();
        message.setPayload(data.getBytes());
        client.publish("SOC/loadData", message);
    }

    private static void manageLogFile() throws IOException {
        if (Files.size(LOG_PATH) > LOG_MAX_SIZE) {
            Files.move(LOG_PATH, Paths.get("logs/sender.log.old"));
            logWriter.close();
            logWriter = new PrintWriter(Files.newBufferedWriter(LOG_PATH, StandardOpenOption.APPEND));
        }
    }
}
EOF

# 創建 FaucetDataGenerator.java 源文件
cat <<'EOF' > src/FaucetDataGenerator.java
import java.util.Random;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;
import com.google.gson.Gson;

public class FaucetDataGenerator {
    
    private static class FaucetData {
        String FaucetID;
        String GroupID;
        long TotalUsageCount;
        double TotalUsageWater;
        double TotalUsageTime;
        boolean StatusLeak;
        boolean StatusSensor;
        long Timestamp;

        FaucetData(String FaucetID, String GroupID, long TotalUsageCount, double TotalUsageWater,
            double TotalUsageTime, boolean StatusLeak, boolean StatusSensor, long Timestamp) {
            this.FaucetID = FaucetID;
            this.GroupID = GroupID;
            this.TotalUsageCount = TotalUsageCount;
            this.TotalUsageWater = TotalUsageWater;
            this.TotalUsageTime = TotalUsageTime;
            this.StatusLeak = StatusLeak;
            this.StatusSensor = StatusSensor;
            this.Timestamp = Timestamp;
        }
    }

    private final ScheduledExecutorService executorService = Executors.newScheduledThreadPool(1);
    private final Gson gson = new Gson();
    private final Random random = new Random();
    private final FaucetData[] faucets = new FaucetData[5]; // Assuming 5 faucets
    
    public FaucetDataGenerator() {
        // Initialize the faucet data
        for (int i = 0; i < faucets.length; i++) {
            String faucetID = "Faucet" + i;
            String groupID = i < 3 ? "Group1" : "Group2"; // First 3 faucets in Group1, remaining in Group2
            faucets[i] = new FaucetData(faucetID, groupID, 0, 0, 0, false, true, System.currentTimeMillis());
        }
    }

    public void startGenerating() {
        executorService.scheduleAtFixedRate(() -> {
            for (FaucetData faucet : faucets) {
                updateAndSendData(faucet);
            }
        }, 0, 5, TimeUnit.SECONDS);
    }

    private void updateAndSendData(FaucetData faucet) {
        // Update the faucet data
        faucet.TotalUsageCount++;
        faucet.TotalUsageWater += random.nextDouble() * 10;  // Increase by up to 10 units
        faucet.TotalUsageTime += random.nextDouble();  // Increase by up to 1 unit
        faucet.StatusLeak = random.nextBoolean();
        faucet.StatusSensor = random.nextBoolean();
        faucet.Timestamp = System.currentTimeMillis();

        // Convert the updated faucet data to JSON and send it
        String json = convertToJson(faucet);
        try {
            Sender.sendData(json);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    private String convertToJson(FaucetData faucetData) {
        return gson.toJson(faucetData);
    }
}
EOF

# 編譯 .java 檔案
javac -d bin -cp lib/org.eclipse.paho.client.mqttv3-1.2.5.jar:lib/gson-2.10.1.jar src/*.java

# 執行 Sender 和 Receiver
java -cp bin:lib/org.eclipse.paho.client.mqttv3-1.2.5.jar:lib/gson-2.10.1.jar Receiver &
java -cp bin:lib/org.eclipse.paho.client.mqttv3-1.2.5.jar:lib/gson-2.10.1.jar Sender