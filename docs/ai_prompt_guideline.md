# Team Prompt Guidelines

## 1. Purpose

This guideline helps team members write clear, consistent, and reusable prompts when working with AI assistants such as Cline, Codex, Claude Code, ChatGPT, or similar tools.

The main goals are:

- Improve the quality of AI-generated output
- Reduce vague or unclear prompts
- Standardize how team members ask AI for help
- Support code review, refactoring, debugging, testing, documentation, and architecture discussion
- Build a shared prompt library for common engineering tasks
- Make AI usage safer and easier to review

---

## 2. Core Prompt Standard

Every prompt should include five key parts:

```text
Role + Context + Task + Constraints + Output Format
```

### 2.1 Role

Tell the AI what role it should act as.

Example:

```text
Act as a senior backend engineer reviewing a FastAPI project.
```

### 2.2 Context

Explain the project, technology stack, current situation, and related files.

Example:

```text
This project uses FastAPI, PostgreSQL, SQLAlchemy, Alembic, and pytest.
The current task is to refactor the document upload API.
```

### 2.3 Task

Clearly describe what you want the AI to do.

Example:

```text
Review the upload service and suggest improvements for error handling and testability.
```

### 2.4 Constraints

Define rules the AI must follow.

Example:

```text
Do not change the public API response schema.
Do not introduce new dependencies.
Follow the existing repository structure.
```

### 2.5 Output Format

Tell the AI how to return the answer.

Example:

```text
Return your answer in this format:
1. Summary
2. Problems found
3. Recommended changes
4. Code examples
5. Test cases to add
```

---

## 3. Default Prompt Template

Team members can use this as the default template:

```text
Act as a [role].

Context:
- Project: [project name]
- Tech stack: [frameworks, libraries, database, tools]
- Current module/file: [file or feature name]
- Current problem: [describe the issue]

Task:
[Clearly describe what you want AI to do]

Constraints:
- [Constraint 1]
- [Constraint 2]
- [Constraint 3]

Expected output:
- [Format requirement]
- [Level of detail]
- [Include code examples? Yes/No]
- [Include tests? Yes/No]

Important:
- Ask questions if the requirement is unclear.
- Explain trade-offs before suggesting major changes.
- Do not make assumptions without stating them.
```

---

## 4. Best Practices

### 4.1 Be specific, not general

Bad prompt:

```text
Improve this code.
```

Better prompt:

```text
Review this FastAPI service and suggest improvements for readability, dependency injection, error handling, and unit test coverage.
```

---

### 4.2 Give enough context

Bad prompt:

```text
Fix this bug.
```

Better prompt:

```text
The upload API returns 500 when the file size is over 10MB.
Expected behavior: return 400 with a clear error message.
Please inspect the validation logic and suggest a fix.
```

---

### 4.3 Define boundaries

Bad prompt:

```text
Refactor this module.
```

Better prompt:

```text
Refactor this module to improve readability and testability, but do not change the database schema, API response format, or existing function names.
```

---

### 4.4 Ask for concise reasoning and trade-offs

Good prompt:

```text
Explain your recommendation briefly and mention the trade-offs.
```

Avoid:

```text
Explain every single thought step by step.
```

Better standard:

```text
Provide a concise explanation of why this solution is better.
```

---

### 4.5 Always ask for tests when code changes are involved

Example:

```text
After suggesting the code change, also suggest unit tests and integration tests that should be added.
```

---

### 4.6 Ask AI to identify risks

Example:

```text
Before changing the code, identify possible risks, backward compatibility issues, and edge cases.
```

---

## 5. Common Prompt Types

### 5.1 Code Review Prompt

```text
Act as a senior software engineer.

Review the following code for:
- Readability
- Maintainability
- Error handling
- Security risks
- Performance issues
- Testability

Do not rewrite the entire code unless necessary.

Return:
1. Overall assessment
2. Issues found
3. Recommended improvements
4. Suggested tests
```

---

### 5.2 Refactoring Prompt

```text
Act as a senior backend engineer.

Refactor this code to improve:
- Separation of concerns
- Dependency injection
- Naming
- Testability

Constraints:
- Do not change external behavior
- Do not change API response format
- Do not introduce new libraries

Return:
1. Refactoring plan
2. Updated code
3. Explanation of changes
4. Tests to update or add
```

---

