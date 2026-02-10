"""iOS Simulator proxy detection and configuration."""

import json
import subprocess

from rich.console import Console
from rich.panel import Panel

console = Console()


def get_booted_simulators() -> list[dict]:
    """Find all booted iOS simulators."""
    try:
        result = subprocess.run(
            ["xcrun", "simctl", "list", "devices", "--json"],
            capture_output=True, text=True, timeout=10,
        )
        if result.returncode != 0:
            return []

        data = json.loads(result.stdout)
        booted = []
        for runtime, devices in data.get("devices", {}).items():
            for device in devices:
                if device.get("state") == "Booted":
                    device["runtime"] = runtime
                    booted.append(device)
        return booted
    except (subprocess.TimeoutExpired, FileNotFoundError, json.JSONDecodeError):
        return []


def show_simulator_info(proxy_port: int):
    """Show iOS simulator status and proxy setup instructions."""
    simulators = get_booted_simulators()

    if simulators:
        sim_names = ", ".join(s["name"] for s in simulators)
        console.print(f"[green]Detected simulators:[/green] {sim_names}")
        console.print()
        console.print(Panel(
            f"[bold]Simulator Proxy Setup[/bold]\n\n"
            f"Run these commands to route traffic through mitmios:\n\n"
            f"  [cyan]xcrun simctl spawn booted launchctl setenv http_proxy http://127.0.0.1:{proxy_port}[/cyan]\n"
            f"  [cyan]xcrun simctl spawn booted launchctl setenv https_proxy http://127.0.0.1:{proxy_port}[/cyan]\n\n"
            f"First time? Run [bold]mitmios setup[/bold] to install the CA certificate.",
            title="iOS Simulator",
            border_style="blue",
        ))
    else:
        console.print("[yellow]No booted iOS simulator detected.[/yellow]")
        console.print("Start a simulator with: [cyan]xcrun simctl boot 'iPhone 16 Pro'[/cyan]")

    console.print()
