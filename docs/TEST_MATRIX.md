# Test matrix

Strict-revision direct tests mock web/model responses and explicitly exercise the independent validator callback. They do not establish live consensus. Lint must pass before this full suite runs.

| Behavior or invariant | Test |
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
| Truncated available prefix cannot pay | `test_truncated_available_prefix_cannot_pay` |
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
| Statuspage resolved before outside window does not pay | `test_statuspage_resolved_before_outside_window_does_not_pay` |
| Statuspage metadata timestamps are uncertain | `test_statuspage_metadata_timestamps_are_uncertain` |
| Severity value may differ from literal quote only in case | `test_severity_value_may_differ_from_literal_quote_only_in_case` |
| Timestamp quote markers are required case insensitively | `test_timestamp_quote_markers_are_required_case_insensitively` |
| Validator rejects page updated at drift even with same facts | `test_validator_rejects_page_updated_at_drift_even_with_same_facts` |
| Validator requires exact stored incident facts | `test_validator_requires_exact_stored_incident_facts` |
| Validator disagrees when verdict differs despite same minute buckets | `test_validator_disagrees_when_verdict_differs_despite_same_minute_buckets` |
| Validator must find its quotes in its own text | `test_validator_must_find_its_quotes_in_its_own_text` |
| Validator rejects supported quote change with same verdict | `test_validator_rejects_supported_quote_change_with_same_verdict` |
| Truncated source cannot be forged into a positive candidate | `test_truncated_source_cannot_be_forged_into_a_positive_candidate` |
| Uncertain claim keeps backing locked during partial withdrawal | `test_uncertain_claim_keeps_backing_locked_during_partial_withdrawal` |

The strict revision compares complete canonical candidates, not headline facts. The tests reject changed page bytes, subminute timestamps, severity spelling, supported-but-changed quotes, stale snapshots, inconsistent source records and forged metadata even when the verdict is unchanged. Identical candidates agree.

Truncated text remains available for inspection, with original/kept sizes and digest validated, but any truncated source forces UNCERTAIN and preserves every balance and OPEN exposure. A partially withdrawn pool must retain backing for that exposure. Original exact-at-limit, multibyte-cut, unavailable-source, unauthorized caller, replay, share rounding, expiry and conservation cases remain.

Every financial scenario asserts conservation and collateral, including rejected operations. Results are recorded in [test-results.md](../verification/test-results.md) and exact sequential lint/test output in [checks.txt](../verification/checks.txt). The changed source is not evidenced by the earlier 86-test run or earlier StudioNet receipts.

Strict revision result on 2026-11-11: **91/91 PASS**, 0 failed, in 12.25 seconds. GenVM lint passed 3 checks and SDK validation passed with 11 methods (6 views, 5 writes), 6 constructor parameters. The runner remains pinned; I200 is informational.
