"""Tracker configuration management."""

import shutil
from pathlib import Path

import typer
import yaml
from rich.console import Console
from rich.table import Table

console = Console()

CONFIG_DIR = Path.home() / ".config" / "mitmios" / "trackers"
BUILTIN_CONFIGS = Path(__file__).parent.parent / "configs"


def ensure_config_dir():
    """Create config directory if it doesn't exist."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)


def manage_config(action: str, path: str | None):
    """Handle config subcommands."""
    if action == "list":
        list_configs()
    elif action == "add":
        if not path:
            console.print("[red]Usage:[/red] mitmios config add <path/to/config.yaml>")
            raise typer.Exit(1)
        add_config(Path(path))
    elif action == "validate":
        if not path:
            console.print("[red]Usage:[/red] mitmios config validate <path/to/config.yaml>")
            raise typer.Exit(1)
        validate_config(Path(path))
    elif action == "example":
        show_example()
    else:
        console.print(f"[red]Unknown action:[/red] {action}")
        console.print("Available: list, add, validate, example")
        raise typer.Exit(1)


def list_configs():
    """List all tracker configurations."""
    ensure_config_dir()

    table = Table(title="Tracker Configurations")
    table.add_column("Name", style="bold")
    table.add_column("Source", style="dim")
    table.add_column("Path")

    # Built-in configs
    if BUILTIN_CONFIGS.exists():
        for f in sorted(BUILTIN_CONFIGS.glob("*.yaml")):
            try:
                data = yaml.safe_load(f.read_text())
                table.add_row(data.get("name", f.stem), "built-in", str(f))
            except yaml.YAMLError:
                table.add_row(f.stem, "built-in", str(f))

    # User configs
    for f in sorted(CONFIG_DIR.glob("*.yaml")):
        try:
            data = yaml.safe_load(f.read_text())
            table.add_row(data.get("name", f.stem), "user", str(f))
        except yaml.YAMLError:
            table.add_row(f.stem, "user", str(f))

    console.print(table)


def add_config(path: Path):
    """Add a tracker config file."""
    if not path.exists():
        console.print(f"[red]File not found:[/red] {path}")
        raise typer.Exit(1)

    validate_config(path, quiet=True)

    ensure_config_dir()
    dest = CONFIG_DIR / path.name
    shutil.copy(path, dest)
    console.print(f"[green]Config added:[/green] {dest}")


def validate_config(path: Path, quiet: bool = False):
    """Validate a tracker config file."""
    if not path.exists():
        console.print(f"[red]File not found:[/red] {path}")
        raise typer.Exit(1)

    try:
        data = yaml.safe_load(path.read_text())
    except yaml.YAMLError as e:
        console.print(f"[red]Invalid YAML:[/red] {e}")
        raise typer.Exit(1)

    errors = []
    if not isinstance(data, dict):
        errors.append("Root must be a mapping")
    else:
        if "name" not in data:
            errors.append("Missing required field: name")
        if "matchers" not in data:
            errors.append("Missing required field: matchers")
        elif not isinstance(data["matchers"], list):
            errors.append("matchers must be a list")
        else:
            for i, m in enumerate(data["matchers"]):
                if "id" not in m:
                    errors.append(f"matchers[{i}]: missing 'id'")
                if "host" not in m and "host_pattern" not in m:
                    errors.append(f"matchers[{i}]: must have 'host' or 'host_pattern'")

    if errors:
        console.print(f"[red]Validation errors in {path.name}:[/red]")
        for e in errors:
            console.print(f"  - {e}")
        raise typer.Exit(1)

    if not quiet:
        console.print(f"[green]Valid:[/green] {path.name} ({data.get('name', 'unnamed')})")


def show_example():
    """Print an example tracker config."""
    example = """\
# Example: Track a custom analytics endpoint
name: "My App Analytics"
description: "Custom analytics event tracking"

matchers:
  - id: "analytics_event"
    label: "Analytics Event"
    color: "#8b5cf6"
    host: "analytics.myapp.com"
    path_pattern: "/v1/events"

extractors:
  - source: "request.body"
    format: "json"
    fields:
      - path: "event_name"
        display_name: "Event Name"
        type: "badge"
      - path: "timestamp"
        display_name: "Timestamp"
        type: "timestamp"

display:
  type: "event_table"
  columns:
    - { field: "event_name", label: "Event", type: "badge" }
    - { field: "timestamp", label: "Time", type: "timestamp" }
    - { field: "status_code", label: "Status", type: "status_code" }
"""
    console.print(example)
