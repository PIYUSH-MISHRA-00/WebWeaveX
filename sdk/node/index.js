const axios = require("axios");

const DEFAULT_RETRY_STATUSES = new Set([408, 429, 500, 502, 503, 504]);

class WebWeaveXError extends Error {
  constructor(message, options = {}) {
    super(message);
    this.name = "WebWeaveXError";
    this.code = options.code;
    this.cause = options.cause;
    this.isRetryable = Boolean(options.isRetryable);
  }
}

class WebWeaveXTimeoutError extends WebWeaveXError {
  constructor(message, options = {}) {
    super(message, { ...options, code: "TIMEOUT", isRetryable: true });
    this.name = "WebWeaveXTimeoutError";
  }
}

class WebWeaveXNetworkError extends WebWeaveXError {
  constructor(message, options = {}) {
    super(message, { ...options, code: "NETWORK", isRetryable: true });
    this.name = "WebWeaveXNetworkError";
  }
}

class WebWeaveXHTTPError extends WebWeaveXError {
  constructor(statusCode, message, responseBody, options = {}) {
    super(message, options);
    this.name = "WebWeaveXHTTPError";
    this.statusCode = statusCode;
    this.responseBody = responseBody;
  }
}

class WebWeaveXClient {
  constructor(baseUrl, options = {}) {
    const {
      timeout = 10_000,
      maxRetries = 2,
      backoffMs = 300,
      retryStatusCodes = [...DEFAULT_RETRY_STATUSES],
    } = options;

    this.baseUrl = baseUrl.replace(/\/$/, "");
    this.maxRetries = Math.max(0, maxRetries);
    this.backoffMs = Math.max(0, backoffMs);
    this.retryStatusCodes = new Set(retryStatusCodes);

    this.client = axios.create({
      timeout,
      headers: { "Content-Type": "application/json" },
    });

    this.client.interceptors.response.use(
      (response) => response,
      (error) => Promise.reject(this._normalizeError(error)),
    );
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
    const endpoint = `${this.baseUrl}${path}`;
    let lastError;

    for (let attempt = 0; attempt <= this.maxRetries; attempt += 1) {
      try {
        const response = await this.client.post(endpoint, payload);
        return response.data;
      } catch (error) {
        const sdkError = error instanceof WebWeaveXError ? error : this._normalizeError(error);
        lastError = sdkError;
        if (this._shouldRetry(sdkError, attempt)) {
          await this._sleep(this._delayFor(attempt));
          continue;
        }
        throw sdkError;
      }
    }

    throw lastError || new WebWeaveXError(`Request failed for ${endpoint}`);
  }

  _shouldRetry(error, attempt) {
    if (attempt >= this.maxRetries) {
      return false;
    }
    if (error instanceof WebWeaveXTimeoutError || error instanceof WebWeaveXNetworkError) {
      return true;
    }
    if (error instanceof WebWeaveXHTTPError) {
      return this.retryStatusCodes.has(error.statusCode);
    }
    return Boolean(error.isRetryable);
  }

  _delayFor(attempt) {
    return this.backoffMs * (2 ** attempt);
  }

  _sleep(ms) {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }

  _normalizeError(error) {
    if (error instanceof WebWeaveXError) {
      return error;
    }
    if (error && error.code === "ECONNABORTED") {
      return new WebWeaveXTimeoutError(`Request timed out: ${error.message}`, { cause: error });
    }
    if (error && error.response) {
      const statusCode = error.response.status;
      const responseBody = typeof error.response.data === "string"
        ? error.response.data
        : JSON.stringify(error.response.data);
      return new WebWeaveXHTTPError(
        statusCode,
        `Request failed with HTTP ${statusCode}`,
        responseBody,
        { cause: error, isRetryable: this.retryStatusCodes.has(statusCode) },
      );
    }
    if (error && error.request) {
      return new WebWeaveXNetworkError(`No response received: ${error.message}`, { cause: error });
    }
    return new WebWeaveXError(`Request failed: ${error && error.message ? error.message : String(error)}`, {
      cause: error,
    });
  }
}

module.exports = {
  WebWeaveXClient,
  WebWeaveXError,
  WebWeaveXTimeoutError,
  WebWeaveXHTTPError,
  WebWeaveXNetworkError,
};
