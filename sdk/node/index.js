const axios = require('axios');

class WebWeaveXClient {
  constructor(baseUrl) {
    this.baseUrl = baseUrl.replace(/\/$/, "");
    this.client = axios.create({
      timeout: 10000,
      headers: { "Content-Type": "application/json" }
    });
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
    try {
      const response = await this.client.post(`${this.baseUrl}${path}`, payload);
      return response.data;
    } catch (error) {
      if (error.response) {
        throw new Error(`Request failed: ${error.response.status} ${error.response.statusText}`);
      } else if (error.request) {
        throw new Error(`Request failed: No response received`);
      } else {
        throw new Error(`Request failed: ${error.message}`);
      }
    }
  }
}

module.exports = { WebWeaveXClient };
