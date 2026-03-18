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
      debug = false,
      logger = null,
    } = options;

    this.baseUrl = baseUrl.replace(/\/$/, "");
    this.maxRetries = Math.max(0, maxRetries);
    this.backoffMs = Math.max(0, backoffMs);
    this.retryStatusCodes = new Set(retryStatusCodes);
    this.debug = Boolean(debug);
    this.logger = typeof logger === "function" ? logger : (message) => console.debug(message);

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

  async crawl_site(url) {
    return this.crawlSite(url);
  }

  async ragDataset(url) {
    return this._post("/rag_dataset", { url });
  }

  async rag_dataset(url) {
    return this.ragDataset(url);
  }

  async knowledgeGraph(url) {
    return this._post("/knowledge_graph", { url });
  }

  async knowledge_graph(url) {
    return this.knowledgeGraph(url);
  }

  async _post(path, payload) {
    const endpoint = `${this.baseUrl}${path}`;
    let lastError;

    for (let attempt = 0; attempt <= this.maxRetries; attempt += 1) {
      const attemptNo = attempt + 1;
      this._log(`POST ${endpoint} attempt ${attemptNo}/${this.maxRetries + 1}`);
      try {
        const response = await this.client.post(endpoint, payload);
        this._log(`POST ${endpoint} succeeded with HTTP ${response.status}`);
        return response.data;
      } catch (error) {
        const sdkError = error instanceof WebWeaveXError ? error : this._normalizeError(error);
        lastError = sdkError;
        if (this._shouldRetry(sdkError, attempt)) {
          this._log(`${sdkError.message}. Retrying in ${this._delayFor(attempt)}ms`);
          await this._sleep(this._delayFor(attempt));
          continue;
        }
        this._log(`POST ${endpoint} failed after ${attemptNo} attempts: ${sdkError.message}`);
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
      return new WebWeaveXTimeoutError(`Request timed out for ${error.config?.url || "endpoint"}: ${error.message}`, { cause: error });
    }
    if (error && error.response) {
      const statusCode = error.response.status;
      const responseBody = typeof error.response.data === "string"
        ? error.response.data
        : JSON.stringify(error.response.data);
      return new WebWeaveXHTTPError(
        statusCode,
        `Request failed with HTTP ${statusCode} for ${error.config?.url || "endpoint"}`,
        responseBody,
        { cause: error, isRetryable: this.retryStatusCodes.has(statusCode) },
      );
    }
    if (error && error.request) {
      return new WebWeaveXNetworkError(`No response received from ${error.config?.url || "endpoint"}: ${error.message}`, { cause: error });
    }
    return new WebWeaveXError(`Request failed: ${error && error.message ? error.message : String(error)}`, {
      cause: error,
    });
  }

  _log(message) {
    if (this.debug) {
      this.logger(`[WebWeaveX SDK] ${message}`);
    }
  }
}

module.exports = {
  WebWeaveXClient,
  WebWeaveXError,
  WebWeaveXTimeoutError,
  WebWeaveXHTTPError,
  WebWeaveXNetworkError,
};
