# Security Policy

AI Engineering Lab is a training repository: it contains educational notebooks and
guides, not production services. Still, learners execute this code with real
credentials, so we take a few things seriously.

## Reporting a vulnerability

If you find something that could put a learner's cloud account, API key, or data
at risk, a notebook pattern that leaks secrets, an insecure default in a guide,
please report it privately to **info@zorost.com** (or via GitHub's private
vulnerability reporting). We will acknowledge within 5 business days.

## Rules we follow (and you should too)

1. **No secrets in the repo.** Never commit API keys, tokens, or workspace URLs.
   Use the `.env.example` pattern; each notebook documents which variable it needs.
2. **Least privilege.** Cloud setup guides (Weeks 18 to 24) always start from
   minimal IAM roles / scoped permissions, never admin.
3. **Blast radius.** Agent guides (Weeks 12 to 17) mark commands that touch
   production data, spend money, or are irreversible with a ⚠️ banner.
4. **Untrusted content.** Prompt-injection and jailbreak material is educational
   and always paired with defenses (knowledge-base 04).
5. **Cost guardrails.** Every paid-platform guide tells you to set a budget
   alert before running anything.

## For contributors

If you add a notebook that calls a paid API, it must (a) read the key from an
environment variable, (b) print an estimated cost before running heavy loops,
and (c) include a kill switch note.

---
© 2026 Zorost Intelligence LLC · https://zorost.com
