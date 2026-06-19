# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///

"""Detect installed IDEs and generate marketplace-first onboarding data for birdcc."""

from __future__ import annotations

import argparse
import json
import os
import platform
import shlex
import shutil
import subprocess
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path

BIRD_VSCODE_EXTENSION_ID = "birdcc.bird2-lsp"
BIRD_JETBRAINS_PLUGIN_ID = "dev.birdcc.idea"


@dataclass(frozen=True)
class Product:
    id: str
    name: str
    family: str
    cli: tuple[str, ...]
    marketplace: str
    mac_apps: tuple[str, ...] = ()
    win_dirs: tuple[str, ...] = ()
    linux_desktop: tuple[str, ...] = ()


@dataclass
class Detection:
    id: str
    name: str
    family: str
    marketplace: str
    found_by: str
    executable: str | None = None
    app_path: str | None = None
    version: str | None = None
    extension_status: str = "unknown"
    install_command: list[str] | None = None
    marketplace_hint: str | None = None
    agent_message: str | None = None
    notes: list[str] = field(default_factory=list)


PRODUCTS: tuple[Product, ...] = (
    Product(
        "vscode",
        "Visual Studio Code",
        "vscode-like",
        ("code",),
        "Visual Studio Marketplace",
        ("Visual Studio Code.app",),
        ("Microsoft VS Code",),
        ("code.desktop", "visual-studio-code.desktop"),
    ),
    Product(
        "vscode-insiders",
        "Visual Studio Code Insiders",
        "vscode-like",
        ("code-insiders",),
        "Visual Studio Marketplace",
        ("Visual Studio Code - Insiders.app",),
        ("Microsoft VS Code Insiders",),
        ("code-insiders.desktop",),
    ),
    Product(
        "vscodium",
        "VSCodium",
        "vscode-like",
        ("codium", "vscodium"),
        "OpenVSX",
        ("VSCodium.app",),
        ("VSCodium",),
        ("codium.desktop", "vscodium.desktop"),
    ),
    Product(
        "code-oss",
        "Code - OSS",
        "vscode-like",
        ("code-oss",),
        "OpenVSX",
        ("Code - OSS.app",),
        ("Code - OSS",),
        ("code-oss.desktop",),
    ),
    Product(
        "cursor",
        "Cursor",
        "vscode-like",
        ("cursor",),
        "Cursor / VS Code-compatible extensions",
        ("Cursor.app",),
        ("Cursor",),
        ("cursor.desktop",),
    ),
    Product(
        "windsurf",
        "Windsurf",
        "vscode-like",
        ("windsurf",),
        "OpenVSX",
        ("Windsurf.app",),
        ("Windsurf",),
        ("windsurf.desktop",),
    ),
    Product(
        "trae",
        "Trae",
        "vscode-like",
        ("trae",),
        "VS Code-compatible extensions",
        ("Trae.app",),
        ("Trae",),
        ("trae.desktop",),
    ),
    Product(
        "kiro",
        "Kiro",
        "vscode-like",
        ("kiro",),
        "OpenVSX",
        ("Kiro.app",),
        ("Kiro",),
        ("kiro.desktop",),
    ),
    Product(
        "code-server",
        "code-server",
        "vscode-like",
        ("code-server",),
        "OpenVSX / configured extension gallery",
    ),
    Product(
        "openvscode-server",
        "OpenVSCode Server",
        "vscode-like",
        ("openvscode-server",),
        "OpenVSX / configured extension gallery",
    ),
    Product(
        "idea",
        "IntelliJ IDEA",
        "jetbrains",
        ("idea", "idea.sh", "idea64.exe"),
        "JetBrains Marketplace",
        (
            "IntelliJ IDEA.app",
            "IntelliJ IDEA CE.app",
            "IntelliJ IDEA Ultimate.app",
        ),
        ("JetBrains\\IntelliJ IDEA", "JetBrains\\IntelliJ IDEA Community Edition"),
    ),
    Product(
        "webstorm",
        "WebStorm",
        "jetbrains",
        ("webstorm", "webstorm.sh", "webstorm64.exe"),
        "JetBrains Marketplace",
        ("WebStorm.app",),
        ("JetBrains\\WebStorm",),
    ),
    Product(
        "pycharm",
        "PyCharm",
        "jetbrains",
        ("pycharm", "pycharm.sh", "pycharm64.exe"),
        "JetBrains Marketplace",
        (
            "PyCharm.app",
            "PyCharm CE.app",
            "PyCharm Professional.app",
        ),
        ("JetBrains\\PyCharm", "JetBrains\\PyCharm Community Edition"),
    ),
    Product(
        "goland",
        "GoLand",
        "jetbrains",
        ("goland", "goland.sh", "goland64.exe"),
        "JetBrains Marketplace",
        ("GoLand.app",),
        ("JetBrains\\GoLand",),
    ),
    Product(
        "clion",
        "CLion",
        "jetbrains",
        ("clion", "clion.sh", "clion64.exe"),
        "JetBrains Marketplace",
        ("CLion.app",),
        ("JetBrains\\CLion",),
    ),
)


