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
    
    public void startGenerating() {
        executorService.scheduleAtFixedRate(() -> {
            FaucetData faucetData = generateData();
            String json = convertToJson(faucetData);
            try {
                Sender.sendData(json); // This assumes Sender.java has a static method 'sendData(String data)'
            } catch (Exception e) {
                e.printStackTrace();
            }
        }, 0, 5, TimeUnit.SECONDS);
    }

    private FaucetData generateData() {
        // Generate random data for FaucetData. You can adjust these as necessary.
        String faucetID = "Faucet" + random.nextInt(1000);
        String groupID = "Group" + random.nextInt(100);
        long totalUsageCount = random.nextLong();
        double totalUsageWater = random.nextDouble() * 1000;
        double totalUsageTime = random.nextDouble() * 100;
        boolean statusLeak = random.nextBoolean();
        boolean statusSensor = random.nextBoolean();
        long timestamp = System.currentTimeMillis();

        return new FaucetData(faucetID, groupID, totalUsageCount, totalUsageWater, totalUsageTime,
            statusLeak, statusSensor, timestamp);
    }

    private String convertToJson(FaucetData faucetData) {
        return gson.toJson(faucetData);
    }
}
