import com.google.gson.Gson
import com.google.gson.JsonSyntaxException
import com.google.gson.annotations.SerializedName
import com.google.gson.reflect.TypeToken
import java.io.IOException
import java.io.InputStream
import java.lang.reflect.Type
import java.net.HttpURLConnection
import java.net.SocketTimeoutException
import java.net.URI
import java.nio.charset.StandardCharsets

class WebWeaveXClient(
  baseUrl: String,
  private val timeoutMillis: Int = 10_000,
  maxRetries: Int = 2,
  private val backoffMillis: Long = 300,
  retryStatusCodes: Set<Int> = DEFAULT_RETRY_STATUSES,
) {
  companion object {
    private val DEFAULT_RETRY_STATUSES = setOf(408, 429, 500, 502, 503, 504)
    private val PAGE_LIST_TYPE: Type = object : TypeToken<List<PageResult>>() {}.type
    private val RAG_LIST_TYPE: Type = object : TypeToken<List<RagRecord>>() {}.type
  }

  private val baseUrl: String = baseUrl.trimEnd('/')
  private val gson = Gson()
  private val maxRetries: Int = maxRetries.coerceAtLeast(0)
  private val retryStatusCodes: Set<Int> = retryStatusCodes.toSet()

  fun crawl(url: String): PageResult = post("/crawl", url, PageResult::class.java)

  fun crawlSite(url: String): List<PageResult> = post("/crawl_site", url, PAGE_LIST_TYPE)

  fun ragDataset(url: String): List<RagRecord> = post("/rag_dataset", url, RAG_LIST_TYPE)

  fun knowledgeGraph(url: String): KnowledgeGraphResponse = post("/knowledge_graph", url, KnowledgeGraphResponse::class.java)

  fun close() {
    // No-op: HttpURLConnection is per-request and closed after each call.
  }

  private fun <T> post(path: String, targetUrl: String, responseType: Type): T {
    val payload = gson.toJson(mapOf("url" to targetUrl))
    var lastError: WebWeaveXException? = null

    for (attempt in 0..maxRetries) {
      var connection: HttpURLConnection? = null
      try {
        val endpoint = URI.create(baseUrl + path).toURL()
        connection = endpoint.openConnection() as HttpURLConnection
        connection.requestMethod = "POST"
        connection.setRequestProperty("Content-Type", "application/json")
        connection.connectTimeout = timeoutMillis
        connection.readTimeout = timeoutMillis
        connection.doOutput = true

        val bytes = payload.toByteArray(StandardCharsets.UTF_8)
        connection.setFixedLengthStreamingMode(bytes.size)
        connection.outputStream.use { output ->
          output.write(bytes)
        }

        val status = connection.responseCode
        val body = readBody(connection, status)

        if (status !in 200..299) {
          val httpError = WebWeaveXHttpException(
            statusCode = status,
            message = "Request failed with HTTP $status for $path",
            responseBody = body,
          )
          lastError = httpError
          if (shouldRetryStatus(status, attempt)) {
            sleepBackoff(attempt)
            continue
          }
          throw httpError
        }

        return gson.fromJson(body, responseType)
      } catch (exception: SocketTimeoutException) {
        lastError = WebWeaveXTimeoutException("Request timed out after ${timeoutMillis}ms for $path", exception)
      } catch (exception: JsonSyntaxException) {
        throw WebWeaveXException("Invalid JSON response for $path", exception)
      } catch (exception: IOException) {
        lastError = WebWeaveXNetworkException("Network failure for $path: ${exception.message}", exception)
      } finally {
        connection?.disconnect()
      }

      if (attempt < maxRetries) {
        sleepBackoff(attempt)
        continue
      }

      throw lastError ?: WebWeaveXException("Request failed for $path")
    }

    throw lastError ?: WebWeaveXException("Request failed for $path")
  }

  private fun shouldRetryStatus(statusCode: Int, attempt: Int): Boolean {
    return attempt < maxRetries && retryStatusCodes.contains(statusCode)
  }

  private fun sleepBackoff(attempt: Int) {
    if (backoffMillis <= 0) {
      return
    }
    val delayMillis = backoffMillis * (1L shl attempt)
    try {
      Thread.sleep(delayMillis)
    } catch (exception: InterruptedException) {
      Thread.currentThread().interrupt()
      throw WebWeaveXException("Retry interrupted", exception)
    }
  }

  private fun readBody(connection: HttpURLConnection, status: Int): String {
    val stream: InputStream? = if (status in 200..299) connection.inputStream else connection.errorStream
    if (stream == null) {
      return ""
    }
    return stream.bufferedReader(StandardCharsets.UTF_8).use { it.readText() }
  }
}

open class WebWeaveXException(message: String, cause: Throwable? = null) : IOException(message, cause)

class WebWeaveXTimeoutException(message: String, cause: Throwable? = null) : WebWeaveXException(message, cause)

class WebWeaveXNetworkException(message: String, cause: Throwable? = null) : WebWeaveXException(message, cause)

class WebWeaveXHttpException(
  val statusCode: Int,
  message: String,
  val responseBody: String,
) : WebWeaveXException(message)

data class PageResult(
  val url: String? = null,
  val status: Int? = null,
  val html: String? = null,
  val links: List<Link> = emptyList(),
  val metadata: Metadata = Metadata(),
  val markdown: String? = null,
  val text: String? = null,
)

data class Link(
  val url: String? = null,
  val text: String? = null,
)

data class Metadata(
  val title: String? = null,
  val meta: Map<String, String> = emptyMap(),
)

data class RagRecord(
  val text: String? = null,
  val url: String? = null,
  val title: String? = null,
  @SerializedName("chunk_id") val chunkId: Int? = null,
  @SerializedName("content_hash") val contentHash: String? = null,
  val meta: Map<String, Any?> = emptyMap(),
)

data class KnowledgeGraphResponse(
  val nodes: List<GraphNode> = emptyList(),
  val edges: List<GraphEdge> = emptyList(),
)

data class GraphNode(
  val id: String? = null,
  val label: String? = null,
)

data class GraphEdge(
  val source: String? = null,
  val target: String? = null,
  val relation: String? = null,
)
