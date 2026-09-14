# Research Note 001 — When PASS Is Not Promotion

**Binding evaluations to the exact input consumed** · Version 1.0.1 · 14 September 2026

By **Xián Blanco Méndez**.

A writer's concern for what a story can honestly claim becomes a concrete engineering question. The technical argument, example and limits are set out in the note.

A passing check does not identify the candidate it evaluated unless the evidence binds the run to the input actually consumed. This note separates test results, admission eligibility and authoritative state.

- [Read the four-page note](research-note-001.pdf)
- [Editable Word document](research-note-001.docx)
- [Plain-text source](research-note-001.md)
- [Run or inspect the synthetic example](binding_example.py)
- [Recorded example output](example-output.json)

## Reproduce the example

With Python 3.10 or later, run:

```text
python binding_example.py
```

On systems where the command is named `python3`, use that name instead. No installation of packages is needed. The example does not use private data, write files, access the network or perform admission actions.

Expected observations: distinct inputs produce the same unbound PASS receipt; missing binding evidence yields UNKNOWN; contradictory identities yield REJECTED; matching evidence yields BINDING_CHECK_PASS_ONLY. Promotion remains NOT_EVALUATED.

## Scope

The historical case is a sanitized, author-reported account from a private project. Its source records are not distributed here. The example is synthetic and does not validate the private system. It assumes an honest local recorder and provides no durable or cryptographic attestation mechanism. See the note for prior art and full limitations.

The checksums describe the distributed files; they do not prove historical consumption, publication authority or factual correctness. Version changes should preserve the earlier release and state the correction.

## Revision history

Version 1.0.1 clarifies that a timestamp records a claimed time; it does not by itself prove event ordering. The finding and synthetic example are unchanged. Version 1.0 remains in the repository history.
