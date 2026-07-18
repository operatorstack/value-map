<p align="center">
  <img src="assets/value-map-mark.svg" width="96" alt="Value Map logo">
</p>

<h1 align="center">Value Map</h1>

<p align="center"><strong>Map the idea. Check the code. Decide what matters.</strong></p>

Paste a message, post, or half-formed idea. Value Map helps you understand what a CEO, customer, product person, Hacker News post, LinkedIn post, or tweet could mean for the product you have—or are just starting. It grounds the interpretation in your code and project context, showing what exists, what may need building, where the potential value is, and when an appealing outside idea does not yet have enough evidence to fit.

It does not score the sender or declare an idea valuable. It separates the idea from the available evidence and returns a testable value hypothesis so you can decide what deserves attention.

```text
/value-map "We can configure workflow templates, but customers cannot run one on a real project..."
```

```text
WHAT THIS MEANS
The product stores workflow intent, but users cannot yet turn it into a result.

WHERE THE VALUE IS
A user goes from a saved template to one useful, traceable project outcome.

REALITY CHECK
EXISTING   Template configuration
PARTIAL    Project context
PROPOSED   Controlled execution

VERDICT
Repo-grounded, testable value hypothesis.
```

Value Map is designed for conversation. The first response establishes a trustworthy shared understanding. Ask follow-up questions when you want the evidence, contradictions, source paths, or a deeper explanation.

## Useful when the idea did not start in your repository

- a CEO or product lead sends a long message and you need the product meaning;
- a customer describes a problem in their own vocabulary;
- a Hacker News, LinkedIn, or X post sounds relevant but you do not want to copy it blindly;
- you are beginning an individual project and need to separate a promising outcome from an attractive implementation idea;
- an existing codebase and an external description disagree about what is already built;
- you are unsure whether something is useful and want a testable value hypothesis before planning it.

When the repository is mature, Value Map grounds the interpretation in code evidence. When the project is just beginning, it clearly grades the result as source-only or unresolved rather than inventing implementation facts.

## Why use it

Business language and code drift apart easily. A confident summary may describe planned behavior as shipped, replace the original user outcome with implementation vocabulary, or silently turn an unknown into an assumption.

Value Map keeps two sources of authority separate:

```text
external message  ──► source meaning ──┐
                                       ├──► conversational value map
current codebase  ──► code evidence ───┘
```

It reports capabilities with explicit status:

| Status | Meaning |
|---|---|
| `EXISTING` | Directly supported by inspected repository evidence |
| `PARTIAL` | Some behavior exists, but the value-producing transition is incomplete |
| `PROPOSED` | The context suggests something that would need to be built |
| `UNKNOWN` | The inspected source and code cannot establish whether it exists |

## What it does

- preserves the exact pasted message with a source fingerprint;
- identifies the user, present state, missing transition, and desired outcome;
- checks relevant claims against a minimal repository slice;
- corrects contradictions without replacing the source's meaning;
- distinguishes existing capabilities from new ideas;
- identifies the smallest observable proof of the value hypothesis;
- returns everything in the current coding-agent conversation.

## What it does not do

- modify the repository;
- generate planning or product documents;
- create a backlog or implementation plan;
- stage, commit, publish, or ship changes;
- claim that customer value has already been proven.

Use a planning and delivery workflow after you understand the context and decide that the value hypothesis is worth pursuing.

## Install

Value Map supports Codex, Cursor, and Claude Code. Install the latest verified release from the repository root where you want to use it.

### Codex

```bash
curl -fsSL https://raw.githubusercontent.com/operatorstack/value-map/main/install.sh | VALUE_MAP_HOST=codex bash
```

### Cursor

```bash
curl -fsSL https://raw.githubusercontent.com/operatorstack/value-map/main/install.sh | VALUE_MAP_HOST=cursor VALUE_MAP_REPO="$PWD" bash
```

Reload Cursor after installation, then invoke `/value-map "..."`.

### Claude Code

```bash
curl -fsSL https://raw.githubusercontent.com/operatorstack/value-map/main/install.sh | VALUE_MAP_HOST=claude bash
```

PowerShell users can run `install.ps1` with `-HostName codex`, `cursor`, or `claude`.

## How grounding works

Value Map first projects the external message without reading the repository. It preserves actors, capabilities, constraints, uncertainty, negation, and sequence. Those relations become targeted repository searches for the smallest relevant entry points, interfaces, decision functions, tests, and reliability boundaries.

The two slices are joined without letting code terminology overwrite business meaning. Repository evidence can support, correct, contradict, or leave a claim unresolved. A contradiction in a core value relation blocks the hypothesis.

## Evidence, not a verdict

Value Map uses deterministic checks for the parts that should not depend on taste: the response stays bound to the exact source, projected claims retain their source lineage, repository claims cite inspected paths, contradictions remain visible, unknowns do not silently become assumptions, and the smallest proof has an observable signal.

An LLM still performs semantic projection, so the result is not a scientific measurement of whether an idea or sender is good. It is a traceable, falsifiable interpretation. The final judgment remains yours.

## Source and releases

The canonical operator and evaluation work lives in [Intelligence Flow](https://github.com/operatorstack/intelligence-flow/tree/main/labs/14-product-value-projection). This repository owns the public product surface, installation, compatibility checks, and releases.

`UPSTREAM.json` binds projected files to their exact Intelligence Flow commit. A scheduled workflow proposes upstream changes through a pull request. Every merged Value Map pull request creates a patch release by default; `minor`, `major`, and `skip-release` labels adjust that behavior.

## License

Value Map is licensed under [Apache-2.0](LICENSE).
