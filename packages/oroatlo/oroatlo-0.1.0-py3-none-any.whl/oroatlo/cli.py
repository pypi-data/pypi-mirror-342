import typer
from rich.console import Console
from typing import Optional
from .api import TLOApi, TLOApiError
import os

app = typer.Typer(help="OroaTLO CLI - A command-line interface for TLO searches")
console = Console()

def get_admin_key() -> str:
    key_file = os.path.expanduser("~/.oroatlo")
    if os.path.exists(key_file):
        with open(key_file) as f:
            return f.read().strip()
    return ""

def save_admin_key(key: str):
    key_file = os.path.expanduser("~/.oroatlo")
    with open(key_file, "w") as f:
        f.write(key)

@app.command()
def config(
    admin_key: str = typer.Option(..., "--admin-key", "-k", help="Set your admin key"),
):
    """
    Configure your admin key
    """
    save_admin_key(admin_key)
    console.print("[green]Admin key saved successfully!")

@app.command()
def search(
    first_name: Optional[str] = typer.Option(None, "--first-name", "-f", help="First name"),
    middle: Optional[str] = typer.Option(None, "--middle", "-m", help="Middle name"),
    last_name: Optional[str] = typer.Option(None, "--last-name", "-l", help="Last name"),
    street: Optional[str] = typer.Option(None, "--street", "-s", help="Street address"),
    city: Optional[str] = typer.Option(None, "--city", "-c", help="City"),
    state: Optional[str] = typer.Option(None, "--state", "-st", help="State"),
    zip_code: Optional[str] = typer.Option(None, "--zip", "-z", help="ZIP code"),
    admin_key: Optional[str] = typer.Option(None, "--admin-key", "-k", help="Admin key (optional if already configured)"),
):
    """
    Search for a person by name or address
    """
    with console.status("[bold green]Searching..."):
        try:
            key = admin_key or get_admin_key()
            if not key:
                console.print("[red]Error: Admin key not provided. Either use --admin-key or run 'oroatlo config' first.")
                raise typer.Exit(1)

            api = TLOApi(key)
            params = {
                "firstName": first_name,
                "middle": middle,
                "lastName": last_name,
                "street": street,
                "city": city,
                "state": state,
                "zip": zip_code,
            }
            params = {k: v for k, v in params.items() if v is not None}
            
            if not params:
                console.print("[red]Error: At least one search parameter is required")
                raise typer.Exit(1)
            
            result = api.search(**params)
            formatted = api.format_person_data(result)
            console.print(formatted)
            
        except TLOApiError as e:
            console.print(f"[red]Error: {str(e)}")
            raise typer.Exit(1)
        except Exception:
            console.print("[red]Error: An unexpected error occurred")
            raise typer.Exit(1)

if __name__ == "__main__":
    app() 