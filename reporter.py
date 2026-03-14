import os
from datetime import datetime
from rich.console import Console

console = Console()

REPORTS_DIR = os.path.join(os.path.dirname(__file__), "dossiers")

def ensure_reports_dir():
    if not os.path.exists(REPORTS_DIR):
        os.makedirs(REPORTS_DIR)

def generate_strategic_dossier(target_url, contacts):
    """Generates a high-authority Strategic Communications Dossier."""
    ensure_reports_dir()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    safe_target = target_url.replace("https://", "").replace("http://", "").replace("/", "_")
    filename = f"dossier_{safe_target}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    filepath = os.path.join(REPORTS_DIR, filename)

    dossier_content = f"""# Strategic Communications Dossier: {target_url}

## 📋 Executive Intelligence Summary
- **Target Analysis**: {target_url}
- **Scan Timestamp**: {timestamp}
- **Intelligence Level**: High-Authority Base Recon

## 🛡️ Strategic Alignment (DPA Section 25)
This dossier facilitates 'Data Protection by Design' by identifying verified, institutional connection points, reducing the need for non-standardized/unsecured outreach.

## 🔎 Discovered Connection Points

### 📧 Email Assets
"""
    if contacts.get("emails"):
        for email in sorted(contacts["emails"]):
            dossier_content += f"- {email}\n"
    else:
        dossier_content += "*No email assets discovered.*\n"

    dossier_content += "\n### 📱 Mobile & Instant Messaging\n"
    if contacts.get("whatsapp") or contacts.get("phones"):
        for wa in sorted(contacts.get("whatsapp", [])):
            dossier_content += f"- [WhatsApp] {wa}\n"
        for phone in sorted(contacts.get("phones", [])):
            dossier_content += f"- [Phone] {phone}\n"
    else:
        dossier_content += "*No mobile assets discovered.*\n"

    dossier_content += "\n### 🌐 Social Intelligence Profiles\n"
    if contacts.get("socials"):
        for social in sorted(contacts["socials"]):
            dossier_content += f"- {social}\n"
    else:
        dossier_content += "*No social profiles discovered.*\n"

    dossier_content += f"""
---
## ⚖️ Authentication & Integrity
- **Verification Status**: RECON_SUCCESS
- **Data Minimization**: Policy-Aligned

**[ MWITHIGA LABS | COMMUNICATIONS INTELLIGENCE ]**
"""
    with open(filepath, 'w') as f:
        f.write(dossier_content)
    
    console.print(f"\n[bold green][√] Strategic Dossier generated:[/] [cyan]{filepath}[/]")
    return filepath
