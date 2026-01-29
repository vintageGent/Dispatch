import sys
import re
import subprocess
import urllib.parse
import os
import requests
from requests_html import HTMLSession
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt, IntPrompt

console = Console()

def display_banner():
    """Displays a professional banner for Dispatch."""
    console.print("\n" + "="*60, style="blue")
    console.print(r"""
  _____  _                 _       _      _ 
 |  __ \(_)               | |     | |    | |
 | |  | |_ ___ _ __   __ _| |_ ___| |__  | |
 | |  | | / __| '_ \ / _` | __/ __| '_ \ | |
 | |__| | \__ \ |_) | (_| | || (__| | | ||_|
 |_____/|_|___/ .__/ \__,_|\__\___|_| |_|(_)
              | |                           
              |_|                           
    """, style="bold cyan")
    console.print("="*60, style="blue")
    console.print("  Dispatch: The Fast-Track Connection Engine", style="italic")
    console.print("="*60, style="blue")
    console.print("\n[bold cyan]Welcome to Dispatch![/] Find your point of contact instantly.")
    console.print("Whether it's an email, a phone number, or a social profile, we bridge")
    console.print("the gap between your inquiry and their inbox.\n")

def harvest_contacts(url):
    """Fetches and extracts various contacts from a given URL."""
    contacts = {
        "emails": set(),
        "phones": set(),
        "socials": set(),
        "whatsapp": set()
    }
    
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            progress.add_task(description="Initializing headless browser...", total=None)
            session = HTMLSession()
            
            progress.add_task(description="Downloading page content...", total=None)
            response = session.get(url, timeout=30)
            
            progress.add_task(description="Rendering JavaScript (dynamic content)...", total=None)
            response.html.render(sleep=2, timeout=30)
            
            html_text = response.html.text
            links = response.html.absolute_links
            
            progress.print("[dim]Scanning for contacts...[/]")
            
            # 1. Emails
            email_regex = r"[a-zA-Z0-9._%+-]+@(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}"
            contacts["emails"] = set(re.findall(email_regex, html_text))
            
            # 2. Phones (International and local variants)
            phone_regex = r"\+?\d[\d\s\-\(\)]{8,}\d"
            potential_phones = re.findall(phone_regex, html_text)
            for p in potential_phones:
                clean_p = re.sub(r'[\s\-\(\)]', '', p)
                if 9 <= len(clean_p) <= 15: # Standard phone length
                    contacts["phones"].add(p.strip())
            
            # 3. Social Media & WhatsApp
            social_domains = ['instagram.com', 'twitter.com', 'x.com', 'facebook.com', 'linkedin.com', 'wa.me', 'whatsapp.com']
            for link in links:
                if any(domain in link.lower() for domain in social_domains):
                    if 'wa.me' in link.lower() or 'whatsapp.com' in link.lower():
                        contacts["whatsapp"].add(link)
                    else:
                        contacts["socials"].add(link)
            
        return contacts

    except Exception as e:
        console.print(f"[bold red]Error during harvesting:[/] {e}")
        return contacts

def generate_email_draft(intent):
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

    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url

    results = harvest_contacts(url)
    
    # Flatten results for selection
    all_contacts = []
    
    table = Table(title=f"Discovered Connection Points: {url}")
    table.add_column("ID", justify="right", style="cyan", no_wrap=True)
    table.add_column("Type", style="green")
    table.add_column("Contact Information", style="magenta")

    idx = 1
    for email in sorted(results["emails"]):
        table.add_row(str(idx), "Email", email)
        all_contacts.append({"type": "email", "val": email})
        idx += 1
    for wa in sorted(results["whatsapp"]):
        table.add_row(str(idx), "WhatsApp", wa)
        all_contacts.append({"type": "whatsapp", "val": wa})
        idx += 1
    for phone in sorted(results["phones"]):
        table.add_row(str(idx), "Phone", phone)
        all_contacts.append({"type": "phone", "val": phone})
        idx += 1
    for social in sorted(results["socials"]):
        table.add_row(str(idx), "Social", social)
        all_contacts.append({"type": "social", "val": social})
        idx += 1

    if not all_contacts:
        console.print("[bold yellow]No contact information discovered on this page.[/]")
        sys.exit(0)

    console.print(table)

    # Selection
    choice_id = IntPrompt.ask("\nSelect a contact ID to connect (or 0 to exit)", choices=[str(i) for i in range(idx)])
    
    if choice_id == 0:
        console.print("[dim]Exiting...[/]")
        sys.exit(0)

    selection = all_contacts[choice_id - 1]
    console.print(f"\n[bold green]Connecting via {selection['type']}...[/]")

    if selection['type'] == 'email':
        intent = Prompt.ask("\nWhat is the purpose of this email?", default="Business Inquiry")
        subject, body = generate_email_draft(intent)
        
        draft_panel = Panel(f"[bold blue]Subject:[/] {subject}\n---\n{body}", title="Draft Inquiry", border_style="green")
        console.print(draft_panel)
        
        if Prompt.ask("Launch mail client?", choices=["y", "n"], default="y") == 'y':
            mailto = f"mailto:{selection['val']}?subject={urllib.parse.quote(subject)}&body={urllib.parse.quote(body)}"
            os.system(f"xdg-open '{mailto}'")
            
    elif selection['type'] == 'whatsapp' or selection['type'] == 'social':
        console.print(f"[bold blue]Opening link:[/] {selection['val']}")
        os.system(f"xdg-open '{selection['val']}'")
        
    elif selection['type'] == 'phone':
        console.print(f"[bold yellow]Phone number detected:[/] {selection['val']}")
        console.print("[dim]Tip: You can dial this number directly on your mobile device.[/]")
        if Prompt.ask("Try to open dialer? (Desktop supported)", choices=["y", "n"], default="n") == 'y':
            os.system(f"xdg-open 'tel:{selection['val']}'")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[red]Session terminated.[/]")
        sys.exit(0)
