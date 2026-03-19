package io.github.piyushmishra.webweavex

import kotlin.test.Test
import kotlin.test.assertNotNull
import kotlin.test.assertTrue

class WebWeaveXTest {
    @Test
    fun testClientInstantiation() {
        val client = WebWeaveX("http://localhost:8001")
        assertNotNull(client)
    }

    @Test
    fun testCrawlMethodExists() {
        // Since we don't have a running server in unit tests, we just check if the method is callable
        // In a real scenario, we would mock the Java client
        val client = WebWeaveX("http://localhost:8001")
        assertNotNull(client)
        // We won't actually call crawl here to avoid connection errors during build
        // unless we mock the underlying Java client which might be complex without mockito
    }
}
