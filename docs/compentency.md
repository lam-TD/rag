https://docs.google.com/spreadsheets/d/1yeO6Z9HIb1jyG59JuY-RuayC-PuiHiKXJ6zdrYuThT0/edit?usp=drivesdk



# Research Spike: Evaluate migration from gpt-5-mini to gpt-5.4-mini

## Context

We are planning to migrate the current OpenAI model from `gpt-5-mini` to `gpt-5.4-mini`. Before estimating and implementing the main migration task, we need to evaluate compatibility, implementation impact, behavior changes, cost, latency, and rollout risks.

## Goal

Produce a technical assessment that allows the team to estimate the main migration task with clear scope, assumptions, risks, and recommended implementation approach.

## Scope

- Review current OpenAI integration.
- Identify all usages of model name and model configuration.
- Compare current model behavior/configuration with `gpt-5.4-mini`.
- Validate API parameter compatibility.
- Run a small evaluation using representative prompts/use cases.
- Assess quality, structured output stability, citation behavior, latency, and cost.
- Recommend migration approach and estimate range.

## Out of Scope

- Do not implement production migration.
- Do not change production model configuration.
- Do not refactor unrelated LLM architecture unless required for the estimate.
- Do not tune all prompts in this task; only identify required prompt changes.

## Research Questions

1. Can `gpt-5.4-mini` replace `gpt-5-mini` through configuration only?
2. Are there parameter compatibility issues?
3. Are changes needed for reasoning effort, max output tokens, structured output, tools, or streaming?
4. Which files/modules/tests are affected?
5. Does output quality or format change on key use cases?
6. What are the cost and latency differences?
7. What is the safest rollout and rollback strategy?
8. What is the estimated effort for the main migration task?

## Deliverables

1. Compatibility report.
2. Code impact analysis.
3. Evaluation result summary.
4. Cost and latency comparison.
5. Risk matrix.
6. Recommended migration approach.
7. Estimate proposal for the main implementation task.

## Acceptance Criteria

- [ ] Current OpenAI integration flow is documented.
- [ ] All affected config/code/test areas are listed.
- [ ] Parameter compatibility is checked.
- [ ] At least 20 representative test cases are evaluated.
- [ ] Old model vs new model results are compared.
- [ ] Risks and rollback strategy are documented.
- [ ] Main migration estimate is provided with assumptions.