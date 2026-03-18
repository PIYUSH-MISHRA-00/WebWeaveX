// Java SDK integration test
import java.util.Map;
import java.util.Scanner;

public class TestJavaSDK {
  public static void main(String[] args) {
    WebWeaveXClient client = new WebWeaveXClient("http://127.0.0.1:8001");
    
    try {
      // Test crawl
      Map<String, Object> result = client.crawl("http://example.com");
      
      // Validate response
      Double status = ((Number) result.get("status")).doubleValue();
      if (status != 200.0) {
        throw new Exception("Expected status 200, got " + status);
      }
      System.out.println("✅ Java SDK crawl test passed");
      
      // Validate JSON structure
      if (!result.containsKey("html")) {
        throw new Exception("Missing html in response");
      }
      if (!result.containsKey("metadata")) {
        throw new Exception("Missing metadata in response");
      }
      if (!result.containsKey("url")) {
        throw new Exception("Missing url in response");
      }
      System.out.println("✅ Java SDK response structure validated");
      
      // Test JSON parsing
      if (!(result instanceof Map)) {
        throw new Exception("Response should be a Map");
      }
      System.out.println("✅ Java SDK response is valid JSON object");
      
      System.exit(0);
    } catch (Exception error) {
      System.out.println("❌ Java SDK test failed: " + error.getMessage());
      error.printStackTrace();
      System.exit(1);
    }
  }
}
