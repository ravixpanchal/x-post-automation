# 🎬 Simple Video Script: Twitter Automation Engine

A beginner-friendly guide and step-by-step video script for presenting or explaining this project clearly in under 4 minutes.

---

## ⚡ Key Takeaway: Everything Runs via 1 Single Command!

```bash
docker-compose up --build -d
```

Running this **single command** launches **all 4 core components** at once inside Docker:
1. 🌐 **Flask Webhook Server** (`app.py`: port 5000)
2. 🔗 **Ngrok Public Tunnel** (connects Slack buttons to Flask)
3. 🤖 **AI Tweet Generator Loop** (`generate_post.py`: initial draft + periodic schedule)
4. 🎭 **Playwright Twitter Auto-Poster** (`post_to_x.py`: posts approved tweets)

---

## 💡 Quick Project Summary (30 Seconds)

- **Problem**: Twitter API costs \$100+/month, while 100% fully-automated bots post weird/unwanted tweets when unmonitored.
- **Solution**: An AI bot that drafts tech/AI tweets for free using **OpenRouter LLMs**, sends interactive **Approve/Reject** cards to **Slack**, and uses **Playwright browser automation** inside **Docker** to post approved tweets—**100% Free!**

```text
[ OpenRouter AI ] ──> Generates Tweet ──> Sends Card to [ Slack ]
                                                 │
                                         (Click Approve ✅)
                                                 │
                                                 ▼
[ Twitter (X) ] <── Posts Automatically <── [ Playwright + Flask ]
```

---

## 📁 Understanding Key Files (1 Line Each)

| File | What it does |
| :--- | :--- |
| **`docker-compose.yml`** | **The Magic Launcher**: Runs Flask, Ngrok, Generator, and Playwright in 1 command. |
| **`generate_post.py`** | Calls OpenRouter AI to write a tweet, cleans AI thinking notes, and avoids duplicate posts. |
| **`send_to_slack.py`** | Sends the tweet draft card to Slack with **Approve ✅** and **Reject ❌** buttons. |
| **`app.py`** | Flask server listening for Slack button clicks. When approved, triggers Playwright. |
| **`post_to_x.py`** | Playwright script that opens a headless browser, logs into Twitter using `auth_state.json`, and clicks Post. |
| **`login_x.py`** | One-time setup script to log into Twitter and save your cookies into `auth_state.json`. |

---

## ⏱️ Video Outline (3 - 4 Minutes)

| Timestamp | Section | Visual |
| :--- | :--- | :--- |
| **00:00 - 00:30** | **Hook & Problem** | Click Approve in Slack $\rightarrow$ Show tweet going live on Twitter |
| **00:30 - 01:15** | **How It Works** | Show the simple flow diagram (AI $\rightarrow$ Slack $\rightarrow$ Playwright) |
| **01:15 - 02:30** | **1-Command Demo** | Run `docker-compose up --build -d`, show Slack notification, click Approve |
| **02:30 - 03:30** | **Code Walkthrough** | Briefly show `docker-compose.yml`, `generate_post.py`, and `app.py` |
| **03:30 - 04:00** | **Wrap Up** | Explain how to set it up with 1 command |

---

## 📜 Scene-by-Scene Script & Dialogue

### Scene 1: Hook (00:00 - 00:30)

**[VISUAL]**: Show Slack on top right, Twitter profile on bottom right. Click **Approve ✅** in Slack and show the tweet appearing on Twitter.

**[SPOKEN DIALOGUE]**:
> "What if you could automate your Twitter content using AI, keep 100% control over what gets posted, and pay **zero dollars** for the official Twitter API?
> 
> In this video, I'll show you how I built an automated Twitter pipeline using Python, OpenRouter free AI, Slack, and Playwright inside Docker.
> 
> The best part? The **entire system runs with a single Docker command**! Let me show you how it works."

---

### Scene 2: How It Works (00:30 - 01:15)

**[VISUAL]**: Show the simple 3-step diagram on screen.

**[SPOKEN DIALOGUE]**:
> "Here is how the architecture works:
> 
> 1. **AI Generation**: A Python script calls free AI models via OpenRouter to write a unique tech tweet and cleans out any LLM reasoning notes.
> 2. **Slack Human Approval**: It sends an interactive draft card to my private Slack channel with **Approve** and **Reject** buttons.
> 3. **Headless Posting**: When I click Approve, Slack notifies a Flask server, which launches Playwright Chromium to post the tweet automatically using saved session cookies.
> 
> And all of these services launch together in one single container."

---

### Scene 3: Live 1-Command Demo (01:15 - 02:30)

**[VISUAL]**: Open Terminal. Type `docker-compose up --build -d` and hit Enter.

**[SPOKEN DIALOGUE]**:
> "Let's test it live. To launch everything—Flask server, Ngrok tunnel, AI generator, and auto-poster—we just type one command:
> 
> `docker-compose up --build -d`
> 
> Docker builds our container and starts all background services automatically."

**[ACTION]**: Switch window to Slack channel.

> "Within seconds, we get our first draft card in Slack:
> 
> *'AI agents are moving from simple chat to autonomous reasoning and tool integration... #AI #Tech'*
> 
> Now watch what happens when I click **Approve**."

**[ACTION]**: Click **Approve** button in Slack, then open Twitter profile in browser and hit Refresh.

> "Flask caught the approval signal, opened Playwright in the background, typed out the post, and clicked Post. And here it is live on Twitter!"

---

### Scene 4: Code Walkthrough (02:30 - 03:30)

**[VISUAL]**: Open VS Code with project files.

**[SPOKEN DIALOGUE]**:
> "Let's quickly check the core files:
> 
> 1. **`docker-compose.yml`**: The magic launcher that ties together Flask, Ngrok, and our generator loop.
> 2. **`generate_post.py`**: Uses OpenRouter's free models (like Gemma 31B and Minimax) and strips out reasoning tags like `<think>`.
> 3. **`app.py`**: A Flask server receiving Slack button clicks and triggering Playwright in a non-blocking background thread."

---

### Scene 5: Wrap Up & How to Run (03:30 - 04:00)

**[VISUAL]**: GitHub Repository page.

**[SPOKEN DIALOGUE]**:
> "To run this yourself:
> 1. Clone the repo and set your Slack Webhook URL in `.env`.
> 2. Run `docker-compose up --build -d`.
> 
> That's literally it! The code is completely free and open source on GitHub. Thanks for watching!"

---

## ❓ Frequently Asked Questions (For Video Q&A)

1. **Q: Why run everything with `docker-compose up --build -d`?**
   - *A: It eliminates manual terminal management by running Flask, Ngrok, and the background timer in unison.*
2. **Q: Why not use official Twitter API?**
   - *A: Twitter charges \$100/month for basic API write access. Playwright automates the browser for free.*
3. **Q: How does it stay logged in?**
   - *A: `login_x.py` saves browser cookies to `auth_state.json`, which Docker mounts automatically.*
