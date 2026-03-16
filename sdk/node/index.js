class WebWeaveXClient {
  constructor(baseUrl) {
    this.baseUrl = baseUrl.replace(/\/$/, "");
  }

  async crawl(url) {
    return this._post("/crawl", { url });
  }

  async crawlSite(url) {
    return this._post("/crawl_site", { url });
  }

  async ragDataset(url) {
    return this._post("/rag_dataset", { url });
  }

  async knowledgeGraph(url) {
    return this._post("/knowledge_graph", { url });
  }

  async _post(path, payload) {
    const response = await fetch(`${this.baseUrl}${path}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    if (!response.ok) {
      const text = await response.text();
      throw new Error(`Request failed: ${response.status} ${text}`);
    }

    return await response.json();
  }
}

module.exports = { WebWeaveXClient };
