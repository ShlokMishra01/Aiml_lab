# Week 16: Quiz (10 questions, 8/10 to pass)

> Each question names its source section or notebook cell. Answer, then check the key.

1. **(MCQ)** In the MCP architecture, which role runs the LLM and initiates connections, and
   which role exposes the capabilities? (see Concepts §"MCP: one protocol instead of N
   integrations")
   - (a) Host runs the LLM and initiates; server exposes capabilities.
   - (b) Server runs the LLM; host exposes capabilities.
   - (c) Client runs the LLM; server initiates connections.
   - (d) Host and server are the same thing.

2. **(MCQ)** MCP messages are JSON-RPC 2.0 over two transports. Which pair is correct, and
   which one does the notebook use? (see Concepts and notebook 01 cell [8])
   - (a) stdio and Streamable HTTP; the notebook uses **stdio**.
   - (b) WebSocket and gRPC; the notebook uses WebSocket.
   - (c) stdio and gRPC; the notebook uses gRPC.
   - (d) HTTP/1.1 and HTTP/2; the notebook uses HTTP/2.

3. **(MCQ)** Which of these is a **primitive** an MCP server can expose, and what is the
   ZoroLogistics example given in the README? (see Concepts §"MCP: one protocol instead of N
   integrations")
   - (a) A "tool", a model-invoked function such as `track_shipment(shipment_id)`.
   - (b) A "channel", a messaging surface such as WebChat.
   - (c) A "checkpoint", a saved graph state.
   - (d) A "thread", a conversation key.

4. **(MCQ)** The single most important reason to prefer the **supervisor / manager-worker**
   pattern first is: (see Concepts §"Multi-agent: the first lesson is restraint")
   - (a) it is always the fastest.
   - (b) it centralizes control, decompose, delegate, synthesize, while remaining conservative and debuggable.
   - (c) it needs no context isolation.
   - (d) it never makes bad handoffs.

5. **(MCQ)** MCP and A2A are complementary, not competing. Which statement is correct? (see
   Concepts §"MCP vs. A2A")
   - (a) MCP is for agent-to-agent delegation; A2A is for tools.
   - (b) MCP connects one agent to tools/data; A2A lets agents delegate to agents across systems.
   - (c) A2A replaces MCP in all cases.
   - (d) They are the same protocol with different names.

6. **(Short answer)** The notebook's `team_run` charges a fixed `+200` tokens on top of the
   specialists' work. What do those 200 tokens represent, and why would an A/B that *omitted*
   them be unfair to the single agent? (see notebook 02 cell [8] and Concepts §"How it breaks")

7. **(MCQ)** In the 10-ticket A/B, the notebook's `justification` concludes the team is *not*
   justified for this slice. Which combination of observations drives that conclusion? (see
   notebook 02 cell [13])
   - (a) Equal accuracy, but the team spends more tokens on handoffs + synthesis with no accuracy gain.
   - (b) The team is more accurate but slower.
   - (c) The single agent is less accurate and cheaper.
   - (d) The team routes nothing correctly.

8. **(Short answer)** `list_tools()` in the MCP client returns the tool schema for
   `track_shipment`. Write what that schema's `required` array contains, and explain what the
   model does with the schema when deciding to call. (see notebook 01 cell [10] and Concepts
   §"MCP: one protocol instead of N integrations")

9. **(MCQ)** The ground-truth mapping in notebook 02 maps the ticket category `"billing"` to
   which specialist route? (see notebook 02 cell [2])
   - (a) `tracking`
   - (b) `docs`
   - (c) `refunds`
   - (d) `escalate`

10. **(Short answer)** Name two *benefits* and two *costs* of multi-agent systems, and state the
    Anthropic rule that decides when the split is worth it. (see Concepts §"Multi-agent: the
    first lesson is restraint")

---

## Answer key

1. **(a)**: The host runs the LLM and initiates connections; the client (inside the host) holds
   connections; the server exposes capabilities.

2. **(a)**: stdio (local subprocess) and Streamable HTTP (remote). The notebook launches the
   server as a stdio subprocess via `StdioServerParameters`.

3. **(a)**: A tool is a model-invoked function, e.g. `track_shipment(shipment_id)`. Resources
   and prompts are the other two primitives; channels/checkpoints/threads are not MCP
   primitives.

4. **(b)**: Supervisor centralizes control (decompose → delegate → synthesize) and is the
   conservative, debuggable default. It still bottlenecks and can still misroute, so (a)/(d)
   are false.

5. **(b)**: MCP is the capability layer (agent ↔ tools/data); A2A is the interop layer (agent
   ↔ agent). They're complementary.

6. The +200 tokens model the supervisor handoff and the synthesis step. Omitting them would
   undercount the team's real cost, the single agent has no handoff, so the comparison would
   unfairly favor the team. (Full credit for naming "supervisor handoff + synthesis overhead"
   and "it makes the team look cheaper than it is.")

7. **(a)**: Equal accuracy but more tokens/cost from handoffs + synthesis with no accuracy gain
   means the team is not justified for this slice.

8. `"required": ["shipment_id"]`. The model reads the schema (name, properties, required) as the
   contract for *how* to call the tool, what argument to supply and what type it must be,
   which is the same "description is prompt engineering" idea now enforced by the protocol.

9. **(c)**: `CAT_TO_ROUTE` maps `billing` (and `refund`, `damage`) to `refunds`.

10. Benefits (any two): context isolation, role specialization, parallelism, failure isolation.
    Costs (any two): coordination overhead, latency, tokens, bad handoffs. The rule: start with
    one well-prompted agent plus good tools, add workflows before agents, and split only when a
    measured benefit outweighs the cost.