def decode_output(data: bytes | None) -> str:
    if data is None:
        return ""
    return data.decode("utf-8", errors="replace").strip()


def run(cmd: list[str], timeout: int = 8) -> tuple[int, str, str]:
    try:
        p = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
            check=False,
        )
        return p.returncode, decode_output(p.stdout), decode_output(p.stderr)
    except subprocess.TimeoutExpired as exc:
        stdout = decode_output(exc.stdout)
        stderr = decode_output(exc.stderr)
        return 124, stdout, f"command timed out after {timeout}s: {stderr}".strip()
    except Exception as exc:
        return 127, "", str(exc)


def q(cmd: list[str]) -> str:
    return subprocess.list2cmdline(cmd) if os.name == "nt" else " ".join(
        shlex.quote(x) for x in cmd
    )


def first_line(text: str) -> str | None:
    for line in text.splitlines():
        line = line.strip()
        if line:
            return line
    return None


def path_cli(product: Product) -> tuple[str, str] | None:
    for name in product.cli:
        exe = shutil.which(name)
        if exe:
            return exe, "path"
    return None


def mac_cli_or_app(product: Product) -> tuple[str | None, str | None, str] | None:
    if platform.system() != "Darwin":
        return None

    for base in (Path("/Applications"), Path.home() / "Applications"):
        for app_name in product.mac_apps:
            app = base / app_name
            if not app.exists():
                continue

            for cli_name in product.cli:
                bundled = app / "Contents/Resources/app/bin" / cli_name
                if bundled.exists():
                    return str(bundled), str(app), "macos-app-bundled-cli"

            return None, str(app), "macos-app"

    return None


def windows_cli(product: Product) -> tuple[str, str] | None:
    if platform.system() != "Windows":
        return None

    roots = [
        os.getenv("LOCALAPPDATA"),
        os.getenv("APPDATA"),
        os.getenv("ProgramFiles"),
        os.getenv("ProgramFiles(x86)"),
    ]

    suffixes = []
    for cli in product.cli:
        suffixes.extend((f"bin\\{cli}", f"resources\\app\\bin\\{cli}"))

    for root in filter(None, roots):
        for app_dir in product.win_dirs:
            for suffix in suffixes:
                candidate = Path(root) / app_dir / suffix
                if candidate.exists():
                    return str(candidate), "windows-known-path"

    return None


def linux_desktop(product: Product) -> tuple[str, str] | None:
    if platform.system() not in {"Linux", "FreeBSD"}:
        return None

    bases = (
        Path("/usr/share/applications"),
        Path("/usr/local/share/applications"),
        Path.home() / ".local/share/applications",
    )

    for base in bases:
        for desktop_id in product.linux_desktop:
            desktop = base / desktop_id
            if desktop.exists():
                return str(desktop), "linux-desktop-entry"

    return None


def resolve(product: Product) -> tuple[str | None, str | None, str] | None:
    if hit := path_cli(product):
        return hit[0], None, hit[1]

    if hit := mac_cli_or_app(product):
        return hit

    if hit := windows_cli(product):
        return hit[0], None, hit[1]

    if hit := linux_desktop(product):
        return None, hit[0], hit[1]

    return None


def list_vscode_extensions(exe: str) -> set[str] | None:
    rc, out, _ = run([exe, "--list-extensions"], timeout=15)
    if rc != 0:
        return None
    return {line.strip().lower() for line in out.splitlines() if line.strip()}


