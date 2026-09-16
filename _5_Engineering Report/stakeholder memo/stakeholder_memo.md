# Stakeholder Memo: AfyaPlus AI Service Platform

**Date:** 16 September 2026  
**Decision requested:** Approve a controlled pilot, subject to the conditions below.

## Executive recommendation

**GO for a limited, supervised pilot; NO-GO for unsupervised production use at this stage.** The platform has a credible technical foundation for testing with a small group of authorised coordinators. Before wider rollout, the live agent workflow, clinical response quality, and operational monitoring must be verified against the conditions in this memo.

## What was built

The project delivers an integrated service platform for secure AI-assisted triage and clinic logistics:

- A FastAPI triage service with typed Pydantic request models, field constraints, health checks, JWT login, protected routes, and clear handling for invalid, unauthorised, rate-limited, and unavailable-upstream requests.
- Docker and Docker Compose packaging for repeatable deployment of the triage and agent services.
- An MCP logistics server backed by clinic data, exposing stock checks, clinic directory access, delivery-route planning, and delivery ETA estimation.
- An authenticated agent API that connects user questions to the logistics tool layer, with request tracing and bounded input length.
- Supporting evidence of API, MCP, containerisation, and version-control workflows in the engineering report.

## Highest-value component

**The secured triage API is the highest-value component.** It establishes the trust boundary that makes the rest of the platform usable in an operational setting: identity is verified before protected actions, inputs are constrained, requests are rate-limited, service health is probeable, and upstream model failures are surfaced instead of being presented as successful answers. This foundation reduces the risk of exposing an AI capability as an uncontrolled endpoint and provides a clear path for audit and incremental integration.

## Key risk and mitigation

**Risk: unreliable or unsafe AI/agent output could influence clinical or logistics decisions.** The current agent integration still contains a placeholder return path rather than a completed live model response, and even a live model may produce incomplete, incorrect, or stale advice. The logistics route is also explicitly a nearest-neighbour heuristic, not a guaranteed-optimal route.

**Mitigation:** keep the pilot human-in-the-loop; restrict use to decision support rather than autonomous clinical action; require an authorised coordinator to review and approve outputs; validate responses against approved clinical and inventory rules; log user, trace, model, and tool outcomes; monitor upstream failures and rate-limit events; and complete end-to-end testing of the live agent path before production approval. Label heuristic route results and require confirmation before dispatch.

## Conditions for progression

1. Replace the agent placeholder with a tested live integration and document its model, prompt, and failure behaviour.
2. Complete representative tests for authentication, validation, rate limiting, upstream failure, MCP tools, and response quality.
3. Define clinical escalation, data-retention, access-review, and incident-response procedures.
4. Run a time-boxed pilot with named users, approved clinics, human approval of every recommendation, and measurable success/safety thresholds.

**Decision:** Proceed to the controlled pilot only after conditions 1–2 are demonstrated; defer production expansion until all four conditions are met.
