fun main() {
  val client = WebWeaveXClient("http://127.0.0.1:8001")
  val result = client.crawl("https://example.com")

  println("Kotlin SDK test passed")
  println("Status: ${result.status}")
  println("URL: ${result.url}")
  println("Title: ${result.metadata.title}")

  client.close()
}
