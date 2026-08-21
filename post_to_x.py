import json

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

    with sync_playwright() as p:

        context = p.chromium.launch_persistent_context(
            user_data_dir="/home/ravi/.config/twitter-automation-chrome-profile",
            channel="chrome",
            headless=True,
            viewport={"width": 1280, "height": 800},
            args=[
                "--disable-blink-features=AutomationControlled"
            ]
        )

        page = context.new_page()

        page.goto("https://x.com/compose/post")

        # Wait for compose box
        page.wait_for_selector(
            '[data-testid="tweetTextarea_0"]',
            timeout=15000
        )

        # Focus and fill text
        textbox = page.locator('[data-testid="tweetTextarea_0"]').first
        textbox.focus()
        textbox.fill(tweet_text)

        time.sleep(1.5)

        # Capture screenshot before posting
        script_dir = os.path.dirname(os.path.abspath(__file__))
        scratch_dir = os.path.join(script_dir, "scratch")
        os.makedirs(scratch_dir, exist_ok=True)
        page.screenshot(path=os.path.join(scratch_dir, "before_post.png"))
        print(f"Captured {os.path.join(scratch_dir, 'before_post.png')}")

        # Wait for Post button to be active (not disabled)
        print("Clicking final Post button...")
        try:
            page.wait_for_selector(
                '[data-testid="tweetButton"]:not([aria-disabled="true"]), [data-testid="tweetButtonInline"]:not([aria-disabled="true"])',
                timeout=5000
            )
            post_button = page.locator('[data-testid="tweetButton"], [data-testid="tweetButtonInline"]').filter(has_text="Post").first
            post_button.click()
        except Exception as e:
            print(f"Button click fallback: {e}")
            # Keyboard shortcut Ctrl+Enter to post on X
            textbox.press("Control+Enter")

        time.sleep(4)

        # Capture screenshot after posting
        page.screenshot(path=os.path.join(scratch_dir, "after_post.png"))
        print(f"Captured {os.path.join(scratch_dir, 'after_post.png')}")

        print("Tweet posted successfully!")
        record_posted_tweet(tweet_text)

        time.sleep(1)

        context.close()