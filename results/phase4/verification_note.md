# Phase 4 verification record

- Input: original 11 `conversations-###.json` files and `export_manifest.json`, previous local Phase 1/2 index files.
- Manifest: all 11 sizes matched; private SHA-256 digests generated for later replay checks.
- Source graph: all 1,049 `current_node` paths traversed without reported cycles or missing endpoints.
- Phase 2: all source pointers from 2,028 heuristic candidate events resolved to the indicated conversation branch; zero missing visible-source message pointers.
- Pilot: 25 per first-pass stratum; 20 additional nontext-enriched per screening category; five lexical-rescue records; 140 distinct review records after overlap removal.
- Unit tests: 7 fixture-based tests passed; `python3 -m compileall -q scripts tests` passed.
- **Not passed**: formal corpus inclusion, private exposure classification, independent scientific coding, intervention counts, causal AI/human attribution, artifact-level propagation and final retention. These have intentionally not been performed.

This record documents execution, not validation of scientific interpretation.
