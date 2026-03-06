# 📡 PhoneHome

> Know the moment your phone leaves — or returns to — your home network.

PhoneHome is a lightweight Python service that monitors your home network and sends instant **Telegram notifications** when your phone disconnects or reconnects. Runs silently in the background on a Raspberry Pi via PM2.

---

## ✨ Features

- 🔍 Detects phone presence via ARP + ping
- 📲 Instant Telegram alerts on leave/arrive
- 🔁 Retry logic — confirms 3 times before alerting
- ⚙️ Configurable via `.env` — no hardcoded values
- 🚀 Runs 24/7 on Raspberry Pi with PM2

---

## 🛠️ Requirements

- Python 3.9+
- Raspberry Pi (or any Linux machine)
- Node.js + PM2
- Telegram Bot Token + Chat ID

---

## 🚀 Setup

### 1. Clone the repo

```bash
git clone https://github.com/youruser/phonehome.git
cd phonehome
```

### 2. Create virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` with your values:

```env
PHONE_IP=your_phone_ip
PHONE_MAC=your_phone_mac
PING_FLAG=-c
TELEGRAM_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
CHECK_INTERVAL=60
```

### 4. Run with PM2

```bash
pm2 start ecosystem.config.js
pm2 save
pm2 startup
```

---

## 📁 Project Structure

```
phonehome/
├── phoneHome.py          # main script
├── ecosystem.config.js   # PM2 config
├── requirements.txt      # Python dependencies
├── .env                  # environment variables (not committed)
├── .env.example          # env template
└── README.md
```

---

## 📬 Telegram Notifications

| Event | Message |
|-------|---------|
| Phone left home | 🚨 Phone left home! |
| Phone arrived home | ✅ Phone is back home! |

---

## ⚙️ PM2 Commands

```bash
pm2 status               # check status
pm2 logs phone-tracker   # view logs
pm2 restart phone-tracker
pm2 stop phone-tracker
```

---

## 📄 License

MIT