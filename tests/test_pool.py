import copy
import hashlib
import json
from pathlib import Path

import pytest

SDK = "v0.6.0-rc5"
URL = "https://status.example.org/incidents/one"
SERVICES = [{"id": "api", "name": "Example API", "urls": [URL]}]
TRIGGERS = [{"id": "major_30", "minimum_severity": "MAJOR", "minimum_minutes": 30}]
START = "2030-01-02T00:00:00Z"
END = "2030-01-03T00:00:00Z"
CLAIM = "2030-01-03T01:00:00Z"
DEADLINE = "2030-01-04T00:00:00Z"


def key(address):
    return "0x" + address.hex() if isinstance(address, bytes) else str(address).lower()


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def digest(value):
    return "sha256:" + hashlib.sha256(canonical(value).encode()).hexdigest()


def deploy(vm, direct_deploy, owner, **overrides):
    args = dict(pool_id="coverage-demo", services_json=json.dumps(SERVICES),
                triggers_json=json.dumps(TRIGGERS), premium_bps=1000, claim_period_seconds=86400, historical_demo_mode=False)
    args.update(overrides)
    vm.sender = owner
    vm.warp("2030-01-01T12:00:00Z")
    return direct_deploy("contracts/parametric_coverage_pool.py", *args.values(), sdk_version=SDK)


def conserved(contract):
    a = contract.get_accounting()
    assert a["conserved"] and a["collateralised"]
    assert a["deposited_units"] + a["premiums_paid_units"] == a["pool_capital_units"] + a["payouts_made_units"] + a["withdrawn_units"]
    return a


def buy(contract, vm, holder, amount=100, identity="policy", **overrides):
    args = dict(policy_id=identity, service_id="api", trigger_id="major_30", coverage_units=amount,
                window_start_iso=START, window_end_iso=END)
    args.update(overrides)
    with vm.prank(holder):
        result = contract.buy_policy(*args.values())
    conserved(contract)
    return result


def finding(severity="MAJOR", start="2030-01-02T10:00:00Z", end="2030-01-02T11:00:00Z", incident="API outage", verdict="QUALIFYING"):
    values = dict(incident=incident, severity=severity, start=start, end=end)
    lines = {field: f"{field}: {value}" for field, value in values.items()}
    lines["end"] = f"resolved end: {end}"
    return dict(verdict=verdict, **values, quotes={field: {"url": URL, "line": line} for field, line in lines.items()}), "\n".join(lines.values())


def mock(vm, result=None, body=None, status=200):
    if result is None:
        result, default = finding()
    else:
        default = "\n".join(q["line"] for q in result["quotes"].values())
    vm.clear_mocks()
    vm.mock_web(r".*", {"status": status, "body": default if body is None else body})
    vm.mock_llm(r"PARAMETRIC COVERAGE INCIDENT REVIEW", json.dumps(json.dumps(result)))


@pytest.fixture
def pool(direct_vm, direct_deploy, direct_owner, direct_alice):
    c = deploy(direct_vm, direct_deploy, direct_owner)
    conserved(c)
    with direct_vm.prank(direct_owner):
        assert c.deposit(1000) == 1000
    conserved(c)
    buy(c, direct_vm, direct_alice)
    direct_vm.sender = direct_alice
    direct_vm.warp(CLAIM)
    return c


def test_qualifying_payout_and_replayed_claim_reverts(pool, direct_vm, direct_alice):
    mock(direct_vm)
    assert pool.claim("policy")["judgment"]["verdict"] == "QUALIFYING"
    assert pool.get_policy("policy")["status"] == "PAID"
    assert pool.get_account(key(direct_alice))["payouts_received_units"] == 100
    assert conserved(pool)["pool_capital_units"] == 910
    assert direct_vm.run_validator()
    with direct_vm.expect_revert("not open"):
        pool.claim("policy")
    assert conserved(pool)["payouts_made_units"] == 100


