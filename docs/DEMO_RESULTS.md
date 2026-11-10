# StudioNet demo results

StudioNet demo passed: both major incidents paid 100 synthetic units each; the minor and outside-window policies paid nothing. All 15 transactions finalized (11 successful executions and four expected rollbacks). The underwriter withdrew the remaining 840 units; final capital, exposure and shares are zero, and 1,000 deposits + 40 premiums = 200 payouts + 840 withdrawals.

Source commit: `8682be72a878885f612cb6e6e812455d8d4010c4`.

[GenLayer Explorer Contract](https://explorer-studio.genlayer.com/address/0x264f3189aFccA46881DB959Aa1a20D0E2bA12521) — verified in the browser on the StudioNet Explorer.

[Complete receipts and exact latest-final readbacks](../deployments/studionet-demo-2026-11-11.json).

| Operation | Lifecycle | Execution | Expected rollback | Transaction |
|---|---|---|---|---|
| deployment | FINALIZED | SUCCESS | no | [0xebb2c02b04…](https://explorer-studio.genlayer.com/tx/0xebb2c02b04550fe1def68e1df3f3ee36bf580e4127cd16d83f5774aff777fd8a) |
| deposit_1000 | FINALIZED | SUCCESS | no | [0x7e4e5b6095…](https://explorer-studio.genlayer.com/tx/0x7e4e5b609513a8ab929013c109e289740f30590efab6b0049b983073b4e0c4c3) |
| buy_compact | FINALIZED | SUCCESS | no | [0x53aea164ba…](https://explorer-studio.genlayer.com/tx/0x53aea164bad4e2b45c54d4d084d3a13fdeabdc27d556a18ef7128d780fa8a611) |
| buy_truncated | FINALIZED | SUCCESS | no | [0xd483dcc626…](https://explorer-studio.genlayer.com/tx/0xd483dcc626a2e0fde944529d61647cd48dd2423f8a55273364eef215ad37470a) |
| buy_minor | FINALIZED | SUCCESS | no | [0xc794a3c239…](https://explorer-studio.genlayer.com/tx/0xc794a3c2394a77791634f2b2f9de201f8183fd3c9a7ad3699f62646a0b5056dc) |
| buy_outside | FINALIZED | SUCCESS | no | [0xb9718d83e2…](https://explorer-studio.genlayer.com/tx/0xb9718d83e2ca7cfe458e33cfdc392d12c28ce840be5f32b034d2a8cffab8bc54) |
| reject_under_collateralising_withdrawal | FINALIZED | ERROR | yes | [0x174ba42a55…](https://explorer-studio.genlayer.com/tx/0x174ba42a5573144bad3b5a73bd952e192bf5d5d042423a344f4d6f6007082261) |
| reject_overexposure_purchase | FINALIZED | ERROR | yes | [0x6d570cc831…](https://explorer-studio.genlayer.com/tx/0x6d570cc831fac2f07c8647ee5973f59d5db3499f120be1e833832dab56425586) |
| claim_compact | FINALIZED | SUCCESS | no | [0x1307bfb609…](https://explorer-studio.genlayer.com/tx/0x1307bfb609eb87548518cd1793ed93ebcee1041e8bb6688a6bfe93d16ce3986e) |
| claim_truncated | FINALIZED | SUCCESS | no | [0x7e1237e70f…](https://explorer-studio.genlayer.com/tx/0x7e1237e70f501096b5f957bb99d6a0626c814d7c41b7e179cf6648954f7be8d0) |
| claim_minor | FINALIZED | SUCCESS | no | [0x4e154b3124…](https://explorer-studio.genlayer.com/tx/0x4e154b312449ce9d55c8324cdfbda111b301867759e39089754e17ff16724d69) |
| claim_outside | FINALIZED | SUCCESS | no | [0x3a411581f7…](https://explorer-studio.genlayer.com/tx/0x3a411581f7aaae2811ef47ab9265380b37e68e5d33909301e91f404752a428f1) |
| reject_replay_compact | FINALIZED | ERROR | yes | [0x9dc41be645…](https://explorer-studio.genlayer.com/tx/0x9dc41be645dcca42638b79517236b6ec3530161526c28daddd46b0fbb3cedf29) |
| reject_replay_outside | FINALIZED | ERROR | yes | [0x3d78fb84d1…](https://explorer-studio.genlayer.com/tx/0x3d78fb84d15bff5d1070c89a67c54c36e9fc4deeb63dd6034db11fde5c8d2198) |
| withdraw_remaining_840 | FINALIZED | SUCCESS | no | [0x2442bf47ec…](https://explorer-studio.genlayer.com/tx/0x2442bf47ecb94a896ebcd818b89d3903ef453fee4de0180603c2f385b98526bf) |

## Claim results

| Policy | Verdict | State | Source status |
|---|---|---|---|
| compact | QUALIFYING | PAID | fetched |
| truncated | QUALIFYING | PAID | truncated |
| minor | NOT_QUALIFYING | DENIED | truncated |
| outside | NOT_QUALIFYING | DENIED | fetched |

## Scope

- Historical synthetic replay; not prospective underwriting or insurance.
- Synthetic ledger units are not GEN, a token, custody, or real payment.
- Public page metadata and content digests may drift while incident facts remain stable.
- UTC date of transactions can precede the Africa/Lagos release date by one day.
- Source commit identifies exact committed LF bytes. Tests used the equivalent CRLF working copy; hashes and newline-only equality are recorded.
- No push, repository creation, visibility change, or Portal submission.

Independent read-only verification rechecked all 15 finalized transactions, the deployed source hash, and 16 latest-final calls covering all six public views. [Audit record](../verification/studionet-independent-readback-2026-11-11.json).

One intermediate readback received a temporary HTTP 502. The saved transaction hashes were reused during recovery; no finalized write was resubmitted. Original timestamped readbacks were preserved.
