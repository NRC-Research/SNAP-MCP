# SNAP-MCP Code Guide

Developer reference for the SNAP-MCP codebase.

---

## Handoff — 2026-08-08

No code changed this session. The subject was **this repository being public**, and what had
already been published in it.

### What was found

An audit of the handoff sections above turned up material that should not have been in a public
repo: a named licensee plant model together with an assertion of a modeling defect in it, names
and PR numbers belonging to private repositories, provisioning role paths, a self-hosted model
endpoint name, host topology including the route to the development VM, and a narrative of a
vendor plugin jar being modified. A repo-wide sweep found three more instances outside
`CODE_GUIDE.md` — the companion MELCOR README carried the fullest provisioning paths of all.

Deliberately **kept**: the weak-agent autonomy narrative. Demonstrating that a weak local model
can drive these tools unaided is the point of the project, not an incidental disclosure.

### What was done

- **PR #12** redacted all of it, replacing identifiers with generic phrasing. Every engineering
  lesson survives — the vessel junction GRAV finding, the provisioning allowlist asymmetry, the
  shared-home versus host-local `/opt` trap, the jar integrity rules.
- **History was rewritten** (`git filter-repo`) and force-pushed: `main` `7d7407d` → `5090e2a`,
  50 → 48 commits. Two doc-only commits became empty once the doc versions collapsed to one and
  were pruned; their text survives in the current file. Verified 0 pattern hits across all
  branch history.
- **Both deployed checkouts were reset** and garbage-collected. Note the trap: `git reset --hard`
  cleans tracked files but leaves `__pycache__/*.pyc`, which embeds docstrings — an unredacted
  copy of a docstring survived there, gitignored and invisible to a source grep. Clear bytecode
  caches on every machine that imported the module.

### What a rewrite does NOT fix

**Force-pushing branches does not touch `refs/pull/*`.** GitHub creates those refs when a PR is
opened, they survive merge, branch deletion, and force-push, and nothing you control can delete
them. Because they stay reachable, the pre-rewrite commits are never garbage-collected — the old
diffs still render on PR pages #1-#12. Only GitHub Support can remove them.

**GitHub Support ticket #4646440** was filed for that purge (severity: security exposure; First
Changed Commit `6838376` → `655935f`, i.e. the root commit — the material was present from the
initial public release). Until Support acts, the redaction is incomplete. The risk to watch is
their policy of removing sensitive data only and not "non-sensitive data"; with no credentials
involved they may decline. The argument made in the ticket is that credential rotation is not an
available mitigation here, so removal is the only one.

Verify closure with a 404 on the pre-rewrite commit via the REST API, and an empty
`git ls-remote origin 'refs/pull/*'`.

### Guardrails added (PR #13, PR #15)

`main` now carries a ruleset: PR + 1 approval, no force-push, no deletion, and a required
`redaction-scan` check. Org and repo admins retain `always` bypass, so it stops accidents and
everyone else, but is advisory for an admin acting deliberately.

- `.githooks/pre-commit` blocks staged content matching a denylist; `.githooks/commit-msg`
  rejects AI attribution in commit messages (message only — the docs discuss AI tooling as
  subject matter, which is legitimate).
- `.github/workflows/redaction-check.yml` runs the same scan on every PR. Hooks are per-clone and
  never travel with a push, so the workflow is the backstop for machines that skipped
  installation and for merges made in the web UI.
- Secret scanning **push protection** was enabled (it was off). It only catches credentials —
  it would never have caught these identifiers, which is why the custom check exists.

**The denylist is deliberately not in this repo.** A file listing the strings being kept out
would republish them. It lives at `~/.config/snap-mcp/redaction-patterns.txt` (mode 600, and note
`/home` is NFS-shared, so it is visible from any host sharing that home) and in the
`REDACTION_PATTERNS` Actions secret. Neither the hook nor the workflow ever prints a matched
line — Actions logs on a public repo are world-readable, so echoing a match would leak it as
effectively as committing it. Both report `file:line` only.

**Both fail closed**, and this was not theoretical: the first hook revision used `mapfile`, absent
from the bash 3.2 macOS ships. It errored and *allowed* the commit it should have blocked — a
guardrail that looks installed and does nothing. Now verified on bash 3.2 and 5.1 with negative
controls, and the CI check was verified to actually fail on a violation using a benign sentinel
pattern (never a real identifier, which would have published it).

### Where to pick up

- **Ticket #4646440 is the only open item.** Chase it; verify rather than trusting the
  confirmation, since GC can lag.
- **Hooks are installed on the Mac clone and the development VM only.** Any third machine that
  commits needs the pattern file plus one run of `scripts/install-hooks.sh`.
- **The denylist is only as good as its 17 entries.** Add new categories as they appear, and
  re-run `gh secret set REDACTION_PATTERNS` so CI and hooks stay in sync.
- The commit-msg hook described in global instructions as "installed in this repository" was
  **not** actually present before this session. It is now, via `.githooks`.

---

## Handoff — 2026-08-06

### What was actually wrong

Tool-using `crush run` invocations had been returning **exit 0 with empty output** while a
no-tool prompt worked. None of it was this codebase's quality, and none of it was the crush
version — two things that had been blamed in turn.

- **A hyphen in the MCP server key** (client-side, `crush.json`). crush derives each tool's name
  from the server key, so `"snap-trace"` yields `mcp_snap-trace_create_model`; the model emits
  the hyphen back as an **underscore**, crush answers `tool not found`, the agent retries ~10x
  and exits 0 having printed nothing. **No log line names the cause.** `ssh` was never affected
  because its key has no hyphen. Fixed in the running config, in both provisioning roles, and in
  the internal skills repo that had been publishing the broken config.