@pytest.mark.parametrize("changes", [
    pytest.param(dict(severity="MINOR"), id="minor-on-same-page"),
    pytest.param(dict(start="2030-01-01T10:00:00Z", end="2030-01-01T11:00:00Z"), id="outside-window"),
    pytest.param(dict(end="2030-01-02T10:29:59Z"), id="duration-one-second-short"),
    pytest.param(dict(start=END, end="2030-01-03T01:00:00Z"), id="half-open-end-boundary"),
])
def test_nonqualifying_facts_cannot_pay_even_if_model_says_qualifying(pool, direct_vm, changes):
    result, body = finding(**changes)
    mock(direct_vm, result, body)
    assert pool.claim("policy")["judgment"]["verdict"] == "NOT_QUALIFYING"
    assert pool.get_policy("policy")["status"] == "DENIED"
    assert conserved(pool)["payouts_made_units"] == 0
    assert direct_vm.run_validator()
    with direct_vm.expect_revert("not open"):
        pool.claim("policy")
    conserved(pool)


def test_major_selected_among_minor_incidents(pool, direct_vm):
    major, text = finding()
    _, minor = finding(severity="MINOR", incident="Minor latency")
    mock(direct_vm, major, minor + "\n" + text)
    assert pool.claim("policy")["judgment"]["verdict"] == "QUALIFYING"
    conserved(pool)


def test_uncertain_leaves_policy_and_all_balances_unchanged_then_retry_pays(pool, direct_vm):
    before, policy = pool.get_accounting(), pool.get_policy("policy")
    uncertain = dict(verdict="UNCERTAIN", incident="", severity="", start="", end="", quotes={})
    mock(direct_vm, uncertain, "Incident details have not been published.")
    assert pool.claim("policy")["judgment"] == uncertain
    assert pool.get_accounting() == before and pool.get_policy("policy") == policy
    assert pool.get_sources("policy")[0]["available"] is True
    assert direct_vm.run_validator()
    mock(direct_vm)
    pool.claim("policy")
    assert pool.get_policy("policy")["status"] == "PAID"
    conserved(pool)


@pytest.mark.parametrize("status,body", [(503, b"down"), (200, b""), (200, b"\xff"), (200, b"   ")])
def test_failed_fetch_keeps_policy_open_and_records_unavailability(pool, direct_vm, status, body):
    before = pool.get_accounting()
    mock(direct_vm, body=body, status=status)
    assert pool.claim("policy")["judgment"]["verdict"] == "UNCERTAIN"
    assert pool.get_accounting() == before
    source = pool.get_sources("policy")[0]
    assert source["status"] == "unavailable" and not source["available"]
    assert source["byte_count"] == len(body) and source["kept_byte_count"] == 0
    assert direct_vm.run_validator()
    conserved(pool)


def test_two_sources_one_unavailable(direct_vm, direct_deploy, direct_owner, direct_alice):
    services = copy.deepcopy(SERVICES)
    second = "https://status.example.org/incidents/two"
    services[0]["urls"].append(second)
    c = deploy(direct_vm, direct_deploy, direct_owner, services_json=json.dumps(services))
    c.deposit(1000)
    buy(c, direct_vm, direct_alice)
    direct_vm.sender = direct_alice
    direct_vm.warp(CLAIM)
    direct_vm.mock_web(URL + "$", {"status": 200, "body": finding()[1]})
    direct_vm.mock_web(second + "$", {"status": 503, "body": "down"})
    assert c.claim("policy")["judgment"]["verdict"] == "UNCERTAIN"
    assert [s["status"] for s in c.get_sources("policy")] == ["fetched", "unavailable"]
    assert direct_vm.run_validator()
    conserved(c)


def test_overexposure_purchase_reverts_without_premium_movement(pool, direct_vm, direct_alice):
    direct_vm.warp("2030-01-01T12:00:00Z")
    before = pool.get_accounting()
    with direct_vm.expect_revert("exceed pool capital"):
        buy(pool, direct_vm, direct_alice, amount=911, identity="too_large")
    assert pool.get_accounting() == before
    conserved(pool)


def test_undercollateralising_withdrawal_and_other_account_shares_revert(pool, direct_vm, direct_owner, direct_bob):
    before = pool.get_accounting()
    with direct_vm.prank(direct_owner):
        with direct_vm.expect_revert("under-collateralise"):
            pool.withdraw(1000)
    with direct_vm.prank(direct_bob):
        with direct_vm.expect_revert("insufficient caller shares"):
            pool.withdraw(1)
    assert pool.get_accounting() == before
    conserved(pool)


