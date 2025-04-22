#!/usr/bin/env python
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "typer",
#     "httpx",
#     "rich",
# ]
# ///

import json
import os
from pathlib import Path
from typing import List, Optional, Annotated, Dict, Any

import httpx
import typer
from rich.console import Console
from rich.panel import Panel

app = typer.Typer(help="CLI tool for creating GitHub issues via webhook proxy")
console = Console()

CONFIG_FILE = Path.home() / ".config" / "gh-notify" / "config.json"


def load_config() -> Dict[str, Any]:
    """Load configuration from file if it exists."""
    if not CONFIG_FILE.exists():
        return {}
    
    try:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, PermissionError) as e:
        console.print(f"[yellow]Warning:[/] Could not read config file: {e}")
        return {}


def create_issue(
    url: str,
    auth_token: str,
    title: str,
    body: str,
    existing: str = "update",
    labels: Optional[str] = None,
) -> dict:
    """Send a request to create or update a GitHub issue via the webhook proxy."""
    headers = {
        "Content-Type": "application/json",
        "x-auth": auth_token,
    }
    
    payload = {
        "title": title,
        "body": body,
        "existing": existing,
    }
    
    if labels:
        payload["labels"] = labels
    
    try:
        response = httpx.post(url, headers=headers, json=payload, timeout=30.0)
        response.raise_for_status()
        return response.json() if response.text else {"status": "success"}
    except httpx.HTTPStatusError as e:
        error_data = e.response.json() if e.response.text else {"error": str(e)}
        return {"status": "error", "status_code": e.response.status_code, **error_data}
    except httpx.RequestError as e:
        return {"status": "error", "message": f"Request failed: {str(e)}"}


@app.command()
def create(
    title: Annotated[str, typer.Option("--title", "-t", help="Title for the GitHub issue")],
    body: Annotated[
        Optional[str], 
        typer.Option("--body", "-b", help="Body content for the GitHub issue")
    ] = None,
    body_file: Annotated[
        Optional[Path], 
        typer.Option("--body-file", "-f", help="File containing body content for the GitHub issue")
    ] = None,
    existing: Annotated[
        str, 
        typer.Option(
            "--existing", 
            "-e", 
            help="How to handle existing issues: 'ignore', 'update', 'new', or 'comment'",
        )
    ] = "update",
    labels: Annotated[
        Optional[str], 
        typer.Option("--labels", "-l", help="Comma-separated list of labels to apply")
    ] = None,
    url: Annotated[
        Optional[str], 
        typer.Option("--url", "-u", help="URL of the webhook proxy")
    ] = None,
    auth_token: Annotated[
        Optional[str], 
        typer.Option("--auth-token", "-a", help="Auth token for the webhook proxy")
    ] = None,
    config: Annotated[
        Optional[Path], 
        typer.Option("--config", "-c", help="Path to alternative config file")
    ] = None,
):
    """Create or update a GitHub issue via webhook proxy."""
    # Load config
    cfg = {}
    if config and config.exists():
        try:
            with open(config, "r") as f:
                cfg = json.load(f)
        except (json.JSONDecodeError, PermissionError) as e:
            console.print(f"[bold red]Error:[/] Could not read specified config file: {e}")
            raise typer.Exit(1)
    else:
        cfg = load_config()

    # Merge config with command-line parameters (CLI params take precedence)
    webhook_url = url or cfg.get("url")
    auth = auth_token or cfg.get("auth_token")
    
    # Validate required parameters
    if not webhook_url:
        console.print("[bold red]Error:[/] Webhook URL is required. Provide it via --url or config file.")
        raise typer.Exit(1)
    
    if not auth:
        console.print("[bold red]Error:[/] Auth token is required. Provide it via --auth-token or config file.")
        raise typer.Exit(1)
    
    # Handle body content
    issue_body = body
    
    if body_file:
        if not body_file.exists():
            console.print(f"[bold red]Error:[/] Body file not found: {body_file}")
            raise typer.Exit(1)
        try:
            with open(body_file, "r") as f:
                issue_body = f.read()
        except Exception as e:
            console.print(f"[bold red]Error:[/] Could not read body file: {e}")
            raise typer.Exit(1)
    
    if not issue_body:
        console.print("[bold red]Error:[/] Issue body is required. Provide it via --body, --body-file, or stdin.")
        raise typer.Exit(1)
    
    # Validate existing parameter
    valid_existing_values = ["ignore", "update", "new", "comment"]
    if existing not in valid_existing_values:
        console.print(f"[bold red]Error:[/] Invalid 'existing' value. Must be one of: {', '.join(valid_existing_values)}")
        raise typer.Exit(1)
    
    # Create the issue
    with console.status("[bold green]Sending request to create GitHub issue..."):
        result = create_issue(
            url=webhook_url,
            auth_token=auth,
            title=title,
            body=issue_body,
            existing=existing,
            labels=labels,
        )
    
    if result.get("status") == "error":
        console.print(Panel(
            f"[bold red]Error creating issue:[/]\n{json.dumps(result, indent=2)}", 
            title="Error",
            border_style="red"
        ))
        raise typer.Exit(1)
    else:
        console.print(Panel(
            f"[bold green]Successfully sent issue creation request[/]\n\n"
            f"[bold]Title:[/] {title}\n"
            f"[bold]Existing:[/] {existing}\n"
            f"[bold]Labels:[/] {labels or 'None'}", 
            title="Success",
            border_style="green"
        ))


