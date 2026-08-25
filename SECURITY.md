# Security

## Scope

This repository contains one bounded Intelligent Contract, direct tests, a five-validator GLSim test, and an opt-in StudioNet smoke test. It has no frontend, backend, database, token, payout, proxy upgrade, or repository secret.

## Trust model

Untrusted evidence is delimited as data, model outputs use closed schemas, and validator replay must agree before semantic state is stored.

The deployer is the issuer and names one different claimant. Only the claimant submits or supplements; only the issuer routes the screened package.

## Implemented controls

- Concrete immutable GenVM runner hash; no floating runner dependency.
- Address normalization, explicit role separation, collection caps, one-time actions, and lifecycle locks.
- Bounded text plus strict `[EXPECTED]` and `[LLM_ERROR]` failure classes.
- Sorted, delimited evidence packets and independent validator replay.
- Storage is copied before nondeterministic callbacks; static audit requires zero callback reads from `self`.
- No cross-contract calls, fund custody, transfer, automated purchase, external deletion, or webhook.
- `.env`, caches, artifacts, wallet files, and local secrets are ignored. Live wallets are encrypted outside the workspace.

## Contract-specific safety properties

- Purchase and condition rules freeze in the constructor.
- Only the designated claimant can submit or supplement the package.
- MANUAL_REVIEW routing requires both document lanes to be PRESENT.
- AI cannot decide coverage, fault, payment, repair, replacement, eligibility, or legal rights.

## Residual risks

- The contract records declarations and does not authenticate receipts, images, serials, ownership, or product condition.
- READY means ready for a human desk, not covered, valid, payable, repairable, or replaceable.
- This intake workflow is not legal advice and does not alter warranty rights.

Do not use this contract to make legal, medical, financial, employment, admission, credit, or physical-safety decisions beyond the explicit low-risk policy in its source. A new use case requires a fresh deployment and independent domain review.

## Reporting

Report vulnerabilities privately to the repository owner with the contract name, affected method, reproduction, expected invariant, and impact. Never include private keys, wallet passwords, or personal data.
