suspend fun main() {
  val client = WebWeaveXClient("http://localhost:8000")
  val result = client.crawl("https://example.com")
  println(result)
  client.close()
}
