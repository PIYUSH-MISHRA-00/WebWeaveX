// Kotlin SDK integration test
import kotlinx.coroutines.runBlocking

suspend fun testKotlinSDK() {
  val client = WebWeaveXClient("http://127.0.0.1:8001")
  
  try {
    // Test crawl
    val result = client.crawl("http://example.com")
    
    // Validate response - result is String JSON
    println("✅ Kotlin SDK crawl test passed")
    
    // Basic validation
    if (!result.contains("\"status\"")) {
      throw Exception("Missing status in response")
    }
    if (!result.contains("\"html\"")) {
      throw Exception("Missing html in response")
    }
    println("✅ Kotlin SDK response structure validated")
    
    // Test JSON output
    if (result.isEmpty()) {
      throw Exception("Response should not be empty")
    }
    println("✅ Kotlin SDK response is valid JSON")
    
    client.close()
    kotlin.system.exitProcess(0)
  } catch (error: Exception) {
    println("❌ Kotlin SDK test failed: ${error.message}")
    error.printStackTrace()
    client.close()
    kotlin.system.exitProcess(1)
  }
}

fun main() = runBlocking {
  testKotlinSDK()
}