### 5.3 Bug Investigation Prompt

```text
Act as a debugging assistant.

Context:
[Describe the feature and expected behavior]

Problem:
[Describe the actual error]

Logs/Error:
[Paste logs]

Task:
Find the most likely root cause and suggest a fix.

Return:
1. Possible causes
2. Most likely cause
3. Suggested fix
4. How to verify
5. Regression tests to add
```

---

### 5.4 Test Generation Prompt

```text
Act as a QA automation engineer.

Generate tests for this feature.

Context:
- Framework: pytest
- API: FastAPI
- Database: PostgreSQL
- Existing test style: [describe or paste example]

Task:
Create test cases for normal cases, edge cases, and failure cases.

Return:
1. Test scenarios
2. Test data
3. pytest code examples
4. Notes about mocks/fixtures
```

---

### 5.5 Architecture Review Prompt

```text
Act as a senior system architect.

Review this design for:
- Scalability
- Maintainability
- Security
- Observability
- Failure handling
- Testing strategy

Context:
[Describe the system]

Return:
1. Summary
2. Strengths
3. Weaknesses
4. Risks
5. Recommended improvements
6. Decision recommendation
```

---

### 5.6 Documentation Prompt

```text
Act as a technical writer.

Create or improve documentation for this feature.

Context:
- Target audience: [developer / QA / business user / manager]
- Feature: [feature name]
- Existing documentation: [paste or describe]

Task:
Write clear documentation that explains the purpose, usage, important rules, and examples.

Return:
1. Overview
2. When to use
3. How it works
4. Examples
5. Common mistakes
6. Notes for maintainers
```

---

### 5.7 Pull Request Review Prompt

```text
Act as a senior engineer reviewing a pull request.

Context:
- Project: [project name]
- PR goal: [describe goal]
- Changed files: [list files]
- Risk level: [low / medium / high]

Task:
Review the PR and identify issues before merging.

Check:
- Correctness
- Code quality
- Testing
- Security
- Performance
- Backward compatibility

Return:
1. Merge recommendation
2. Blocking issues
3. Non-blocking suggestions
4. Missing tests
5. Questions for the author
```

---

## 6. Prompt Quality Checklist

Before submitting a prompt to AI, team members should check:

```markdown
## Prompt Checklist

- [ ] Did I define the AI role?
- [ ] Did I provide enough project context?
- [ ] Did I clearly describe the task?
- [ ] Did I include constraints?
- [ ] Did I specify the expected output format?
- [ ] Did I mention what should not be changed?
- [ ] Did I ask for tests if code is changed?
- [ ] Did I include logs/errors if debugging?
- [ ] Did I ask the AI to explain risks or trade-offs?
- [ ] Did I verify the AI output before applying it?
```

---

## 7. Rules for Using AI Output

Team members should follow these rules when using AI-generated results:

### 7.1 Do not copy AI code directly without review

The developer is still responsible for the final code.

### 7.2 AI suggestions must follow project conventions

If AI output conflicts with team standards, team standards win.

### 7.3 AI-generated code must be tested

At minimum, add or update related unit tests.

### 7.4 AI should not decide architecture alone

Major design decisions need team review.

### 7.5 Do not paste sensitive data

Avoid sharing:

- API keys
- Access tokens
- Customer data
- Production credentials
- Private business data
- Sensitive logs
- Internal security information

### 7.6 Ask AI to explain trade-offs

This helps the developer understand the impact before applying changes.

### 7.7 Use AI as an assistant, not an authority

AI can suggest, but the developer must verify.

---

## 8. Common Mistakes

### 8.1 Prompt is too vague

Example:

```text
Fix this code.
```

Problem: AI does not know what kind of fix is expected.

---

### 8.2 No context

Problem: AI does not know the project structure, conventions, or business rules.

---

### 8.3 No constraints

Problem: AI may change too much, introduce unnecessary dependencies, or break existing behavior.

---

### 8.4 No expected output format

Problem: The answer may become too long, too short, or hard to use.

---

### 8.5 No verification

Problem: Developer applies AI output without checking correctness.

---

### 8.6 Ignoring tests

Problem: Code is changed but no test is added.

---

### 8.7 Sharing sensitive information

Problem: Developer may expose secrets, customer data, credentials, or production information.

---

## 9. Suggested Guideline Document Structure

Use this structure for the final team guideline document:

