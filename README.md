# Dispatch

Hey there, fellow seeker! I'm Mwithiga.

As a Public Relations student, I've seen firsthand how the right connection can change a story. My goal is to improve the world of PR by leveraging code and technology to create faster, smarter ways to connect.

Ever feel the frustration of landing on a website, needing to reach out, but finding yourself trapped in the "hustle" of digging through hidden pages just to find a simple email or contact form? 

I have. And that frustrated seeker moment is exactly why **Dispatch** was born.

Dispatch is a high-performance connection engine designed to bridge the gap between discovery and action. I wanted a tool that could "see" through the noise even on complex, JavaScript heavy sites and present every available connection point in a clean, actionable format. Whether it is an email, a phone number, a WhatsApp chat, or a social media profile, Dispatch finds it so you can initiate the conversation instantly.

## The Development Journey

Moving beyond a simple email harvester was a deliberate step in architecture. I realized that the "hustle" of contact discovery isn't just about emails; it's about finding the *right* way to connect.

The technical challenge was expanding the scope of detection without sacrificing accuracy. I implemented a modular harvesting logic that uses a combination of robust regular expressions for phone numbers and an intelligent link analysis system for social profiles and WhatsApp discovery. By leveraging a headless browser session through requests-html, Dispatch renders dynamic content, ensuring no valid contact is left behind.

I also focused on the "how" of communication. I didn't just want to list contacts; I wanted to act on them. This led to the creation of a unified connection menu that adapts to the type of contact found—launching mail clients with AI-drafted content, opening WhatsApp chats, or navigating directly to social profiles.

## Features

- **Multi-Contact Harvesting**: Automatically extracts emails, phone numbers, social media profiles (Instagram, Twitter, LinkedIn), and WhatsApp links.
- **Dynamic Content Support**: Executes JavaScript to find contacts that are hidden from static scrapers.
- **Intelligent Connection Menu**: Automatically chooses the right action (AI drafting for emails, direct links for socials, WhatsApp redirection).
- **Professional CLI**: A clean, "Rich" terminal experience that keeps the focus on the mission.

## Getting Started

To get a local instance of Dispatch up and running, follow these steps.

### Prerequisites

- Python 3.x
- A Linux environment (for desktop integration features)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/vintageGent/dispatch.git
   cd dispatch
   ```

2. Setup the virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

### Usage

The simplest way to use Dispatch is to provide a target URL:

```bash
python3 main.py https://example.com
```

Dispatch will scan the target, present a categorized table of connection points, and allow you to reach out with a single selection.

## A Personal Connection

Dispatch represents my philosophy that technology should remove barriers, not create them. For every seeker who has ever been stuck behind a "Contact Us" page that leads nowhere, this tool is for you. It turns the "hustle" of searching into the ease of connecting.
