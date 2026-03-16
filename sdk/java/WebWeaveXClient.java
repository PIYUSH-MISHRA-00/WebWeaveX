import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

public class WebWeaveXClient {
  private final String baseUrl;
  private final HttpClient client;

  public WebWeaveXClient(String baseUrl) {
    this.baseUrl = baseUrl.replaceAll("/$", "");
    this.client = HttpClient.newHttpClient();
  }

  public String crawl(String url) throws IOException, InterruptedException {
    return post("/crawl", url);
  }

  public String crawlSite(String url) throws IOException, InterruptedException {
    return post("/crawl_site", url);
  }

  public String ragDataset(String url) throws IOException, InterruptedException {
    return post("/rag_dataset", url);
  }

  public String knowledgeGraph(String url) throws IOException, InterruptedException {
    return post("/knowledge_graph", url);
  }

  private String post(String path, String url) throws IOException, InterruptedException {
    String payload = String.format("{\"url\":\"%s\"}", url);
    HttpRequest request = HttpRequest.newBuilder()
        .uri(URI.create(baseUrl + path))
        .header("Content-Type", "application/json")
        .POST(HttpRequest.BodyPublishers.ofString(payload))
        .build();

    HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
    if (response.statusCode() < 200 || response.statusCode() >= 300) {
      throw new IOException("Request failed: " + response.statusCode() + " " + response.body());
    }
    return response.body();
  }
}