def test_share_math_deposit_premium_payout_withdraw(direct_vm, direct_deploy, direct_owner, direct_alice, direct_bob):
    c = deploy(direct_vm, direct_deploy, direct_owner)
    assert c.deposit(100) == 100
    conserved(c)
    buy(c, direct_vm, direct_alice, amount=90)  # Capital 109, supply 100.
    with direct_vm.prank(direct_bob):
        assert c.deposit(50) == 45  # floor(5000/109).
    assert conserved(c)["pool_capital_units"] == 159
    direct_vm.warp(CLAIM)
    direct_vm.sender = direct_alice
    mock(direct_vm)
    c.claim("policy")  # Capital 69; total shares 145.
    assert conserved(c)["pool_capital_units"] == 69
    with direct_vm.prank(direct_bob):
        assert c.withdraw(45) == 21  # floor(45*69/145).
    assert conserved(c)["total_shares"] == 100
    with direct_vm.prank(direct_owner):
        assert c.withdraw(100) == 48
    assert conserved(c)["pool_capital_units"] == 0


def test_premium_rounds_up_and_zero_share_deposit_reverts(direct_vm, direct_deploy, direct_owner, direct_alice):
    c = deploy(direct_vm, direct_deploy, direct_owner, premium_bps=1)
    c.deposit(100)
    assert buy(c, direct_vm, direct_alice, amount=1)["premium_units"] == 1
    before = c.get_accounting()
    with direct_vm.expect_revert("zero shares"):
        c.deposit(1)
    assert c.get_accounting() == before
    conserved(c)


def test_expiry_releases_exposure_permissionlessly_and_replay_reverts(pool, direct_vm, direct_bob):
    direct_vm.sender = direct_bob
    direct_vm.warp(DEADLINE)
    with direct_vm.expect_revert("has not passed"):
        pool.expire_policy("policy")
    direct_vm.warp("2030-01-04T00:00:01Z")
    pool.expire_policy("policy")
    assert conserved(pool)["open_exposure_units"] == 0
    assert pool.get_policy("policy")["status"] == "EXPIRED"
    with direct_vm.expect_revert("not open"):
        pool.claim("policy")
    with direct_vm.expect_revert("not open"):
        pool.expire_policy("policy")
    conserved(pool)


def test_access_and_exact_claim_deadlines(pool, direct_vm, direct_bob, direct_alice):
    direct_vm.sender = direct_bob
    with direct_vm.expect_revert("only the policyholder"):
        pool.claim("policy")
    direct_vm.sender = direct_alice
    direct_vm.warp(END)
    with direct_vm.expect_revert("outside claim period"):
        pool.claim("policy")
    direct_vm.warp("2030-01-04T00:00:01Z")
    with direct_vm.expect_revert("outside claim period"):
        pool.claim("policy")
    direct_vm.warp(DEADLINE)
    mock(direct_vm)
    pool.claim("policy")
    conserved(pool)


@pytest.mark.parametrize("body,expected_status,kept", [
    pytest.param(b"x" * 5000, "fetched", 5000, id="exact-limit"),
    pytest.param(b"x" * 5001, "truncated", 5000, id="over-limit"),
    pytest.param(b"x" * 4999 + "€".encode() + b"tail", "truncated", 4999, id="multibyte-cut"),
    pytest.param(b"x" * 4997 + "€".encode(), "fetched", 5000, id="multibyte-exact-limit"),
    pytest.param(b"x\xff" + b"x" * 5000, "unavailable", 0, id="invalid-interior-utf8"),
    pytest.param(b" " * 5001, "truncated", 5000, id="whitespace-truncated"),
])
def test_fetch_byte_limits_and_utf8(pool, direct_vm, body, expected_status, kept):
    before = pool.get_accounting()
    mock(direct_vm, body=body)
    assert pool.claim("policy")["judgment"]["verdict"] == "UNCERTAIN"
    source = pool.get_sources("policy")[0]
    assert source["status"] == expected_status
    assert source["byte_count"] == len(body) and source["kept_byte_count"] == kept
    assert len(source["text"].encode()) == kept
    assert source["content_digest"] == "sha256:" + hashlib.sha256(body[:kept]).hexdigest()
    assert pool.get_accounting() == before
    assert direct_vm.run_validator()
    conserved(pool)


