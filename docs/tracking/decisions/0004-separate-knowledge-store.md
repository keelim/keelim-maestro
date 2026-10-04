# Separate operator knowledge store

## Context

Collecting product source, secrets, and caches alongside operational documents would blur access and ownership. Local PGLite also has exclusive-access constraints.

## Decision and alternatives

Use a separate operator store with explicitly allowed document inputs. Avoid indiscriminate child-source collection. Confirm a trusted destination before an external database transfer.

## Consequences

Input lists do not establish retrieval readiness. Batch jobs and the server must not overlap. Root automation does not install, ingest, or transfer GBrain data automatically.
