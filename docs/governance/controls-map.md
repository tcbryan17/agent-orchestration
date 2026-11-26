# Controls map

*Each row maps one framework requirement to the concept guide(s) that address it and to the evidence in the repo. Status starts as "planned". Change it only when the evidence exists. Framework wording is paraphrased; check the source text before quoting. This is not a compliance claim.*

Concept IDs: C1 agent loop, C2 tool dispatch, C3 tool schema, C4 untrusted tool output, C5 supervisor handoff, C6 run state, C7 budget guardrails, C8 reviewer loop, C9 human approval, C10 content policy, C11 audit and provenance, C12 eval rubric.

| Control ID | Framework | Requirement in plain words | Repo evidence (file/test/log) | Status |
|---|---|---|---|---|
| CM-001 (example) | NIST AI RMF GOVERN | Roles, responsibilities and risk tolerance are written down. Concepts: C7, C9 | `docs/governance/risk-register.md`; ADR for budget caps (not yet written) | planned |
| CM-002 | NIST AI RMF GOVERN | Policies and accountability for the AI system are documented (owner, approval, review). C9, C11 | to fill | planned |
| CM-003 | NIST AI RMF MAP | Intended use, context and limits are documented. C3, C5 | `docs/governance/system-card.md` | planned |
| CM-004 | NIST AI RMF MAP | Risks and impacts are identified for the context of use. C10 | `docs/governance/risk-register.md` | planned |
| CM-005 | NIST AI RMF MEASURE | The system is tested against defined metrics, including a baseline. C12 | to fill (Phase 7) | planned |
| CM-006 | NIST AI RMF MEASURE | Behaviour is traced so it can be assessed later. C1, C6, C11 | to fill | planned |
| CM-007 | NIST AI RMF MANAGE | Identified risks are treated, with limits that stop runaway behaviour. C7, C8, C10 | to fill | planned |
| CM-008 | NIST AI RMF MANAGE | There is a response to incidents and a way to stop or roll back. C9, C11 | to fill | planned |
| CM-009 | NIST AI 600-1 confabulation | Claims in outputs are checked against sources; unsupported claims are rejected. C8, C11, C12 | to fill | planned |
| CM-010 | NIST AI 600-1 information security | Prompt injection and tool misuse are limited. C2, C4 | to fill | planned |
| CM-011 | NIST AI 600-1 information integrity | Outputs are labelled and traceable; records cannot be silently altered. C11 | to fill | planned |
| CM-012 | NIST AI 600-1 value chain and component integration | Third-party models and data are tracked and changes are noticed. C1, C12 | `docs/governance/suppliers.md` | planned |
| CM-013 | NIST AI 600-1 intellectual property | Copyrighted source text is not copied into outputs. C10 | to fill | planned |
| CM-014 | EU AI Act Art. 50 (transparency) | Users are told they are dealing with AI, and AI-generated content is marked. C10 | to fill (Phase 6 and 8) | planned |
| CM-015 | EU AI Act Art. 12 (logging; voluntary here, as it formally applies to high-risk systems) | Events are logged automatically over the system's life. C1, C6, C11 | to fill | planned |
| CM-016 | EU AI Act Art. 14 (human oversight; voluntary here) | A person can oversee, intervene and stop the system. C9 | to fill | planned |
| CM-017 | EU AI Act Art. 15 (accuracy, robustness, cybersecurity; voluntary here) | Accuracy is measured and the system resists errors and attacks. C2, C4, C7, C12 | to fill | planned |
| CM-018 | ISO/IEC 42001 clause 6.1 (risk assessment; clause numbers to verify) | AI risks are assessed and treated through a defined process. C7, C8 | `docs/governance/risk-register.md` | planned |
| CM-019 | ISO/IEC 42001 AI system impact assessment (clause number to verify) | The impact on people and society is assessed. | to fill | planned |
| CM-020 | ISO/IEC 42001 Annex A: lifecycle and event logging | Annex A control number to verify against the standard. C1, C6, C11 | to fill | planned |
| CM-021 | ISO/IEC 42001 Annex A: data quality and provenance | Annex A control number to verify against the standard. C5, C11 | `docs/governance/data-card.md` | planned |
| CM-022 | ISO/IEC 42001 Annex A: information for interested parties | Annex A control number to verify against the standard. C10 | `docs/governance/system-card.md` | planned |
| CM-023 | ISO/IEC 42001 Annex A: human oversight and responsible use | Annex A control number to verify against the standard. C9 | to fill | planned |
| CM-024 | ISO/IEC 42001 Annex A: third-party relationships | Annex A control number to verify against the standard. | `docs/governance/suppliers.md` | planned |
| CM-025 | OWASP LLM Top 10: prompt injection (LLM01; verify numbering for the current edition) | Untrusted text cannot take over the agent. C4 | to fill | planned |
| CM-026 | OWASP LLM Top 10: excessive agency (verify numbering) | Agents only have the tools and powers they need. C2, C3, C5 | to fill | planned |
| CM-027 | GDPR / UK GDPR Art. 5(1)(c) minimisation | Only the personal data needed is processed. C2, C4, C5 | `docs/governance/gdpr.md` | planned |
| CM-028 | GDPR / UK GDPR Art. 17 erasure | A person's data can be deleted on a valid request, including from logs. C11 | `docs/governance/gdpr.md` | planned |
| CM-029 | GDPR / UK GDPR Art. 30 record of processing | Processing activities are recorded. | `docs/governance/gdpr.md` | planned |