def test_quote_past_cut_point_is_uncertain(pool, direct_vm):
    result, body = finding()
    mock(direct_vm, result, "x" * 5000 + "\n" + body)
    assert pool.claim("policy")["judgment"]["verdict"] == "UNCERTAIN"
    assert pool.get_sources("policy")[0]["status"] == "truncated"
    assert conserved(pool)["payouts_made_units"] == 0
    assert direct_vm.run_validator()


def test_truncated_available_prefix_cannot_pay(pool, direct_vm):
    result, text = finding()
    mock(direct_vm, result, text + "x" * 6000)
    before = pool.get_accounting()
    assert pool.claim("policy")["judgment"]["verdict"] == "UNCERTAIN"
    assert pool.get_sources("policy")[0]["status"] == "truncated"
    assert pool.get_sources("policy")[0]["available"] is True
    assert pool.get_policy("policy")["status"] == "OPEN"
    assert pool.get_accounting() == before
    assert direct_vm.run_validator()
    conserved(pool)


@pytest.mark.parametrize("mutation", ["status", "small_original", "kept_count", "digest", "same_size_text", "available", "extra", "stale", "verdict", "quote", "field"])
def test_validator_rejects_forged_records_and_judgments(pool, direct_vm, mutation):
    result, text = finding()
    mock(direct_vm, result, text + "\nmetadata:stable")
    pool.claim("policy")
    assert direct_vm.run_validator()
    honest = pool.get_assessment("policy")
    forged = copy.deepcopy(honest)
    source = forged["sources"][0]
    if mutation == "status":
        source["status"] = "truncated"
    elif mutation == "small_original":
        source["byte_count"] = 5001
    elif mutation == "kept_count":
        source["kept_byte_count"] -= 1
    elif mutation == "digest":
        source["content_digest"] = "sha256:" + "0" * 64
    elif mutation == "same_size_text":
        source["text"] = source["text"][:-1] + "y"
        source["content_digest"] = "sha256:" + hashlib.sha256(source["text"].encode()).hexdigest()
    elif mutation == "available":
        source["available"] = False
    elif mutation == "extra":
        forged["untrusted"] = "extra"
    elif mutation == "stale":
        forged["input_snapshot_digest"] = "sha256:" + "0" * 64
    elif mutation == "verdict":
        forged["judgment"]["verdict"] = "NOT_QUALIFYING"
    elif mutation == "quote":
        forged["judgment"]["quotes"]["severity"]["line"] = "invented"
    else:
        forged["judgment"]["incident"] = "Another incident"
    # Rebinding digests cannot repair invalid source metadata, unsupported quotes,
    # stale policy bindings, or inconsistent/different incident facts.
    forged["evidence_digest"] = digest({"input_snapshot_digest": forged["input_snapshot_digest"], "sources": forged["sources"]})
    forged["snapshot_digest"] = digest({"input_snapshot_digest": forged["input_snapshot_digest"], "evidence_digest": forged["evidence_digest"]})
    assert direct_vm.run_validator(leader_result=forged) is False
    conserved(pool)


@pytest.mark.parametrize("change", ["missing_quote", "made_up_quote", "unknown_severity", "no_timezone", "reverse_times"])
def test_unsupported_literal_fields_are_uncertain(pool, direct_vm, change):
    kwargs = {"unknown_severity": dict(severity="SEV-1"), "no_timezone": dict(start="2030-01-02T10:00:00"),
              "reverse_times": dict(end="2030-01-02T09:00:00Z")}.get(change, {})
    result, text = finding(**kwargs)
    if change == "missing_quote":
        del result["quotes"]["start"]
    elif change == "made_up_quote":
        result["quotes"]["severity"]["line"] = "invented MAJOR line"
    mock(direct_vm, result, text)
    assert pool.claim("policy")["judgment"]["verdict"] == "UNCERTAIN"
    assert pool.get_policy("policy")["status"] == "OPEN"
    conserved(pool)


