"""mitmios CLI - iOS network debugging tool."""

import typer
from rich.console import Console

from mitmios import __version__

app = typer.Typer(
    name="mitmios",
    help="iOS network debugging tool with configurable analytics tracking",
    no_args_is_help=True,
)
console = Console()


def version_callback(value: bool):
    if value:
        console.print(f"mitmios v{__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: bool = typer.Option(
        False, "--version", "-v", callback=version_callback, is_eager=True,
        help="Show version and exit",
    ),
):
    """mitmios - iOS network debugging tool built on mitmproxy."""
    pass


@app.command()
def start(
    port: int = typer.Option(8081, "--port", "-p", help="Web UI port"),
    proxy_port: int = typer.Option(8080, "--proxy-port", help="Proxy listen port"),
    host: str = typer.Option("127.0.0.1", "--host", help="Web UI host"),
    no_browser: bool = typer.Option(False, "--no-browser", help="Don't open browser"),
    no_simulator: bool = typer.Option(False, "--no-simulator", help="Skip simulator proxy info"),
):
    """Start mitmios proxy and web dashboard."""
    from mitmios.proxy import show_simulator_info

    console.print(f"[bold green]mitmios v{__version__}[/bold green] - iOS Network Debugging Tool")
    console.print()

    if not no_simulator:
        show_simulator_info(proxy_port)

    console.print(f"[bold]Starting mitmweb...[/bold]")
    console.print(f"  Proxy:  http://{host}:{proxy_port}")
    console.print(f"  Web UI: http://{host}:{port}")
    console.print()

    args = [
        "--web-host", host,
        "--web-port", str(port),
        "--listen-port", str(proxy_port),
    ]
    if no_browser:
        args.extend(["--set", "web_open_browser=false"])

    try:
        from mitmproxy.tools.main import mitmweb
        mitmweb(args)
    except ImportError:
        console.print("[red]Error:[/red] mitmproxy is not installed.")
        console.print("Install it with: [bold]pip install mitmproxy[/bold]")
        console.print("Or: [bold]uv pip install 'mitmios[proxy]'[/bold]")
        raise typer.Exit(1)


@app.command()
def setup():
    """First-time setup: install mitmproxy CA certificate."""
    from mitmios.cert import run_setup
    run_setup()


@app.command()
def config(
    action: str = typer.Argument(help="Action: list, add, validate, example"),
    path: str = typer.Argument(None, help="Config file path (for add/validate)"),
):
    """Manage tracker configurations."""
    from mitmios.config import manage_config
    manage_config(action, path)
