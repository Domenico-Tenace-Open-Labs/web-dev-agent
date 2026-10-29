---
name: security-audit
description: Audits codebase for security vulns, misconfigs, cybersecurity risks: source code, deps, config files, IaC (Docker, Terraform, Kubernetes, CI/CD). Produces severity-ranked report (Critical/High/Medium/Low/Info) in chat. Trigger when user says "handle security", "review security", "security audit", "find vulnerabilities", "find security issues", "check for vulnerabilities", "cybersecurity review", "is this code secure", "pentest this", "check for secrets/exposed keys", or asks to scan/review/check repo/folder/file for security problems — even without word "security" (e.g. "can someone hack this", "any risks in this code"). Always use this skill instead of ad-hoc read-through.
---

# Security Audit

Systematic security review of codebase. Covers source code, deps, config/secrets, infrastructure-as-code. Output: concise, deduplicated, severity-ranked report in chat — no file unless user asks.

## Workflow

1. **Scope target.** Find root path to scan (user-given path, or cwd/repo if unspecified — ask only if ambiguous, e.g. multiple unrelated repos). Detect stack: language(s), frameworks, package managers, Docker/Terraform/K8s/CI config.

2. **Scan in passes**, using `references/checklist.md` for concrete patterns per category:
   - **Source code** — injection flaws, auth/session issues, unsafe deserialization, path traversal, SSRF, weak crypto, insecure error handling.
   - **Secrets & hardcoded credentials** — API keys, passwords, tokens, private keys, connection strings anywhere in tracked files (config, `.env` committed by mistake, code comments).
   - **Dependencies** — parse manifest/lockfiles (`package.json`/`package-lock.json`, `requirements.txt`/`poetry.lock`, `*.csproj`/`packages.lock.json`, `go.mod`, `pom.xml`, etc). Flag known-vulnerable or abandoned/unpinned versions. Use web search for CVE lookups on suspect packages/versions if available; else flag as "needs CVE verification" not guessing.
   - **Config & IaC** — Dockerfiles, docker-compose, Terraform, Kubernetes manifests, CI/CD pipelines, nginx/apache configs, cloud policy files. Look for permissive access, exposed ports/services, root containers, plaintext secrets, disabled TLS verification, wildcard permissions.

3. **Deduplicate before reporting.** Same root cause repeats across files (e.g. one vulnerable dep in 12 places, same unsafe pattern copy-pasted) → report **once** as single finding listing all affected locations — never repeat explanation per occurrence. Hard requirement, not style.

4. **Assign severity** using rubric below. Be consistent; don't inflate or downplay.

5. **Write report** in chat following format below. Skip empty severity sections (omit, not "No findings"), except note total categories scanned at top.

## Severity rubric

| Severity | Criteria |
|---|---|
| **Critical** | Remotely exploitable, no auth, full compromise, data breach, or RCE (e.g. SQLi on unauthenticated endpoint, hardcoded prod credentials, exposed private key). |
| **High** | Exploitable with some precondition (auth, local access, specific config), or high-impact (auth bypass, SSRF, unsafe deserialization, known-CVE dep with available exploit). |
| **Medium** | Significant preconditions or user interaction (reflected XSS needing victim click, weak crypto not yet broken, missing rate limiting, verbose error leaking stack traces). |
| **Low** | Defense-in-depth gaps, best-practice violations with limited real-world impact (missing security headers, outdated non-vulnerable dep, verbose logging). |
| **Info** | Worth noting, not a vuln (missing `.gitignore` entries, no `SECURITY.md`, dep close to EOL). |

## Report format

```
# Security Audit — <scope>

Scanned: <n files/dirs>, categories: code / secrets / dependencies / config & IaC
Findings: X Critical, Y High, Z Medium, W Low, V Info

## Critical
### <Short title>
- **Where:** file:line (list all locations if repeated)
- **Issue:** one or two sentences, no boilerplate
- **Impact:** one sentence
- **Fix:** concrete, actionable

## High
...
```

Keep each finding tight: 4 lines max unless genuinely complex. No repeated preambles on every item — say it once per finding. If category scanned with zero findings, don't list in body; summary line covers it.

## When context is large

Big repos: don't read every file verbatim into context. Prioritize: entry points (routes/controllers), auth code, anything handling user input, config/env files, IaC files, manifest/lockfiles. Use grep/search for known-risky patterns (see checklist) before deep-reading, then read only hits with surrounding context.

## After the report

Offer, don't push: "Want me to go deeper on any of these, or help fix the Critical/High ones first?" Don't generate a file unless asked.