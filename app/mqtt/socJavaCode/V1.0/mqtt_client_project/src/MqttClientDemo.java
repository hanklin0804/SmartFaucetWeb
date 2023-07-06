// 匯入所需的 Java 套件
import org.eclipse.paho.client.mqttv3.*;
import java.util.Timer;
import java.util.TimerTask;
import java.io.FileInputStream;
import java.io.IOException;
import java.util.Properties;
import java.io.File;
import java.io.PrintStream;
import java.io.FileNotFoundException;

// 定義 MqttClientDemo 類別
public class MqttClientDemo {
    // 定義最大重連次數、初始重連延遲時間 (毫秒) 和最大重連延遲時間 (毫秒)
    private static final int MAX_RECONNECT_ATTEMPTS = 10;
    private static final int INITIAL_RECONNECT_DELAY_MS = 1000;
    private static final int MAX_RECONNECT_DELAY_MS = 60000;
    // log文件限制大小
    private static final long MAX_LOG_FILE_SIZE = 1000;  //單位byte
    private static PrintStream currentLogStream;
    
    // 主函數
    public static void main(String[] args) {
        // 將系統的標準輸出和標準錯誤輸出導向到檔案
        try {
            currentLogStream = new PrintStream("./logs/MqttClientDemo.log");
            System.setOut(currentLogStream);
            System.setErr(currentLogStream);
        } catch (FileNotFoundException e) {
            e.printStackTrace();
            System.exit(1);
        }

        // 讀取設定檔案 (config.properties)
        Properties properties = new Properties();
        try {
            properties.load(new FileInputStream("./resources/config.properties"));
        } catch (IOException e) {
            e.printStackTrace();
            System.exit(1);
        }

        // 從設定檔案中讀取 MQTT 代理伺服器的 URL 和客戶端 ID
        String brokerUrl = properties.getProperty("brokerUrl");
        String clientId = properties.getProperty("clientId");
        
        // 定義一個 MqttClient 類別的陣列和一個 Timer 類別的物件
        final MqttClient[] client = new MqttClient[1];
        Timer timer = new Timer();

        timer.schedule(new TimerTask() {
            @Override
            public void run() {
                checkLogFileSizeAndSwitchIfNeeded();
            }
        }, 0, 60 * 1000);  // 單位:毫秒

        try {
            // 建立一個新的 MqttClient 物件
            client[0] = new MqttClient(brokerUrl, clientId);
            // 建立一個新的 MqttConnectOptions 物件，用於設定 MQTT 連線的選項
            MqttConnectOptions options = new MqttConnectOptions();
            options.setCleanSession(true);  // 設定清除會話
            options.setAutomaticReconnect(true);  // 設定自動重新連線
            options.setConnectionTimeout(10);  // 設定連線超時時間

            // 為 MQTT 客戶端設定回呼函數
            client[0].setCallback(new MqttCallback() {
                // 定義重新連線嘗試的次數和延遲時間
                private int reconnectAttempts = 0;
                private int reconnectDelay = INITIAL_RECONNECT_DELAY_MS;

                // 當連線丟失時的動作
                @Override
                public void connectionLost(Throwable cause) {
                    System.out.println("Connection lost!");
                    // 如果客戶端尚未連線，且重新連線嘗試的次數小於最大嘗試次數，則嘗試重新連線
                    while (!client[0].isConnected() && reconnectAttempts < MAX_RECONNECT_ATTEMPTS) {
                        try {
                            System.out.println("Attempting to reconnect...");
                            client[0].connect(options);
                            System.out.println("Reconnected!");
                            reconnectAttempts = 0;
                            reconnectDelay = INITIAL_RECONNECT_DELAY_MS;
                        } catch (MqttException e) {
                            // 如果重新連線失敗，則增加重新連線嘗試的次數，並延長下次嘗試的延遲時間
                            reconnectAttempts++;
                            System.out.println("Reconnection attempt " + reconnectAttempts + " failed. Trying again in " + reconnectDelay/1000 + " seconds...");
                            try {
                                Thread.sleep(reconnectDelay);
                            } catch (InterruptedException ie) {
                                ie.printStackTrace();
                            }
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

                // 當訊息到達時的動作
                @Override
                public void messageArrived(String topic, MqttMessage message) {
                    // 打印出接收到的訊息
                    System.out.println("Received message: " + new String(message.getPayload()));
                }

                // 當訊息送達完成時的動作
                @Override
                public void deliveryComplete(IMqttDeliveryToken token) {
                    // 在這個範例中，我們並沒有做任何事情
                }
            });

            // 嘗試連接到 MQTT 代理伺服器
            try {
                client[0].connect(options);
            } catch (MqttException e) {
                // 依照不同的錯誤原因，給出對應的錯誤訊息
                if (e.getReasonCode() == MqttException.REASON_CODE_SERVER_CONNECT_ERROR) {
                    System.out.println("Unable to connect to server, please check your network connection or broker URL");
                } else if (e.getReasonCode() == MqttException.REASON_CODE_CLIENT_TIMEOUT) {
                    System.out.println("Connection attempt timed out, please try again");
                } else if (e.getReasonCode() == MqttException.REASON_CODE_CONNECTION_LOST) {
                    System.out.println("Connection was lost, attempting to reconnect...");
                } else {
                    e.printStackTrace();
                }
            }

            // 為每個水龍頭訂閱對應的主題
            for (Faucet faucet : FaucetDataGenerator.faucets) {
                client[0].subscribe("CompanyID/BuildingID/#");
            }

            // 每隔五秒鐘，發送一次水龍頭的狀態資訊
            timer.schedule(new TimerTask() {
                @Override
                public void run() {
                    for (Faucet faucet : FaucetDataGenerator.faucets) {
                        // 更新水龍頭的狀態
                        try {
                            faucet.update();
                        } catch (Exception e) {
                            e.printStackTrace();
                            continue;
                        }

                        // 獲取水龍頭的資訊
                        String data;
                        try {
                            data = faucet.getInfo();
                        } catch (Exception e) {
                            e.printStackTrace();
                            continue;
                        }

                        // 建立一個新的 MQTT 訊息並設定 QoS 等級為 0
                        MqttMessage message = new MqttMessage(data.getBytes());
                        message.setQos(0);  

                        // 發送訊息
                        try {
                            client[0].publish(faucet.getTopic(), message);
                            System.out.println("Message sent: " + data);
                        } catch (MqttException e) {
                            e.printStackTrace();
                        }
                    }
                }
            }, 0, 5000);

        } catch (MqttException e) {
            e.printStackTrace();
        } finally {
            // 在程式結束時執行的動作
            Runtime.getRuntime().addShutdownHook(new Thread(() -> {
                // 取消定時器
                timer.cancel();
                // 如果 MQTT 客戶端仍在連接中
                if (client[0].isConnected()) {
                    try {
                        // 為每個水龍頭取消訂閱
                        for (Faucet faucet : FaucetDataGenerator.faucets) {
                            client[0].unsubscribe("CompanyID/BuildingID/#");
                        }
                        // 斷開與 MQTT 代理伺服器的連接
                        client[0].disconnect();
                        System.out.println("Disconnected from the MQTT broker");
                    } catch (MqttException e) {
                        e.printStackTrace();
                    }
                }
            }));
        }
    }

    // log文件過大，則刪除並重建新的
    private static void checkLogFileSizeAndSwitchIfNeeded() {
        File file = new File("./logs/MqttClientDemo.log");
        if (file.length() > MAX_LOG_FILE_SIZE) {
            currentLogStream.close();
            file.delete();
            try {
                currentLogStream = new PrintStream(file);
                System.setOut(currentLogStream);
                System.setErr(currentLogStream);
            } catch (FileNotFoundException e) {
                e.printStackTrace();
            }
        }
    }
}
