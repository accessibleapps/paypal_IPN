# PayPal IPN Python 3 compatibility draft

## Goal

Preserve QActivate's existing PayPal callback contract while repairing the Python 3 mapping/text/response incompatibilities in its existing dependency. No purchase redesign, provider calls, release or publication.

## State

Owner identity verified: origin git@github.com:accessibleapps/paypal_IPN.git, original clean master e1d96346dc5dc3208bd991eec347aa9382357498, tracking 0/0 without refresh. Isolated worktree/branch codex/paypal-ipn-python3; original master preserved. No repository-specific AGENTS/CLAUDE/agent-notes found. Current Accessible Apps topology lacks this node; parent explicitly authorized this isolated owner draft despite that omission. Manifest dependency in QActivate pyproject.toml:16 and hash-locked paypal-ipn 0.16 archive uv.lock:683-689 prove consumer identity. Public archive hash matches lock and installed helper bytes.

## Decisions

Keep endpoints, verify-before-decode, UTF-8 form encoding, response strictness, mapping order, list normalization and transport-error propagation intact. Fix only items(), Python 2/3 text type selection and byte VERIFIED comparison. Retain Python 2 compatibility in production library syntax; tests target candidate Python 3. No setup version bump/release implicit. Parent owns shared-worker coordination/publication approval.

## Next step

Owner TDD complete: 10 failed before repair (iteritems), 10 passed afterward on Python3.12.5. Only library changes: mapping items(), Python2/3 text alias for UTF8 encoding, byte VERIFIED comparison. Authored tests cover dict/OrderedDict, live/sandbox endpoint selection with fake HTTP, Unicode/bytes payloads, exact response rejection, list normalization and transport exceptions; sockets blocked. Code commit 778ccbfcc60d34443d2d3d9e83ae6f57bac662a6 is unpublished. QActivate real helper/sale/redelivery and Stripe transport consumer fixtures: 12 passed with explicit test-only source overlay, no app implementation or user venv change. Additional old-host Python2 in-memory execution of this public candidate source passed VERIFIED/UTF8/list normalization/rejection checks using only invented inputs, fake HTTP and blocked sockets; no production app import or files written. This is not a Python2 full-suite run or actual provider verification. Task-root qactivate-paypal-pin.patch passes git apply --check but remains unapplied pending owner publication and resolver-generated lock update. No push/PR/release/merge.
