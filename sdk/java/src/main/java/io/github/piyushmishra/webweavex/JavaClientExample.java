package io.github.piyushmishra.webweavex;

public class JavaClientExample {
  public static void main(String[] args) throws WebWeaveXClient.WebWeaveXException {
    WebWeaveXClient client = new WebWeaveXClient("http://127.0.0.1:8001");
    WebWeaveXClient.PageResult result = client.crawl("https://example.com");

    System.out.println("Java SDK test passed");
    System.out.println("Status: " + result.status);
    System.out.println("URL: " + result.url);
    System.out.println("Title: " + (result.metadata == null ? null : result.metadata.title));
  }
}
