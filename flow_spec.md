# Use-Case Flow Specification

## Use Case: Evaluate Feature Flag

**Primary Actor:** Software Engineer (via Client SDK)
**Related Requirement:** FR-001, FR-003, FR-004
**Includes:** Authenticate Request
**Extended by:** Apply Beta Cohort Targeting

### Preconditions
- The feature flag being requested exists in the system and has at least one configured environment.
- The client SDK holds a valid, active API key for the target environment.
- Targeting rules (percentage rollout and/or environment overrides) have been configured for the flag by a Release Manager.

### Postconditions
- A boolean flag state has been returned to the calling client SDK.
- The evaluation event (flag key, user context, environment, resulting state, timestamp) has been recorded in the audit log.

### Main Success Scenario
1. The Client SDK sends a flag evaluation request to the API, supplying the flag key, environment, and user context (User ID and any relevant attributes).
2. The system authenticates the request using the supplied API key **«include» Authenticate Request**.
3. The system retrieves the flag's configuration, including its default state and rollout rules.
4. The system computes a deterministic hash of the User ID and compares it against the configured rollout percentage to determine cohort membership.
5. The system checks whether an environment-specific override exists for the requesting environment and applies it if present.
6. The system returns the resulting boolean flag state to the Client SDK.
7. The system logs the evaluation details to the audit trail.

### Alternate Flow — A1: Environment Override Active
- **Trigger:** At step 5, the system finds an active environment override for the requesting environment.
- **A1.1:** The system bypasses the percentage-rollout computation from step 4 and instead applies the override value directly.
- **A1.2:** The system returns the override value to the Client SDK.
- **A1.3:** The system logs the evaluation, tagging it as "override-applied" in the audit trail.
- The flow then rejoins the main scenario at step 7 (logging) and completes normally.

### Extension — Apply Beta Cohort Targeting («extend»)
- **Trigger:** At step 4, the user context indicates the user belongs to the registered Beta cohort, regardless of computed rollout percentage.
- The system overrides the percentage-based result and returns an enabled state for that user, then rejoins the main flow at step 6.
