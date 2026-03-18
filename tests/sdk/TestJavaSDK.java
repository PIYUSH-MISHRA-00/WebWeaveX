public class TestJavaSDK {
  public static void main(String[] args) {
    WebWeaveXClient client = new WebWeaveXClient("http://127.0.0.1:8001");

    try {
      WebWeaveXClient.PageResult result = client.crawl("http://example.com");

      if (result.status == null || result.status != 200) {
        throw new Exception("Expected status 200, got " + result.status);
      }
      System.out.println("Java SDK crawl test passed");

      if (result.html == null) {
        throw new Exception("Missing html in response");
      }
      if (result.metadata == null) {
        throw new Exception("Missing metadata in response");
      }
      if (result.url == null) {
        throw new Exception("Missing url in response");
      }
      System.out.println("Java SDK response structure validated");

      System.exit(0);
    } catch (Exception error) {
      System.out.println("Java SDK test failed: " + error.getMessage());
      error.printStackTrace();
      System.exit(1);
    }
  }
}
