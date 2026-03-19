package io.github.piyushmishra.webweavex

import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.delay
import kotlinx.coroutines.withContext
import kotlin.math.min

data class WebWeaveXConfig(
    val baseUrl: String,
    val retries: Int = 3,
    val backoffMillis: Long = 300,
    val debug: Boolean = false
)

class WebWeaveX private constructor(
    private val config: WebWeaveXConfig
) : AutoCloseable {

    private val client = WebWeaveXClient(config.baseUrl)

    companion object {
        fun create(block: Builder.() -> Unit): WebWeaveX {
            val builder = Builder().apply(block)
            return WebWeaveX(builder.build())
        }
    }

    class Builder {
        var baseUrl: String = "http://localhost:8001"
        var retries: Int = 3
        var backoffMillis: Long = 300
        var debug: Boolean = false

        fun build(): WebWeaveXConfig {
            require(baseUrl.isNotBlank()) { "baseUrl must not be blank" }
            return WebWeaveXConfig(baseUrl, retries, backoffMillis, debug)
        }
    }

    private suspend fun <T> retry(block: suspend () -> T): T {
        var attempt = 0
        var lastError: Exception? = null

        while (attempt <= config.retries) {
            try {
                return block()
            } catch (e: Exception) {
                lastError = e
                if (attempt == config.retries) break

                val delayTime = min(config.backoffMillis * (1 shl attempt), 5000L)
                if (config.debug) println("Retry ${attempt + 1} in ${delayTime}ms")

                delay(delayTime)
                attempt++
            }
        }
        throw lastError ?: RuntimeException("Unknown error")
    }

    suspend fun crawl(url: String): PageResult =
        withContext(Dispatchers.IO) { retry { client.crawl(url) } }

    suspend fun rag(url: String): List<RagRecord> =
        withContext(Dispatchers.IO) { retry { client.ragDataset(url) } }

    suspend fun graph(url: String): KnowledgeGraphResponse =
        withContext(Dispatchers.IO) { retry { client.knowledgeGraph(url) } }

    override fun close() {
        try {
            client.close()
        } catch (_: Exception) {
            if (config.debug) println("Error closing client")
        }
    }
}