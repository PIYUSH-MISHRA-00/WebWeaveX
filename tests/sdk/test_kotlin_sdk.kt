fun main() {
  val client = WebWeaveXClient("http://127.0.0.1:8001")

  try {
    val result = client.crawl("http://example.com")

    if (result.status == null) {
      throw Exception("Missing status in response")
    }
    if (result.html.isNullOrEmpty()) {
      throw Exception("Missing html in response")
    }
    println("Kotlin SDK response structure validated")

    client.close()
    kotlin.system.exitProcess(0)
  } catch (error: Exception) {
    println("Kotlin SDK test failed: ${error.message}")
    error.printStackTrace()
    client.close()
    kotlin.system.exitProcess(1)
  }
}
