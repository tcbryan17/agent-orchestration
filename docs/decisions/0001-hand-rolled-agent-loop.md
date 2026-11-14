# 0001. Hand-rolled agent loop on the `anthropic` SDK

- **Status:** Accepted
- **Date:** 2026-11-14

## Context
The project shows a supervisor delegating to specialist agents, with every step traced. It is also a learning project: the owner needs to explain the agent loop, tool dispatch, handoffs and termination in interviews and customer conversations, so those parts must be visible and owned.

## Options considered
- **Claude Agent SDK**: the full Claude Code harness as a library (built-in file/bash/web tools, subagents, hooks). Fast to build with, but the loop, context management and delegation are hidden inside it. It is also built for coding and filesystem agents, not business workflows.
- **Tool Runner** (`client.beta.messages.tool_runner`): the SDK runs the request → execute tools → repeat cycle over tools we define. Less code, but we don't write the `stop_reason` handling or the tool-result assembly, which are the parts worth learning.
- **Manual loop on the Messages API**: we write the `while stop_reason == "tool_use"` loop, the tool dispatch, and the event emission ourselves.
- **A framework (LangGraph, CrewAI, etc.)**: extra abstractions and dependencies, and it would hide the same parts.

## Decision
A manual loop on the plain `anthropic` Python SDK, with tools we define (plus Anthropic server tools where they fit, e.g. web search).

## Why
Every concept the project demonstrates sits in code we own: stop reasons, parallel tool results, error results, handoffs, context isolation, budget checks, and tracing at the exact point each event happens. We give up speed of building and the Tool Runner's built-in conveniences (compaction, retries). Knowing what it would have done for us is part of the lesson.

## Consequences
- More code to test. A fake client lets CI test the loop without API calls or a key.
- Handling `refusal`, `max_tokens` and `pause_turn` is our job.
- Revisit if the project grows into long-running sessions where compaction or managed sandboxes matter more than visibility.
