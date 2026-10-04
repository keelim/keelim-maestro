# Access and protected assets

Protected assets include child working trees and local commits, private repository content, provider credentials, operational data, and knowledge stores. The root has no product-user account or login service. Agents and helpers act within the operator's local permissions; they do not replace a connected provider's authentication or authorization.

## Permissions

| Subject and action | Required condition | Prohibited action |
| --- | --- | --- |
| Agent reading or editing locally | Current request includes the path and its owner | Overwriting unrelated work or editing an unrelated sibling |
| Repository update or pointer change | Request covers the change and current state has been inspected | Force-pushing, resetting, or rewriting history to eliminate conflicts |
| External message, publication, deployment, or credential change | User explicitly requests that external action | Treating documentation or research as authorization to publish |
| Local runtime control | Necessary target and impact are identified | Starting, stopping, or deleting runtime state during a status-only request |
| Knowledge transfer to an external database | User confirms a trusted destination | Assuming any reachable database is the intended destination |

## Authentication and credential lifecycle

Git, package registries, and MCP providers validate their own credentials. Missing, expired, or rejected credentials leave the affected verification unconfirmed. Do not switch accounts, bypass controls, or substitute simulation results for successful access.

Keep keys, tokens, and secrets embedded in database URLs out of source, documentation, reports, and command output. Supply package credentials through the operator's environment, such as `NODE_AUTH_TOKEN`. The root does not issue, renew, or revoke credentials. Creation, permission changes, rotation, and revocation occur through the owning service within the user's request. Report confirmed exposure immediately without reproducing the secret. No common expiration or automatic rotation policy is defined.

## Local connections and data

Codex app-server defaults to loopback. Do not omit the helper's required authentication option for an external `ws://` listener. That check does not establish the safety of every transport; verify actual access control before introducing a public listener or another transport.

Managed MCP configuration routes through agentgateway. Check initialization, tool enumeration, and an authorized read-only method separately. Report the actual boundary where access failed; do not infer the internal wiring of host-provided tools.

Knowledge input excludes credentials, caches, generated output, broad child source trees, archived `toto`, and remote-less `quant`. PGLite requires exclusive access: stop the matching server before batch import, sync, stats, or other CLI work, then run sequentially.

## Evidence and incident reporting

There is no common audit server. Record changed owners and paths, performed checks and outcomes, and unverified scope. Cross-repository delivery records commits, order, and rollback instructions. Report authentication failure, secret exposure, unauthorized changes, and data loss without recording secret values.