@app.command()
def setup(
    url: Annotated[str, typer.Option("--url", "-u", help="URL of the webhook proxy")] = None,
    auth_token: Annotated[str, typer.Option("--auth-token", "-a", help="Auth token for the webhook proxy")] = None,
    force: Annotated[bool, typer.Option("--force", "-f", help="Overwrite existing config")] = False,
):
    """Setup or update the configuration file."""
    # Check if config directory exists, create if not
    config_dir = CONFIG_FILE.parent
    if not config_dir.exists():
        try:
            config_dir.mkdir(parents=True, exist_ok=True)
        except PermissionError as e:
            console.print(f"[bold red]Error:[/] Could not create config directory: {e}")
            raise typer.Exit(1)
    
    # Load existing config if it exists
    existing_config = {}
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r") as f:
                existing_config = json.load(f)
        except json.JSONDecodeError:
            if not force:
                console.print("[bold yellow]Warning:[/] Config file exists but is not valid JSON.")
                if not typer.confirm("Do you want to overwrite it?"):
                    raise typer.Exit(0)
        except PermissionError as e:
            console.print(f"[bold red]Error:[/] Could not read config file: {e}")
            raise typer.Exit(1)
    
    # Update config with new values
    new_config = existing_config.copy()
    
    if url is not None:
        new_config["url"] = url
    elif "url" not in new_config:
        new_url = typer.prompt("Enter webhook proxy URL")
        new_config["url"] = new_url
    
    if auth_token is not None:
        new_config["auth_token"] = auth_token
    elif "auth_token" not in new_config:
        new_token = typer.prompt("Enter webhook auth token", hide_input=True)
        new_config["auth_token"] = new_token
    
    # Write updated config
    try:
        print(f"Attempting to write config to: {CONFIG_FILE}")
        with open(CONFIG_FILE, "w") as f:
            json.dump(new_config, f, indent=2)
        console.print(f"[bold green]Configuration saved to {CONFIG_FILE}[/]")
    except PermissionError as e:
        console.print(f"[bold red]Error:[/] Could not write to config file: {e}")
        raise typer.Exit(1)


@app.command()
def stdin_create(
    title: Annotated[str, typer.Argument(help="Title for the GitHub issue")],
    existing: Annotated[
        str, 
        typer.Option(
            "--existing", 
            "-e", 
            help="How to handle existing issues: 'ignore', 'update', 'new', or 'comment'",
        )
    ] = "update",
    labels: Annotated[
        Optional[str], 
        typer.Option("--labels", "-l", help="Comma-separated list of labels to apply")
    ] = None,
    url: Annotated[
        Optional[str], 
        typer.Option("--url", "-u", help="URL of the webhook proxy")
    ] = None,
    auth_token: Annotated[
        Optional[str], 
        typer.Option("--auth-token", "-a", help="Auth token for the webhook proxy")
    ] = None,
):
    """Create a GitHub issue with body content from stdin."""
    import sys
    
    # Load config
    cfg = load_config()
    
    # Read from stdin
    body = sys.stdin.read()
    
    # Merge config with command-line parameters (CLI params take precedence)
    webhook_url = url or cfg.get("url")
    auth = auth_token or cfg.get("auth_token")
    
    # Validate required parameters
    if not webhook_url:
        console.print("[bold red]Error:[/] Webhook URL is required. Provide it via --url or config file.")
        raise typer.Exit(1)
    
    if not auth:
        console.print("[bold red]Error:[/] Auth token is required. Provide it via --auth-token or config file.")
        raise typer.Exit(1)
    
    # Validate existing parameter
    valid_existing_values = ["ignore", "update", "new", "comment"]
    if existing not in valid_existing_values:
        console.print(f"[bold red]Error:[/] Invalid 'existing' value. Must be one of: {', '.join(valid_existing_values)}")
        raise typer.Exit(1)
    
    # Create the issue
    with console.status("[bold green]Sending request to create GitHub issue..."):
        result = create_issue(
            url=webhook_url,
            auth_token=auth,
            title=title,
            body=body,
            existing=existing,
            labels=labels,
        )
    
    if result.get("status") == "error":
        console.print(Panel(
            f"[bold red]Error creating issue:[/]\n{json.dumps(result, indent=2)}", 
            title="Error",
            border_style="red"
        ))
        raise typer.Exit(1)
    else:
        console.print(Panel(
            f"[bold green]Successfully sent issue creation request[/]\n\n"
            f"[bold]Title:[/] {title}\n"
            f"[bold]Existing:[/] {existing}\n"
            f"[bold]Labels:[/] {labels or 'None'}", 
            title="Success",
            border_style="green"
        ))


if __name__ == "__main__":
    app()
