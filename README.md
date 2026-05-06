# OSINT-Pro-Tool
Powerful open-source intelligence platform with dual interface (Desktop GUI + Telegram Bot) that searches social media using a single username, phone number, or name.

## Features

- **Single Identifier Input** – Automatically detects whether you’ve entered a username, phone number, or name.
- **Real Social Media Searches** – Public profile lookup on Telegram and Instagram (with metadata and post extraction).
- **Dual Interface** –  
  - Desktop GUI (dark mode, built with CustomTkinter)  
  - Telegram Bot (commands + inline buttons)
- **Instagram Media Download** – Save public posts straight to your machine via Instaloader.
- **Search History** – Local SQLite database stores every search with timestamps.
- **Modular Core** – Easily add new platforms or features.

## Quick Start

1. **Clone the repository**
``bash
   git clone https://github.com/yourusername/osint-pro-tool.git
   cd osint-pro-tool

   pip install -r requirements.txt
   
   python gui/app.py
   
(Optional) Run the Telegram bot
Get a token from @BotFather
Set the token in bot/telegram_bot.py (or environment variable BOT_TOKEN)
Launch the bot:python bot/telegram_bot.py

Project Structure

osint-pro-tool/
├── core/                  # Core OSINT logic
│   └── osint_functions.py
├── gui/                   # Desktop application
│   └── app.py
├── bot/                   # Telegram bot
│   └── telegram_bot.py
├── database/              # History and storage
│   └── history.py
├── downloads/             # Saved Instagram media
├── requirements.txt
└── README.md

## Supported Platforms

| Platform   | Status          | Capabilities                              |
|------------|-----------------|-------------------------------------------|
| Telegram   | ✅ Working      | Profile info, bio, photo URL              |
| Instagram  | ✅ Working      | Profile info, follower count, post download |
| Soroush    | ⚠️ Placeholder  | No public API available                   |
| Bale       | ⚠️ Placeholder  | No public API available                   |
| Rubika     | ⚠️ Placeholder  | No public API available                   |

## Telegram Bot Commands

| Command            | Description                     |
|--------------------|---------------------------------|
| `/start`           | Welcome message                 |
| `/search <input>`  | Search all platforms            |
| `/telegram <user>` | Telegram lookup only            |
| `/instagram <user>`| Instagram lookup only           |
| `/help`            | Show available commands         |

## Configuration

- **Proxy support** – Add your proxy details inside `core/osint_functions.py` if you are in a restricted network.
- **Environment variables** – Use `BOT_TOKEN` to keep your Telegram credentials safe (avoid hardcoding).
- **Virtual environment** recommended for isolation.

## Roadmap

- [ ] Reverse image search (Google / TinEye)
- [ ] Email breach checker (Have I Been Pwned)
- [ ] Username cross‑platform enumeration (Sherlock‑style)
- [ ] Web dashboard (Flask)
- [ ] Export to PDF / CSV / JSON
- [ ] EXIF and geolocation tools

## Important Notes

- **Educational & ethical use only** – only search for information you’re legally allowed to access.
- Private profiles cannot be viewed without authorization.
- The Iranian messenger placeholders exist because those apps lack open APIs.

## Contributing

Pull requests are welcome! Please:

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/amazing`)
3. Commit your changes
4. Push to the branch
5. Open a PR

Follow PEP 8 and include docstrings + type hints where possible.

## License

This project is licensed under the MIT License. See `LICENSE` for details.


---

If you need the description **shorter** (e.g., for a GitHub repo tagline or a social media post) just tell me and I’ll trim it further.