- **`_sync_wrapper` refused instead of waiting** (`5383d05`..`12cc3f2`). Tools already called
  `snap_env.wait_ready()` in their bodies, but the wrapper raised `_INITIALIZING_MSG` first —
  so the two mechanisms fought and the in-body wait was dead code. The message told the caller
  to poll `snap_status()` and retry, which **an LLM agent cannot do**: no clock, no sleep tool,
  ten turns spent polling. Now waits on the init thread (`SNAP_MCP_STARTUP_WAIT`, default 90 s)
  and raises only on a genuinely stuck start. **The protection from `e31c7e4` is intact** — a
  waiting call is parked on an event, so it cannot reach the gateway or trip `reset()` mid-init,
  and unlike a refusal it does not come straight back as a retry.
- **The provisioning allowlist is static and crush silently enforces it.** Six shipped tools
  were absent from the images in use: `get_model_options`, `get_vessel_junctions`,
  `set_vessel_junction_grav`, `compute_vessel_junctions`, `apply_vessel_junctions`, `run_trace`.
  The provisioning role clones `SNAP-MCP@main` with `force: true`, so **code flows in
  automatically while the allowlist does not** — that asymmetry is how the gap opened, and it
  will reopen the same way.

### Changed here

- **PR #7** — `list[str] = None` / `int = None` → `T | None` on `get_vessel_tables(tables)`,
  `list_components(component_type)`, `set_vessel_junction_grav(junction_cc)`. The old form makes
  the schema advertise a non-null type with a `null` default, which strict clients reject.
- **PR #8** — the wait above, plus `path` accepted as an alias for `med_file_path`/`trcin_path`
  (everyone guesses `path`; the validation error then names a field the caller never used, which
  reads as a broken tool), plus server instructions that no longer write tool names bare (clients
  expose them prefixed) and that state a clean `validate_model` is **not** proof a deck runs.
- **PR #9** — `list_models` is summary-first. The registry is append-only and never pruned (160+
  rows on the dev box); it returned every one. Now returns the 20 newest with a true `total`,
  plus `limit`, `name_contains`, `detail='full'`.

### Performance reality — it is decode speed, not a hang

`EXIT=124` with complete output is **not** a shutdown hang; it is a timeout firing during
generation. Measured against the self-hosted devstral endpoint, elapsed time tracks *output
size* at roughly **12 tokens/sec**: 16 B → 20 s, 387 B → 28 s, 15.9 KB → 332 s (twice). The
tools are fast — an 819-component plant model opens in **5.8 s** and `get_vessel_junctions`
answers in **0.3 s**.

Three things that look like a stall and are not: a goroutine parked in
`chunkedReader.beginChunk` (waiting for the next token, ~80 ms apart), an unanswered HTTP
request in crush's debug log (still generating — it replays standalone in 7 s), and output
looking complete while the process runs on (earlier turns streamed; a later turn is decoding).
`Connection: close` changed nothing (333 s vs 332 s), which rules out connection reuse — though
the model server *does* close idle keep-alive connections at exactly **5 s** (uvicorn default)
while MCP tool calls routinely idle longer.

**So prompt shape is the cost driver, not tool speed.** `"report exactly what it returns"`
against `list_models` cost 332 s; `"report only how many models exist"` cost 20 s. Guidance for
analysts is in the internal snap-trace skills README ("Asking well").

### Verified

```
crush run --quiet "Open the SNAP model file .../<a large plant deck>.med and report how many
                   vessel junction edges have GRAV of zero, and how many models are now in
                   the registry. Be brief."
→ "36 vessel junction edges have GRAV of zero. There are 162 models in the registry."   (22 s)
```

Every vessel junction edge in that deck reads zero, which is ground truth for it — a defect
invisible to `find_component()` and to SNAP's own validation (SNAP-issues#130).

### Where to pick up

- **An image rebuild is pending** for the provisioning fix, so freshly built images do not carry
  it yet. Confirm the rebuild has run before treating a new image as fixed.
- **Watch the checkout, not just the deploy.** The deployed checkout was found **9 commits behind
  `origin/main`**, and a redeploy from it silently shipped without `run_trace` or the
  vessel-junction tools. Pull first, then grep the deployed tree for the tools you expect.
- `mcp-ssh-go` is **healthy**. A one-shot `printf | server` test exits 1 with
  `server is closing: EOF` — normal for MCP Go SDK servers when stdin closes. Do not conclude
  from that test that a server is broken.
- Remaining agent-side friction is devstral's own reliability: the same task phrased two ways
  either answers in 2 model calls or loops ten times and stops with empty content. The tools are
  no longer what stands in the way.

---

## Handoff — 2026-05-30

### Milestone reached

**A weak local model (devstral, via crush) built a complete, VALID single-loop PWR
primary TRACE model end-to-end through the snap-trace MCP tools, with no human
intervention** — correct components + connections, `validate_model` 0 errors, and it
saved the deck itself (`~/test-ai/dev-crush.med`, also `/tmp/dev-crush.med`). The goal
was never "produce a valid model" — it was "make the MCP forgiving enough that a weak
agent produces one itself." That is now demonstrated.

### What this session changed (all on `main`, pushed)

Driven by watching where devstral failed, then making each failure impossible or
self-explanatory. Most-impactful first:

