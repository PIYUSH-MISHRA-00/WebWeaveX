import java.util.Map;

public class JavaClientExample {
  public static void main(String[] args) throws Exception {
    WebWeaveXClient client = new WebWeaveXClient("http://127.0.0.1:8001");
    Map<String, Object> result = client.crawl("https://example.com");
    System.out.println("✅ Java SDK test passed");
    System.out.println(result);
  }
}
