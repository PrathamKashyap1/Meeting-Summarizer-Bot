from playwright.sync_api import sync_playwright
import time

def main():
    with sync_playwright() as p:
        # Launch browser
        args=  []
        args.append("--disable-blink-features=AutomationControlled")
        args.append("--use-fake-ui-for-media-stream")

        browser = p.chromium.launch(headless=False,slow_mo=60,args=args)
        context = browser.new_context(no_viewport=True)
        page = context.new_page()
        # Navigate to URL
        try:
            meeting_link = input("Enter meeting link for me to join")
            page.goto(meeting_link)
            time.sleep(2)
            page.click('button:has-text("Got it")');
            time.sleep(1);
            page.locator('.qdOxv-fmcmS-wGMbrd').fill("Pr-bot");

            mic_class = "Pr6Uwe"
            cam_class = ".utiQxe"
            page.locator(cam_class).click();
            time.sleep(2);
            page.locator('.UywwFc-vQzf8d').click();

            
            page.wait_for_load_state('domcontentloaded')
            time.sleep(150)
        
        except Exception as e:
            print(e)
        finally:
            page.close()        
            browser.close()

if __name__ == "__main__":
    main()