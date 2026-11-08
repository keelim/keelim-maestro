# Separate operator knowledge store

Status: retired on 2026-10-25. The operator no longer uses GBrain, so its
workspace helper integration and dedicated rollout contracts are removed.
Existing external stores, installations, and user records are preserved.

## Context

Collecting product source, secrets, and caches alongside operational documents would blur access and ownership. Local PGLite also has exclusive-access constraints.

## Historical decision and alternatives

Use a separate operator store with explicitly allowed document inputs. Avoid indiscriminate child-source collection. Confirm a trusted destination before an external database transfer.

## Consequences

Input lists do not establish retrieval readiness. Batch jobs and the server must not overlap. This record retains the former ownership boundary; it does not authorize a knowledge-service rollout.
