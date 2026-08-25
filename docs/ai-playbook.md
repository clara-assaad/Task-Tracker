# Personal AI Coding Playbook

The decisions below reflect how I currently want to use AI in my coding workflow.

## 1. When I Reach for AI First

- **Task type:** Planning and brainstorming, repetitive or straightforward coding tasks, and debugging.
- **Situation or trigger:** I use AI when I understand the context but want to save time, explore possible approaches before deciding, or narrow down an error with many possible causes.
- **Desired outcome:** I want AI to help me explore options, accelerate work I understand, and narrow down solutions while I retain the final decision and verify the result.

## 2. When I Do Not Reach for AI

- **Task type:** Simple tasks I can confidently handle myself, or sensitive and high-impact work where an incorrect change could affect other parts of the system.
- **Risk or boundary:** I do not share passwords, credentials, private IDs, usernames, or other private information with AI. For high-impact work, I may use AI for assistance, but I do not give it uncontrolled authority over changes.
- **Reason:** I use AI when it adds value, not simply because it is available. Doing simple work myself keeps my skills active. Sensitive or high-impact work requires greater control because mistakes could create more work than AI saves or introduce privacy and security risks.

## 3. My Non-Negotiables

- **Security boundary:** I will never share sensitive or private information with AI, including passwords, usernames, credentials, private IDs, or other confidential data.
- **Quality requirement:** Before accepting AI-generated work, I check that it matches the task and context and produces the result I intended. I prefer reviewing a draft or proposed change before approving it.
- **Ownership principle:** I am responsible for understanding and reviewing AI-generated work and making the final decision. I will not approve something only because the AI says it is correct.

## 4. My Review Rules

- **What I verify:** I check that the result matches my request, the logic makes sense, related files and functions still work together, and nothing important was invented or omitted.
- **How I validate:** I use evidence appropriate to the task, such as running the code, using the terminal, sending API requests, checking the health endpoint, running tests, or inspecting the frontend. If something fails, I use that evidence to refine the solution.
- **What requires extra review:** Changes affecting multiple files, core logic, APIs, security-sensitive behavior, infrastructure, or other areas where a small mistake could have a wider impact.

## 5. What I Am Still Figuring Out

- **Open question:** How much context and detail to provide so the response is useful without becoming too long or mixing unrelated concerns.
- **Workflow to evaluate:** How to manage longer, multi-step AI-assisted tasks without wasting context or tokens.
- **Skill to develop:** Breaking larger tasks into smaller prompts and selecting enough context to receive focused answers without losing control of the workflow.

## Decision Card

- **For a new feature I reach for:** Browser-based AI such as ChatGPT or Claude for planning and discussion, then Copilot in VS Code for straightforward implementation.
- **For a code review I reach for:** Gemini or Claude in the terminal to inspect the code and repository context.
- **For debugging I reach for:** Gemini or Claude in the terminal to narrow down possible causes and suggest fixes I can test.
- **For infrastructure I reach for:** Codex, especially when the task requires understanding multiple repository files, configuration, Docker, or CI context.
- **I will never paste:** Sensitive or private information, such as passwords, credentials, private IDs, or other confidential data, into an AI tool.
- **My one rule is:** Always test and verify AI-generated work before accepting it.
