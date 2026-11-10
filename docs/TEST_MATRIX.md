# Test matrix

Direct-mode tests use mocked web and model responses and explicitly invoke captured validator callbacks. They exercise independent fetch/derivation but do not establish network consensus. The Windows compatibility fixture is copied unchanged from the auction.

All financial scenarios assert the exposed conservation identity and collateral bound; rejected actions also check unchanged state where relevant. Per-parameter PASS/FAIL results and exact output are in [test-results.md](../verification/test-results.md) and [checks.txt](../verification/checks.txt).

| Invariant or behavior | Test |
|---|---|
| Qualifying payout and replayed claim reverts | `test_qualifying_payout_and_replayed_claim_reverts` |
| Nonqualifying facts cannot pay even if model says qualifying | `test_nonqualifying_facts_cannot_pay_even_if_model_says_qualifying` |
| Major selected among minor incidents | `test_major_selected_among_minor_incidents` |
| Uncertain leaves policy and all balances unchanged then retry pays | `test_uncertain_leaves_policy_and_all_balances_unchanged_then_retry_pays` |
| Failed fetch keeps policy open and records unavailability | `test_failed_fetch_keeps_policy_open_and_records_unavailability` |
| Two sources one unavailable | `test_two_sources_one_unavailable` |
| Overexposure purchase reverts without premium movement | `test_overexposure_purchase_reverts_without_premium_movement` |
| Undercollateralising withdrawal and other account shares revert | `test_undercollateralising_withdrawal_and_other_account_shares_revert` |
| Share math deposit premium payout withdraw | `test_share_math_deposit_premium_payout_withdraw` |
| Premium rounds up and zero share deposit reverts | `test_premium_rounds_up_and_zero_share_deposit_reverts` |
| Expiry releases exposure permissionlessly and replay reverts | `test_expiry_releases_exposure_permissionlessly_and_replay_reverts` |
| Access and exact claim deadlines | `test_access_and_exact_claim_deadlines` |
| Fetch byte limits and utf8 | `test_fetch_byte_limits_and_utf8` |
| Quote past cut point is uncertain | `test_quote_past_cut_point_is_uncertain` |
| Truncated available prefix can pay | `test_truncated_available_prefix_can_pay` |
| Validator rejects forged records and judgments | `test_validator_rejects_forged_records_and_judgments` |
| Unsupported literal fields are uncertain | `test_unsupported_literal_fields_are_uncertain` |
| Malformed model reverts with no state change | `test_malformed_model_reverts_with_no_state_change` |
| Constructor bounds | `test_constructor_bounds` |
| Policy and amount bounds | `test_policy_and_amount_bounds` |
| Holder lifetime policy bound | `test_holder_lifetime_policy_bound` |
| Literal lowercase severity and offset times | `test_literal_lowercase_severity_and_offset_times` |
| Fractional seconds use integer duration | `test_fractional_seconds_use_integer_duration` |
| Validator refetches and rejects changed source | `test_validator_refetches_and_rejects_changed_source` |
| Total policy bound | `test_total_policy_bound` |
| Total account bound | `test_total_account_bound` |
| Share supply bound after loss | `test_share_supply_bound_after_loss` |
| Model quote and field size bounds | `test_model_quote_and_field_size_bounds` |
| Historical demo mode allows replay only during claim period | `test_historical_demo_mode_allows_replay_only_during_claim_period` |
| Multiple policies preserve backing after one pays | `test_multiple_policies_preserve_backing_after_one_pays` |

Required gates run sequentially: `genvm-lint check` (AST lint plus SDK validation), then `pytest`. Runner-update information does not change the pinned header. No dependencies are upgraded. The transcript records exact commands, stdout/stderr, exit codes, and the tested contract SHA-256. ABI extraction is recorded after the tests.

The historical demo-mode tests additionally cover the explicitly selected replay facility, while default-mode tests reject retroactive purchases. Bounds include services, triggers, URLs, configuration text, per-holder and global policy counts, global accounts, cumulative units, shares, kept body bytes, incident fields, and quote sizes.

Final result on 2026-11-10: **69/69 PASS**, 0 failed, in 8.93 seconds. GenVM lint passed 3 checks; SDK validation passed with 11 public methods and 6 constructor parameters. `GENVM_VERSION=v0.6.0-rc5` selects an already cached bundle, not a contract runner change. See the full transcript for I200 runner-update information. An initial unpinned release lookup was interrupted before tests; the final pinned sequence passed in order.
