package io.github.piyushmishra.webweavex;

import com.google.gson.Gson;
import com.google.gson.JsonSyntaxException;
import com.google.gson.reflect.TypeToken;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.lang.reflect.Type;
import java.net.HttpURLConnection;
import java.net.SocketTimeoutException;
import java.net.URI;
import java.net.URL;
import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.function.Consumer;

public class WebWeaveXClient {
  private static final Set<Integer> DEFAULT_RETRY_STATUSES = Collections.unmodifiableSet(
      new HashSet<Integer>(Arrays.asList(408, 429, 500, 502, 503, 504))
  );
  private static final Type PAGE_LIST_TYPE = new TypeToken<List<PageResult>>() {}.getType();
  private static final Type RAG_LIST_TYPE = new TypeToken<List<RagRecord>>() {}.getType();

  private final String baseUrl;
  private final Gson gson;
  private final int timeoutMillis;
  private final int maxRetries;
  private final int backoffMillis;
  private final Set<Integer> retryStatuses;
  private final boolean debug;
  private final Consumer<String> logger;

  public WebWeaveXClient(String baseUrl) {
    this(baseUrl, 10_000, 2, 300, DEFAULT_RETRY_STATUSES, false, null);
  }

  public WebWeaveXClient(
      String baseUrl,
      int timeoutMillis,
      int maxRetries,
      int backoffMillis,
      Set<Integer> retryStatuses
  ) {
    this(baseUrl, timeoutMillis, maxRetries, backoffMillis, retryStatuses, false, null);
  }

  public WebWeaveXClient(
      String baseUrl,
      int timeoutMillis,
      int maxRetries,
      int backoffMillis,
      Set<Integer> retryStatuses,
      boolean debug,
      Consumer<String> logger
  ) {
    this.baseUrl = baseUrl.replaceAll("/$", "");
    this.gson = new Gson();
    this.timeoutMillis = Math.max(1, timeoutMillis);
    this.maxRetries = Math.max(0, maxRetries);
    this.backoffMillis = Math.max(0, backoffMillis);
    this.retryStatuses = retryStatuses == null
        ? DEFAULT_RETRY_STATUSES
        : Collections.unmodifiableSet(new HashSet<Integer>(retryStatuses));
    this.debug = debug;
    this.logger = logger == null ? System.out::println : logger;
  }

  public PageResult crawl(String url) throws WebWeaveXException {
    return post("/crawl", url, PageResult.class);
  }

  public List<PageResult> crawlSite(String url) throws WebWeaveXException {
    return post("/crawl_site", url, PAGE_LIST_TYPE);
  }

  public List<RagRecord> ragDataset(String url) throws WebWeaveXException {
    return post("/rag_dataset", url, RAG_LIST_TYPE);
  }

  public KnowledgeGraphResponse knowledgeGraph(String url) throws WebWeaveXException {
    return post("/knowledge_graph", url, KnowledgeGraphResponse.class);
  }

  private <T> T post(String path, String targetUrl, Type responseType) throws WebWeaveXException {
    Map<String, String> requestPayload = new HashMap<String, String>();
    requestPayload.put("url", targetUrl);
    String payload = gson.toJson(requestPayload);
    WebWeaveXException lastError = null;

    for (int attempt = 0; attempt <= maxRetries; attempt++) {
      HttpURLConnection connection = null;
      try {
        int attemptNo = attempt + 1;
        log("POST " + path + " attempt " + attemptNo + "/" + (maxRetries + 1));
        URL endpoint = URI.create(baseUrl + path).toURL();
        connection = (HttpURLConnection) endpoint.openConnection();
        connection.setRequestMethod("POST");
        connection.setRequestProperty("Content-Type", "application/json");
        connection.setConnectTimeout(timeoutMillis);
        connection.setReadTimeout(timeoutMillis);
        connection.setDoOutput(true);

        byte[] bytes = payload.getBytes(StandardCharsets.UTF_8);
        connection.setFixedLengthStreamingMode(bytes.length);
        try (OutputStream output = connection.getOutputStream()) {
          output.write(bytes);
        }

        int status = connection.getResponseCode();
        String body = readBody(connection, status);

        if (status < 200 || status >= 300) {
          WebWeaveXHTTPException error = new WebWeaveXHTTPException(
              status,
              "Request failed with HTTP " + status + " for " + path,
              body
          );
          lastError = error;
          if (shouldRetryStatus(status, attempt)) {
            log(error.getMessage() + "; retrying in " + (backoffMillis * (1L << attempt)) + "ms");
            sleepBackoff(attempt);
            continue;
          }
          throw error;
        }

        log("POST " + path + " succeeded with HTTP " + status);
        return gson.fromJson(body, responseType);
      } catch (SocketTimeoutException exception) {
        lastError = new WebWeaveXTimeoutException(
            "Request timed out after " + timeoutMillis + "ms for " + path,
            exception
        );
      } catch (JsonSyntaxException exception) {
        throw new WebWeaveXException("Invalid JSON response for " + path, exception);
      } catch (IOException exception) {
        lastError = new WebWeaveXNetworkException("Network failure for " + path + ": " + exception.getMessage(), exception);
      } finally {
        if (connection != null) {
          connection.disconnect();
        }
      }

      if (attempt < maxRetries) {
        if (lastError != null) {
          log(lastError.getMessage() + "; retrying in " + (backoffMillis * (1L << attempt)) + "ms");
        }
        sleepBackoff(attempt);
        continue;
      }

      throw lastError == null ? new WebWeaveXException("Request failed for " + path) : lastError;
    }

    throw lastError == null ? new WebWeaveXException("Request failed for " + path) : lastError;
  }

