# Warranty Ready

Screens a designated claimant's purchase and condition document declarations for intake readiness, then leaves routing to the issuer without deciding coverage or remedy.

## Why it is an Intelligent Contract

Return a two-character lane code where each lane is PRESENT, MISSING, or CONFLICT; the contract derives READY, MISSING, or CONFLICT deterministically. GenLayer validators independently replay that semantic judgment before it becomes shared state. Claimant authorization, lane-code decoding, combined readiness, one supplement, and issuer-only MANUAL_REVIEW, RETURN, or ARCHIVE routing are deterministic.

## Reusable deployment model

Deploy once per warranty intake package and designated claimant. Use a fresh deployment for another claimant, product reference, or intake policy.

A completed deployment is an auditable record and is not reset or silently repurposed. Reuse means deploying the same reviewed source with new constructor data.

## Roles and workflow

The deployer is the issuer and names one different claimant. Only the claimant submits or supplements; only the issuer routes the screened package.

State path: `AWAITING_PACKAGE → READY_FOR_SCREENING → ISSUER_ROUTING → COMPLETE, with one bounded supplement loop for missing records`

## Evidence boundary

The stored product line, intake policy, purchase-record rule, condition-record rule, product reference, incident summary, two document declarations, and optional supplement. Documents are not fetched or authenticated.

## Core invariants

- Purchase and condition rules freeze in the constructor.
- Only the designated claimant can submit or supplement the package.
- MANUAL_REVIEW routing requires both document lanes to be PRESENT.
- AI cannot decide coverage, fault, payment, repair, replacement, eligibility, or legal rights.

## Public interface

Write methods: `route_to_desk, screen_document_lanes, submit_intake_package, supplement_records`

View methods: `get_document_rules, get_policy, get_state`

`get_policy` exposes the machine-readable operating boundary and confirms that this contract never custodies funds.

## Verification

Pinned GenVM runner: `py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6`

```powershell
python -m pip install -r requirements.txt
genvm-lint check contracts/warranty_ready.py
genvm-lint typecheck contracts/warranty_ready.py
pytest tests/direct -q
python tests/run_glsim.py --port 4000 --validators 5 --no-browser
gltest tests/integration/test_glsim_consensus.py --network localnet -q
```

The StudioNet smoke test is opt-in and uses three disposable Mimi-only accounts protected outside the workspace. It asserts finalized successful execution and reads committed state with `LATEST_FINAL`.

## Final StudioNet proof

- Contract: https://explorer-studio.genlayer.com/address/0x75e2B891dc2061A06457C6fcf66409A5cc026291
- Studio import: https://studio.genlayer.com/?import-contract=0x75e2B891dc2061A06457C6fcf66409A5cc026291
- Deployment transaction: https://explorer-studio.genlayer.com/tx/0xa758684f639dcda75eeacdfc05fb08160d30233cf2fb96882a95bac152524ece
- Intelligent transaction: https://explorer-studio.genlayer.com/tx/0xc27018ff904b92c77388d5c36bdc5b39c95a4716960f17b5cd619118f7dbb2df
- Observed committed state: `{"condition_state":"PRESENT","purchase_state":"PRESENT","readiness":"READY"}`
- Audited source SHA-256: `f9e4fb59571f70d12e938988f258ce0232c8aae369b3ad573547c6bccbe1b0d6`

## Limitations

- The contract records declarations and does not authenticate receipts, images, serials, ownership, or product condition.
- READY means ready for a human desk, not covered, valid, payable, repairable, or replaceable.
- This intake workflow is not legal advice and does not alter warranty rights.

## Repository map

- `contracts/warranty_ready.py` — Intelligent Contract source
- `tests/direct` — hardened leader/validator and lifecycle tests
- `tests/integration/test_glsim_consensus.py` — five-validator simulator flow
- `tests/integration/test_studionet_smoke.py` — live opt-in proof
- `deployments/studionet.json` — source-bound public deployment evidence
- `ARCHITECTURE.md`, `SOURCE_POLICY.md`, `SECURITY.md`, `AUDIT.md` — reviewer material

License: MIT.
