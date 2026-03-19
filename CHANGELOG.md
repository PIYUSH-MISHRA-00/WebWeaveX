# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-03-18

### Added

- Multi-language production SDK baseline for Python, Node.js, Dart, Java, and Kotlin.
- Structured SDK error models across all languages (timeout/network/http/application categories).
- Retry with exponential backoff and configurable timeout controls in all SDKs.
- Typed Java/Kotlin response models for crawl, RAG dataset, and knowledge graph APIs.
- SDK debug/log mode hooks for easier troubleshooting and integration diagnostics.
- Expanded root and per-SDK documentation with installation, quick start, security notes, and examples.
- CI pipeline coverage for Python, Node, Dart, Java, and Kotlin in `.github/workflows/ci.yml`.
- Release workflow builds for Java and Kotlin artifacts in `.github/workflows/release.yml`.
- Repository settings template `.github/settings.yml` for OSS discoverability topics/metadata.
- End-to-end verification artifact in `reports/FINAL_PROOF.md`.

### Changed

- Upgraded root README with a stronger product narrative, 10-second demo, comparison table, and simplified onboarding.
- Improved package metadata quality for Python (`setup.py`), Node (`sdk/node/package.json`), Dart (`sdk/dart/pubspec.yaml`), Java (`sdk/java/pom.xml`), and Kotlin (`sdk/kotlin/pom.xml`).
- Refined Kotlin SDK package structure (`io.github.piyushmishra.webweavex`) and aligned source files for production.
- Updated Java and Kotlin SDK examples/tests to use typed models and cleaner output.
- Normalized SDK API naming by adding cross-style aliases (`snake_case` + `camelCase`) where appropriate.

### Fixed

- Resolved Java source encoding BOM issue that caused compiler failures.
- Eliminated publish dry-run noise for Dart by validating package from a clean staging copy.
- Removed temporary execution script `phase10.ps1` and enforced final repo cleanup checks.
