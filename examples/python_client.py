import requests


def main() -> None:
  response = requests.post(
    "http://127.0.0.1:8001/crawl",
    json={"url": "https://example.com"}
  )
  result = response.json()
  print("✅ Python SDK test passed")
  print(f"Status: {result['status']}")
  print(f"URL: {result['url']}")
  print(f"Title: {result['metadata']['title']}")


if __name__ == "__main__":
  main()