- **`is_connection_broken` no longer misreads Java errors as a dead gateway** (`f136acf`).
  It matched the substring `"GatewayConnection"`, present in the `at py4j.GatewayConnection.run`
  frame of EVERY `Py4JJavaError` traceback — so a routine Java/modeling error (e.g. a bad
  `connect_components` `setJun2`) reset a *healthy* gateway on every failed call. devstral
  makes many imperfect calls, so it looked like the gateway broke constantly; it never did.
  Now only true network errors (Py4JNetworkError, connection refused, broken pipe) count.
- **`connect_components` auto-resolves the target junction slot** (`b5da3e2`). The slot is the
  TARGET's junction label, not the source's — agents always got it wrong, looping on
  `InvalidFaceException`. Now BREAK/FILL→`[JUN1] Inlet`, pipe→free end; a wrong/blank value is
  corrected (`slot_note`), and a no-free-junction target returns a clear actionable error
  ("a pipe cannot connect both ends to the same target…") instead of a raw Py4J trace.
- **Real in-process gateway recovery** (`b614e81`, `567c1c9`, `388406c`, `e1000dc`, `b46ad38`):
  on a genuine break, `reset()` kills the old JVM once, `shutdown()`s SNAP's `__MODEL_EDITOR__`
  singleton, and `find_plugin` relaunches MEBatch in the same process; `get_model()` reloads each
  model from its autosaved `.med`, so an agent's `model_id` survives a restart. Do NOT kill the
  in-flight relaunch or evict snap/py4j modules — that was the wedge. ("TRACE already loaded" in
  the MEBatch log is benign — appears on every launch.)
- **Gateway serialized** (`e31c7e4`, `e1000dc`): a single `_GATEWAY_LOCK` serializes
  all tool calls (the Py4J socket is not thread-safe; FastMCP runs sync tools on a thread pool).
  Tools originally *failed fast* while `not is_ready()`; they now **wait** on the init thread
  (`SNAP_MCP_STARTUP_WAIT`, default 90 s) and only raise if startup genuinely never completes.
  The protection is unchanged — a waiting call is parked on an event, so it still cannot reach
  the gateway or trip `reset()` mid-init — but "poll snap_status and retry" was an instruction
  no LLM agent could follow, and it made the server unusable from crush/devstral.
