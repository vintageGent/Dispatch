import os
import sys
import argparse
import webbrowser
import subprocess # Added subprocess
import urllib.parse
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table

console = Console()

def display_banner():
    banner = """
    [bold cyan]
     _____                     
    |  __ \                    
    | |__) |___  ___ ___  _ __ 
    |  _  // _ \/ __/ _ \| '_ \\
    | | \ \  __/ (_| (_) | | | |
    |_|  \_\___|\___\___/|_| |_|
    [/bold cyan]
    [italic]Intelligence Pivot: Email Recon Module[/italic]
    """
    console.print(Panel(banner, border_style="cyan"))

def analyze_domain(email):
    """Break down the email to understand the 'Pivot'."""
    try:
        domain = email.split('@')[1]
    except IndexError:
        return "Invalid Email", "Unknown"
    
    personal_domains = ['gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com', 'icloud.com']
    
    if domain in personal_domains:
        return domain, "Personal (Standard)"
    else:
        return domain, "Corporate/Private (High Value)"

def generate_recon_links(email, domain):
    """Generates OSINT links for deeper investigation."""
    encoded_email = urllib.parse.quote(email)
    
    links = [
        {"platform": "EPIEOS (Social Presence)", "url": f"https://epieos.com/?q={encoded_email}"},
        {"platform": "HaveIBeenPwned (Breaches)", "url": f"https://haveibeenpwned.com/account/{encoded_email}"},
        {"platform": "LinkedIn (Social Search)", "url": f"https://www.linkedin.com/search/results/all/?keywords={encoded_email}"},
        {"platform": "Hunter.io (Organization Pivot)", "url": f"https://hunter.io/search/{domain}"},
        {"platform": "RocketReach (Contact Intel)", "url": f"https://rocketreach.co/search?keyword={domain}"},
        {"platform": "Google Dork (Web History)", "url": f"https://www.google.com/search?q=intext:\"{encoded_email}\""},
    ]
    
    return links

def main():
    parser = argparse.ArgumentParser(description="Intelligence Pivot: Email Recon Module")
    parser.add_argument("--target", help="Target Email for Recon")
    args = parser.parse_args()

    if not args.target:
        os.system('clear')
        display_banner()
        target = Prompt.ask("\n[bold cyan][?][/bold cyan] Enter Target Email for Recon")
    else:
        target = args.target

    if "@" not in target:
        console.print("[red][!] Invalid input. Email must contain '@'[/red]")
        sys.exit(1)
        
    domain_name, domain_type = analyze_domain(target)
    
    # Intelligence Report Table
    table = Table(title=f"Intelligence Report: {target}", border_style="cyan")
    table.add_column("Field", style="bold green")
    table.add_column("Finding", style="white")
    
    table.add_row("Target Email", target)
    table.add_row("Primary Domain", domain_name)
    table.add_row("Domain Type", domain_type)
    
    console.print(table)
    
    console.print("\n[bold yellow][*] Generating OSINT Pivot Links...[/bold yellow]")
    recon_links = generate_recon_links(target, domain_name)
    
    link_table = Table(show_header=True, header_style="bold magenta")
    link_table.add_column("ID", justify="right")
    link_table.add_column("Intelligence Platform")
    
    for idx, link in enumerate(recon_links, 1):
        link_table.add_row(str(idx), link['platform'])
        
    console.print(link_table)
    
    if not args.target:
        choice = Prompt.ask("\n[bold cyan][?][/bold cyan] Select an Intelligence Platform to pivot (or 'q' to exit)", choices=[str(i) for i in range(1, len(recon_links)+1)] + ['q'])
        
        if choice.lower() != 'q':
            selected_link = recon_links[int(choice)-1]['url']
            console.print(f"[bold green][*] Pivoting to Intelligence Source...[/bold green]")
            # We use webbrowser for professional feel, if console allows
            console.print(f"[dim]Commanding system to open: {selected_link}[/dim]")
            
            # If we have xdg-open (linux), we use it. Otherwise webbrowser.
            if sys.platform.startswith('linux'):
                 os.system(f"xdg-open '{selected_link}'")
            else:
                 webbrowser.open(selected_link)

        # Strategic Hub Pivot
        if Prompt.ask("\n[bold cyan][?][/bold cyan] Pivot to Organization Connection Engine (main.py)?", choices=["y", "n"], default="y") == 'y':
            console.print(f"[bold green][*] Pivoting to Organizational Recon for {domain_name}...[/bold green]")
            subprocess.run([sys.executable, "main.py", f"https://{domain_name}"])
    else:
        console.print("\n[bold green][*] Recon summary generated. Use the links above for investigation.[/bold green]")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[red][!] Recon session terminated.[/red]")
        sys.exit(0)
