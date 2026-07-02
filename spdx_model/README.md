# SPDX model files

SPDX model files bundled for offline builds.
Each subdirectory corresponds to one SPDX version and contains:

| File | Description | Canonical URL |
| ---- | ----------- | ------------- |
| `spdx-model.ttl` | RDF+SHACL model | `https://spdx.org/rdf/{VERSION}/spdx-model.ttl` |
| `spdx-context.jsonld` | JSON-LD context | `https://spdx.org/rdf/{VERSION}/spdx-context.jsonld` |
| `spdx-json-serialize-annotations.ttl` | JSON-LD serialization annotations | `https://spdx.org/rdf/{VERSION}/spdx-json-serialize-annotations.ttl` |
| `spdx-json-schema.json` | JSON Schema | `https://spdx.org/schema/{VERSION}/spdx-json-schema.json` |

Files were sourced from the [spdx-spec](https://github.com/spdx/spdx-spec) repository:

- `3.0.1/` — released; from `https://spdx.github.io/spdx-spec/v3.0.1/rdf/` (fetched 2026-06-24)
- `3.1/` — **draft (pre-release)**; from `https://spdx.github.io/spdx-spec/v3.1/rdf/` (fetched 2026-06-24, tracking `3.1-dev`)

> **Note:** SPDX 3.1 is still in development. The bundled `3.1/` files are a
> snapshot of the draft and may change before the spec is finalized. The
> `v3_1` bindings are provided for early testing and can change without notice.
> When the canonical `https://spdx.org/rdf/3.1/` URLs go live, refresh these
> files from there.

The build script (`gen/generate-bindings`) uses these files automatically when
`SHACL2CODE_SPDX_DIR` is not set, avoiding network access during the build.
Set `SHACL2CODE_SPDX_FORCE_NETWORK=1` to skip bundled files and fetch from the network instead.
