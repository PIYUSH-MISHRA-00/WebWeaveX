import com.google.gson.Gson;
import com.google.gson.JsonElement;
import com.google.gson.reflect.TypeToken;
import java.io.IOException;
import java.io.InputStream;
import java.lang.reflect.Type;
import java.net.HttpURLConnection;
import java.net.URI;
import java.net.URL;
import java.nio.charset.StandardCharsets;
import java.util.List;
import java.util.Map;

public class WebWeaveXClient {
  private static final Type MAP_TYPE = new TypeToken<Map<String, Object>>() {}.getType();
  private static final Type LIST_MAP_TYPE = new TypeToken<List<Map<String, Object>>>() {}.getType();

  private final String baseUrl;
  private final Gson gson;

  public WebWeaveXClient(String baseUrl) {
    this.baseUrl = baseUrl.replaceAll("/$", "");
    this.gson = new Gson();
  }

  public Map<String, Object> crawl(String url) throws IOException {
    JsonElement body = post("/crawl", url);
    return gson.fromJson(body, MAP_TYPE);
  }

  public List<Map<String, Object>> crawlSite(String url) throws IOException {
    JsonElement body = post("/crawl_site", url);
    return gson.fromJson(body, LIST_MAP_TYPE);
  }

  public List<Map<String, Object>> ragDataset(String url) throws IOException {
    JsonElement body = post("/rag_dataset", url);
    return gson.fromJson(body, LIST_MAP_TYPE);
  }

  public Map<String, Object> knowledgeGraph(String url) throws IOException {
    JsonElement body = post("/knowledge_graph", url);
    return gson.fromJson(body, MAP_TYPE);
  }

  private JsonElement post(String path, String url) throws IOException {
    String payload = gson.toJson(Map.of("url", url));
    URL endpoint = URI.create(baseUrl + path).toURL();
    HttpURLConnection connection = (HttpURLConnection) endpoint.openConnection();
    connection.setRequestMethod("POST");
    connection.setRequestProperty("Content-Type", "application/json");
    connection.setDoOutput(true);

    byte[] bytes = payload.getBytes(StandardCharsets.UTF_8);
    connection.setFixedLengthStreamingMode(bytes.length);
    try (var output = connection.getOutputStream()) {
      output.write(bytes);
    }

    int status = connection.getResponseCode();
    InputStream stream = status >= 200 && status < 300
        ? connection.getInputStream()
        : connection.getErrorStream();
    String responseBody;
    try (stream) {
      responseBody = new String(stream.readAllBytes(), StandardCharsets.UTF_8);
    }
    if (status < 200 || status >= 300) {
      throw new IOException("Request failed: " + status + " " + responseBody);
    }
    return gson.fromJson(responseBody, JsonElement.class);
  }
}
