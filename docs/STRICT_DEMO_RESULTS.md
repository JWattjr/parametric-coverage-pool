# Strict StudioNet demo results

The strict StudioNet demo passed. The complete major incident paid 100 units; truncated evidence returned UNCERTAIN without balance changes and kept its policy OPEN. The complete minor and outside-window incidents paid nothing. All 16 transactions finalized: 11 successful executions and five expected rollbacks. A partial withdrawal returned 840 units while 100 capital remained locked against 100 open exposure; withdrawing that backing was rejected.

Source commit: `92e7800ca6c52eaece182f550baade6d33a41c6c`, pushed and anonymously verified before deployment.

[GenLayer Explorer Contract](https://explorer-studio.genlayer.com/address/0x90eC3dd7D0B644f817fF84320502e6cb63808Cb9) — browser-verified contract address, creator and deployment on StudioNet.

[Public GitHub repository](https://github.com/JWattjr/parametric-coverage-pool). [Deployed source](https://github.com/JWattjr/parametric-coverage-pool/blob/92e7800ca6c52eaece182f550baade6d33a41c6c/contracts/parametric_coverage_pool.py). [Full release manifest](../deployments/studionet-strict-release-2026-11-11.json).

| Operation | Finality | Execution | Expected rollback | Transaction |
|---|---|---|---|---|
| deployment | FINALIZED | SUCCESS | no | [0x8ad1833a51...](https://explorer-studio.genlayer.com/tx/0x8ad1833a51017fb942574a9689aea0928166e0b62cf807f261c1e39ec339b600) |
| deposit_1000 | FINALIZED | SUCCESS | no | [0x2e703fe04b...](https://explorer-studio.genlayer.com/tx/0x2e703fe04b364e3a0e0e73e38649f576c188e1493bf76fab5b2cf8b261330d96) |
| buy_compact | FINALIZED | SUCCESS | no | [0x8687d70efb...](https://explorer-studio.genlayer.com/tx/0x8687d70efb5f02162bbd24de772d7b7e1d435ac111183cabcfa66a9de5c8e439) |
| buy_truncated | FINALIZED | SUCCESS | no | [0x09e35dbfc4...](https://explorer-studio.genlayer.com/tx/0x09e35dbfc4d279a15dcb8421c41dc92df81eb379af70e41a80cad05c11cfce64) |
| buy_minor | FINALIZED | SUCCESS | no | [0x6ca4937363...](https://explorer-studio.genlayer.com/tx/0x6ca4937363ba78e0deddb75b4081921d59ee2264517d72760b9dd76bccc5dbe3) |
| buy_outside | FINALIZED | SUCCESS | no | [0xdb65c2bfe7...](https://explorer-studio.genlayer.com/tx/0xdb65c2bfe76fda62ae3c374a14e07b6882a4baf061db691f6262f69515d2824c) |
| reject_under_collateralising_withdrawal | FINALIZED | ERROR | yes | [0x4b2a06faf3...](https://explorer-studio.genlayer.com/tx/0x4b2a06faf3c579d0f26e366261eaef05faaae6545e85d0caeda66cc8afdc9247) |
| reject_overexposure_purchase | FINALIZED | ERROR | yes | [0x6108d6c7f7...](https://explorer-studio.genlayer.com/tx/0x6108d6c7f7de0142d485ba727a3b9085a1abf4bae262cb6c51b1ea040ccb8495) |
| claim_compact | FINALIZED | SUCCESS | no | [0xbeee12d85f...](https://explorer-studio.genlayer.com/tx/0xbeee12d85f852cd43c845eb9f02353c5416ed4e156efedc61ee2da1e6356c925) |
| claim_truncated | FINALIZED | SUCCESS | no | [0xb56684af91...](https://explorer-studio.genlayer.com/tx/0xb56684af91010e2809cd30d293dabfb5f1dd20e58aea36ea34c9427768c5a940) |
| claim_minor | FINALIZED | SUCCESS | no | [0xe531489d32...](https://explorer-studio.genlayer.com/tx/0xe531489d3247b3c97a10f47d90cfa6331c3b4fc6f25dffe5ea140fb19c1d1881) |
| claim_outside | FINALIZED | SUCCESS | no | [0x4579ae4775...](https://explorer-studio.genlayer.com/tx/0x4579ae477519c3ac500173c0e06549efa223d24c783c18155639d03dcab83a69) |
| reject_replay_compact | FINALIZED | ERROR | yes | [0x555b947c2a...](https://explorer-studio.genlayer.com/tx/0x555b947c2a1ac5ca43beae2a625b74f91cb7124dbb405cdc7eebc79c70621131) |
| reject_replay_outside | FINALIZED | ERROR | yes | [0xddcd31e281...](https://explorer-studio.genlayer.com/tx/0xddcd31e28184a9a3ebf7e52caec473d7d4ae309208522bafee2914cc2b698716) |
| withdraw_free_840 | FINALIZED | SUCCESS | no | [0xa96737251b...](https://explorer-studio.genlayer.com/tx/0xa96737251b56c6493d60a9d6aea7ebdd5820a36daa70935c4d3e7ac79318b1bb) |
| reject_withdrawal_of_uncertain_backing | FINALIZED | ERROR | yes | [0xf2afdba950...](https://explorer-studio.genlayer.com/tx/0xf2afdba950a734f596b205a0203a9728694bc54f4fcc92184000067d31bff0f1) |

| Policy | Verdict | Policy state |
|---|---|---|
| compact | QUALIFYING | PAID |
| truncated | UNCERTAIN | OPEN |
| minor | NOT_QUALIFYING | DENIED |
| outside | NOT_QUALIFYING | DENIED |

Final conservation: `1000 deposits + 40 premiums = 100 payout + 840 withdrawals + 100 capital`. Open exposure is 100, free capital zero, and 106 shares remain backing the uncertain policy.

[Independent audit](../verification/studionet-strict-independent-readback-2026-11-11.json) rechecked all 16 receipts, exact source bytes and 16 latest-final calls across every public view.

## Readiness gates

| Gate | Result |
|---|---|
| technical readiness | PASS |
| distinctiveness | PASS |
| evidence readiness | PASS |

- Historical synthetic replay, not real insurance, custody, or a native/token transfer.
- 100 units remain reserved for the OPEN uncertain policy until its claim deadline or later permissionless expiry; this is intended fail-closed backing.
- Incident-specific public API responses can change; strict full-result comparison rejects differing evidence rather than accepting approximate agreement.
- Local distinctiveness review includes the identified same-week forecast project, not proof of all Portal cohort submissions.
- Learned review guidance is not official criteria or a promise of points.
- Repository publication is authorised; final Portal submission is not and has not occurred.
