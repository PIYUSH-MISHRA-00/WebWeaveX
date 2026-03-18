public class TestJavaSDK {
  public static void main(String[] args) {
    WebWeaveXClient client = new WebWeaveXClient("http://127.0.0.1:8001");

    try {
      WebWeaveXClient.PageResult result = client.crawl("https://example.com");

      if (result.status == null || result.status != 200) {
        throw new Exception("Expected status 200, got " + result.status);
      }
      if (result.html == null || result.metadata == null || result.url == null) {
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
