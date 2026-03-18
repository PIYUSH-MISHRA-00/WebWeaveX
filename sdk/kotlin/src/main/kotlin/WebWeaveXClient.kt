import java.io.IOException
import java.net.HttpURLConnection
import java.net.URI
import java.net.URL
import java.nio.charset.StandardCharsets

class WebWeaveXClient(baseUrl: String) {
  private val baseUrl: String = baseUrl.trimEnd('/')

  fun crawl(url: String): String = post("/crawl", url)

  fun crawlSite(url: String): String = post("/crawl_site", url)

  fun ragDataset(url: String): String = post("/rag_dataset", url)

  fun knowledgeGraph(url: String): String = post("/knowledge_graph", url)

  private fun post(path: String, url: String): String {
    val payload = """{"url":"$url"}"""
    val endpoint = URI.create(baseUrl + path).toURL()
    val connection = endpoint.openConnection() as HttpURLConnection
    connection.requestMethod = "POST"
    connection.setRequestProperty("Content-Type", "application/json")
    connection.doOutput = true

    val bytes = payload.toByteArray(StandardCharsets.UTF_8)
    connection.setFixedLengthStreamingMode(bytes.size)
    connection.outputStream.use { output ->
      output.write(bytes)
    }

    val status = connection.responseCode
    val responseBody = (if (status in 200..299) connection.inputStream else connection.errorStream)
      .bufferedReader(StandardCharsets.UTF_8)
      .use { it.readText() }

    if (status !in 200..299) {
      throw IOException("Request failed: $status $responseBody")
    }
    return responseBody
  }
}
