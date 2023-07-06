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