def test_malformed_model_reverts_with_no_state_change(pool, direct_vm):
    result, text = finding()
    result["extra"] = "untrusted"
    mock(direct_vm, result, text)
    before = pool.get_accounting()
    with direct_vm.expect_revert("invalid judgment schema"):
        pool.claim("policy")
    assert pool.get_accounting() == before and pool.get_assessment("policy") == {}
    conserved(pool)


@pytest.mark.parametrize("overrides,message", [
    (dict(premium_bps=0), "bounded integer"),
    (dict(premium_bps=10001), "bounded integer"),
    (dict(claim_period_seconds=2592001), "bounded integer"),
    (dict(pool_id="x" * 65), "length"),
    (dict(services_json="[]"), "configuration count"),
    (dict(services_json=json.dumps(SERVICES * 9)), "configuration count"),
    (dict(triggers_json=json.dumps(TRIGGERS * 5)), "configuration count"),
    (dict(services_json=json.dumps(SERVICES * 2)), "duplicate configuration"),
    (dict(services_json=json.dumps([dict(SERVICES[0], urls=[URL] * 4)])), "URL count"),
    (dict(services_json=json.dumps([dict(SERVICES[0], name="x" * 101)])), "length"),
    (dict(services_json=json.dumps([dict(SERVICES[0], urls=["https://127.0.0.1/a"])])), "public DNS"),
    (dict(triggers_json=json.dumps([dict(TRIGGERS[0], minimum_severity="EXTREME")])), "severity threshold"),
    (dict(triggers_json=json.dumps([dict(TRIGGERS[0], minimum_minutes=43201)])), "bounded integer"),
    (dict(services_json="x" * 16001), "bounded JSON"),
])
def test_constructor_bounds(direct_vm, direct_deploy, direct_owner, overrides, message):
    with direct_vm.expect_revert(message):
        deploy(direct_vm, direct_deploy, direct_owner, **overrides)


def test_policy_and_amount_bounds(pool, direct_vm, direct_alice, direct_owner):
    direct_vm.warp("2030-01-01T12:00:00Z")
    before = pool.get_accounting()
    cases = [(dict(policy_id="x" * 33), "identifier"), (dict(coverage_units=0), "bounded integer"),
             (dict(service_id="unknown"), "unknown frozen"), (dict(trigger_id="unknown"), "unknown frozen"),
             (dict(window_start_iso="2030-01-01T12:00:00Z"), "future"),
             (dict(window_end_iso="2030-03-01T00:00:00Z"), "bounded"),
             (dict(window_start_iso="2030-01-02T00:00:00"), "timezone"),
             (dict(policy_id="policy"), "already exists")]
    for override, message in cases:
        with direct_vm.expect_revert(message):
            buy(pool, direct_vm, direct_alice, identity="invalid", **override)
        assert pool.get_accounting() == before
    with direct_vm.prank(direct_owner):
        for amount in (0, 10**12 + 1):
            with direct_vm.expect_revert("bounded integer"):
                pool.deposit(amount)
        with direct_vm.expect_revert("cumulative unit limit"):
            pool.deposit(10**12)
    conserved(pool)


def test_holder_lifetime_policy_bound(pool, direct_vm, direct_alice):
    direct_vm.warp("2030-01-01T12:00:00Z")
    for i in range(7):
        buy(pool, direct_vm, direct_alice, amount=1, identity=f"p{i}")
    before = pool.get_accounting()
    with direct_vm.expect_revert("holder policy limit"):
        buy(pool, direct_vm, direct_alice, amount=1, identity="ninth")
    assert pool.get_accounting() == before
    conserved(pool)


def test_literal_lowercase_severity_and_offset_times(pool, direct_vm):
    result, text = finding(severity="major", start="2030-01-02T11:00:00+01:00", end="2030-01-02T12:00:00+01:00")
    mock(direct_vm, result, text)
    assert pool.claim("policy")["judgment"] == result
    assert direct_vm.run_validator()
    conserved(pool)


