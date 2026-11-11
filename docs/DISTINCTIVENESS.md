# Distinctiveness audit

Scope: source/document review of the closest local portfolio mechanisms and standalone TruthGraph. This is a local comparison, not an ecosystem-wide originality claim.

**Disposition: locally distinct prototype.** The distinguishing interaction is shared underwriting capital backing multiple independent coverage windows, with share value changing through premiums and once-only payouts. Incident extraction gates an exposure-conserving risk pool rather than allocating a single award or resolving a standalone predicate.

| Closest comparator | Its judgment, participants, and state | Capability or invariant implemented here |
|---|---|---|
| specification-bid-auction | Buyer freezes one job; suppliers commit/reveal; validators assess eligibility; code chooses the lowest eligible bid and reserves one award until acceptance/expiry. | Multiple underwriters enter/exit at current capital per share; multiple policyholders pay premiums; concurrent open exposure constrains purchases and withdrawals; qualifying incidents burn capital while releasing their exact reserved coverage. No sealed bidding or price winner exists. |
| repair-refund-escrow | Buyer and named supplier track criterion-specific defects across bounded delivery/repair versions and settle fixed escrow allocations. | There is no deliverable or repair round. A common reserve covers independently timed public-service incidents; premium accrual and loss change all remaining underwriters' share values, while every policy pays at most once. |
| license-bundle-clearinghouse | Requester selects versioned licences; validators assess compatibility; every required licensor consents to exact evidence before funded permission issuance and fee credit. | No licence composition or multi-party approval is required. Pre-existing share capital backs immutable policy terms; the crucial reservation is aggregate exposure, not scoped licence fees or consent. |
| Standalone TruthGraph predicate resolver | Freezes 1-12 public claim atoms and an AND/OR/NOT/K_OF_N graph; validators classify atoms; code derives TRUE/FALSE/UNRESOLVED and stores attempt state. | This pool carries share ownership, paid premiums, collateral constraints, policy windows, claim expiry, and single-payment lifecycle. It does not merely store an incident truth value or graph outcome. |

Source anchors: `ParametricCoveragePool.deposit`, `withdraw`, `buy_policy`, `claim`, `expire_policy`, and `get_accounting`. The invariant distinguishing this pool is that aggregate OPEN coverage never exceeds shared capital and withdrawals cannot remove backing, even after other policies earn premiums or pay losses.

Evidence status: local lint/SDK validation and 86 mocked direct tests passed. The authorised StudioNet run and exact observed outcomes are recorded in [DEMO_RESULTS.md](DEMO_RESULTS.md); consult that record rather than treating the original proposed outcomes as observed. The comparison does not establish economic soundness, legal insurance, production safety, ecosystem originality, or future Portal acceptance.

## Same-week local cohort review (2026-11-09 through 2026-11-15)

Read-only portfolio Git metadata and the current README/DESIGN/DISTINCTIVENESS documents identify `calibrated-forecast-pool` (latest local commit `e6bd779`, 2026-11-11) as the other same-week project. Its mechanism is sealed probabilities plus equal stakes, followed by integer Brier-score allocation, forfeiture, dust and refund of a single rival-funded pot. It does not price underwriter shares against changing capital or lock withdrawals against concurrent independent coverage policies. This pool instead preserves `open exposure <= capital` across deposits, premium accrual, losses, partial withdrawals and policy expiry. The incident interpreter is shared infrastructure, not the claimed distinction. These participant actions and accounting transitions differ beyond domain labels.

Only this project is changed or published by this task. The scan identifies local commit dates, not actual Portal submission dates, and cannot establish all projects in a review cohort. This is a local comparison, not an ecosystem-wide originality claim or a prediction of points. The user's November 11 guidance is learned review guidance, not official scoring criteria.

The earlier demo demonstrates commit 8682be7 only. The strict revision requires full canonical agreement, rejects positive use of truncated evidence, and needs its own pushed source and new live evidence. See STRICT_DEMO_PLAN.md.
