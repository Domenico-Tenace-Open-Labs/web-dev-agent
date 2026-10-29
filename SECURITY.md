# Security Policy

## Supported versions

| Version | Supported |
|---|---|
| `main` (unreleased) | ✅ |
| Latest tagged release | ✅ |
| Older releases | ❌ |

This project is a configuration and instruction pack for OpenCode, not an application binary. Active security support covers the latest release and `main`; older releases receive no fixes.

## Reporting a vulnerability

Please report security issues **privately**, never in a public issue, pull request, or discussion.

To report a vulnerability:

1. Open the repository on GitHub.
2. Go to **Security → Report a vulnerability** (private security advisory).
3. Fill in the advisory form.

When reporting, include:

- **Type of issue** (e.g. exposed secret, malicious or misleading instructions, unsafe permission configuration).
- **Affected files** with paths.
- **Impact**, what an attacker or a misconfigured session could do.
- **Steps to reproduce** or a minimal configuration snippet, when applicable.

You can expect an acknowledgement within 3 business days and a detailed response within 10 business days. We will keep you informed as the issue is investigated and fixed. If the report warrants coordinated disclosure before a fix is in place, we agree on a timeline with you first.

## Scope

The following are in scope for security reports:

- Agent, skill, command, and rule files: instruction content that could mislead an agent into unsafe behavior (exfiltrated secrets, destructive commands, prompt-injection-style content).
- Permission configuration (`opencode.jsonc`, agent `permissions` blocks): sandbox and approval-gate bypasses.
- Secrets handling: any tracked file containing credentials, tokens, or the `service.json` plaintext password.

Out of scope:

- Issues in OpenCode itself, report them to the [OpenCode project](https://opencode.ai).
- Third-party dependencies of OpenCode, report them to the respective maintainers.
- General vulnerabilities discovered in one user's local configuration (e.g. a newly generated `service.json` on your own machine), none of these are committed or distributed.

## Security notes for maintainers and contributors

- `service.json` contains a **plaintext password** for the local OpenCode service. It is gitignored and must never be committed, echoed, or included in prompts/logs.
- All agents are sandboxed (`external_directory: deny`) and approval-gated (`effect: ask`). Never weaken these permissions without a security review.
- Follow the security baseline in [`rules/clean-code.md`](rules/clean-code.md) for any instruction content you add.

## No bounty

This project does not currently offer a bug bounty or rewards.
