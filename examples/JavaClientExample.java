public class JavaClientExample {
  public static void main(String[] args) throws Exception {
    WebWeaveXClient client = new WebWeaveXClient("http://localhost:8000");
    String result = client.crawl("https://example.com");
    System.out.println(result);
  }
}
