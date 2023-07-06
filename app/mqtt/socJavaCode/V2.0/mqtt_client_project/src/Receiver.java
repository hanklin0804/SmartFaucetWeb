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
