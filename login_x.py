from playwright.sync_api import sync_playwright

with sync_playwright() as p:

    context = p.chromium.launch_persistent_context(
        user_data_dir="/home/ravi/.config/twitter-automation-chrome-profile",
        channel="chrome",
        headless=False,
        args=[
            "--disable-blink-features=AutomationControlled"
        ]
    )

    page = context.new_page()

    page.goto("https://x.com/home")

    input("Press Enter to exit...")

    context.close()