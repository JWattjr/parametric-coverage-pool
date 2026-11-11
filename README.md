# Parametric Coverage Pool

[Public GitHub repository](https://github.com/JWattjr/parametric-coverage-pool).

Current revision: strict canonical agreement across every stored result field; any truncated source yields UNCERTAIN. A fresh demo must evidence this changed source. The earlier fact-only/truncation-positive demo is historical and does not prove this revision.

`ParametricCoveragePool` coordinates underwriters and policyholders in a bounded synthetic-unit pool. Frozen public status-page URLs supply incident evidence. Validators independently fetch the same sources and extract literal incident facts; deterministic code checks severity, duration, overlap, collateral, shares, and settlement.

This is an independent demo-unit ledger. Deposits and premiums are declared synthetic contributions, not assets received from a wallet. Withdrawals and payouts are accounting entries, not transfers of native value or tokens.

## Toolchain

The runner header is copied verbatim from specification-bid-auction:
`py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6`.
Use the existing portfolio `.venv` with Python 3.14.2, genvm-linter 0.11.1rc2, genlayer-test 0.30.0rc2, genlayer-py 0.19.0rc2, and pytest 9.1.1. No dependency upgrade is needed. Any future StudioNet runtime client must use the separate genlayer-py 0.18.0 environment; no runtime call is made here.

Run from the project root, in this order. Pin the linter to the existing cached GenVM bundle so it does not perform a latest-release lookup:

```powershell
$env:GENVM_VERSION = "v0.6.0-rc5"
..\.venv\Scripts\python.exe -B -c "from genvm_linter.cli import cli; cli()" check contracts/parametric_coverage_pool.py --json
..\.venv\Scripts\python.exe -B -m pytest -v -o addopts= -p no:cacheprovider --tb=short --junitxml=verification/pytest.xml
```

The Windows/legacy-SDK fixture is copied unchanged from the auction. Tests use its `v0.6.0-rc5` SDK selection, mocked web and model responses, and explicit `run_validator()` calls. These exercise the stored validator callback independently; they do not establish live network consensus.

## Lifecycle

1. The constructor freezes services, HTTPS source URLs, trigger thresholds, premium basis points, and claim period, plus an immutable historical demo flag (default false). The owner has no subsequent configuration or withdrawal privilege.
2. Anyone may declare a synthetic deposit and receive pool shares. Existing shares capture premiums and losses. A caller may withdraw only their own shares, and only without reducing capital below open exposure.
3. A holder buys a uniquely identified policy before its window starts in normal mode. Historical demo mode also permits past windows whose claim deadline has not passed. Exposure is reserved against capital before counting that purchase's premium. Premiums round upward; deposits and withdrawals round downward.
4. After the window ends, and through the inclusive claim deadline, only its holder may claim. A qualifying claim pays the coverage once. A determinate nonqualifying claim closes as DENIED. UNCERTAIN or a failed source leaves the policy OPEN and every balance unchanged, retaining its latest assessment for inspection and allowing retry.
5. Anyone may expire an OPEN policy strictly after its claim deadline, releasing exposure without refunding the premium.

## Historical demo mode

`historical_demo_mode` exists only to replay past incidents in the demo. It is fixed at deployment and visible in `get_pool`. It must be `false` for any real use.

## API

Constructor: `pool_id`, `services_json`, `triggers_json`, `premium_bps`, `claim_period_seconds`, optional `historical_demo_mode=false`. See [constructor.json](examples/constructor.json).

Writes: `deposit`, `withdraw`, `buy_policy`, `claim`, `expire_policy`.

Views: `get_pool`, `get_policy`, `get_account`, `get_accounting`, `get_assessment`, `get_sources`. [ABI](contracts/abi.json) is extracted by the installed linter.

## Documentation and limitations

- [Design and rounding rules](docs/DESIGN.md)
- [Tests and invariant mapping](docs/TEST_MATRIX.md)
- [Local distinctiveness comparison](docs/DISTINCTIVENESS.md)
- [Historical pre-strict demo plan](docs/DEMO_PLAN.md)
- [Strict fresh-demo plan](docs/STRICT_DEMO_PLAN.md)
- [Historical pre-strict StudioNet demo results](docs/DEMO_RESULTS.md)
- [Exact verification transcript](verification/checks.txt)
- [Per-case test results](verification/test-results.md)

The authorised StudioNet demonstration is recorded in [DEMO_RESULTS.md](docs/DEMO_RESULTS.md). The repository is public; no Portal submission occurred. Public source URLs were rechecked anonymously for that run. Stable incident-specific URLs are not immutable publisher commitments; validators require equality of complete canonical results, including response evidence bytes. The fixed severity taxonomy deliberately treats other labels as UNCERTAIN. No legal coverage, real insurance, payment custody, publisher authentication, or production underwriting is implemented.

Current strict local result: **91 passed in 12.25s**; lint 3/3 and SDK validation passed (11 methods: 6 views, 5 writes; 6 constructor parameters). ABI extraction passed. The I200 informational notice reports a newer runner in the cached bundle; the auction runner remains pinned. An initial unpinned release lookup was interrupted before testing; its transcript is retained separately.
