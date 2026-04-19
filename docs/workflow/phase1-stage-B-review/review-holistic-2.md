No blocking findings. Round 1 critiques are substantively resolved, with one minor wording residue.

- `METHODOLOGY`: Resolved. The physical path now cleanly separates per-arm depolarization from effective QBER via `arm_depol_p`, and the new public builder uses the default-path extractor rather than the Werner override ([mdi.py](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/qkdx/protocols/mdi.py:225>), [mdi.py](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/qkdx/protocols/mdi.py:412>)). `bb84_alice_source()` is ideal-only, so there is no hidden double-counting ([bb84.py](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/qkdx/protocols/bb84.py:24>)).

- `FINDING STRENGTH`: Mostly resolved. The body of §3.6.2 is now correctly framed as an ADR-style API semantic issue, not a physics finding ([PHASE1_LOG.md](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/docs/PHASE1_LOG.md:121>)). Minor residue remains: the section title still says `发现...`, and one test docstring still says `[FIND,ADR]` ([PHASE1_LOG.md](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/docs/PHASE1_LOG.md:109>), [test_mdi_bell.py](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/tests/test_protocols/test_mdi_bell.py:239>)).

- `PLAN ALIGNMENT`: Resolved. This is squarely Stage B work: default-path realization, physical builder exposure, tighter pinning, and deferral of the actual API convention decision to Stage D.

- `SCOPE DISCIPLINE`: Resolved. `build_mdi_bell_protocol` stays `partial` and now states the real blocker: its `executed_state()` is q-independent without per-arm depol in-channel ([mdi.py](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/qkdx/protocols/mdi.py:384>)).

- `NEXT STAGE PREP`: Good. The 28-case test module now covers trace preservation, zero-noise equivalence, formula pinning, Werner form, and input validation.

`pytest` could not start in this sandbox because there is no writable temp dir; I instead ran direct runtime checks, which confirmed 64 Kraus operators, `partial` scope, q-independence of `build_mdi_bell_protocol.executed_state()`, and formula agreement to ~`4e-17`.