- **Multi-tenant MEBatch** (`6d3a5a0`, `77b0f79`): startup and `reset()` no longer `pkill -f MEBatch`
  (killed other crush/Copilot/Claude tenants' JVMs); they reap orphans / own-only.
- **Weak-agent forgiveness**: property "did you mean" + real settable names on unknown-prop errors
  (`cb32af0`); `review_model` structural flags (`995925b`); VESSEL `name`→`ctitle`; y-angle
  full-circle snap-to-360.
- **New read/review tools**: `get_pipe_edges`, `get_pipe_cells`, `get_vessel_tables`, `review_model`
  (`02fc679`, `9572e99`) — for reviewing existing/imported decks. **Tool count is now 27.**
- **Diagnostics**: server logs to `~/.snap_trace/server.log` and logs the real exception + tool
  + args on a gateway break (`fb5b357`) — invaluable; the `is_connection_broken` root cause came
  straight from it.

### Image provisioning

Both the Linux and Windows images install snap-trace via an Ansible role that clones
`SNAP-MCP@main` with `force: true` on every build → **code fixes flow in automatically**.
The one manual step is the **static crush allowed-tools list** carried in each role (crush won't
call a tool not in the list). It was missing `set_pipe_ics`, `check_loop_closure`,
`export_check_report` plus the 4 new tools — now updated to all 27 in both. **Whenever a tool is
added/removed, update both allowlists.**

### Where to pick up

- snap-trace + the recovery/forgiveness work is solid; both crush (devstral) and Claude/Copilot
  drive it cleanly. Pending from earlier: the MELCOR-mirror task (see 2026-05-24 below).
- If revisiting devstral autonomy, run crush-vpc on the development VM and watch
  `~/.snap_trace/server.log` + the model `.med` growth; the next weak-agent friction will show
  there. Keep the loop: drive the agent → see where the tool fails it → make the tool forgiving.
- Note: `crush-vpc` had an unrelated startup break this session (Catwalk catalog shipped Bedrock
  `us.anthropic.*` models v0.60.0 rejects); fixed by `CATWALK_URL`→a local clean catalog in the
  root-owned wrapper. See memory `reference-crush-vpc-catwalk-fix`.

---

## Handoff — 2026-05-28

### Where to pick up

**State:** snap-trace and snap-melcor are both working on **the development VM** and wired into
**two MCP clients** — GitHub Copilot CLI (new this session) and crush. All 15 snap-trace tools
were smoke-tested green against the live build (no version-API gaps).

**Open / next task (carried from 2026-05-24, still pending):** Build the MELCOR mirror of
`~/test-ai/vessel-test.inp` via snap-melcor — see the 2026-05-24 handoff below for the
`crush-vpc` recipe and the model scale-up blocker. Copilot CLI is now an
alternative driver (uses GitHub's `claude-opus-4.6`, independent of the model hosting cluster),
so the MELCOR-mirror task can be run through Copilot without scaling up the cluster.

### Host / install topology (important — caused a wrong-path detour this session)

- The login host and the development VM are **different hosts** that share **`/home` over a
  network filesystem**, while **`/opt` is host-local** — so `/opt/snap` exists only on the
  development VM. A shared home directory makes the two look identical until an `/opt` path is
  involved. Always run/test SNAP on the development VM, not the login host.
- **Two SNAP installs, use the right one per server:**
  - `/opt/snap/python` — TRACE plugin **4.7.0**, has `snap.codes.trace.new_model()`. **snap-trace.**
  - `~/snap/python` — OLDER TRACE 4.5.2 (no `new_model`); has MELCOR plugin 2.7.1. **snap-melcor only.**
  - Pointing snap-trace at `~/snap/python` → `create_model` fails with
    `module 'snap.codes.trace' has no attribute 'new_model'`.

### MCP client config

**Copilot CLI** (`~/.copilot/mcp-config.json`; manage with `copilot mcp add|list|get`;
non-interactive `copilot --allow-all-tools -p "..."`):
```jsonc
"snap-trace":  { "type":"local","command":"python3.12",
                 "args":["/home/user/SNAP-MCP/mcp_server.py"],
                 "env":{"SNAP_PYTHON_PATH":"/opt/snap/python"}, "tools":["*"], "timeout":60000 }
"snap-melcor": { "type":"local","command":"python3.12",
                 "args":["/home/user/SNAP-MCP/snap-melcor/mcp_server.py"],
                 "env":{"SNAP_PYTHON_PATH":"/home/user/snap/python",
                        "PYTHONPATH":"/home/user/SNAP-MCP/snap-melcor:/home/user/snap/python"},
                 "tools":["*"], "timeout":60000 }
```
**crush** (`~/.config/crush/crush.json`, MCP under top-level `"mcp"`): snap-trace env corrected
back to `/opt/snap/python` this session (snap-melcor unchanged at `~/snap/python`).

### Plugin jar integrity (resolved)

The vendor's TRACE plugin jar is signed, and a modified copy will not load — TRACE fails with
`PluginNotFound: 'TRACE'` and `snap_status` stays `ready:false`. **Do not modify or rebuild the
plugin jar**; it is not a supported path. Use the Py4J reflection path the MCP already uses.

Two operational notes that cost time here:

- Keep a pristine copy of the vendor jar alongside the installed one, so the original can be put
  back without a reinstall.
- Make sure the restored jar is readable by the account running SNAP. An unreadable jar surfaces
  as `plugin_version: null` rather than as an obvious permission error, which is easy to
  misdiagnose as a plugin problem.

Healthy state after recovery: cold start `ready:true`, `snap_plugin_version:"4.7.0"`.

### What was completed this session

- Registered snap-trace + snap-melcor in Copilot CLI on the development VM; verified `create_model`,
  `melcor_status` end-to-end.
- Corrected `SNAP_PYTHON_PATH` for snap-trace (Copilot + crush) to `/opt/snap/python`.
- Smoke-tested all 15 snap-trace tools (create/schema/add ×3/set/set_pipe_ics/connect ×2/
  get_connections/list/get/validate/export/save) — all pass, `validate_model` 0 errors/0 warnings
  (confirms the Java-reflection validation paths work on the live signed jar).
- Diagnosed and recovered the plugin jar loading failure (above).

---

## Handoff — 2026-05-24

### Where to pick up

**Immediate next task:** Run `crush-vpc` on the development VM (as target user) and ask it to use the **snap-melcor** MCP tools to build a MELCOR mirror of the TRACE input deck at `~/test-ai/vessel-test.inp`. Save output to `~/test-ai/vessel_test_melcor.med` and `~/test-ai/vessel_test_melcor.inp`.

**Blocker:** The model deployment backing `crush-vpc` was scaled to zero, so the endpoint refused
connections. It has to be scaled back up before running; cold start takes ~15–20 min (GPU node
scheduling plus image pull).

**snap-melcor is fully registered** in `~/.config/crush/crush.json` on the development VM and exposes 15 tools. Configuration block:
```json
"snap-melcor": {
  "type": "stdio",
  "command": "python3.12",
  "args": ["/home/user/SNAP-MCP/snap-melcor/mcp_server.py"],
  "env": {
    "SNAP_PYTHON_PATH": "/home/user/snap/python",
    "PYTHONPATH": "/home/user/SNAP-MCP/snap-melcor:/home/user/snap/python"
  },
  "timeout": 60,
  "disabled": false
}
```

### What was completed this session

**snap-trace (VESSEL improvements):**
- Added `connect_pipe_to_vessel` tool — fixes silent junction failure; VESSEL API rejects `[JUN1] Inlet`, needs `"Positive Azimuthal"` etc.
- Added `set_vessel_table` tool — sets per-cell ICs and edge HDs via `Hydro3DPropertyTable` (unreachable via `set_component_property`)
- Both tools live-tested with crush-vpc on the development VM; `vessel-test.inp` in `~/test-ai/` has all vessel ICs and HDs set

**snap-melcor (new server, fully functional):**
- Fixed session.register() signature mismatch
- Fixed `open_med_model` — `snap.codes.melcor.open_model()` checks for `"MELCOR"` but plugin ID is `"MELCOR2X"`; use `snap.model_editor.open_model()` directly
- Added `create_model` tool (bootstraps via minimal MELGEN import — no blank-canvas API)
- Added `add_component` tool with Java `createComponent(jm)` + `addToModel(jm)` pattern
- Fixed Py4J class name lookup — `type(obj).__name__` always returns `"JavaObject"`; use `obj.getClass().getSimpleName()`
- Fixed property setters — MELCOR unit-typed setters need CReal get-mutate-set pattern (see snap-melcor quirks below)
- Added `list_component_properties` tool — returns all setter names via Java reflection
- Fixed stdout corruption from `snap.codes.melcor` import hijacking `sys.stdout`
- Built `primary_loop_melcor.med` / `.inp` in `~/test-ai/` using geometry extracted from the TRACE TRCIN

---

---

## Architecture overview

```
mcp_server.py               ← entry point; wires FastMCP + all modules
snap_trace/
  snap_env.py               ← SNAP bootstrap, py4j / MEBatch startup
  session.py                ← model registry (SQLite + in-memory cache)
  component_map.py          ← TRACE component type → SNAP API method map
  type_converter.py         ← enum string + value conversion
  resources.py              ← MCP resources (static reference content)
  tools/
    model_tools.py          ← snap_status, create_model, open_med, import_trcin, list_models
    component_tools.py      ← add_component, set_component_property, list_components, get_component, get_component_schema
    connection_tools.py     ← connect_components, get_connections
    export_tools.py         ← export_trcin, save_med, validate_model
```

The MCP framework used is **FastMCP** (`mcp[cli]>=1.0`). Each tool module exposes a `register(mcp)` function that decorates its tools with `@mcp.tool()`. Resources follow the same pattern in `resources.py`.

Transport is **stdio** only — Claude Code (and Claude Desktop) connect via subprocess stdin/stdout.

---

## mcp_server.py

Entry point. Three responsibilities:

1. **Save real stdout** (`_real_stdout = sys.stdout`) before any SNAP import. SNAP's `snap.streams` module replaces `sys.stdout` with a `_StreamLogHandler` when `snap.model_editor` is imported. MCP's stdio transport later calls `sys.stdout.buffer` and crashes if stdout has been replaced. Restoring it at the top of `main()` before `mcp.run()` fixes this.

2. **Trigger MEBatch startup** by importing `snap_trace.snap_env` (side-effectful). This starts the background thread immediately so the first tool call doesn't have to wait.

3. **Register all tools and resources** by calling each module's `register(mcp)`.

FastMCP constructor note: as of MCP v1.27.1, the description kwarg is `instructions`, not `description`.

---

## snap_env.py

Bootstraps the SNAP Python path and starts MEBatch.

- Inserts `SNAP_PYTHON_PATH` at the front of `sys.path` so `snap.*` imports resolve.
- Fires a daemon thread (`snap-init`) that calls `snap.model_editor.find_plugin("TRACE")`, which triggers the py4j handshake with the MEBatch JVM process.
- Exposes `status()` → dict and `wait_ready(timeout)` used by tools that require SNAP to be up before proceeding.

The thread is daemon so it doesn't prevent process exit if SNAP fails to start.

---

## session.py

Maintains two parallel stores for `TraceModel` objects:

- **In-memory dict** (`_models: dict[str, TraceModel]`) — fast access during a session.
- **SQLite database** (`~/.snap_trace/models.db`) — survives restarts; maps `model_id → med_path`.

`model_id` is an 8-character hex string from `uuid4`. Models are stored on disk as `.med` files under `~/.snap_trace/models/`.

**autosave** is called by every mutating tool after making changes. It writes the current in-memory model object back to its `.med` file. On the next server start, `get_model()` reloads from disk if the model is not in `_models`.

Key functions:

| Function | What it does |
|----------|-------------|
| `create_model(name, version)` | Creates a new TraceModel via `trace.new_model()`, saves to disk, registers in DB |
| `register_model(name, model, source_path)` | Registers a model already opened from a file (used by `open_med_model` and `import_trcin`) |
| `get_model(model_id)` | Returns from cache or reloads from `.med` if not cached |
| `autosave(model_id)` | Writes in-memory model to its `.med` path |
| `list_models()` | Returns all rows from the SQLite models table |

---

## component_map.py

`COMPONENT_MAP` is the single source of truth mapping MCP component type strings (e.g. `"PIPE"`) to the SNAP Python API. Each entry has four fields:

| Field | Purpose |
|-------|---------|
| `create` | `TraceModel` method name for creation (e.g. `"create_pipe"`) |
| `list` | `TraceModel` method that returns all components of this type (e.g. `"pipes"`) |
| `initializer` | Category string passed to `model.component_initializer()`, or `None` |
| `first_arg` | Property key whose value becomes the first positional arg to the create method (used by `CONTROL_BLOCK` and `SIGNAL_VARIABLE`) |

Three utility functions use this map:

- **`create_component`** — factory: resolves the create method, builds an initializer if needed, calls the create method with the right argument order, then applies all properties. Enum properties are applied before scalar properties because SNAP requires the type selector to be set before dependent fields (e.g. `FILL.ifty` before `FILL.flowin`).

- **`find_component`** — scans every `list` method on the model to find a component by CC number. Returns `(comp_type_str, component)`.

- **`iter_all_components`** — yields `(comp_type, component)` for every component in the model, used by `list_components` and `get_connections`.

One subtlety: SNAP's list methods sometimes return a single object instead of a list when there is only one component. `_coerce_list()` normalizes this.

---

## type_converter.py

Converts values from the JSON/AI representation to what the SNAP Python API expects.

**`resolve_enum(value: str)`** — parses `"ClassName.MethodName"` strings, looks up the class in `snap.codes.trace.enums`, and calls the method to get the enum instance. Returns `None` if the string isn't a valid enum reference.

**`convert(value)`** — applies `resolve_enum` first, then handles `"true"`/`"false"` strings.

**`set_property(comp, name, value)`** — the main entry point for property assignment:
- If `value` is a list-of-lists: treats it as a table and calls `.read([...])` on each row of the named attribute. This is how `initial_conditions_cell_table` and `friction_edge_table` are populated.
- If `value` is a flat list: converts each element and sets the attribute directly.
- Otherwise: converts and calls `setattr`.

Dot-path traversal one level deep (e.g. `"fluid_segment.friction_edge_table"`) is handled in `component_tools.py:set_component_property`, not here.

---

## tools/model_tools.py

Thin wrappers around `snap_env` and `session`. All tools that need SNAP running call `snap_env.wait_ready()` before proceeding. `open_med_model` and `import_trcin` use SNAP's `trace.open_model()` and `trace.import_ascii()` then hand off to `session.register_model()`.

---

## tools/component_tools.py

Most complex tool module. Key points:

- `get_component_schema` returns a hardcoded dict per component type. Adding a new type requires updating both `COMPONENT_MAP` and the `schemas` dict here.
- `add_component` delegates entirely to `component_map.create_component`, then calls `session.autosave`.
- `get_component` reflects all non-callable, non-private attributes. This is a best-effort inspector; some SNAP proxy attributes may throw on access and are silently skipped. For `HEAT_STRUCTURE` components, `_extract_mesh_info` is called after the flat scan and its result is returned as a top-level `radial_mesh` key.

**`_extract_mesh_info(comp)`** walks `comp.mesh.material_regions` and returns a dict with a `layers` list. Each layer entry contains:

| Field | Source |
|-------|--------|
| `material` | `str(region.material)` — see quirk below |
| `thickness_m` | `float(region.thickness)` |
| `meshpoints` | `[float(p) for p in region.meshpoints]` — normalized radial coordinates (0–1) |

All field accesses are individually try/caught so a failure on one field doesn't suppress the others.

---

## tools/connection_tools.py

`connect_components` does a single `setattr(comp, face, (slot, target_cc, cell))` — directly mirroring the SNAP Python API pattern from the standpipe example. The tuple assignment is how SNAP wires junctions.

**VESSEL connection quirk:** `connect_components` does NOT work for VESSEL targets. The Java `setMultiJunctionConnection` method does strict string matching on face labels and throws `RuntimeException` for `"[JUN1] Inlet"` when the target is a `VesselComponent`. Use `connect_pipe_to_vessel` instead.

`connect_pipe_to_vessel` converts (level, ring, sector) coordinates to the flat cell index `(level-1)*(nr*nt) + (ring-1)*nt + (sector-1) + 1` and calls `setattr(hydro_comp, pipe_face, (vessel_face, vessel_cc, flat_cell))`. Valid `vessel_face` strings for cylindrical geometry: `"Positive Azimuthal"`, `"Negative Azimuthal"`, `"Positive Radial"`, `"Negative Radial"`. Axial faces are excluded by the SNAP API for external connections.

`get_connections` iterates all components and tries `getattr(comp, face)` for `inlet`, `outlet`, and `side`. Non-existent faces return `None` and are skipped.

---

## tools/export_tools.py

`export_trcin`:
- Calls `model.export(path)`. SNAP writes the file synchronously and then returns an export result set.
- The result set's `.iterator()` call raises a `Py4JError` due to Java module access restrictions — this is benign (the file is already written). The exception is caught and ignored.
- Reads the written file back as a string and returns it.
- If no `output_path` is given, uses `tempfile.mkstemp` and deletes it after reading.

`validate_model`:
- Calls `model.export(tmp_path, check=True)`.
- SNAP raises on hard errors; soft warnings still produce a file. The exception message is inspected for `"warning"` to distinguish the two cases.

---

## resources.py

Five `@mcp.resource(uri)` functions returning static strings. They exist so an AI assistant can reference workflow steps, enum values, connection syntax, and example code without needing tool calls.

`trace://example/standpipe` reads `~/run-snap500/Samples/TRACE/Standpipe/standpipe.py` at request time. All others return inline strings.

---

## tools/component_tools.py — set_vessel_table

VESSEL per-cell initial conditions (pressure, temperatures, void fraction) and edge hydraulic diameters are stored in `Hydro3DPropertyTable` objects. These are NOT reachable via `set_component_property`'s dot-path traversal. `set_vessel_table` accesses them directly.

Table accessor pattern:
- **Cell tables** (no axis arg): `vessel.p_table`, `vessel.tl_table`, `vessel.tv_table`, `vessel.alp_table`, `vessel.pa_table`, `vessel.s_table`
- **Edge tables** (take `AxisSel` enum): `vessel.hd_table(AxisSel.AXIAL())`, `vessel.hd_table(AxisSel.AZIMUTHAL())`, `vessel.hd_table(AxisSel.RADIAL())`, and similarly for `frac_table`, `kfac_table`, `vv_table`, `vl_table`
- `AxisSel` is in `snap.codes.trace.enums`. `AxisSel.AXIAL()` is a factory method — must be called.

`Hydro3DPropertyTable` interface: `table.row_count` = nz (axial levels), `table.column_count` = nr×nt (planar cells per level). Set via `table[row_idx] = [v1, v2, ...]` (0-based row index).

Broadcasting in `_broadcast_vessel_value`: float → uniform; `list[float]` of length nz → per-level; `list[list[float]]` of shape nz×(nr×nt) → full grid.

---

## Known quirks and gotchas

| Issue | Detail |
|-------|--------|
| `sys.stdout` hijack | `snap.streams` replaces `sys.stdout` on import. Fixed in `mcp_server.py` by saving/restoring around `mcp.run()`. |
| `model.breaks()` coercion | SNAP returns a bare object (not a list) when there is exactly one break. `_coerce_list()` in `component_map.py` handles this. |
| Enum factory methods need `()` | `BreakIbtySel.No_Tables` is a method, not a constant — it must be called. `type_converter.py` calls it automatically when given `"BreakIbtySel.No_Tables"`. |
| Py4JError on export | `model.export()` raises after writing the file. Caught and ignored in `export_tools.py`. |
| FastMCP v1.27.1 API | Constructor arg is `instructions`, not `description`. |
| Enum ordering in `create_component` | Enum-valued properties are applied before scalars because SNAP gates some scalar fields on the enum selector being set first. |
| `ComponentReference.name` inaccessible | `mesh.material_regions[i].material` returns a `ComponentReference` proxy whose `.name` attribute raises. Use `str(region.material)` instead — it returns the material name string directly (e.g. `"Material 8"`). |
| `HEAT_STRUCTURE` mesh is not a flat property | `comp.mesh` returns a nested `MeshpointTable` object that `str()` renders as `""`. The flat-property scan in `get_component` cannot see it; `_extract_mesh_info` handles it explicitly. |
| `fluid_segment` setter is broken in SNAP API | The `fluid_segment.setter` on PIPE (run-snap500 version) has an `if/elif` chain that leaves `java_value` unbound when passed a plain string. Setting it via MCP always fails. Do not include `fluid_segment` in `add_component` properties or `set_component_property` calls — it is a display label only and does not affect physics. Excluded from prompt generation in `run_tests.py`. |
| `add_component` property failures are non-fatal | A failing property (e.g. `fluid_segment`) no longer aborts the whole call. `create_component` now collects failures and returns them as `warnings` in the result. All other properties in the dict are still applied. |
| `rftn_table` is a `TemperatureTable`, not a row-based table | The old `set_property` code called `table[i].read(row)` for list-of-lists values, which works for some table types but not `rftn_table` — its rows are `PropertyValueList` objects (no `.read()`). Fixed in `type_converter.py`: now calls `table.read(rows)` on the table itself, with fallback to `table[i] = row`. |
| HS-to-fluid coupling requires `connect_heat_structure` | `cells[i].inner.hcom.reference` is three levels deep; `set_component_property` dot-path only traverses one level. Use the dedicated `connect_heat_structure` tool instead. |
| HS-to-VESSEL coupling broken via `hcom.reference` | `setReferencedCellID(cc*1000+flat_cell)` is decoded by `CellReconnector` as `(within_level_0based, axial_0based)` — not a flat sequential index — causing `ArrayIndexOutOfBoundsException`. For VESSEL targets, call `setHydroRef`/`setCellRef` directly on `surface.hcom.java_object`: `vessel_j.getCellAt(flat_0based)` uses the single-arg overload which correctly computes `level = flat // (nr*nt)`, `within = flat % (nr*nt)`. The packed-integer read-back (`getReferencedCellID`) also overflows 32-bit `int` for vessel cells and cannot be round-tripped. |
| SNAP plugin 4.7.0 vs TRACE 5.0p9 FILL SV card mismatch | SNAP plugin 4.7.0 exports a 5-field signal-variable card for FILL components (`ifmlsv ifmvsv iftlsv iftvsv ifasv`) but TRACE 5.0 Patch 9 on the target development host expects the older 4-field layout (`ifmmsv iftlsv iftvsv ifasv`). The extra field shifts all subsequent cards by one token and causes a cascading parse failure. Fixed in `export_trcin` via `_fixup_trcin()` which collapses the 5-field layout to 4-field on export. **Prefer `save_med` over `export_trcin` for model handoff — `.med` is version-independent.** |
| Integer-flag fields exported as floats | SNAP stores some integer-type FILL fields (e.g. `falk`) as Java `double` internally; Py4J prints them as `0.0`, `1.0` etc. in the ASCII export. The TRACE parser rejects these for integer-only fields. Fixed in `export_trcin` via `_fixup_trcin()` which replaces `N.0` tokens with `N`. |
| `.inp` files are TRACE-version sensitive | SNAP's `model.export()` always writes the TRCIN format for the TRACE version the plugin was built against. Importing a SNAP-exported `.inp` into a different TRACE plugin version will fail with card-format errors. Use `save_med` + `validate_model` as the primary model artifact; only call `export_trcin` when preparing an actual TRACE run. |
| Blank junction label maps to `[JUN1] Inlet` | When the raw connection data shows `('', cc, cell)`, the SNAP face name is actually `[JUN1] Inlet`. `connect_components` must use `[JUN1] Inlet`, not `""`. |
| `FILL.name` has no setter | Setting `name` on a `Fill` object raises "property 'name' of 'Fill' object has no setter". Do not include `name` in `add_component` properties for FILL components. |
| `HEAT_STRUCTURE.nfax` is a per-cell array | `nfax` (fine mesh nodes per axial cell) cannot be set as a scalar integer — SNAP stores it as an array indexed per cell. Setting it via `add_component` fails with `'int' object is not subscriptable`. Use `set_component_property` with a list (e.g. `[3, 3, 3, 3]` for 4 axial cells) after creation. |

---

## Adding a new component type

1. Add an entry to `COMPONENT_MAP` in `component_map.py` with `create`, `list`, `initializer`, and `first_arg`.
2. Add a `schemas[TYPE]` entry in `component_tools.py:get_component_schema` with `description`, `initializer_fields`, `key_properties`, and `connection_slots`.
3. If the type belongs to a new category, add it to the category dict in `resources.py:component_types`.

---

## Configuration

The server reads three environment variables at startup. For Claude Code, set them via `claude mcp add -e KEY=VALUE` — the registration is stored in `~/.claude.json`. For Claude Desktop, set them in the `env` block of `~/Library/Application Support/Claude/claude_desktop_config.json`.

| Variable | Default | Purpose |
|----------|---------|---------|
| `SNAP_PYTHON_PATH` | `~/run-snap500/python` | Path to SNAP's Python API directory |
| `SNAP_TRACE_DB` | `~/.snap_trace/models.db` | SQLite model registry |
| `SNAP_TRACE_WORKDIR` | `~/.snap_trace/models/` | Working .med file storage |
| `SNAP_TRACE_TARGET_VERSION` | `V5.0p9` | TRACE binary version being exported for; controls which `_fixup_trcin` patches are applied and the default version used in `create_model` |

---

---

## snap-melcor — companion MELCOR2X MCP server

Lives in `snap-melcor/`. Mirrors the snap-trace structure but talks to `snap.codes.melcor` instead of `snap.codes.trace`.

### Architecture

```
snap-melcor/
  mcp_server.py               ← entry point
  snap_melcor/
    snap_env.py               ← SNAP path bootstrap + melcor import (stdout fix)
    session.py                ← model registry (in-memory only, no SQLite)
    bindings/
      components.py           ← auto-generated wrappers (278 classes)
      enums.py                ← auto-generated enum classes (203 enums)
    tools/
      model_tools.py          ← melcor_status, create_model, import_melgen,
                                 open_med_model, list_models, close_model
      component_tools.py      ← add_component, list_components, get_component,
                                 get_component_schema, set_component_property,
                                 list_component_properties
      export_tools.py         ← validate_model, export_melgen, save_med
```

### Key API facts (MELCOR2X 2.7.1 on RHEL9)

**No blank-canvas model creation.** `snap.codes.melcor` has no `create_model()`. `create_model` writes a minimal MELGEN title card to a temp file, calls `mc.import_melgen(tmp)`, and deletes the temp file.

**Component creation pattern:**
```python
cats = list(jm.getCategories())
cat = next(c for c in cats if "CVH" in str(c.getShortName()).upper())
comp = cat.createComponent(jm)
comp.addToModel(jm)
comp.setName("CV-DOME")
```
Category short names are full display strings like `"Control Volumes (CVH)"` — match by substring, not exact equality.

**Java class names** (confirmed via `obj.getClass().getSimpleName()`):
- CVH → `VolumeComponent`
- FL → `FlowPath`
- HS → `HeatComponent`
- NCG → `NCGasComponent`

`type(obj).__name__` always returns `"JavaObject"` in Py4J — always use `getClass().getSimpleName()` for type identification.

**Property setter dispatch (CReal pattern):**
MELCOR unit-typed setters (`setPvolr`, `setTatmr`, etc.) take SNAP `CReal` subclass objects (Pressa, Temp, Length…), not raw Python floats. Py4J cannot auto-coerce across classloaders. Pattern:
```python
creal_obj = java_comp.getPvolr()   # get existing CReal instance
creal_obj.setValue(float(value))   # mutate in-place
java_comp.setPvolr(creal_obj)      # pass back
```
`LengthControlArc` setters (diamf, diamr, zfm, zto) need an extra indirection:
```python
arc = java_comp.getDiamf()
arc.getLength().setValue(float(value))
arc.setLength(arc.getLength())
```
CV reference setters (`setKcvfm`, `setKcvto`) take an integer CC number. If a string name is passed, resolve it to CC# via `_find_component(jm, name).getCCnumber()`.

All four dispatch paths are implemented in `_call_setter()` in `component_tools.py`.

**`open_med_model` bug:** `snap.codes.melcor.open_model()` checks `plugin_id != "MELCOR"` but the actual plugin ID is `"MELCOR2X"` → always raises `ValueError`. Use `snap.model_editor.open_model(path)` directly.

**`sys.stdout` hijack:** `snap.codes.melcor` replaces `sys.stdout` with a `_StreamLogHandler` on import (same as `snap.codes.trace`). Fixed in `snap_env.py` by saving/restoring real stdout around the import.

**Human-friendly property aliases** (`_PROPERTY_ALIASES` in `component_tools.py`):
- CVH: `volume→pvolr`, `pressure→pncg`, `temperature→tatmr`, `pool_temp→tpolr`, `pool_elevation→zpolr`
- FL: `from_cv→kcvfm`, `to_cv→kcvto`, `flow_area→flara`, `diameter→diamf`, `length→fllen`, `elevation_from→zfm`, `elevation_to→zto`
- HS: `geometry→igeom`, `initial_temp→initialTemp`, `left_bc→ibcl`, `right_bc→ibcr`, `left_htc→xhtfcl`, `right_htc→xhtfcr`

**Default model components:** Every new MELCOR model auto-creates three NCG components — POOL (cc=1), FOG (cc=2), H2O-VAP (cc=3). These are MELCOR defaults and cannot be removed.

**`validate_model` fallback:** MELCOR's `java_model.validate()` may not exist; the tool falls back to a temp-file export check.

---

## Dependencies

| Package | Role |
|---------|------|
| `mcp[cli]>=1.0` | FastMCP framework; tested against v1.27.1 |
| `pydantic>=2.0` | Used internally by FastMCP |
| `snap.codes.trace` | SNAP Python API (bundled with SNAP installation, not on PyPI) |
| `snap.codes.melcor` | SNAP MELCOR2X Python API (requires melcor2x.jar in SNAP plugins/) |
| `py4j` | JVM bridge used by the SNAP API |
| `anyio` | Async I/O; pulled in by `mcp` |
