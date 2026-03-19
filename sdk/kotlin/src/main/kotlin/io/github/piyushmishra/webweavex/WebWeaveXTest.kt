package io.github.piyushmishra.webweavex

import kotlinx.coroutines.runBlocking
import kotlin.test.Test
import kotlin.test.assertNotNull

class WebWeaveXTest {

    @Test
    fun testClientCreation() = runBlocking {
        val client = WebWeaveX.create {
            baseUrl = "http://localhost:8001"
        }

        assertNotNull(client)
    }
}