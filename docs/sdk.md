# SDKs

WebWeaveX provides SDKs for Python, Node.js, Java, Kotlin, and Dart. All SDKs expose the
same high-level API to ensure consistent behavior across ecosystems.

## Design Goals

- Identical method signatures across languages
- Clear error handling and HTTP status propagation
- Simple integration with the WebWeaveX API server

## Core APIs

- `crawl(url)`
- `crawlSite(url)`
- `ragDataset(url)`
- `knowledgeGraph(url)`

## Python

```python
from sdk.python.webweavex_client import WebWeaveXClient

client = WebWeaveXClient("http://localhost:8000")
result = client.crawl("https://example.com")
print(result)
```

## Node.js

```javascript
const { WebWeaveXClient } = require("./sdk/node/index.js");

const client = new WebWeaveXClient("http://localhost:8000");
client.crawl("https://example.com").then(console.log);
```

## Dart

```dart
import 'package:webweavex/webweavex.dart';

final client = WebWeaveXClient('http://localhost:8000');
final result = await client.crawl('https://example.com');
print(result);
```

## Java

```java
WebWeaveXClient client = new WebWeaveXClient("http://localhost:8000");
String response = client.crawl("https://example.com");
System.out.println(response);
```

## Kotlin

```kotlin
val client = WebWeaveXClient("http://localhost:8000")
val response = client.crawl("https://example.com")
println(response)
```
