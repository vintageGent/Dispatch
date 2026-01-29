import sys
import re
import subprocess
import urllib.parse
import requests
from requests_html import HTMLSession
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt, IntPrompt

console = Console()

def display_banner():
    """Displays a professional banner for the Email Assistant."""
    console.print("\n" + "="*60, style="blue")
    console.print(r"""
  ______                 _ _      _         _     _             _ 
 |  ____|               (_) |    / \   ___ (_)___| |_ __ _ _ __| |_
 | |__   _ __ ___   __ _ _| |   / _ \ / __|| / __| __/ _` | '_ \ __|
 |  __| | '_ ` _ \ / _` | | |  / ___ \\__ \| \__ \ || (_| | | | | |_ 
 | |____| | | | | | (_| | | | /_/   \_\___/|_|___/\__\__,_|_| |_|\__|
 |______|_| |_| |_|\__,_|_|_|                                        
    """, style="bold cyan")
    console.print("="*60, style="blue")
    console.print("  Email Assistant: Automated Contact Harvesting & AI Drafting", style="italic")
    console.print("="*60, style="blue")
    console.print("\n[bold cyan]Welcome to Email Assistant![/] This tool helps you extract contact emails")
    console.print("from websites and quickly draft professional inquiries for your needs.\n")

def display_help():
    """Displays a usage guide for the Email Assistant."""
    help_panel = Panel(
        "[bold cyan]Usage Guide[/]\n\n"
        "1. [bold white]Harvesting:[/] Provide a URL, and the tool will use a headless browser\n"
        "   to find all unique email addresses, even those rendered via JavaScript.\n\n"
        "2. [bold white]Selection:[/] Choose an email address from the discovered list.\n\n"
        "3. [bold white]AI Drafting:[/] Provide your intent (e.g., 'applying for a job'), and\n"
        "   the tool will generate a professional draft for you.\n\n"
        "4. [bold white]Launching:[/] Automatically open your default email client with the\n"
        "   draft ready to go.",
        title="[bold green]HOW IT WORKS[/]",
        expand=False
    )
    console.print(help_panel)
    Prompt.ask("\nPress [bold white]Enter[/] to continue")

def harvest_emails(url):
    """Fetches and extracts emails from a given URL using requests-html."""
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            progress.add_task(description="Initializing headless browser...", total=None)
            session = HTMLSession()
            
            task_download = progress.add_task(description="Downloading page content...", total=None)
            response = session.get(url, timeout=30)
            
            task_render = progress.add_task(description="Rendering JavaScript (dynamic content)...", total=None)
            response.html.render(sleep=2, timeout=30)
            
            progress.update(task_render, description="Scanning for emails...")
            email_regex = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
            emails = set(re.findall(email_regex, response.html.text))
            
        return list(emails)

    except Exception as e:
        console.print(f"[bold red]Error during harvesting:[/] {e}")
        return []

def generate_draft(intent):
    """Generates a professional email draft based on intent."""
    subject = f"Inquiry: {intent}"
    body = (
        f"Dear Sir/Madam,\n\n"
        f"I am writing to you regarding the following: {intent}.\n\n"
        f"I found your contact information listed on your website and wanted to reach out directly.\n\n"
        f"Any information or guidance you could provide would be greatly appreciated.\n\n"
        f"Thank you for your time.\n\n"
        f"Sincerely,\n\n"
        f"[Your Name]"
    )
    return subject, body

def main():
    display_banner()

    if len(sys.argv) < 2:
        console.print("[yellow]Hint:[/] Run with a URL to start harvesting immediately.")
        console.print("[dim]Usage: python3 main.py <URL>[/]")
        url = Prompt.ask("\nEnter target URL to scan")
    else:
        url = sys.argv[1]

    emails = harvest_emails(url)

    if not emails:
        console.print("[bold yellow]No email addresses found on this page.[/]")
        sys.exit(0)

    # Display results in a table
    table = Table(title=f"Discovered Contacts for {url}")
    table.add_column("ID", justify="right", style="cyan", no_wrap=True)
    table.add_column("Email Address", style="magenta")

    for i, email in enumerate(emails):
        table.add_row(str(i + 1), email)

    console.print(table)

    # Selection
    choice = IntPrompt.ask("\nSelect an email ID to compose a draft (or 0 to exit)", choices=[str(i) for i in range(len(emails) + 1)])
    
    if choice == 0:
        console.print("[dim]Exiting...[/]")
        sys.exit(0)

    selected_email = emails[choice - 1]
    console.print(f"\nLocked on: [bold green]{selected_email}[/]")

    # Intent and Drafting
    intent = Prompt.ask("\nWhat is the purpose of this email?", default="Business Inquiry")
    
    subject, body = generate_draft(intent)

    draft_panel = Panel(
        f"[bold blue]Subject:[/] {subject}\n"
        f"--------------------------------------------------\n"
        f"{body}",
        title="[bold green]AI GENERATED DRAFT[/]",
        border_style="green"
    )
    console.print("\n", draft_panel)

    # Launching
    confirm = Prompt.ask("\nLaunch email client with this draft?", choices=["y", "n"], default="y")

    if confirm.lower() == 'y':
        console.print("[bold blue]Launching default mail client...[/]")
        encoded_subject = urllib.parse.quote(subject)
        encoded_body = urllib.parse.quote(body)
        mailto_link = f"mailto:{selected_email}?subject={encoded_subject}&body={encoded_body}"

        try:
            subprocess.run(['xdg-open', mailto_link], check=True)
            console.print("[bold green]✔ Success![/] Opening your email application.")
        except Exception as e:
            console.print(f"[bold red]Failed to launch client:[/] {e}")
            console.print("\n[dim]Manual link:[/]\n", mailto_link)
    else:
        console.print("[yellow]Draft discarded.[/]")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[red]Process interrupted by user.[/]")
        sys.exit(0)
