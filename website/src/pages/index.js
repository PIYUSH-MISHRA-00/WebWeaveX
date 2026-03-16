import React from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';

export default function Home() {
  return (
    <Layout title="WebWeaveX" description="Universal Web Intelligence Engine">
      <main className="homepage">
        <section className="hero">
          <div className="hero-content">
            <p className="hero-eyebrow">Universal Web Intelligence Engine</p>
            <h1>WebWeaveX</h1>
            <p className="hero-subtitle">
              Crawl, render, and transform the open web into structured knowledge, RAG-ready
              datasets, and semantic graphs for AI systems.
            </p>
            <div className="hero-actions">
              <Link className="button button--primary" to="/docs/getting-started">
                Get Started
              </Link>
              <a
                className="button button--secondary"
                href="https://github.com/PIYUSH-MISHRA-00/WebWeaveX"
              >
                View on GitHub
              </a>
            </div>
          </div>
          <div className="hero-panel">
            <div className="panel-title">What you get</div>
            <ul>
              <li>Async crawling with robots + sitemap compliance</li>
              <li>LLM-ready extraction and chunked datasets</li>
              <li>Knowledge graphs with entities and relationships</li>
              <li>Distributed crawling with Redis workers</li>
              <li>SDKs, CLI, plugins, and an HTTP API</li>
            </ul>
          </div>
        </section>

        <section className="section">
          <h2>Why WebWeaveX</h2>
          <p>
            Most crawlers stop at HTML. WebWeaveX goes further by converting content into
            structured knowledge that powers search, RAG, and analytics workflows.
          </p>
        </section>

        <section className="section features">
          <h2>Key Features</h2>
          <div className="feature-grid">
            <div className="feature-card">
              <h3>Modern Web Support</h3>
              <p>Playwright-backed JS rendering with configurable wait strategies.</p>
            </div>
            <div className="feature-card">
              <h3>LLM-Ready Output</h3>
              <p>Markdown extraction, clean text, and chunked dataset builders.</p>
            </div>
            <div className="feature-card">
              <h3>Knowledge Graphs</h3>
              <p>Entity and relationship extraction with export formats for Neo4j or Gephi.</p>
            </div>
            <div className="feature-card">
              <h3>Distributed Crawling</h3>
              <p>Coordinator + worker architecture with Redis queue support.</p>
            </div>
            <div className="feature-card">
              <h3>SDKs + CLI</h3>
              <p>Python, Node, Java, Kotlin, Dart, plus a developer-friendly CLI.</p>
            </div>
            <div className="feature-card">
              <h3>Plugin Extensions</h3>
              <p>Drop-in plugins for domain-specific extraction and enrichment.</p>
            </div>
          </div>
        </section>

        <section className="section callout">
          <div>
            <h2>Ready to build?</h2>
            <p>Start crawling in minutes and ship AI-ready datasets with confidence.</p>
          </div>
          <Link className="button button--primary" to="/docs/getting-started">
            Read the Docs
          </Link>
        </section>
      </main>
    </Layout>
  );
}
