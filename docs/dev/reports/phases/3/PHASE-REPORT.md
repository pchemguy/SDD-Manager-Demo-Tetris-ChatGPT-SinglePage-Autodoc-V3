# Phase 3 review

## Outcome

Phase review checked against its PLAN/SPEC scope. Source baseline 668ed1544278c597f211544f7158ad27c35d8e1e plus this task-owned diff.

## Code review and verification

Complete phase Engine/controller/presentation code review found no unresolved S3 finding; four initial delivery closures audited with no exceptions; packaged 0.3.0 full suite passed 97 tests in 110.75s; Prettier and independent artifact inventory/hash gates passed; milestones 3.1 and 3.2 closed/read back; exact-tip CI, explicit main integration and release remain coordinator gates. Reviewed owned implementation, callers, lifecycle/error/resource paths and regression coverage. No unresolved contract violation remains for the included scope.

## TODO

None.

## Pending publication

Task commit/push, issue and milestone closure require readback. Phase integration/release remain subsequent coordinator operations.

## Phase code review

Inspected complete board/feasibility/landing/movement/rotation/lock paths: strict settlement and traversable placement remain separate; ordinary pieces stop at their first obstacle; penetrators select the greatest legal anchor below them, never erase settled cells and cannot move into a state without a future legal landing. Contact derives from the shared landing; activation releases old support only when the landing becomes lower. Hold cannot discard penetrator status. Four clears award after settlement through cap three; restart resets. Active and ghost penetrators are white, with no regular shading; settled/held/preview/ordinary pieces retain the non-white palette. Actual keyboard play earns/spends/locks a bonus in both protocols/browsers. No unresolved code/contract finding remains.

## Coverage and limits

Prior classic and modern rules remain in the full packaged suite. Native Windows/headed OS-window behavior remain outside verified scope. Settings, persistence and results/file exchange remain intentionally pending later phases. Exact phase-tip CI, explicit main integration and downloaded-release checks are subsequent coordinator gates.

## Hosted-check recovery P3-F1

Final initial CI 41320906295 failed one existing Firefox/file held-Z timing assertion (96 passed); integration/release held. The same failure reproduced locally even with a polling DOM assertion; the phase remained Playing. The isolated case and instrumented runs could pass, so it was not treated as an engine diagnosis. Inspection found test clock installation occurred after initial application navigation, followed by reload, replacing a running animation clock. The controlled-page fixture now installs before the first app navigation; other real-time tests keep their original fixture. Ten repeated Firefox/file cases passed in 25.56s with this setup. An additional pure held-Z test verifies unchanged exact 999/1000ms locking. No production source changed for this recovery. Review issue 28 and milestone 10 were reopened; full candidate checks and reclosure remain pending.

P3-F1 further diagnosis: pre-navigation fixture changes and DOM polling were insufficient; later local suites failed in Firefox HTTP as well. Read-only snapshot tracing captured performance time at 2000ms followed by about 130ms (another run 55ms) at input, with no following game animation frames during clock advancement. A no-reload clock bridge also failed. Temporary tracing, repeated-case parameters and clock fixtures were removed. Browser scenarios now retain native animation time and wait for observable state transitions; deterministic domain checks retain exact timing assertions. No accepted gameplay requirement or browser/protocol coverage was removed and no production timing code changed. Final native-time checks/publication remain pending.

P3-F1 final local recheck: all 68 affected unit/modern/penetrator/completion checks passed using native animation time in 169.08s. Transition waits were then aligned with animation frames to observe new pieces promptly; all 16 affected modern/penetrator packaged browser cases passed in 70.33s across both protocols/browsers. Exact engine boundaries remain 999/1000ms; no production source changed. Full final hosted CI and review reclosure remain subsequent gates.
