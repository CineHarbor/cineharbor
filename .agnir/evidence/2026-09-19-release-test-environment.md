# Release test environment materialization

Facade baseline: `6ea79cdfa5a218fc7ec9c374e14127ed4b959cbc`. Project identity/selected lineage and Agnir provenance remain unchanged. This is diagnostic/test infrastructure under the Principal's autonomous release authorization; it does not alter the product acceptance criteria.

The local executor cannot resolve network hosts, but authorized GitHub Actions can materialize already-declared locked dependencies. The new read-only workflow exports a pinned Rust 1.98.1 toolchain, matching wasm-bindgen CLI, Cargo registries and frozen Node dependency trees for isolated testing. It records the exact source revisions and archive checksums. It does not export Git credentials, signing keys, secret-store values, Git configuration or font files. Artifacts expire after two days and are not public releases.

Producing or importing a test environment is not a passing product test. Compiler, unit, browser, security, installation, updater and production-deployment results must still be independently observed and tied to the tested revisions. Source snapshots and final publication status remain governed by `docs/releases/1.0.0/scope.md`.
