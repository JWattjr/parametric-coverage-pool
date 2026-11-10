# Design

## Boundary

Policyholder action -> frozen service URLs -> independently fetched kept text -> literal incident extraction -> normalised incident-fact agreement -> deterministic coverage payout or denial. Frontends may display policy/account views and preview evidence, but have no settlement authority. External publishers own the raw text and can edit it. GenLayer owns only incident interpretation and its consensus-bound state transition. Pool arithmetic, ownership checks, deadlines, and exposure release are deterministic.

## Frozen configuration and actors

The owner is the constructor sender. Services have exactly `id`, `name`, and `urls`; triggers have exactly `id`, `minimum_severity`, and `minimum_minutes`. IDs are unique lowercase identifiers. The fixed ordered severity labels are MINOR < MAJOR < CRITICAL; case-insensitive literal labels are accepted in evidence, and unknown publisher-specific labels are UNCERTAIN rather than inferred. Premium rate is 1-10,000 basis points, claim period 1 second through 30 days, and trigger duration 1-43,200 minutes. There are no owner-only setters, mint-to-another-account methods, or owner overrides.

Underwriters declare synthetic deposits for their own address. Holders pay synthetic premiums in the same explicit ledger sense as the auction's seeded budget. The prototype does not debit an external wallet or enforce a scarce spendable currency. It records cumulative contributions and per-address shares, premiums, payouts, and withdrawals. Shares cannot be transferred. Withdrawals and claims always use the authenticated transaction sender.

## Accounting and integer rounding

Let C be current pool capital, E open exposure, S total shares, d deposit units, s caller shares to burn, q coverage, and r frozen basis points.

| Action | Arithmetic | Rounding and effect |
|---|---|---|
| First deposit | mint d shares | 1 unit = 1 share at bootstrap |
| Later deposit | mint floor(d*S/C) | Caller receives no fractional share; zero-share mint reverts |
| Premium | ceil(q*r/10000) = (q*r+9999)//10000 | Caller pays at least the exact fractional premium |
| Withdraw | return floor(s*C/S) | Caller receives no fractional unit; burn exactly s owned shares |
| Payout | C -= q; E -= q | Exact policy coverage, once |
| Denial / expiry | E -= q | Capital unchanged; premium retained |

Purchase requires E+q <= C before adding its premium, conservatively avoiding self-collateralisation by that premium. Withdrawal requires C-returned_units >= E. On payout, both C and E decrease by q, so the collateral margin is preserved. A denial or expiry releases exposure exactly once. Every successful mutation preserves:

`deposited_units + premiums_paid_units = pool_capital_units + payouts_made_units + withdrawn_units`.

`get_accounting` exposes every term, free capital, total shares, and independent `conserved` and `collateralised` flags. Tests check these after each scenario and after rejected actions. Lifetime contributions (deposits plus premiums) and outstanding shares are each capped at 10^12. This bounds u256 arithmetic even after losses change share value. A defensive zero-capital/nonzero-share state requires old holders to burn worthless shares before recapitalisation.

## Time and policy lifecycle

The auction's `_time`, `_time_text`, and `_now` patterns are copied: explicit ISO timezone offsets, UTC conversion, canonical second-resolution policy deadlines, and time from `gl.message_raw['datetime']`. Windows must be ordered and at most 30 days. The default `historical_demo_mode=false` additionally requires purchase strictly before the window starts. The optional constructor-frozen `historical_demo_mode=true` permits replay of published past incidents, but only while that policy's claim period is still open. The flag is exposed in `get_pool` and bound into each input snapshot. This mode is explicitly synthetic: it permits buying after an incident is known and is unsuitable for funded coverage. This is a deliberate product choice made after the user asked the agent to choose how to reconcile safe default purchases with permanent historical demo evidence. Incident timestamps retain their verbatim source spelling, including fractions, while consensus also normalises UTC instants. Duration is calculated in integer microseconds, including exact threshold edges.

Coverage is the half-open interval [start,end); a completed incident overlaps when incident_start < policy_end and incident_end > policy_start. Claims open strictly after window end and are allowed at the exact deadline (end plus frozen claim period). Expiry opens strictly after that deadline. This avoids a terminal early denial while the window could still contain a subsequent incident. Paid, denied, and expired policies cannot be claimed again. Policy IDs are never reused.

## Approved deviation: bounded source truncation

The auction treats oversized bodies as unavailable. The user's explicit override replaces that behavior with the research-novelty-bounty source-record pattern, extended as follows:

| Status | Constraints |
|---|---|
| fetched | HTTP 200, nonempty usable UTF-8, original and kept byte counts equal, 1 through 5,000 bytes |
| truncated | HTTP 200, original count > 5,000; keep the first 5,000 bytes, removing only an incomplete final UTF-8 character; available=true |
| unavailable | Failed request, non-200, empty/whitespace bounded body, invalid interior UTF-8, or non-byte response; available=false, zero kept bytes and empty kept text |

