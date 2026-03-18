import java.util.Map;

public class TestJavaSDK {
  public static void main(String[] args) {
    WebWeaveXClient client = new WebWeaveXClient("http://127.0.0.1:8001");

    try {
      Map<String, Object> result = client.crawl("https://example.com");

      Double status = ((Number) result.get("status")).doubleValue();
      if (status != 200.0) {
        throw new Exception("Expected status 200, got " + status);
      }
      if (!result.containsKey("html") || !result.containsKey("metadata") || !result.containsKey("url")) {
        throw new Exception("Missing required fields in crawl response");
      }

      System.out.println("Java SDK crawl test passed");
      System.exit(0);
    } catch (Exception error) {
      System.out.println("Java SDK test failed: " + error.getMessage());
      error.printStackTrace();
      System.exit(1);
    }
  }
}