```markdown
# Team Prompt Guidelines

## 1. Purpose

## 2. When to Use AI Assistants

## 3. Standard Prompt Structure
- Role
- Context
- Task
- Constraints
- Output Format

## 4. Prompt Template

## 5. Prompt Examples
- Code review
- Refactoring
- Bug fixing
- Test generation
- Documentation
- Architecture review
- Pull request review

## 6. Best Practices

## 7. Common Mistakes

## 8. Security and Privacy Rules

## 9. AI Output Review Checklist

## 10. Prompt Library
```

---

## 10. Recommended Team Standard

For the first version, the team should start with this simple rule:

```text
Every prompt should include:
Role + Context + Task + Constraints + Output Format
```

Then the team can gradually build a shared prompt library for common tasks:

- Code review
- Refactoring
- Bug fixing
- Test generation
- API design
- Database migration
- Documentation
- Security review
- Performance review
- Pull request review

This will help team members use AI more consistently and make AI-assisted work easier to compare, review, and improve.

---

## 11. Reference Links

Last reviewed: 2026-06-25

Use these references when improving the team prompt standard, creating prompt templates, or training team members.

### 11.1 Official Prompt Engineering References

#### OpenAI

- [OpenAI API Docs — Prompt Engineering](https://developers.openai.com/api/docs/guides/prompt-engineering)  
  Recommended use: General prompt engineering concepts, instruction design, model behavior, and evaluation mindset.

- [OpenAI Help Center — Best Practices for Prompt Engineering with OpenAI API](https://help.openai.com/en/articles/6654000-best-practices-for-prompt-engineering-with-openai-api)  
  Recommended use: Practical prompting tips and common prompt patterns.

#### Anthropic Claude

- [Anthropic Claude Docs — Prompt Engineering Overview](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview)  
  Recommended use: Prompt quality improvement, success criteria, evaluations, role prompting, examples, and prompt iteration.

- [Anthropic Engineering — Effective Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)  
  Recommended use: Understanding context management for AI agents, especially when using tools that work across multiple files or long-running tasks.

#### GitHub Copilot

- [GitHub Docs — Prompt Engineering for GitHub Copilot Chat](https://docs.github.com/en/copilot/concepts/prompting/prompt-engineering)  
  Recommended use: Prompting standards for code explanation, code generation, code review, and coding assistant workflows.

- [GitHub Docs — Best Practices for Using GitHub Copilot](https://docs.github.com/en/copilot/get-started/best-practices)  
  Recommended use: Responsible AI coding practices, checking AI output, giving context, and using AI for tests, debugging, and refactoring.

#### Cline

- [Cline Docs — Cline Rules](https://docs.cline.bot/customization/cline-rules)  
  Recommended use: Creating project rules, workspace rules, and conditional rules to keep AI behavior aligned with team standards.

---

### 11.2 Recommended Reading for AI Coding Assistants

These references are useful for understanding practical benefits, risks, and limitations of AI-assisted coding.

- [Practices and Challenges of Using GitHub Copilot: An Empirical Study](https://arxiv.org/abs/2303.08733)  
  Recommended use: Understanding real-world usage patterns, benefits, and limitations of AI coding assistants.

- [Demystifying Practices, Challenges and Expected Features of Using GitHub Copilot](https://arxiv.org/abs/2309.05687)  
  Recommended use: Understanding developer expectations and common challenges when using Copilot-like tools.

- [Exploring Prompt Engineering Practices in the Enterprise](https://arxiv.org/abs/2403.08950)  
  Recommended use: Understanding how prompt engineering works in enterprise environments and why iteration is important.

- [Understanding Prompt Management in GitHub Repositories: A Call for Best Practices](https://arxiv.org/abs/2509.12421)  
  Recommended use: Understanding prompt management, prompt duplication, formatting consistency, and maintainability risks.

---

### 11.3 How the Team Should Use These References

The team should not copy these references directly into every prompt. Instead, use them to improve the team standard.

Recommended usage:

- Use OpenAI and Anthropic references to improve general prompt quality.
- Use GitHub Copilot references to improve coding-related prompt workflows.
- Use Cline Rules to convert repeated prompt instructions into reusable project rules.
- Use research papers for management-level reports, training, or internal AI adoption reviews.
- Review these links every 3 to 6 months because AI assistant features and best practices change quickly.
