# Security Checklist

Concrete patterns to grep/look for, by category. Not exhaustive — use as a starting point and reason beyond it for stack-specific issues.

## Source code

- **Injection**: string-concatenated SQL/NoSQL queries with user input; `eval`/`exec`/`Function()` on user input; OS command building via string concat (`os.system`, `subprocess` with `shell=True`, `child_process.exec`); LDAP/XPath queries built from input.
- **XSS**: unescaped output in templates (`innerHTML`, `dangerouslySetInnerHTML`, `{!! !!}` in Blade, `|safe` in Jinja, raw string interpolation into HTML).
- **Auth/session**: passwords compared with `==` instead of constant-time compare; missing password hashing (plaintext or unsalted MD5/SHA1); JWT with `alg: none` accepted or secret hardcoded; session tokens in URL; missing/weak CSRF protection on state-changing endpoints; missing authorization checks (IDOR — object fetched by ID with no ownership check).
- **Deserialization**: `pickle.loads`, `yaml.load` (not `safe_load`), Java `ObjectInputStream`, PHP `unserialize` on untrusted input.
- **Path traversal / file handling**: user input concatenated into file paths without normalization/sanitization; unrestricted file upload (no type/size check, executable extensions allowed).
- **SSRF**: server-side HTTP requests to URLs built from user input without allow-listing.
- **Crypto**: MD5/SHA1 for security purposes; ECB mode; hardcoded IVs/nonces; custom crypto instead of vetted libraries; weak random (`Math.random`, `rand()`) used for tokens/secrets.
- **Error handling**: stack traces or internal errors returned to the client; verbose debug mode enabled in what looks like a prod config.

## Secrets & credentials

- Regex-style scan for: `api[_-]?key`, `secret`, `password`, `token`, `AKIA[0-9A-Z]{16}` (AWS), `-----BEGIN (RSA|EC|OPENSSH) PRIVATE KEY-----`, database connection strings with embedded credentials, `.env` files that are tracked in git (check for `.gitignore` coverage), hardcoded values passed to auth headers.
- Also check comments and test/fixture files — secrets often leak there, not just "real" code.

## Dependencies

- Parse the manifest/lockfile relevant to the stack (`package.json`+lock, `requirements.txt`/`Pipfile.lock`/`poetry.lock`, `go.mod`/`go.sum`, `pom.xml`/`build.gradle`, `*.csproj`/`packages.lock.json`, `Gemfile.lock`).
- Flag: versions pinned far below current major (multiple majors behind), packages with no updates in years (possibly abandoned), anything the user or web search confirms has a known CVE.
- If web search is available, verify suspicious packages/versions against known CVEs rather than asserting from memory — dependency vulnerability data changes constantly.
- Don't flag every slightly-outdated package as a finding; focus on ones with plausible security relevance (network-facing, parsing, crypto, auth libraries) or confirmed CVEs.

## Config & IaC

- **Docker**: running as root (no `USER` directive), `ADD` from remote URLs, secrets baked into image layers (`ENV`/`ARG` with credentials), `latest` tags in prod, exposed unnecessary ports.
- **docker-compose**: privileged containers, host network mode, bind-mounting sensitive host paths, default/weak passwords in environment blocks.
- **Terraform/CloudFormation**: `0.0.0.0/0` ingress rules, public S3 buckets/storage without justification, IAM policies with `*` actions/resources, unencrypted storage/databases, hardcoded credentials in `.tf`/`.tfvars`.
- **Kubernetes**: containers running as root or privileged, missing resource limits (DoS risk), secrets as plain env vars instead of Secret objects, overly broad RBAC (`cluster-admin` bound broadly).
- **CI/CD**: secrets printed to logs, pull-request workflows with write access to secrets (supply-chain risk), unpinned third-party actions (`uses: some/action@main` instead of a pinned SHA/tag).
- **Web server configs**: TLS verification disabled, weak cipher suites, missing security headers (CSP, HSTS, X-Frame-Options) — treat these as Low unless the app has a specific reason they matter more.