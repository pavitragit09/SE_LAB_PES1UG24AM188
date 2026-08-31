# Jira Lab 2 Report — Feature Flag & Dynamic Config Manager

## 1. Scenario

The selected scenario is **Feature Flag & Dynamic Config Manager**. The Jira project models a system for creating, configuring, targeting, evaluating, synchronizing, auditing, and reliably operating feature flags and dynamic configuration.

### Intended users
- Software Engineer
- Release Manager
- Developer Tools / IT Operations

## 2. Epics

Six epics were created:

| # | Epic |
|---|---|
| 1 | Feature Flag Management |
| 2 | Targeting & Rollouts |
| 3 | Environment Configuration |
| 4 | Feature Flag Evaluation & Audit |
| 5 | SDK Synchronization |
| 6 | Performance, Security & Reliability |

## 3. User Stories and Sprint Allocation

### Sprint 1 — 32 Story Points

| Issue | User Story | Points |
|---|---|---:|
| FFDCM-18 | Evaluate Feature Flag | 8 |
| FFDCM-7 | Create Feature Flag | 3 |
| FFDCM-10 | Configure Percentage Rollout | 5 |
| FFDCM-11 | Deterministic User Targeting | 8 |
| FFDCM-17 | Authenticate Evaluation Request | 3 |
| FFDCM-13 | Configure Environment Override | 5 |
| | **Total** | **32** |

**Sprint Goal:** Implement the core feature flag creation and evaluation workflow.

### Sprint 2 — 46 Story Points

| Issue | User Story | Points |
|---|---|---:|
| FFDCM-8 | Update Feature Flag | 2 |
| FFDCM-9 | Manage Default Flag State | 2 |
| FFDCM-12 | Apply Beta Cohort Targeting | 5 |
| FFDCM-14 | Evaluate Environment-Specific Configuration | 5 |
| FFDCM-15 | Push Real-Time Flag Updates | 8 |
| FFDCM-16 | Synchronize SDK Cache | 5 |
| FFDCM-19 | Record Evaluation Audit Log | 3 |
| FFDCM-20 | Fast and Secure Flag Evaluation | 8 |
| FFDCM-21 | Graceful SDK Fallback | 8 |
| | **Total** | **46** |

**Sprint Goal:** Complete SDK synchronization, targeting, auditing, and system reliability capabilities.

## 4. Sprint Execution

Both sprints were configured as **1-week sprints**.

Stories were demonstrated through the Scrum workflow:

**To Do → In Progress → Done**

Sprint 1 ended with all 6 stories completed.

Sprint 2 ended with all 9 stories completed.

## 5. Burndown Summary

### Sprint 1
Starting work: **32 story points**

Remaining work recorded in the Jira burndown:
**32 → 29 → 24 → 16 → 8 → 5 → 0**

The sprint finished with **0 story points remaining**.

### Sprint 2
Starting work: **46 story points**

Remaining work recorded in the Jira burndown:
**46 → 41 → 36 → 34 → 26 → 21 → 13 → 11 → 8 → 0**

The sprint finished with **0 story points remaining**.

## 6. Reflection

### What went well
The work was divided into clear epics and user stories, and story points were assigned before sprint execution. Both sprints had explicit goals and all planned work reached Done. The burndown charts provide evidence that the remaining story points reached zero in each sprint.

### What could be improved
The sprint simulation was completed in a short period, so the burndown reflects several work-completion events close together rather than a realistic day-by-day development pattern. In a real project, stories would be completed progressively throughout the week and the team would use daily Scrum meetings to identify blockers and adjust work.

### Key learning
The exercise demonstrates how Jira can be used to translate a product scenario into epics and stories, estimate work with story points, plan sprint scope, track status, complete sprints, and review progress through a burndown chart.
