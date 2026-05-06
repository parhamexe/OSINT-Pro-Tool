# OSINT-Pro-Tool
Powerful open-source intelligence platform with dual interface (Desktop GUI + Telegram Bot) that searches social media using a single username, phone number, or name.

🔍 OSINT Pro Tool - Advanced Open Source Intelligence Platform








A powerful, multi-interface OSINT (Open Source Intelligence) tool with both desktop GUI and Telegram Bot interfaces for searching across social media platforms, phone numbers, and usernames.

✨ Features
🔎 Multi-Platform Search
Telegram: Public profile lookup with detailed information extraction
Instagram: Profile detection, metadata extraction, and media downloading
Iranian Platforms: Soroush, Bale, Rubika (placeholder APIs)
Single Identifier: Search by username, phone number, or name only
💻 Dual Interface
Desktop GUI: Modern dark-themed interface with CustomTkinter
Telegram Bot: 24/7 access from anywhere with inline buttons and commands
Unified Backend: Same core functions power both interfaces
📦 Advanced Capabilities
Auto-Type Detection: Automatically identifies input as username/phone/name
Instagram Media Download: Download posts from public profiles (Instaloader)
Search History: SQLite database stores all searches with timestamps
Modular Architecture: Easy to extend with new platforms or features
📸 Screenshots
Desktop GUI
┌─────────────────────────────────────┐

│ 🔍 OSINT Pro Tool │

├─────────────────────────────────────┤

│ Enter Username, Phone, or Name: │

│ [_____________________________] │

│ Type: 👤 Username │

│ │

│ ✓ Telegram ✓ Instagram │

│ ✗ Soroush ✗ Bale ✗ Rubika │

│ │

│ [✓] Download Instagram Media │

│ [✓] Save to Search History │

│ │

│ [🚀 SEARCH ALL PLATFORMS] │

└─────────────────────────────────────┘

Telegram Bot Commands
/search john_doe

/telegram @username

/instagram username

🚀 Quick Start
Prerequisites
Python 3.8 or higher
pip (Python package manager)
Installation
Clone the repository
bash
-----git clone https://github.com/yourusername/osint-pro-tool.git
------cd osint-pro-tool
------Install dependencies
----bash
-------pip install -r requirements.txt
Run the GUI
----bash
----python gui/app.py
📁 Project Structure
osint-pro-tool/

├── core/ # Core OSINT functions

│ ├── init.py

│ └── osint_functions.py # Search logic for all platforms

├── gui/ # Desktop interface

│ └── app.py # Modern GUI with CustomTkinter

├── bot/ # Telegram bot

│ └── telegram_bot.py # Bot implementation

├── database/ # Data storage

│ └── history.py # SQLite database for search history

├── downloads/ # Instagram media downloads

├── requirements.txt # Python dependencies

├── README.md # This file

└── LICENSE # MIT License

🔧 Usage
Desktop GUI
Launch python gui/app.py
Enter any identifier (username, phone, or name)
Select platforms to search
Click “Search All Platforms”
View results and download media if needed
Telegram Bot
Get a bot token from @BotFather
Update BOT_TOKEN in bot/telegram_bot.py
Run the bot: python bot/telegram_bot.py
Interact via Telegram commands
Available Bot Commands:

/start - Show welcome message

/search [identifier] - Search all platforms

/telegram [username] - Search Telegram only

/instagram [username] - Search Instagram only

/help - Show help message

⚙️ Configuration
Environment Variables
For Telegram Bot deployment:

bash
export BOT_TOKEN="your_bot_token_here"
Proxy Support
Add proxy configuration in core/osint_functions.py for network-restricted regions:

python
proxies = {
    'http': 'http://your-proxy:port',
    'https': 'http://your-proxy:port'
}
requests.get(url, proxies=proxies, ...)
📊 Features in Detail
🔍 Search Capabilities
Telegram: Extracts display name, bio, profile photo URL
Instagram: Gets follower count, posts, bio, and media
Auto-Detection: Smart input type recognition
Bulk Search: Search single identifier across multiple platforms
💾 Data Management
SQLite Database: Stores all search results locally
Search History: View and export past searches
Media Downloads: Organized folder structure for Instagram content
🤖 Telegram Bot Features
Inline Buttons: Quick actions for extended search/download
Typing Indicators: Real-time feedback
Markdown Support: Formatted responses
Callback Queries: Interactive button responses
🌐 Platform Support
Platform	Status	Features
Telegram	✅ Working	Profile detection, info extraction
Instagram	✅ Working	Profile info, media download
Soroush	⚠️ Placeholder	No public API available
Bale	⚠️ Placeholder	No public API available
Rubika	⚠️ Placeholder	No public API available
🔒 Security & Privacy
Best Practices
No Credentials in Code: Use environment variables
Local Storage: Search history stored locally by default
Public APIs Only: Only searches publicly available information
Rate Limiting: Respects platform API limits
VPS Deployment
For secure deployment on your VPS:

bash
# 1. SSH to your VPS
ssh user@your-vps-ip

# 2. Clone and setup
git clone https://github.com/yourusername/osint-pro-tool.git
cd osint-pro-tool

# 3. Install in virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 4. Run bot as service
nohup python bot/telegram_bot.py > bot.log 2>&1 &
🛠️ Development
Adding New Platforms
Add search function in core/osint_functions.py:
python
def search_new_platform(identifier: str, identifier_type: str) -> Dict:
    # Your implementation
    return {"success": True, "message": "Found", "data": {...}}
Update platform_functions dictionary
Add to GUI platform selection
Add bot command if needed
Running Tests
bash
python -m pytest tests/
📈 Roadmap
Planned Features
[ ] Reverse Image Search (Google, TinEye)
[ ] Email Breach Check (Have I Been Pwned)
[ ] Username Enumeration (Sherlock integration)
[ ] Web Dashboard (Flask + VPS hosting)
[ ] API Server (RESTful endpoints)
[ ] Export Formats (PDF, CSV, JSON reports)
[ ] Geolocation Tools (EXIF, IP lookup)
Contribution Ideas
Add support for more social platforms
Improve GUI with charts/visualizations
Add multilingual support
Create browser extension
Develop mobile app
⚠️ Important Notes
Legal & Ethical Use
This tool is for educational purposes only
Only search for publicly available information
Respect privacy and applicable laws
Do not use for harassment or illegal activities
Limitations
Iranian apps lack public APIs (placeholders only)
Private profiles cannot be accessed without authorization
Rate limiting may apply to frequent searches
Network restrictions may require VPN/proxy
🤝 Contributing
Contributions are welcome! Please follow these steps:

Fork the repository
Create a feature branch: git checkout -b feature-name
Commit changes: git commit -m 'Add feature'
Push to branch: git push origin feature-name
Open a Pull Request
Code Style
Follow PEP 8 guidelines
Add docstrings to functions
Include type hints where possible
Write clear commit messages
📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

MIT License

Copyright © 2024 Your Name

Permission is hereby granted, free of charge, to any person obtaining a copy

of this software and associated documentation files (the “Software”), to deal

in the Software without restriction, including without limitation the rights

to use, copy, modify, merge, publish, distribute, sublicense, and/or sell

copies of the Software, and to permit persons to whom the Software is

furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all

copies or substantial portions of the Software.
