from sdk.python.webweavex_client import WebWeaveXClient


def main() -> None:
  client = WebWeaveXClient("http://localhost:8000")
  result = client.crawl("https://example.com")
  print(result)
  client.close()


if __name__ == "__main__":
  main()