def supports_flag(exe: str, flag: str) -> bool:
    rc, out, err = run([exe, "--help"], timeout=8)
    return rc in {0, 1} and flag in f"{out}\n{err}"


def marketplace_hint(product: Product, vscode_ext: str, jb_plugin: str) -> str:
    if product.family == "jetbrains":
        return (
            f"JetBrains Marketplace Plugin ID: {jb_plugin}"
            if jb_plugin
            else "JetBrains 插件暂未配置。"
        )

    if product.marketplace == "Visual Studio Marketplace":
        return f"在 Visual Studio Marketplace 搜索/安装：{vscode_ext}"

    if "OpenVSX" in product.marketplace:
        return f"在 OpenVSX 搜索/安装：{vscode_ext}"

    return f"在 {product.name} 的扩展面板搜索/安装：{vscode_ext}"


def _is_numeric_plugin_id(plugin_id: str) -> bool:
    return plugin_id.isdigit()


def deep_link(product: Product, vscode_ext: str, jb_plugin: str) -> str | None:
    if product.family == "vscode-like":
        return f"{product.id}:extension/{vscode_ext}"
    if product.family == "jetbrains" and jb_plugin:
        if _is_numeric_plugin_id(jb_plugin):
            return f"https://plugins.jetbrains.com/plugin/{jb_plugin}"
        return f"https://plugins.jetbrains.com/search?search={jb_plugin}"
    return None


def agent_message(product: Product, status: str) -> str:
    prefix = f"检测到你安装了 {product.name}。"

    if status == "installed":
        return (
            prefix
            + "BIRD 插件已经安装，可以直接使用 BIRD 配置语法高亮、诊断、lint 与 Agent 协作能力。"
        )

    if product.family == "vscode-like":
        return (
            prefix
            + "推荐安装 BIRD VS Code/OpenVSX 插件，用于 BIRD 配置语法高亮、诊断、lint、跳转和 AI Agent 辅助修改。"
        )

    return (
        prefix
        + "推荐安装 BIRD JetBrains 插件，让 IntelliJ 系列 IDE 也能接入 birdcc 的配置诊断与 Agent 工作流。"
    )


def detect(product: Product, vscode_ext: str, jb_plugin: str) -> Detection | None:
    resolved = resolve(product)
    if not resolved:
        return None

    exe, app, found_by = resolved
    item = Detection(
        id=product.id,
        name=product.name,
        family=product.family,
        marketplace=product.marketplace,
        found_by=found_by,
        executable=exe,
        app_path=app,
    )

    if exe:
        rc, out, err = run([exe, "--version"], timeout=6)
        item.version = first_line(out) or first_line(err)

    if product.family == "vscode-like":
        if not exe:
            item.extension_status = "unknown"
            item.notes.append(
                "检测到应用，但没有检测到 CLI。可以引导用户安装 Shell Command，或在扩展面板中搜索 BIRD。"
            )
        else:
            installed = list_vscode_extensions(exe)
            if installed is not None:
                item.extension_status = (
                    "installed" if vscode_ext.lower() in installed else "missing"
                )
            else:
                item.extension_status = "unknown"

            if supports_flag(exe, "--install-extension"):
                item.install_command = [exe, "--install-extension", vscode_ext]
            else:
                item.notes.append(
                    "CLI 未声明支持 --install-extension，建议走 IDE 扩展面板引导。"
                )

    elif product.family == "jetbrains":
        if not jb_plugin:
            item.extension_status = "unknown"
            item.notes.append("未配置 JetBrains Plugin ID。")
        elif exe:
            item.extension_status = "unknown"
            item.install_command = [exe, "installPlugins", jb_plugin]
            item.notes.append("JetBrains CLI 安装插件前通常建议先关闭对应 IDE。")
        else:
            item.extension_status = "unknown"
            item.notes.append(
                "检测到 JetBrains 应用，但没有检测到可用 CLI。建议引导用户在 JetBrains Marketplace 中搜索 BIRD。"
            )

    item.marketplace_hint = marketplace_hint(product, vscode_ext, jb_plugin)
    item.agent_message = agent_message(product, item.extension_status)
    return item


