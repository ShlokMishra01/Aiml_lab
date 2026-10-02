# Week 15: Quiz (10 questions, 8/10 to pass)

> Each question names the section or notebook cell it comes from. Answer, then check the key.

1. **(MCQ)** In the state-graph model, what does a **node** return? (see Concepts §"The
   state-graph mental model" and notebook cell [6])
   - (a) The full state, re-serialized from scratch.
   - (b) A partial state, only the fields the node changed, which the framework merges back.
   - (c) A string answer to print.
   - (d) Nothing; nodes mutate global variables.

2. **(MCQ)** `compute_refund(shipment_id)` in notebook cell [4] returns 10% of declared value
   when the shipment is more than 48 hours late, and 50% when more than 7 days late. A shipment
   delayed **60 hours** with declared value **$6,000** yields which outcome? (see Concepts
   §"Worked example 1")
   - (a) $0 (not late enough)
   - (b) $600, and `needs_approval = True` because it exceeds $500
   - (c) $3,000, and `needs_approval = False`
   - (d) $600, and `needs_approval = False`

3. **(MCQ)** What does `interrupt_before=["refund_approval"]` actually do? (see Concepts
   §"Human-in-the-loop" and notebook cell [8])
   - (a) It deletes the `refund_approval` node.
   - (b) It pauses the graph *before* `refund_approval` and yields control to the caller, who must resume to continue.
   - (c) It routes every ticket to `refund_approval`.
   - (d) It logs a warning but keeps running.

4. **(MCQ)** In notebook cell [10], two invocations run on the same `thread_id` (`t-1`). What
   is the observable consequence, and what does it demonstrate? (see Concepts §"Checkpoints,
   resume, and time-travel")
   - (a) The second run crashes because the thread already exists.
   - (b) The `history` list accumulates across runs, durable conversation memory as state.
   - (c) The second run resets `history` to empty.
   - (d) The two runs are isolated and share nothing.

5. **(MCQ)** Which of these is the *correct* reason to adopt LangGraph rather than keep a
   Week-14 hand-rolled loop? (see Concepts §"Framework judgment")
   - (a) It makes every agent faster.
   - (b) You need durable, auditable, cyclic control flow, checkpoints, resume, HITL.
   - (c) It removes the need for tools.
   - (d) It is always less code.

6. **(Short answer)** Name three distinct fields in `AgentState`, and for each state which node
   writes it. (see Concepts §"The state-graph mental model" table and notebook cell [2])

7. **(Short answer)** A checkpoint stores more than the final answer. List the three things a
   checkpoint records, and explain which one makes "resume after a crash" different from "start
   over." (see Concepts §"Checkpoints, resume, and time-travel")

8. **(MCQ)** In `route_after_intent`, an intent of `"escalate"` returns which key, and that key
   maps to which node in `add_conditional_edges`? (see notebook cell [6] and [8])
   - (a) `"tool"` → `tool_node`
   - (b) `"refund_approval"` → `refund_approval_node`
   - (c) `"escalate"` → `escalate_node`
   - (d) `"generate"` → `generate_node`

9. **(Short answer)** The per-node table (notebook cell [14]) reports `calls`, latency, and
    tokens per node. Why is it a mistake to measure only the final answer's latency, and which
    node do you expect to dominate *output* tokens in a tracking-heavy sample? (see Concepts
    §"Worked example 2")

10. **(MCQ)** When LangGraph is **not installed**, what does the notebook do so the per-node
    table and routing accuracy still print? (see notebook cell [0] and [8])
    - (a) It raises and stops.
    - (b) A manual runner walks the *same node functions* in the *same graph order*.
    - (c) It skips all the cells.
    - (d) It installs LangGraph automatically.

---

## Answer key

1. **(b)**: A node returns only the fields it changed; the framework merges them back into the
   shared state. Returning the full state or mutating globals defeats the explicit-state
   contract.

2. **(b)**: 60 hours > 48h but < 7 days → the 10% branch: $6,000 × 0.10 = $600, which exceeds
   the $500 threshold, so `needs_approval = True`.

3. **(b)**: `interrupt_before` pauses before the named node and yields control; the run only
   proceeds after a resume (e.g. `Command(resume={"approved": True})`).

4. **(b)**: Two runs on the same thread share checkpointed state, so `history` accumulates.
   That is durable conversation memory, not a hidden variable.

5. **(b)**: LangGraph earns its complexity for durable, auditable, cyclic control flow. The
   other options are false (it's more machinery, not automatically faster or shorter).

6. Any three, e.g. `intent` (written by `intent_node`), `shipment_id` (by `intent_node`),
   `refund_amount` and `needs_approval` (by `intent_node`), `tool_result` (by `tool_node`),
   `final_answer` (by `generate`/`escalate`/`refund_approval`), `history` (by every node),
   `escalated` (by `escalate_node`). Full credit for three correct field→writer pairs.

7. A checkpoint records (1) the full current **state** (all fields), (2) the **thread id**, and
   (3) the **position in the graph**. The *state + position* is what makes resume different:
   you continue from the exact node and values where you stopped, rather than re-running from
   the first node with an empty state.

8. **(c)**: `"escalate"` → `escalate_node`; that is the human-handoff branch of the conditional
   edge.

9. Measuring only the final answer hides *where* the time and tokens go, a slow tool node and a
   slow generate node are different problems with different fixes. In a tracking-heavy sample,
   `tool` dominates output tokens because it emits the JSON tracking/policy results.

10. **(b)**: The notebook defines a `manual_run` fallback that walks the same nodes in the same
    order, so the per-node table and routing accuracy print regardless of whether LangGraph is
    installed.
