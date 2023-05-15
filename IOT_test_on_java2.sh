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

        final MqttClient[] client = new MqttClient[1];
        Timer timer = new Timer();

        try {
            client[0] = new MqttClient(brokerUrl, clientId);
            MqttConnectOptions options = new MqttConnectOptions();
            options.setCleanSession(true);

            client[0].setCallback(new MqttCallback() {
                private int reconnectAttempts = 0;
                private int reconnectDelay = INITIAL_RECONNECT_DELAY_MS;

                @Override
                public void connectionLost(Throwable cause) {
                    System.out.println("Connection lost!");
                    while (!client[0].isConnected() && reconnectAttempts < MAX_RECONNECT_ATTEMPTS) {
                        try {
                            System.out.println("Attempting to reconnect...");
                            client[0].connect(options);
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

            client[0].connect(options);

            for (Faucet faucet : FaucetDataGenerator.faucets) {
                client[0].subscribe("CompanyID/BuildingID/#");
            }

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
            // Cancel the timer task and disconnect from the MQTT broker when the application shuts down
            Runtime.getRuntime().addShutdownHook(new Thread(() -> {
                timer.cancel();
                if (client[0].isConnected()) {
                    try {
                        for (Faucet faucet : FaucetDataGenerator.faucets) {
                            client[0].unsubscribe("CompanyID/BuildingID/#");
                        }
                        client[0].disconnect();
                        System.out.println("Disconnected from the MQTT broker");
                    } catch (MqttException e) {
                        e.printStackTrace();
                    }
                }
            }));
        }
    }
}
