suspend fun main() {
  val client = WebWeaveXClient("http://127.0.0.1:8001")
  val result = client.crawl("https://example.com")
  println("✅ Kotlin SDK test passed")
  println(result)
  client.close()
}
