// 匯入 Java 內建的套件
import java.util.*;

// 定義 Faucet 類別來模擬水龍頭的資訊
class Faucet {
    // 定義水龍頭的各項屬性
    String SocIP; // 板子的IP
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
    Faucet(String SocIP, String deviceName, String deviceModel, String deviceSN, String deviceID, String fwVersion, String topic) {
        this.SocIP = SocIP;
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
        return  "Soc IP: " + this.SocIP + "\n" +
                "Device Name: " + this.deviceName + "\n" +
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
    static String SocIP = "140.118.122.123";
    static String commonTopic = "CompanyID/BuildingID/FloorID/Restroom";
    static String specialTopic = "CompanyID/BuildingID/FloorID/Kitchen";

    // 創建三個水龍頭的實例
    static Faucet faucet1 = new Faucet(SocIP,"Faucet1", "Model1", "SN1", "ID1", "Version1", commonTopic);
    static Faucet faucet2 = new Faucet(SocIP,"Faucet2", "Model2", "SN2", "ID2", "Version2", commonTopic);
    static Faucet faucet3 = new Faucet(SocIP,"Faucet3", "Model3", "SN3", "ID3", "Version3", specialTopic);

    // 將三個水龍頭實例放入一個列表中，方便管理和操作
    public static List<Faucet> faucets = Arrays.asList(faucet1, faucet2, faucet3);
}
