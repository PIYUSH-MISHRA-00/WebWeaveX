import org.jetbrains.kotlin.gradle.tasks.KotlinCompile

plugins {
    kotlin("jvm") version "1.9.24"
    `maven-publish`
    signing
    id("org.sonatype.central-publishing") version "0.10.0"
}

group = "io.github.piyush-mishra-00"
version = "0.1.0"

repositories {
    mavenCentral()
}

dependencies {
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-core:1.8.1")
    implementation("com.google.code.gson:gson:2.10.1")
    testImplementation(kotlin("test"))
}

kotlin {
    jvmToolchain(21)
}

java {
    withSourcesJar()
    withJavadocJar()
}

// Aggressive target alignment in afterEvaluate
afterEvaluate {
    tasks.withType<JavaCompile>().configureEach {
        sourceCompatibility = "21"
        targetCompatibility = "21"
    }
    tasks.withType<KotlinCompile>().configureEach {
        kotlinOptions {
            jvmTarget = "21"
        }
    }
}

val sonatypeUser: String = project.findProperty("sonatypeUsername") as String? ?: ""
val sonatypePass: String = project.findProperty("sonatypePassword") as String? ?: ""

publishing {
    publications {
        create<MavenPublication>("mavenJava") {
            from(components["java"])
            artifactId = "webweavex-kotlin"

            pom {
                name.set("WebWeaveX Kotlin SDK")
                description.set("Kotlin SDK for WebWeaveX AI-native web crawling platform")
                url.set("https://github.com/PIYUSH-MISHRA-00/WebWeaveX")

                licenses {
                    license {
                        name.set("Apache License, Version 2.0")
                        url.set("https://www.apache.org/licenses/LICENSE-2.0.txt")
                    }
                }

                developers {
                    developer {
                        id.set("piyush-mishra-00")
                        name.set("Piyush Mishra")
                        email.set("piyushmishra.professional@gmail.com")
                    }
                }

                scm {
                    connection.set("scm:git:git://github.com/PIYUSH-MISHRA-00/WebWeaveX.git")
                    developerConnection.set("scm:git:ssh://git@github.com:PIYUSH-MISHRA-00/WebWeaveX.git")
                    url.set("https://github.com/PIYUSH-MISHRA-00/WebWeaveX")
                }
            }
        }
    }
}

signing {
    useGpgCmd()
    sign(publishing.publications["mavenJava"])
}

centralPublishing {
    publishingType.set("AUTOMATIC")
    serverUrl.set("https://central.sonatype.com/api/v1/publisher")
    tokenUsername.set(sonatypeUser)
    tokenPassword.set(sonatypePass)
}