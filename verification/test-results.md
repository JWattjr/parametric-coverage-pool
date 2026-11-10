# Direct test results

86 parameter-expanded tests. Mocked local execution; not a live network demo.

| Test | Result |
|---|---|
| `tests.test_pool::test_qualifying_payout_and_replayed_claim_reverts` | PASS |
| `tests.test_pool::test_nonqualifying_facts_cannot_pay_even_if_model_says_qualifying[minor-on-same-page]` | PASS |
| `tests.test_pool::test_nonqualifying_facts_cannot_pay_even_if_model_says_qualifying[outside-window]` | PASS |
| `tests.test_pool::test_nonqualifying_facts_cannot_pay_even_if_model_says_qualifying[duration-one-second-short]` | PASS |
| `tests.test_pool::test_nonqualifying_facts_cannot_pay_even_if_model_says_qualifying[half-open-end-boundary]` | PASS |
| `tests.test_pool::test_major_selected_among_minor_incidents` | PASS |
| `tests.test_pool::test_uncertain_leaves_policy_and_all_balances_unchanged_then_retry_pays` | PASS |
| `tests.test_pool::test_failed_fetch_keeps_policy_open_and_records_unavailability[503-down]` | PASS |
| `tests.test_pool::test_failed_fetch_keeps_policy_open_and_records_unavailability[200-]` | PASS |
| `tests.test_pool::test_failed_fetch_keeps_policy_open_and_records_unavailability[200-\xff]` | PASS |
| `tests.test_pool::test_failed_fetch_keeps_policy_open_and_records_unavailability[200-   ]` | PASS |
| `tests.test_pool::test_two_sources_one_unavailable` | PASS |
| `tests.test_pool::test_overexposure_purchase_reverts_without_premium_movement` | PASS |
| `tests.test_pool::test_undercollateralising_withdrawal_and_other_account_shares_revert` | PASS |
| `tests.test_pool::test_share_math_deposit_premium_payout_withdraw` | PASS |
| `tests.test_pool::test_premium_rounds_up_and_zero_share_deposit_reverts` | PASS |
| `tests.test_pool::test_expiry_releases_exposure_permissionlessly_and_replay_reverts` | PASS |
| `tests.test_pool::test_access_and_exact_claim_deadlines` | PASS |
| `tests.test_pool::test_fetch_byte_limits_and_utf8[exact-limit]` | PASS |
| `tests.test_pool::test_fetch_byte_limits_and_utf8[over-limit]` | PASS |
| `tests.test_pool::test_fetch_byte_limits_and_utf8[multibyte-cut]` | PASS |
| `tests.test_pool::test_fetch_byte_limits_and_utf8[multibyte-exact-limit]` | PASS |
| `tests.test_pool::test_fetch_byte_limits_and_utf8[invalid-interior-utf8]` | PASS |
| `tests.test_pool::test_fetch_byte_limits_and_utf8[whitespace-truncated]` | PASS |
| `tests.test_pool::test_quote_past_cut_point_is_uncertain` | PASS |
| `tests.test_pool::test_truncated_available_prefix_can_pay` | PASS |
| `tests.test_pool::test_validator_rejects_forged_records_and_judgments[status]` | PASS |
| `tests.test_pool::test_validator_rejects_forged_records_and_judgments[small_original]` | PASS |
| `tests.test_pool::test_validator_rejects_forged_records_and_judgments[kept_count]` | PASS |
| `tests.test_pool::test_validator_rejects_forged_records_and_judgments[digest]` | PASS |
| `tests.test_pool::test_validator_rejects_forged_records_and_judgments[available]` | PASS |
| `tests.test_pool::test_validator_rejects_forged_records_and_judgments[extra]` | PASS |
| `tests.test_pool::test_validator_rejects_forged_records_and_judgments[stale]` | PASS |
| `tests.test_pool::test_validator_rejects_forged_records_and_judgments[verdict]` | PASS |
| `tests.test_pool::test_validator_rejects_forged_records_and_judgments[quote]` | PASS |
| `tests.test_pool::test_validator_rejects_forged_records_and_judgments[field]` | PASS |
| `tests.test_pool::test_unsupported_literal_fields_are_uncertain[missing_quote]` | PASS |
| `tests.test_pool::test_unsupported_literal_fields_are_uncertain[made_up_quote]` | PASS |
| `tests.test_pool::test_unsupported_literal_fields_are_uncertain[unknown_severity]` | PASS |
| `tests.test_pool::test_unsupported_literal_fields_are_uncertain[no_timezone]` | PASS |
| `tests.test_pool::test_unsupported_literal_fields_are_uncertain[reverse_times]` | PASS |
| `tests.test_pool::test_malformed_model_reverts_with_no_state_change` | PASS |
| `tests.test_pool::test_constructor_bounds[overrides0-bounded integer]` | PASS |
| `tests.test_pool::test_constructor_bounds[overrides1-bounded integer]` | PASS |
| `tests.test_pool::test_constructor_bounds[overrides2-bounded integer]` | PASS |
| `tests.test_pool::test_constructor_bounds[overrides3-length]` | PASS |
| `tests.test_pool::test_constructor_bounds[overrides4-configuration count]` | PASS |
| `tests.test_pool::test_constructor_bounds[overrides5-configuration count]` | PASS |
| `tests.test_pool::test_constructor_bounds[overrides6-configuration count]` | PASS |
| `tests.test_pool::test_constructor_bounds[overrides7-duplicate configuration]` | PASS |
| `tests.test_pool::test_constructor_bounds[overrides8-URL count]` | PASS |
| `tests.test_pool::test_constructor_bounds[overrides9-length]` | PASS |
| `tests.test_pool::test_constructor_bounds[overrides10-public DNS]` | PASS |
| `tests.test_pool::test_constructor_bounds[overrides11-severity threshold]` | PASS |
| `tests.test_pool::test_constructor_bounds[overrides12-bounded integer]` | PASS |
| `tests.test_pool::test_constructor_bounds[overrides13-bounded JSON]` | PASS |
| `tests.test_pool::test_policy_and_amount_bounds` | PASS |
| `tests.test_pool::test_holder_lifetime_policy_bound` | PASS |
| `tests.test_pool::test_literal_lowercase_severity_and_offset_times` | PASS |
| `tests.test_pool::test_fractional_seconds_use_integer_duration[2030-01-02T10:30:00.001Z-QUALIFYING]` | PASS |
| `tests.test_pool::test_fractional_seconds_use_integer_duration[2030-01-02T10:30:00.000Z-NOT_QUALIFYING]` | PASS |
| `tests.test_pool::test_validator_refetches_and_rejects_changed_source` | PASS |
| `tests.test_pool::test_total_policy_bound` | PASS |
| `tests.test_pool::test_total_account_bound` | PASS |
| `tests.test_pool::test_share_supply_bound_after_loss` | PASS |
| `tests.test_pool::test_model_quote_and_field_size_bounds` | PASS |
| `tests.test_pool::test_historical_demo_mode_allows_replay_only_during_claim_period` | PASS |
| `tests.test_pool::test_multiple_policies_preserve_backing_after_one_pays` | PASS |
| `tests.test_pool::test_statuspage_resolved_before_outside_window_does_not_pay` | PASS |
| `tests.test_pool::test_statuspage_metadata_timestamps_are_uncertain[end-updated_at]` | PASS |
| `tests.test_pool::test_statuspage_metadata_timestamps_are_uncertain[start-created_at]` | PASS |
| `tests.test_pool::test_statuspage_metadata_timestamps_are_uncertain[start-monitoring_at]` | PASS |
| `tests.test_pool::test_statuspage_metadata_timestamps_are_uncertain[start-display_at]` | PASS |
| `tests.test_pool::test_severity_value_may_differ_from_literal_quote_only_in_case` | PASS |
| `tests.test_pool::test_timestamp_quote_markers_are_required_case_insensitively[BEGAN-RESOLVED-QUALIFYING]` | PASS |
| `tests.test_pool::test_timestamp_quote_markers_are_required_case_insensitively[event time-resolved-UNCERTAIN]` | PASS |
| `tests.test_pool::test_timestamp_quote_markers_are_required_case_insensitively[started_at-updated_at-UNCERTAIN]` | PASS |
| `tests.test_pool::test_validator_agrees_on_facts_despite_page_updated_at_drift` | PASS |
| `tests.test_pool::test_validator_compares_normalised_incident_facts[subminute-utc]` | PASS |
| `tests.test_pool::test_validator_compares_normalised_incident_facts[milliseconds]` | PASS |
| `tests.test_pool::test_validator_compares_normalised_incident_facts[normalised-title]` | PASS |
| `tests.test_pool::test_validator_compares_normalised_incident_facts[normalised-severity]` | PASS |
| `tests.test_pool::test_validator_compares_normalised_incident_facts[different-severity-same-verdict]` | PASS |
| `tests.test_pool::test_validator_compares_normalised_incident_facts[different-minute]` | PASS |
| `tests.test_pool::test_validator_disagrees_when_verdict_differs_despite_same_minute_buckets` | PASS |
| `tests.test_pool::test_validator_must_find_its_quotes_in_its_own_text` | PASS |
