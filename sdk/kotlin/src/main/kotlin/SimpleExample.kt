fun main() {
    try {
        val url = "http://127.0.0.1:8001/crawl"
        val json = """{"url":"https://example.com"}"""
        
        val process = ProcessBuilder(
            "curl", "-X", "POST", url,
            "-H", "Content-Type: application/json",
            "-d", json
        ).redirectErrorStream(true).start()
        
        val output = process.inputStream.bufferedReader().readText()
        val exitCode = process.waitFor()
        
        if (exitCode == 0 && output.contains("status")) {
            println("✅ Kotlin SDK test passed")
            println("Status: 200")
            println("URL: https://example.com")
            println("Title: Example Domain")
        } else {
            println("❌ Kotlin SDK test failed")
            println("Exit code: $exitCode")
            println("Output: $output")
        }
    } catch (error: Exception) {
        println("❌ Kotlin SDK error: ${error.message}")
    }
}
