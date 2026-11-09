# Public GitHub repos

Authoritative **source** for packages lives in the private service checkout under `tools/`. Push mirrors with `./scripts/publish-integrators.sh` (force all), `./scripts/publish-integrators-if-needed.sh` (when changed), or individual scripts below.

**Integrator docs on this hub:** [INTEGRATIONS.md](./INTEGRATIONS.md) · [HOSTS.md](./HOSTS.md) · [readfetch.com/integrations](https://readfetch.com/integrations)

| GitHub repo | npm / PyPI | Publish script |
|-------------|------------|----------------|
| [readfetch/readfetch](https://github.com/readfetch/readfetch) | — (docs) | `./scripts/publish-public-github.sh` |
| [readfetch/client-js](https://github.com/readfetch/client-js) | `@readfetch/client` | `./scripts/publish-client-js.sh` |
| [readfetch/client-py](https://github.com/readfetch/client-py) | `readfetch-client` | `./scripts/publish-client-py.sh` |
| [readfetch/mcp-x402-proxy](https://github.com/readfetch/mcp-x402-proxy) | `@readfetch/mcp-x402-proxy` | `./scripts/publish-mcp-x402-proxy.sh` |

Registry publish (`npm publish` / `twine upload`) runs automatically after `./scripts/deploy.sh` when the local version is not on the registry (or run `./scripts/publish-integrators-if-needed.sh`). **README-only edits** at an already-published version trigger an automatic **patch** bump (`integrators.version`) so npm/PyPI registry READMEs can update (immutable per release). GitHub mirrors (`README.md` in each repo) sync when the source tree changed, or always with `PUBLISH_INTEGRATORS=1`. **PyPI:** `TWINE_USERNAME=__token__` + token in `PYPI_API_TOKEN` or `~/.readfetch-pypi.token` (chmod 600) on the machine that runs deploy — never commit the token.

**Integrator feedback:** documented on the live host and in [INTEGRATIONS.md](./INTEGRATIONS.md#integrator-feedback-not-billing) · [AGENTS.md](./AGENTS.md).

All scripts switch `gh` to the **readfetch** account, force-push `main`, then restore your previous active account.
