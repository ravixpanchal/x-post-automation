import os
import time
import json
import threading
from playwright.sync_api import sync_playwright

post_lock = threading.Lock()

def record_posted_tweet(tweet_text):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    history_file = os.path.join(script_dir, "posted_history.json")
    posted = []
    if os.path.exists(history_file):
        try:
            with open(history_file, "r") as f:
                posted = json.load(f)
        except Exception:
            posted = []
    if tweet_text not in posted:
        posted.append(tweet_text)
        with open(history_file, "w") as f:
            json.dump(posted, f, indent=2)

def post_to_x(tweet_text):
    with post_lock:
        profile_dir = os.environ.get("CHROME_PROFILE_DIR", os.path.expanduser("~/.config/twitter-automation-chrome-profile"))
        lock_file = os.path.join(profile_dir, "SingletonLock")
        if os.path.exists(lock_file):
            try:
                os.remove(lock_file)
            except Exception as e:
                print(f"Could not remove stale SingletonLock: {e}")

        with sync_playwright() as p:
            channel = os.environ.get("PLAYWRIGHT_CHANNEL", "chrome")
            script_dir = os.path.dirname(os.path.abspath(__file__))
            state_file = os.path.join(script_dir, "auth_state.json")

            launch_kwargs = {
                "user_data_dir": profile_dir,
                "headless": True,
                "viewport": {"width": 1280, "height": 800},
                "args": [
                    "--disable-blink-features=AutomationControlled",
                    "--no-sandbox",
                    "--disable-setuid-sandbox"
                ]
            }
            if channel and channel.strip():
                launch_kwargs["channel"] = channel.strip()

            try:
                context = p.chromium.launch_persistent_context(**launch_kwargs)
            except Exception as e:
                if "channel" in launch_kwargs:
                    print(f"Launch with channel '{channel}' failed ({e}), falling back to default Playwright Chromium...")
                    del launch_kwargs["channel"]
                    context = p.chromium.launch_persistent_context(**launch_kwargs)
                else:
                    raise e

            if os.path.exists(state_file):
                try:
                    with open(state_file, "r") as f:
                        state_data = json.load(f)
                        if isinstance(state_data, dict) and "cookies" in state_data and state_data["cookies"]:
                            cleaned_cookies = []
                            for c in state_data["cookies"]:
                                cookie = dict(c)
                                if "sameSite" in cookie and cookie["sameSite"] not in ["Strict", "Lax", "None"]:
                                    cookie["sameSite"] = "None"
                                cleaned_cookies.append(cookie)
                            context.add_cookies(cleaned_cookies)
                            print(f"Loaded {len(cleaned_cookies)} cookies from {state_file}")
                except Exception as err:
                    print(f"Warning: Could not load {state_file}: {err}")

            # Inject X_AUTH_TOKEN from environment if set
            x_auth_token = os.environ.get("X_AUTH_TOKEN", "").strip()
            x_ct0 = os.environ.get("X_CT0", "").strip()
            if x_auth_token:
                cookies_to_add = [
                    {
                        "name": "auth_token",
                        "value": x_auth_token,
                        "domain": ".x.com",
                        "path": "/",
                        "secure": True,
                        "httpOnly": True
                    },
                    {
                        "name": "auth_token",
                        "value": x_auth_token,
                        "domain": ".twitter.com",
                        "path": "/",
                        "secure": True,
                        "httpOnly": True
                    }
                ]
                if x_ct0:
                    cookies_to_add.extend([
                        {
                            "name": "ct0",
                            "value": x_ct0,
                            "domain": ".x.com",
                            "path": "/",
                            "secure": True,
                            "httpOnly": False
                        },
                        {
                            "name": "ct0",
                            "value": x_ct0,
                            "domain": ".twitter.com",
                            "path": "/",
                            "secure": True,
                            "httpOnly": False
                        }
                    ])
                context.add_cookies(cookies_to_add)
                print("Injected X_AUTH_TOKEN cookie from environment into browser context.")

            page = context.new_page()

            page.goto("https://x.com/compose/post", wait_until="domcontentloaded")

            time.sleep(2)
            # Check if browser was redirected to login modal/page
            current_url = page.url
            is_login_flow = "flow/login" in current_url or page.locator('input[name="text"], [data-testid="loginButton"]').count() > 0
            if is_login_flow:
                script_dir = os.path.dirname(os.path.abspath(__file__))
                scratch_dir = os.path.join(script_dir, "scratch")
                os.makedirs(scratch_dir, exist_ok=True)
                page.screenshot(path=os.path.join(scratch_dir, "not_logged_in.png"))
                msg = (
                    "❌ NOT LOGGED IN TO X (TWITTER): Browser was redirected to the login page.\n"
                    "Please authenticate by running 'python3 login_x.py' on the host machine to save your login session to auth_state.json, "
                    "or set X_AUTH_TOKEN in your .env file."
                )
                print(msg)
                raise RuntimeError(msg)

            print("Waiting for X compose box...")
            # Wait for compose box with extended timeout for headless/docker
            try:
                page.wait_for_selector(
                    '[data-testid="tweetTextarea_0"], div[role="textbox"]',
                    timeout=35000
                )
            except Exception as e:
                print(f"Error waiting for compose box: {e}")
                # Save screenshot of failure for debugging
                script_dir = os.path.dirname(os.path.abspath(__file__))
                scratch_dir = os.path.join(script_dir, "scratch")
                os.makedirs(scratch_dir, exist_ok=True)
                page.screenshot(path=os.path.join(scratch_dir, "timeout_error.png"))
                raise e

            # Focus and fill text
            textbox = page.locator('[data-testid="tweetTextarea_0"], div[role="textbox"]').first
            textbox.focus()
            textbox.fill(tweet_text)

            time.sleep(1.5)

            # Capture screenshot before posting
            script_dir = os.path.dirname(os.path.abspath(__file__))
            scratch_dir = os.path.join(script_dir, "scratch")
            os.makedirs(scratch_dir, exist_ok=True)
            page.screenshot(path=os.path.join(scratch_dir, "before_post.png"))
            print(f"Captured {os.path.join(scratch_dir, 'before_post.png')}")

            # Press Escape to dismiss any active hashtag/mention typeahead dropdown
            page.keyboard.press("Escape")
            time.sleep(0.5)

            # Wait for Post button to be active and click
            print("Clicking final Post button...")
            try:
                post_btn = page.locator('[data-testid="tweetButton"], [data-testid="tweetButtonInline"]').filter(has_text="Post").first
                if post_btn.is_visible():
                    post_btn.click(timeout=5000)
                else:
                    textbox.focus()
                    textbox.press("Control+Enter")
            except Exception as e:
                print(f"Button click fallback error: {e}")
                textbox.focus()
                textbox.press("Control+Enter")

            time.sleep(2)
            # If compose box or post button is still visible, trigger Control+Enter shortcut
            try:
                post_btn = page.locator('[data-testid="tweetButton"]').first
                if post_btn.is_visible():
                    print("Compose button still visible, triggering Control+Enter shortcut...")
                    textbox.focus()
                    textbox.press("Control+Enter")
            except Exception as e:
                print(f"Fallback check error: {e}")

            time.sleep(4)

            # Capture screenshot after posting
            page.screenshot(path=os.path.join(scratch_dir, "after_post.png"))
            print(f"Captured {os.path.join(scratch_dir, 'after_post.png')}")

            print("Tweet posted successfully!")
            record_posted_tweet(tweet_text)

            time.sleep(1)

            context.close()