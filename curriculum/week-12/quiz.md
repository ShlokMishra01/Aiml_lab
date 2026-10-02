# Week 12: Quiz (10 questions, 8/10 to pass)

Answer from memory first, then check the key. Each question names the section or cell it
tests, so a miss tells you exactly what to re-read.

## Questions

1. **(MCQ)** A model and a harness are not the same thing. Which statement captures the
   division of labor correctly? (see Concepts, "What a harness is")
   - A) The harness makes the model smarter by adding more parameters.
   - B) The model supplies reasoning; the harness supplies agency (loop, tools, context, verifiers).
   - C) The harness is just an editor; the model does all the work.
   - D) The model supplies agency; the harness supplies reasoning.

2. **(MCQ)** You are working in OpenCode. Which file does it read automatically as persistent
   project instructions? (see Concepts, "Rules files")
   - A) `CLAUDE.md`
   - B) `opencode.json`
   - C) `AGENTS.md`
   - D) `.cursor/rules/*.mdc`

3. **(Short answer)** In the Week-12 `SPEC.md`, the single most important line is the
   *refused tradeoff*. What does it do that the rest of the spec does not? (see Concepts,
   "Worked example 1")

4. **(MCQ)** Which item belongs in the "stays out" column of the managed-context table?
   (see Concepts, "Managed context")
   - A) The failing test output
   - B) `SPEC.md`
   - C) The `.env` file with API keys
   - D) The specific source file being edited

5. **(Short answer)** The notebook's final cell (cell §5) prints one number. What is it
   called, and exactly what does it count? (see notebook cell §1 and §5)

6. **(MCQ)** A spec is *the definition of done the loop closes against*, which means it is
   primarily… (see Concepts, "Planning vs execution")
   - A) documentation for future human readers
   - B) a prompt to make the model more polite
   - C) an executable statement of what "correct" means, checked by the verifier
   - D) a replacement for writing tests

7. **(Short answer, with numbers)** A harness run uses 40,000 input tokens and 10,000 output
   tokens at $3.00/1M input and $15.00/1M output. Show the arithmetic and give the total cost
   in dollars. (see Concepts, "Worked example 2")

8. **(MCQ)** A blast-radius rule calibrates autonomy… (see Concepts, "Verifiers, SPEC.md, and
   blast radius")
   - A) once per session, at login
   - B) per action, based on how much damage the action can do if wrong
   - C) based on how much you like the model
   - D) only for database writes, never for file reads

9. **(Short answer)** Name any two numeric columns of the comparison worksheet and what each
   one records. (see notebook cell §3)

10. **(MCQ)** In OpenRouter, the `:free` model variant is best used for… (see Concepts,
    "OpenRouter and cost control")
    - A) production throughput with a service-level guarantee
    - B) testing plumbing (auth, config, prompts) before paying for real throughput
    - C) fine-tuning your own model
    - D) replacing the harness's permission system

## Answer key

1. **B.** The harness adds the loop, tools, context management, and verifiers; the model only
   reasons. That is why two harnesses on the same model differ, they differ on those four.

2. **C.** OpenCode auto-loads `AGENTS.md` (project + global). `CLAUDE.md` is Claude Code;
   `.cursor/rules/*.mdc` is Cursor; `opencode.json` is config, not instructions.

3. **It forbids the agent from resolving ambiguity by guessing.** The rest of the spec says
   *what* to build; the refused tradeoff is the one place you say, in advance, where the agent
   is *not allowed* to guess, here, it must never invent an ETA for a missing/NaN shipment.

4. **C.** Secrets (`.env`, keys) stay out of the window, anything pasted in can be logged,
   summarized, or repeated. Spec, failing test output, and the specific source file go *in*.

5. **The harness-readiness score, an integer 0 to 3.** It is `sum(1 for n in ('claude','opencode','dsh') if shutil.which(n))`, the count of the three coding harnesses installed and on your PATH.

6. **C.** The spec is the executable definition of done the verifier checks against, not
   human documentation, and not a substitute for writing the tests (the spec *names* them).

7. **$0.27.** Input: 40,000 × $3.00 / 1,000,000 = $0.12. Output: 10,000 × $15.00 / 1,000,000 =
   $0.15. Total = $0.12 + $0.15 = $0.27.

8. **B.** The leash is per action: reading a scratch file is nearly free to get wrong; writing
   production data is not, the same agent gets different leashes on the two.

9. **Any two of** `plan_quality_1to5` (how close the plan was to your spec), `tokens_used`,
   `cost_usd`, `tests_green_first_try` (whether tests passed first try), `diff_files_changed`,
   `code_quality_1to5`.

10. **B.** `:free` models are zero-cost but rate-limited and lower-availability, use them to
    prove auth/config/prompts work, then swap to a paid slug for real work.
