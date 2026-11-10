# Proposed StudioNet demo

**Earliest deadline: 2026-12-04 at 19:00 UTC (20:00 Africa/Lagos). Complete the proposed sequence before this deadline, or redesign the plan using newly checked incidents.**

Status: the authorised 2026-11-11 StudioNet run is recorded in [DEMO_RESULTS.md](DEMO_RESULTS.md). The original proposed sequence is preserved below. No publication or Portal submission occurred. URL checks below were anonymous HTTP reads on 2026-11-10; exact timestamps, byte sizes, field presence, and SHA-256 values are in [incident-url-checks.json](../verification/incident-url-checks.json).

## Permanent incident evidence

Use these incident-specific JSON representations on GitHub's real public status page, rather than the rolling incident feed. Each URL identifies one completed past incident. All four required literal fields (name, impact, started_at, resolved_at) were verified to occur within its retained prefix. Recorded digests will drift because `page.updated_at` changes even when incident facts do not. Compare the incident identifier/title, severity, `started_at`, and `resolved_at` before a future demo instead of requiring digest equality. Never substitute incident `updated_at`, creation/monitoring/display times, or page-level timestamps for the incident endpoints. Digests remain evidence records of each fetch, not a cross-fetch agreement gate.

| Service fixture | Specific incident URL | Anonymous HTTP | Original bytes | Kept bytes | Recorded impact |
|---|---|---:|---:|---:|---|
| actions_compact | https://www.githubstatus.com/api/v2/incidents/h02n9572mx9y.json | 200 | 2,965 | 2,965 | major |
| actions_truncated | https://www.githubstatus.com/api/v2/incidents/xxb3l2bm76dr.json | 200 | 6,062 | 5,000 | major |
| minor_incident | https://www.githubstatus.com/api/v2/incidents/c9px7cw2ghrs.json | 200 | 5,007 | 5,000 | minor |

Their normal incident pages are obtained by replacing `/api/v2/incidents/ID.json` with `/incidents/ID`; those human-page URLs are navigation aids only, not additional checked or proposed contract sources. The frozen sources above are the anonymously checked JSON endpoints. An additional older GraphQL incident was inspected during source selection (also retained in the check record), but is not part of this proposed deployment.

## Constructor and timing

Use `historical_demo_mode=true`, a 30-day claim period (2,592,000 seconds), premium rate 1,000 basis points, and the three services above, each with exactly one frozen URL. Freeze trigger `major_30`: severity MAJOR, minimum duration 30 minutes. Historical mode is a visible, immutable synthetic replay facility; normal mode remains future-only. These old windows cannot be purchased after their claim deadlines, even in demo mode.

The compact major incident occurred on 2026-11-04, 17:40:33.662Z–18:16:08.361Z. The truncated major incident occurred on 2026-11-09, 10:00:35.209Z–11:50:35.774Z. The minor incident occurred on 2026-11-09, 05:59:07.841Z–09:09:56.174Z. These are source-recorded instants, not a claim that validators have already agreed.

| Policy | Service | UTC window | Coverage | Expected result | Claim deadline |
|---|---|---|---:|---|---|
| compact | actions_compact | Nov 4 17:00–19:00, 2026 | 100 | QUALIFYING, once | Dec 4 19:00, 2026 |
| truncated | actions_truncated | Nov 9 00:00–Nov 10 00:00, 2026 | 100 | QUALIFYING from kept evidence | Dec 10 00:00, 2026 |
| minor | minor_incident | Nov 9 00:00–Nov 10 00:00, 2026 | 100 | NOT_QUALIFYING: literal minor severity | Dec 10 00:00, 2026 |
| outside | actions_compact | Nov 5 00:00–Nov 6 00:00, 2026 | 100 | NOT_QUALIFYING: no overlap | Dec 6 00:00, 2026 |

Run the complete proposed sequence before the earliest deadline, or redesign the plan against newly checked completed incidents. Do not weaken the claim-period bound, edit evidence, fabricate severity, or change frozen URLs to rescue an expired plan.

## Proposed sequence and evidence

1. If separately authorised later, deploy with the pinned runner and the separate genlayer-py 0.18.0 runtime environment. Record exact constructor JSON, source commit/blob, network chain ID, and source readback match. This build does not authorise that deployment.
2. Underwriter declares 1,000 synthetic units, receiving 1,000 shares. A policyholder buys each of the four policies for 100 coverage and 10 premium units. Read back all views: capital 1,040, exposure 400, supply 1,000, premiums 40.
3. Attempt to withdraw all shares while exposure is open, and attempt an additional 2,000-unit policy: both should revert without changing accounting.
4. Claim `compact` and `truncated` only while eligible. Check exact source status/count/hash/quote records and validator-derived facts. The proposed evidence supports two 100-unit payouts. Claim `minor` and `outside`: neither should pay. Replayed claims on PAID/DENIED policies should revert.
5. If any judgment is UNCERTAIN or consensus does not finalise successfully, record the outcome and read back unchanged balances/exposure. Do not count the expected result as observed. UNCERTAIN policies remain OPEN for holder retry through deadline; anyone can expire them strictly afterwards. The direct suite supplies deterministic mocked expiry and uncertain-retry demonstrations without waiting a month on StudioNet.
6. If all four expected terminal outcomes occur, read back capital 840, exposure 0, payouts 200, premiums 40, deposits 1,000. The underwriter burns all 1,000 shares for 840 units. Verify `1000 + 40 = 0 + 200 + 840` and holder payout credits total 200.
7. Any future release evidence must separate finality from execution outcome, distinguish expected rollbacks from operator errors, and include a direct Explorer CONTRACT URL for the actual deployed address on the verified network as its own evidence entry. Verify it opens the correct contract; use Portal type `GenLayer Explorer Contract` if supported. Transaction/source/repository URLs are additional evidence. The actual address and browser-verified contract evidence entry are recorded in DEMO_RESULTS.md; no Portal submission exists.

## Limits

This is historical synthetic replay, not prospective underwriting or evidence of real losses. Public page availability here is outside the validator environment and does not promise GenVM fetch success. Status JSON may change, independently fetched bytes may differ, and LLM field extraction may remain uncertain. Never report this plan as a passed live demo. No private keys or wallet helpers are needed for the completed URL checks.
