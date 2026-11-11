# Portal submission draft

Status: DRAFT ONLY — not submitted. Strict demo evidence is complete.

## Note (801 characters)

Underwriters share a synthetic reserve: premiums and losses change share value, and open coverage limits both purchases and withdrawals. Validators independently interpret public incidents; code derives qualification and a once-only payout. Strict canonical consensus compares every stored evidence/result field. StudioNet: a complete major incident paid 100 units; truncated evidence stayed UNCERTAIN with balances unchanged and backing reserved; minor/outside-window incidents paid nothing. All 16 transactions finalized (11 successes, 5 expected rollbacks), blocking over-exposure, under-collateralising withdrawals and claim replays. Final accounting: 1,000 deposits + 40 premiums = 100 payout + 840 withdrawn + 100 reserved capital. Historical demo; synthetic units, no custody or real insurance.

## Separate evidence entries

- GenLayer Explorer Contract: https://explorer-studio.genlayer.com/address/0x90eC3dd7D0B644f817fF84320502e6cb63808Cb9
- GitHub Repository: https://github.com/JWattjr/parametric-coverage-pool
- Source: https://github.com/JWattjr/parametric-coverage-pool/blob/92e7800ca6c52eaece182f550baade6d33a41c6c/contracts/parametric_coverage_pool.py
- Release Manifest: https://github.com/JWattjr/parametric-coverage-pool/blob/main/deployments/studionet-strict-release-2026-11-11.json
- claim_compact: https://explorer-studio.genlayer.com/tx/0xbeee12d85f852cd43c845eb9f02353c5416ed4e156efedc61ee2da1e6356c925
- claim_truncated: https://explorer-studio.genlayer.com/tx/0xb56684af91010e2809cd30d293dabfb5f1dd20e58aea36ea34c9427768c5a940
- reject_overexposure_purchase — EXPECTED FAILURE: https://explorer-studio.genlayer.com/tx/0x6108d6c7f7de0142d485ba727a3b9085a1abf4bae262cb6c51b1ea040ccb8495
- reject_withdrawal_of_uncertain_backing — EXPECTED FAILURE: https://explorer-studio.genlayer.com/tx/0xf2afdba950a734f596b205a0203a9728694bc54f4fcc92184000067d31bff0f1
- reject_replay_compact — EXPECTED FAILURE: https://explorer-studio.genlayer.com/tx/0x555b947c2a1ac5ca43beae2a625b74f91cb7124dbb405cdc7eebc79c70621131

Select `GenLayer Explorer Contract` for the contract-address entry where supported. The direct contract link has been browser-verified; repository/source/transaction links do not replace it. Final Portal submission requires explicit user approval.