@pytest.mark.parametrize("duration_end,verdict", [
    ("2030-01-02T10:30:00.001Z", "QUALIFYING"),
    ("2030-01-02T10:30:00.000Z", "NOT_QUALIFYING"),
])
def test_fractional_seconds_use_integer_duration(pool, direct_vm, duration_end, verdict):
    result, text = finding(start="2030-01-02T10:00:00.001Z", end=duration_end)
    mock(direct_vm, result, text)
    assert pool.claim("policy")["judgment"]["verdict"] == verdict
    assert direct_vm.run_validator()
    conserved(pool)


def test_validator_refetches_and_rejects_changed_source(pool, direct_vm):
    mock(direct_vm)
    pool.claim("policy")
    assert direct_vm.run_validator()
    assert not direct_vm.run_validator(leader_error="forged classified failure")
    mock(direct_vm, status=503)
    assert not direct_vm.run_validator()
    conserved(pool)


def test_total_policy_bound(direct_vm, direct_deploy, direct_owner):
    c = deploy(direct_vm, direct_deploy, direct_owner)
    c.deposit(10000)
    for i in range(128):
        holder = (i // 8 + 100).to_bytes(20, "big")
        buy(c, direct_vm, holder, amount=1, identity=f"p{i}")
    before = c.get_accounting()
    with direct_vm.expect_revert("pool policy limit"):
        buy(c, direct_vm, (999).to_bytes(20, "big"), amount=1, identity="overflow")
    assert c.get_accounting() == before
    conserved(c)


def test_total_account_bound(direct_vm, direct_deploy, direct_owner):
    c = deploy(direct_vm, direct_deploy, direct_owner)
    c.deposit(1000)
    for i in range(63):
        with direct_vm.prank((i + 100).to_bytes(20, "big")):
            c.deposit(1)
        conserved(c)
    assert c.get_pool()["account_count"] == 64
    before = c.get_accounting()
    with direct_vm.prank((999).to_bytes(20, "big")):
        with direct_vm.expect_revert("account limit"):
            c.deposit(1)
    assert c.get_accounting() == before
    conserved(c)


def test_share_supply_bound_after_loss(direct_vm, direct_deploy, direct_owner, direct_alice):
    c = deploy(direct_vm, direct_deploy, direct_owner, premium_bps=1)
    c.deposit(100)
    buy(c, direct_vm, direct_alice, amount=100)
    direct_vm.warp(CLAIM)
    direct_vm.sender = direct_alice
    mock(direct_vm)
    c.claim("policy")
    assert conserved(c)["pool_capital_units"] == 1
    with direct_vm.expect_revert("share supply limit"):
        c.deposit(10**11)
    conserved(c)


def test_model_quote_and_field_size_bounds(pool, direct_vm):
    for field, value, message in [("incident", "x" * 201, "incident fields"),
                                   ("line", "x" * 1201, "quote size")]:
        result, text = finding()
        if field == "line":
            result["quotes"]["incident"]["line"] = value
        else:
            result[field] = value
        mock(direct_vm, result, text)
        before = pool.get_accounting()
        with direct_vm.expect_revert(message):
            pool.claim("policy")
        assert pool.get_accounting() == before
        conserved(pool)


def test_historical_demo_mode_allows_replay_only_during_claim_period(direct_vm, direct_deploy, direct_owner, direct_alice):
    c = deploy(direct_vm, direct_deploy, direct_owner, historical_demo_mode=True)
    c.deposit(1000)
    direct_vm.warp(CLAIM)
    assert c.get_pool()["historical_demo_mode"] is True
    buy(c, direct_vm, direct_alice)
    direct_vm.sender = direct_alice
    mock(direct_vm)
    assert c.claim("policy")["judgment"]["verdict"] == "QUALIFYING"
    assert direct_vm.run_validator()
    conserved(c)
    direct_vm.warp("2030-01-04T00:00:01Z")
    with direct_vm.expect_revert("open claim period"):
        buy(c, direct_vm, direct_alice, identity="too_late")
    conserved(c)


def test_multiple_policies_preserve_backing_after_one_pays(pool, direct_vm, direct_alice, direct_bob):
    direct_vm.warp("2030-01-01T12:00:00Z")
    buy(pool, direct_vm, direct_bob, amount=900, identity="other")
    assert conserved(pool)["open_exposure_units"] == 1000
    direct_vm.sender = direct_alice
    direct_vm.warp(CLAIM)
    mock(direct_vm)
    pool.claim("policy")
    accounting = conserved(pool)
    assert accounting["open_exposure_units"] == pool.get_policy("other")["coverage_units"] == 900
    assert accounting["pool_capital_units"] == 1000
    assert pool.get_policy("other")["status"] == "OPEN"


def statuspage_finding(page):
    incident = page["incident"]
    fields = {"incident": "name", "severity": "impact", "start": "started_at", "end": "resolved_at"}
    result = {"verdict": "NOT_QUALIFYING", "quotes": {}}
    for field, key_name in fields.items():
        result[field] = incident[key_name]
        result["quotes"][field] = {"url": URL, "line": json.dumps(key_name) + ": " + json.dumps(incident[key_name])}
    return result, json.dumps(page, indent=2)


@pytest.fixture
def statuspage():
    return json.loads((Path(__file__).parent / "fixtures/statuspage_incident.json").read_text())


def test_statuspage_resolved_before_outside_window_does_not_pay(pool, direct_vm, statuspage):
    # The policy covers Jan 2-3, after Jan 1 resolution but before Jan 5 updates.
    result, body = statuspage_finding(statuspage)
    mock(direct_vm, result, body)
    assert pool.claim("policy")["judgment"]["verdict"] == "NOT_QUALIFYING"
    assert pool.get_policy("policy")["status"] == "DENIED"
    assert conserved(pool)["payouts_made_units"] == 0
    assert direct_vm.run_validator()


@pytest.mark.parametrize("field,key_name", [
    ("end", "updated_at"), ("start", "created_at"), ("start", "monitoring_at"), ("start", "display_at"),
])
def test_statuspage_metadata_timestamps_are_uncertain(pool, direct_vm, statuspage, field, key_name):
    result, body = statuspage_finding(statuspage)
    result["verdict"] = "QUALIFYING"
    result[field] = statuspage["incident"][key_name]
    result["quotes"][field]["line"] = json.dumps(key_name) + ": " + json.dumps(result[field])
    mock(direct_vm, result, body)
    before = pool.get_accounting()
    assert pool.claim("policy")["judgment"]["verdict"] == "UNCERTAIN"
    assert pool.get_policy("policy")["status"] == "OPEN"
    assert pool.get_accounting() == before
    assert direct_vm.run_validator()
    conserved(pool)


def test_severity_value_may_differ_from_literal_quote_only_in_case(pool, direct_vm):
    result, body = finding(severity="major")
    result["severity"] = "MAJOR"
    mock(direct_vm, result, body)
    assert pool.claim("policy")["judgment"]["verdict"] == "QUALIFYING"
    assert direct_vm.run_validator()
    conserved(pool)


@pytest.mark.parametrize("start_marker,end_marker,verdict", [
    ("BEGAN", "RESOLVED", "QUALIFYING"),
    ("event time", "resolved", "UNCERTAIN"),
    ("started_at", "updated_at", "UNCERTAIN"),
])
def test_timestamp_quote_markers_are_required_case_insensitively(pool, direct_vm, start_marker, end_marker, verdict):
    result, _ = finding()
    result["quotes"]["start"]["line"] = start_marker + ": " + result["start"]
    result["quotes"]["end"]["line"] = end_marker + ": " + result["end"]
    mock(direct_vm, result)
    assert pool.claim("policy")["judgment"]["verdict"] == verdict
    assert direct_vm.run_validator()
    conserved(pool)


def test_validator_rejects_page_updated_at_drift_even_with_same_facts(pool, direct_vm, statuspage):
    leader, body = statuspage_finding(statuspage)
    mock(direct_vm, leader, body)
    pool.claim("policy")
    stored = pool.get_assessment("policy")
    statuspage["page"]["updated_at"] = "2030-01-06T16:00:00Z"
    mine, changed_body = statuspage_finding(statuspage)
    assert body != changed_body
    assert hashlib.sha256(body.encode()).digest() != hashlib.sha256(changed_body.encode()).digest()
    mock(direct_vm, mine, changed_body)
    assert not direct_vm.run_validator()
    assert pool.get_assessment("policy") == stored  # Leader evidence remains the stored record.
    conserved(pool)


@pytest.mark.parametrize("changes,agrees", [
    pytest.param({}, True, id="identical-candidate"),
    pytest.param(dict(start="2030-01-02T11:00:59.999+01:00", end="2030-01-02T12:00:59.999+01:00"), False, id="subminute-utc"),
    pytest.param(dict(start="2030-01-02T10:00:00.028Z"), False, id="milliseconds"),
    pytest.param(dict(incident="  API    OUTAGE  "), False, id="title-whitespace-case"),
    pytest.param(dict(severity="major"), False, id="severity-case"),
    pytest.param(dict(severity="CRITICAL"), False, id="different-severity-same-verdict"),
    pytest.param(dict(start="2030-01-02T10:01:00Z", end="2030-01-02T11:01:00Z"), False, id="different-minute"),
])
def test_validator_requires_exact_stored_incident_facts(pool, direct_vm, changes, agrees):
    mock(direct_vm)
    pool.claim("policy")
    mine, body = finding(**changes)
    mock(direct_vm, mine, body)
    assert direct_vm.run_validator() is agrees
    conserved(pool)


def test_validator_disagrees_when_verdict_differs_despite_same_minute_buckets(pool, direct_vm):
    leader, body = finding(start="2030-01-02T10:00:00.001Z", end="2030-01-02T10:30:00.001Z")
    mock(direct_vm, leader, body)
    assert pool.claim("policy")["judgment"]["verdict"] == "QUALIFYING"
    mine, changed_body = finding(start="2030-01-02T10:00:00.001Z", end="2030-01-02T10:30:00.000Z")
    mock(direct_vm, mine, changed_body)
    assert not direct_vm.run_validator()
    conserved(pool)


def test_validator_must_find_its_quotes_in_its_own_text(pool, direct_vm):
    mock(direct_vm)
    pool.claim("policy")
    mine, _ = finding()
    mock(direct_vm, mine, "Incident details omitted in this node's fetched page.")
    assert not direct_vm.run_validator()
    conserved(pool)


def test_validator_rejects_supported_quote_change_with_same_verdict(pool, direct_vm):
    result, body = finding()
    alternative = "stated severity: MAJOR"
    mock(direct_vm, result, body + "\n" + alternative)
    pool.claim("policy")
    assert direct_vm.run_validator()
    forged = copy.deepcopy(pool.get_assessment("policy"))
    forged["judgment"]["quotes"]["severity"]["line"] = alternative
    assert forged["judgment"]["verdict"] == "QUALIFYING"
    assert not direct_vm.run_validator(leader_result=forged)
    conserved(pool)


def test_truncated_source_cannot_be_forged_into_a_positive_candidate(pool, direct_vm):
    result, body = finding()
    mock(direct_vm, result, body + "x" * 6000)
    pool.claim("policy")
    forged = copy.deepcopy(pool.get_assessment("policy"))
    forged["judgment"] = result
    assert not direct_vm.run_validator(leader_result=forged)
    assert pool.get_policy("policy")["status"] == "OPEN"
    assert conserved(pool)["open_exposure_units"] == 100


def test_uncertain_claim_keeps_backing_locked_during_partial_withdrawal(pool, direct_vm, direct_owner):
    result, body = finding()
    mock(direct_vm, result, body + "x" * 6000)
    pool.claim("policy")
    with direct_vm.prank(direct_owner):
        # Capital 1010 / 1000 shares. Floor(901*1010/1000) = 910.
        assert pool.withdraw(901) == 910
        a = conserved(pool)
        assert a["pool_capital_units"] == a["open_exposure_units"] == 100
        with direct_vm.expect_revert("under-collateralise"):
            pool.withdraw(99)
    assert pool.get_policy("policy")["status"] == "OPEN"
    conserved(pool)
