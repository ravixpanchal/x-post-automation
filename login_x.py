import os
from playwright.sync_api import sync_playwright

profile_dir = os.environ.get("CHROME_PROFILE_DIR", os.path.expanduser("~/.config/twitter-automation-chrome-profile"))

with sync_playwright() as p:
    channel = os.environ.get("PLAYWRIGHT_CHANNEL", "chrome")
    launch_kwargs = {
        "user_data_dir": profile_dir,
        "headless": False,
        "args": [
            "--disable-blink-features=AutomationControlled"
        ]
    }
    if channel:
        launch_kwargs["channel"] = channel

    try:
        context = p.chromium.launch_persistent_context(**launch_kwargs)
    except Exception as e:
        if "channel" in launch_kwargs:
            del launch_kwargs["channel"]
            context = p.chromium.launch_persistent_context(**launch_kwargs)
        else:
            raise e

    page = context.new_page()

    page.goto("https://x.com/home")

    input("Press Enter to exit after logging into X (Twitter)...")

    script_dir = os.path.dirname(os.path.abspath(__file__))
    state_file = os.path.join(script_dir, "auth_state.json")
    context.storage_state(path=state_file)
    print(f"✅ Saved authentication state to {state_file}")

    context.close()