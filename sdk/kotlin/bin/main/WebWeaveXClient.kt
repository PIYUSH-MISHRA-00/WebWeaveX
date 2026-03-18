import io.ktor.client.HttpClient
import io.ktor.client.engine.cio.CIO
import io.ktor.client.request.post
import io.ktor.client.statement.bodyAsText
import io.ktor.http.ContentType
import io.ktor.http.contentType

class WebWeaveXClient(private val baseUrl: String) {
  private val client = HttpClient(CIO)

  suspend fun crawl(url: String): String = post("/crawl", url)

  suspend fun crawlSite(url: String): String = post("/crawl_site", url)

  suspend fun ragDataset(url: String): String = post("/rag_dataset", url)

  suspend fun knowledgeGraph(url: String): String = post("/knowledge_graph", url)

  private suspend fun post(path: String, url: String): String {
    val payload = "{\"url\":\"$url\"}"
    val response = client.post(baseUrl.trimEnd('/') + path) {
      contentType(ContentType.Application.Json)
      setBody(payload)
    }
    if (response.status.value !in 200..299) {
      throw IllegalStateException("Request failed: ${response.status} ${response.bodyAsText()}")
    }
    return response.bodyAsText()
  }

  suspend fun close() {
    client.close()
  }
}
