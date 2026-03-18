import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;
import java.io.IOException;
import java.lang.reflect.Type;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.Map;

public class WebWeaveXClient {
  private final String baseUrl;
  private final HttpClient client;
  private final Gson gson;

  public WebWeaveXClient(String baseUrl) {
    this.baseUrl = baseUrl.replaceAll("/$", "");
    this.client = HttpClient.newHttpClient();
    this.gson = new Gson();
  }

  public Map<String, Object> crawl(String url) throws IOException, InterruptedException {
    return post("/crawl", url);
  }

  public Map<String, Object> crawlSite(String url) throws IOException, InterruptedException {
    return post("/crawl_site", url);
  }

  public Map<String, Object> ragDataset(String url) throws IOException, InterruptedException {
    return post("/rag_dataset", url);
  }

  public Map<String, Object> knowledgeGraph(String url) throws IOException, InterruptedException {
    return post("/knowledge_graph", url);
  }

  private Map<String, Object> post(String path, String url) throws IOException, InterruptedException {
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
    Type type = new TypeToken<Map<String, Object>>(){}.getType();
    return gson.fromJson(response.body(), type);
  }
}
