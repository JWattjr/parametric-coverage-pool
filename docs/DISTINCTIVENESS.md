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