def build_pretty_text(detections: list[Detection]) -> str:
    if not detections:
        return "没有检测到支持的 IDE。"

    lines: list[str] = []
    for x in detections:
        lines.append(f"\n{x.name} [{x.id}]")
        lines.append(f"  marketplace: {x.marketplace}")
        lines.append(f"  found_by: {x.found_by}")
        lines.append(f"  status: {x.extension_status}")
        if x.version:
            lines.append(f"  version: {x.version}")
        if x.executable:
            lines.append(f"  cli: {x.executable}")
        if x.app_path:
            lines.append(f"  app: {x.app_path}")
        if x.marketplace_hint:
            lines.append(f"  hint: {x.marketplace_hint}")
        if x.install_command:
            lines.append(f"  install: {q(x.install_command)}")
        if x.agent_message:
            lines.append(f"  agent: {x.agent_message}")
        for note in x.notes:
            lines.append(f"  note: {note}")
    return "\n".join(lines)


def build_ui_directives(detections: list[Detection]) -> dict:
    buttons = []
    for item in detections:
        if item.extension_status == "installed":
            continue
        product = next((p for p in PRODUCTS if p.id == item.id), None)
        if product is None:
            continue
        link = deep_link(product, BIRD_VSCODE_EXTENSION_ID, BIRD_JETBRAINS_PLUGIN_ID)
        if not link:
            continue
        buttons.append(
            {
                "ide_id": item.id,
                "title": f"在 {item.name} 中打开 BIRD 插件",
                "description": (
                    "一键唤起插件市场并直达 BIRD 扩展"
                    if item.family == "vscode-like"
                    else "访问 JetBrains Marketplace 获取 BIRD 插件"
                ),
                "action_type": "open_url",
                "url": link,
            }
        )

    return {
        "message": "检测到你本地的开发环境。birdcc 提供对应 IDE 插件，可用于 BIRD 配置语法高亮、诊断、lint、跳转和 AI Agent 协作。是否需要我帮你打开插件市场页面？",
        "buttons": buttons,
    }


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description="Detect installed VS Code-like and JetBrains IDEs for birdcc plugin onboarding."
    )
    p.add_argument("--vscode-extension", default=BIRD_VSCODE_EXTENSION_ID)
    p.add_argument("--jetbrains-plugin", default=BIRD_JETBRAINS_PLUGIN_ID)
    p.add_argument(
        "--install",
        action="store_true",
        help="Run install commands. Requires --confirmed after explicit user approval.",
    )
    p.add_argument(
        "--confirmed",
        action="store_true",
        help="Confirm that the user explicitly approved running external install commands.",
    )
    p.add_argument("--pretty", action="store_true", help="Include human-readable text in the JSON output.")
    args = p.parse_args(argv)

    detections = [
        item
        for product in PRODUCTS
        if (item := detect(product, args.vscode_extension, args.jetbrains_plugin))
    ]

    install_results = []
    if args.install:
        if not args.confirmed:
            install_results.append(
                {
                    "error": "安装操作需要同时提供 --install 和 --confirmed。请先获得用户明确同意后再执行外部安装命令。",
                    "skipped": True,
                }
            )
        else:
            for item in detections:
                if item.extension_status == "installed" or not item.install_command:
                    continue
                rc, out, err = run(item.install_command, timeout=120)
                install_results.append(
                    {
                        "id": item.id,
                        "name": item.name,
                        "command": q(item.install_command),
                        "exit_code": rc,
                        "stdout": out[-3000:],
                        "stderr": err[-3000:],
                    }
                )

    payload = {
        "purpose": "birdcc-ecosystem-onboarding",
        "platform": {
            "system": platform.system(),
            "release": platform.release(),
            "machine": platform.machine(),
        },
        "extensions": {
            "vscode": args.vscode_extension,
            "jetbrains": args.jetbrains_plugin,
        },
        "detected": [
            {
                **asdict(x),
                "install_command_text": q(x.install_command) if x.install_command else None,
            }
            for x in detections
        ],
        "agent_ui_directives": build_ui_directives(detections),
        "install_results": install_results,
        "summary": {
            "detected": len(detections),
            "already_installed": sum(x.extension_status == "installed" for x in detections),
            "actionable": sum(bool(x.install_command) for x in detections),
        },
    }

    if args.pretty:
        payload["pretty"] = build_pretty_text(detections)

    json.dump(payload, sys.stdout, ensure_ascii=False, indent=2)
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
