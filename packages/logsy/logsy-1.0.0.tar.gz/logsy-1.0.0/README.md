# logsy

✨ A clean, colorful, emoji-powered terminal logger with support for boxed messages and file:line context.

---

## 🚀 Features

- Emoji-based logging levels (`🐞 DEBUG`, `ℹ️ INFO`, `⚠️ WARN`, `🛑 ERROR`)
- Boxed messages for visual emphasis
- Colored terminal output using ANSI escape codes
- Shows filename and line number in every log
- Easily integratable into any Python project

---

## 📦 Installation

Install from source:

```bash
git clone https://github.com/prateekgupta1089/logsy.git
cd logsy
pip install -e .

🧪 Usage
from logsy import logger

logger.debug("Debugging stuff")
logger.info("Startup successful")
logger.warn("This might be risky")
logger.error("Oops, something failed")
logger.box("System initialized successfully")

✅ Output:
2025-04-21 12:00:00.123 🐞- Debugging stuff [my_script:10]
2025-04-21 12:00:00.124 ℹ️- Startup successful [my_script:11]
2025-04-21 12:00:00.125 ⚠️- This might be risky [my_script:12]
2025-04-21 12:00:00.126 🛑- Oops, something failed [my_script:13]
2025-04-21 12:00:00.127 [my_script:14] -
+---------------------------------+
| System initialized successfully |
+---------------------------------+

📁 Project Structure
logsy/
├── logsy/
│   └── formatter.py       # main logger class
├── README.md
├── setup.py
└── pyproject.toml

📜 License

This project is licensed under the MIT License.
Feel free to use, modify, and share freely.

✍️ Author

Prateek Gupta
Drop a ⭐ if this saves you time!