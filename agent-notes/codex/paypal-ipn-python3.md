# PayPal IPN Python 3 compatibility draft

## Goal

Preserve QActivate's existing PayPal callback contract while repairing the Python 3 mapping/text/response incompatibilities in its existing dependency. No purchase redesign, provider calls, release or publication.

## State

Owner identity verified: origin git@github.com:accessibleapps/paypal_IPN.git, original clean master e1d96346dc5dc3208bd991eec347aa9382357498, tracking 0/0 without refresh. Isolated worktree/branch codex/paypal-ipn-python3; original master preserved. No repository-specific AGENTS/CLAUDE/agent-notes found. Current Accessible Apps topology lacks this node; parent explicitly authorized this isolated owner draft despite that omission. Manifest dependency in QActivate pyproject.toml:16 and hash-locked paypal-ipn 0.16 archive uv.lock:683-689 prove consumer identity. Public archive hash matches lock and installed helper bytes.

## Decisions

Keep endpoints, verify-before-decode, UTF-8 form encoding, response strictness, mapping order, list normalization and transport-error propagation intact. Fix only items(), Python 2/3 text type selection and byte VERIFIED comparison. Retain Python 2 compatibility in production library syntax; tests target candidate Python 3. No setup version bump/release implicit. Parent owns shared-worker coordination/publication approval.

## Next step

Owner TDD complete: 10 failed before repair (iteritems), 10 passed afterward on Python3.12.5. Only library changes: mapping items(), Python2/3 text alias for UTF8 encoding, byte VERIFIED comparison. Authored tests cover dict/OrderedDict, live/sandbox endpoint selection with fake HTTP, Unicode/bytes payloads, exact response rejection, list normalization and transport exceptions; sockets blocked. Commit owner slice, then test QActivate with exact revision through explicit test-only source overlay. Prepare immutable publication ref/consumer pin without pushing, releasing or editing user's master/venv. Python2 execution not available/claimed; library syntax remains compatible.
