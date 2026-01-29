# Email Assistant

Hey there, fellow seeker! I'm Mwithiga.

In the digital age, finding a point of contact can often feel like searching for a needle in a haystack. I built Email Assistant to streamline the process of discovering and reaching out to the right people. It is a tool designed to close the gap between information discovery and professional communication.

Email Assistant is an automated contact harvesting and AI-assisted drafting tool. It handles the manual labor of scanning web pages—even those with complex, dynamic content—and provides a professional interface to draft and launch inquiries instantly.

## The Development Journey

The inspiration for this project came from my own experiences trying to connect with professionals and organizations. Scanning through multiple pages and manually drafting similar emails felt like a missed opportunity for automation.

The primary technical challenge was ensuring that the tool could see what a human sees. Many modern websites use JavaScript to hide or render content dynamically. By integrating a headless browser session through `requests-html`, I enabled Email Assistant to render the full state of a page, ensuring that no valid contact is missed.

Once the harvesting was reliable, I focused on the "last mile" of the process: the communication. I wanted to move beyond simple extraction and provide a way to act on the information immediately. This led to the creation of the AI drafting engine and the integration with system-level mail clients, turning a multi-step process into a single, cohesive workflow.

## Features

- **Dynamic Harvesting**: Uses a headless browser to extract emails from static and JavaScript-rendered pages.
- **Rich Interactive UI**: A professional terminal interface powered by the `rich` library.
- **AI-Assisted Drafting**: Automatically generates professional email drafts based on your specific intent.
- **One-Click Launch**: Seamlessly opens your default email client with the draft prepared and the recipient set.

## Getting Started

To begin using Email Assistant, follow these steps to prepare your environment.

### Prerequisites

- Python 3.x
- A Linux environment (for `xdg-open` support)

### Installation

1. Clone the repository (or copy the project files):
   ```bash
   cd email_assistant
   ```

2. Set up the virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

### Usage

Run the assistant by providing a target URL:

```bash
python3 main.py https://example.com
```

The tool will scan the page, display the discovered contacts, and walk you through the process of selecting a recipient and drafting your message.

## A Personal Connection

Email Assistant is more than just a scraper; it's a productivity companion. It reflects my belief that technology should serve as a bridge to meaningful interaction. For every fellow seeker looking to reach out and make a connection, I hope this tool helps you find your voice.
