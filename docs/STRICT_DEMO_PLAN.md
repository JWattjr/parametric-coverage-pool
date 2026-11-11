# Strict-revision StudioNet demo plan

**Earliest deadline: 2026-12-04 at 19:00 UTC (20:00 Africa/Lagos).** Use fresh incident checks and finish before this deadline. Historical replay is enabled only for this synthetic demo.

The original [demo](DEMO_RESULTS.md) evidenced commit `8682be7`; its truncated-source payout and fact-only consensus do not evidence the strict revision. Deploy the strict source only after lint, all direct tests, a local commit, public push, and anonymous source-byte verification. Keep the pinned runner and use the separate genlayer-py 0.18.0 runtime client. No Portal submission is authorised.

## Frozen evidence and policies

| Service | Official incident-specific source | Measured bytes at source selection | Policy UTC interval | Expected strict result |
|---|---|---:|---|---|
| actions_compact | https://www.githubstatus.com/api/v2/incidents/h02n9572mx9y.json | 2,965 | Nov 4 17:00–19:00, 2026 | QUALIFYING; major severity and more than 30 minutes |
| actions_truncated | https://www.githubstatus.com/api/v2/incidents/xxb3l2bm76dr.json | 6,062 | Nov 9 00:00–Nov 10 00:00, 2026 | UNCERTAIN; retained prefix cannot qualify |
| minor_compact | https://www.githubstatus.com/api/v2/incidents/pyynvrm1vskw.json | 4,205 | Nov 8 00:00–Nov 9 00:00, 2026 | NOT_QUALIFYING; literal minor severity |
| outside (same actions_compact service) | same frozen compact incident URL | 2,965 | Nov 5 00:00–Nov 6 00:00, 2026 | NOT_QUALIFYING; resolved before policy window |

Recheck anonymous HTTP 200, complete body bytes and required incident fields immediately before deployment. The new minor source states incident `pyynvrm1vskw`, "Increase in timeouts for some unauthenticated users", minor, started_at `2026-11-08T10:36:05.474Z`, resolved_at `2026-11-08T12:32:35.611Z`. These are source-selection facts, not an already observed GenLayer judgment. Each policy has 100 coverage and pays 10 premium units. Freeze rate 1,000 basis points, trigger MAJOR/30 minutes, claim period 30 days, and historical_demo_mode=true.

## Sequence and invariants

1. Deploy the pushed commit, require finalized deployment with successful execution, verify network chain 61999 and byte-identical source readback, and inspect the immutable constructor values.
2. Deposit 1,000 synthetic units for 1,000 shares. Buy all four policies. Capital 1,040, exposure 400, premiums 40.
3. Attempt withdrawing all 1,000 shares and buying 2,000 additional coverage. Both must finalize as explicitly labelled expected rollbacks and leave accounting unchanged.
4. Claim the complete major incident: it should pay 100 once. Claim the truncated incident: it must return UNCERTAIN, preserve the entire accounting snapshot and OPEN policy, and retain its 100-unit exposure. This UNCERTAIN result is the planned fail-closed demonstration, not an unexpected judgment. The model must not be called on incomplete evidence.
5. Resolve the complete minor and outside-window incidents without paying. Replay a paid claim and a denied claim; both must roll back. If any judgment differs from the expected result, stop and report it rather than retrying blindly.
6. Before withdrawal, capital is 940 and exposure 100. Burn 894 shares: floor(894*940/1000)=840 units withdrawn. Capital and open exposure both become 100, with 106 shares remaining. Attempt burning those remaining 106 shares: it must roll back because they back the still-open uncertain policy.
7. Final conservation is `1,000 deposits + 40 premiums = 100 payout + 840 withdrawals + 100 capital`. Free capital is zero. The holder's uncertain policy remains OPEN until its frozen deadline; anyone can expire it strictly afterwards. The demo does not wait a month or manufacture an early expiry.

Expected transaction total: 16, consisting of 11 successful executions and five expected rollbacks. Record acceptance observations, finality, execution, votes, exact method arguments, and latest-final readbacks separately. Independently recheck receipts and every public view. Include a browser-verified direct Explorer contract URL as its own `GenLayer Explorer Contract` evidence entry, plus public repository, deployed-commit source, manifest, and key transactions.

## Evidence limits

Strict consensus compares the full result, including text, metadata, hashes and quotes. These incident-specific API URLs are not cryptographically immutable; page metadata can drift, and strict consensus may fail closed. Do not weaken comparison or claim agreement that did not occur. Synthetic units are not GEN, custody, real premiums, or a legal insurance promise. The initial historical release remains published separately and must not be represented as evidence for this changed source.
