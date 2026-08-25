# Architecture

## Deployment boundary

Deploy once per warranty intake package and designated claimant. Use a fresh deployment for another claimant, product reference, or intake policy.

Constructor data establishes the deployment subject and fixed role boundary. Later writes add only the bounded records permitted by the lifecycle; a completed instance cannot be reopened.

## Participants

The deployer is the issuer and names one different claimant. Only the claimant submits or supplements; only the issuer routes the screened package.

Addresses are normalized before authorization comparisons. Role checks and lifecycle gates execute before semantic assessment.

## State machine

`AWAITING_PACKAGE → READY_FOR_SCREENING → ISSUER_ROUTING → COMPLETE, with one bounded supplement loop for missing records`

The phase-like field is the primary lifecycle lock. Each write advances that path, performs a documented bounded loop, or fails with an `[EXPECTED]` user error.

## Evidence assembly

The stored product line, intake policy, purchase-record rule, condition-record rule, product reference, incident summary, two document declarations, and optional supplement. Documents are not fetched or authenticated.

Before consensus, the contract normalizes bounded text, copies required storage into plain local values, serializes a sorted JSON packet, and places it between explicit START/END delimiters. Nondeterministic callbacks do not read contract storage.

## Consensus boundary

Return a two-character lane code where each lane is PRESENT, MISSING, or CONFLICT; the contract derives READY, MISSING, or CONFLICT deterministically.

The leader callback validates exact JSON shape, field types, closed labels, masks or codes, and length bounds. A validator reruns the same semantic operation and rejects disagreement before state is committed.

## Deterministic boundary

Claimant authorization, lane-code decoding, combined readiness, one supplement, and issuer-only MANUAL_REVIEW, RETURN, or ARCHIVE routing are deterministic.

Important invariants:

- Purchase and condition rules freeze in the constructor.
- Only the designated claimant can submit or supplement the package.
- MANUAL_REVIEW routing requires both document lanes to be PRESENT.
- AI cannot decide coverage, fault, payment, repair, replacement, eligibility, or legal rights.

No method sends value, pays rewards, escrows assets, deletes external data, calls another contract, or invokes a webhook.

## Failure model

- Invalid caller input or lifecycle use raises `[EXPECTED]` and leaves state unchanged.
- Malformed or out-of-policy model output raises `[LLM_ERROR]` and cannot be stored.
- Validator disagreement cannot commit the semantic result.
- StudioNet proof reads explicitly target `LATEST_FINAL`, avoiding stale pre-final state.