Each source contains the frozen URL, status, available flag, original `byte_count`, `kept_byte_count`, `content_digest`, and kept `text`. The content digest is SHA-256 of kept UTF-8 bytes, prefixed `sha256:`. Incomplete final codepoints remove at most three bytes; invalid interior sequences are not silently deleted. A valid oversized whitespace prefix is still recorded as truncated/available; it supplies no incident facts. The body-size cap limits retained/prompt/state bytes; the web API still receives the full response before slicing and is not a streaming download limit.

The judgment sees only kept text. Every determinate field has a bounded source URL and exact quoted substring in available kept text, and that substring must contain the literal stated field value (case-insensitively for severity only). The start quote must contain `start` or `began`, and the end quote must contain `resolved`, case-insensitively; missing markers produce UNCERTAIN. Start is when the incident began (`started_at`); end is when it was resolved (`resolved_at`). `created_at`, `updated_at`, `monitoring_at`, `display_at`, and page-level timestamps must never supply either endpoint. This supports raw JSON/HTML sources without fabricating rendered lines. Missing or nonverbatim support, including support only beyond the cut point, produces the canonical UNCERTAIN result. Source text and quotes are never interpreted as instructions. Full semantic connection between an incident and its quotes remains the validators' independent interpretation; substring membership alone is not semantic proof.

## Consensus and evidence binding

The auction's canonical JSON, SHA-256 snapshot binding, exact result schemas, `gl.vm.run_nondet_unsafe`, independent leader-function rerun, classified leader-error handling, and comparison-vector patterns are preserved. Storage uses class annotations, u256, TreeMap[str,str] for canonical JSON, and DynArray[str] for bounded indexes, as in the auction.

The input digest binds pool ID, contract address, the exact OPEN policy, its service/URLs, trigger, premium rate, and claim period. The evidence digest binds that input digest and all ordered source records including kept text. The result digest binds input and evidence digests. Candidate validation checks exact schemas, source ordering, legal status/count combinations, encoded text lengths, kept-text hashes, canonical judgment, and all digest bindings. Each validator independently refetches and re-derives truncation from its own response, then runs `_valid_candidate` on its own result as well as validating the leader candidate. Every candidate must have valid source metadata, internally consistent digests, and quotes present verbatim in that candidate's own kept text. Evidence records are not compared across nodes.

Validators agree on facts, not bytes. `_status_vector` contains only verdict, incident identifier/title normalised by collapsing whitespace and lowercasing, severity uppercased, and start/end converted to UTC and truncated to the whole minute. Sources, all digests, and quotes are excluded from this comparison. The accepted leader's sources, digests, and exact quotes remain the stored evidence record; validator evidence does not overwrite it. Page-level `updated_at` can change between fetches without changing an incident. Publishers may also show `started_at` and a nearby `created_at` separated by milliseconds: creation time remains forbidden, while minute buckets avoid disagreement over subminute variations in valid incident timestamps. This is bucket equality, not a sliding 60-second tolerance: timestamps across a minute boundary disagree. Duration and window overlap still use exact extracted timestamps before comparison, so a different derived verdict always disagrees even within identical minute buckets. Different severity also disagrees even if both severities would qualify. Each node must independently find support in its own fetched text; agreeing on a vector does not excuse missing quotes or invalid source records.

Missing any frozen source forces UNCERTAIN, even if another source is available. A successful UNCERTAIN attempt updates only its assessment record; policy status, exposure, account balances, and pool capital remain unchanged. Assessments overwrite the previous attempt so retries cannot grow an unbounded history. Malformed model schemas revert as classified LLM errors, matching the auction; no malformed result creates a payout.

## Bounds and limitations

8 services, 3 URLs per service, 4 triggers, 64 lifetime participating accounts, 128 lifetime policies, and 8 lifetime policies per holder cap indexes and persistent state. Each policy holds at most one latest assessment. IDs: 32 characters; pool ID: 64; service name: 100; URLs: 500; configuration JSON: 16,000; fetched kept text: 5,000 bytes/source; model JSON text: 8,000; incident title/id: 200; severity/time fields: 64 each; quote text: 1,200 each, exactly four determinate field quotes. Historical records count toward limits even after closing. Limits are intentionally finite rather than reusable production capacity.

The owner freezes the authoritative URLs, but this is not publisher signature or DNS/redirect verification. The fixed severity taxonomy and literal ISO-time requirement can conservatively leave real incidents uncertain. No real custody, reserve token, share transfer, incident feed rotation, cancellation/refund, appeals, production premiums, external liquidity, or forecast contract is included. The separately authorised StudioNet demo is recorded in DEMO_RESULTS.md.
