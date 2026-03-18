import requests

endpoints = ["crawl", "rag_dataset", "knowledge_graph"]
output_lines = []

for ep in endpoints:
    url = f"http://127.0.0.1:8001/{ep}"
    try:
        r = requests.post(url, json={"url": "https://example.com"}, timeout=30)
        output_lines.append(f"### {ep}\nStatus: {r.status_code}\nBody: {r.text[:1000]}\n")
    except Exception as e:
        output_lines.append(f"### {ep}\nERROR: {e}\n")

with open("reports/api_proof.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(output_lines))

print("Wrote reports/api_proof.txt")