  private boolean shouldRetryStatus(int status, int attempt) {
    return attempt < maxRetries && retryStatuses.contains(status);
  }

  private void sleepBackoff(int attempt) throws WebWeaveXException {
    if (backoffMillis <= 0) {
      return;
    }
    long delayMillis = backoffMillis * (1L << attempt);
    try {
      Thread.sleep(delayMillis);
    } catch (InterruptedException exception) {
      Thread.currentThread().interrupt();
      throw new WebWeaveXException("Retry interrupted", exception);
    }
  }

  private String readBody(HttpURLConnection connection, int status) throws IOException {
    InputStream stream = status >= 200 && status < 300
        ? connection.getInputStream()
        : connection.getErrorStream();
    if (stream == null) {
      return "";
    }
    try (InputStream input = stream; ByteArrayOutputStream buffer = new ByteArrayOutputStream()) {
      byte[] chunk = new byte[4096];
      int read;
      while ((read = input.read(chunk)) != -1) {
        buffer.write(chunk, 0, read);
      }
      return new String(buffer.toByteArray(), StandardCharsets.UTF_8);
    }
  }

  private void log(String message) {
    if (debug) {
      logger.accept("[WebWeaveX SDK] " + message);
    }
  }

  public static class WebWeaveXException extends IOException {
    public WebWeaveXException(String message) {
      super(message);
    }

    public WebWeaveXException(String message, Throwable cause) {
      super(message, cause);
    }
  }

  public static class WebWeaveXTimeoutException extends WebWeaveXException {
    public WebWeaveXTimeoutException(String message, Throwable cause) {
      super(message, cause);
    }
  }

  public static class WebWeaveXNetworkException extends WebWeaveXException {
    public WebWeaveXNetworkException(String message, Throwable cause) {
      super(message, cause);
    }
  }

  public static class WebWeaveXHTTPException extends WebWeaveXException {
    private final int statusCode;
    private final String responseBody;

    public WebWeaveXHTTPException(int statusCode, String message, String responseBody) {
      super(message);
      this.statusCode = statusCode;
      this.responseBody = responseBody;
    }

    public int getStatusCode() {
      return statusCode;
    }

    public String getResponseBody() {
      return responseBody;
    }
  }

  public static class PageResult {
    public String url;
    public Integer status;
    public String html;
    public List<Link> links = Collections.emptyList();
    public Metadata metadata = new Metadata();
    public String markdown;
    public String text;
  }

  public static class Link {
    public String url;
    public String text;
  }

  public static class Metadata {
    public String title;
    public Map<String, String> meta = Collections.emptyMap();
  }

  public static class RagRecord {
    public String text;
    public String url;
    public String title;
    public Integer chunk_id;
    public String content_hash;
    public Map<String, Object> meta = Collections.emptyMap();
  }

  public static class KnowledgeGraphResponse {
    public List<GraphNode> nodes = Collections.emptyList();
    public List<GraphEdge> edges = Collections.emptyList();
  }

  public static class GraphNode {
    public String id;
    public String label;
  }

  public static class GraphEdge {
    public String source;
    public String target;
    public String relation;
  }
}
