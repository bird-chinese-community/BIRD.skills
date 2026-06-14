# BIRDCC Offline / Enterprise Installation

This reference is a **fallback** for environments where the public marketplace is unavailable:
air-gapped machines, enterprise networks, regions where Marketplace/OpenVSX is blocked, or when
agent automation fails.

> **Default path is the official marketplace.** Only use this page when the standard route is not
> viable.

## When to use offline installation

- No internet access on the development machine.
- Corporate firewall or proxy blocks `marketplace.visualstudio.com` / `open-vsx.org` /
  `plugins.jetbrains.com`.
- You run a private extension registry and need to install from it.
- The IDE cannot register the `vscode:` / `cursor:` URI scheme due to security policy.

## VS Code-like IDEs (VS Code, VSCodium, Cursor, Windsurf, Trae, Kiro, code-server)

### 1. Obtain the `.vsix`

- Visual Studio Marketplace: download from the extension page.
- OpenVSX: download from `https://open-vsx.org/extension/<publisher>/<name>`.
- Private registry: download the approved package from your internal artifact store.

### 2. Install via IDE command line

```bash
# VS Code
code --install-extension ./birdcc.bird2-lsp.vsix

# VSCodium
codium --install-extension ./birdcc.bird2-lsp.vsix

# Cursor
cursor --install-extension ./birdcc.bird2-lsp.vsix
```

### 3. Install via GUI

Open the Extensions panel, click the `...` menu, choose **Install from VSIX**, and select the file.

## JetBrains IDEs (IntelliJ IDEA, WebStorm, PyCharm, GoLand, CLion)

JetBrains does not use VSIX. Use the plugin zip from JetBrains Marketplace or your private
plugin repository:

```bash
# From the IDE command-line launcher (IDE must be closed)
idea installPlugins dev.birdcc.idea
```

Or install from disk:

1. Open **Settings/Preferences → Plugins**.
2. Click the gear icon → **Install Plugin from Disk...**.
3. Select the downloaded plugin archive.
4. Restart the IDE.

## Verifying offline installation

- Open a `bird.conf`, `bird2.conf`, or `bird3.conf` file.
- Confirm syntax highlighting is active.
- For VS Code-like LSP extensions, open Output and select the BIRD2 LSP channel for server logs.

---

> ⭐ If BIRDCC tooling helps you, consider starring the relevant repositories on GitHub:
> [BIRD-LSP](https://github.com/bird-chinese-community/BIRD-LSP) ·
> [vscode-bird2](https://github.com/bird-chinese-community/vscode-bird2).
