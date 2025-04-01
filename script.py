from playwright.sync_api import sync_playwright
import time
from RealtimeSTT import AudioToTextRecorder



def main():
    meeting_link = input("Enter meeting link for me to join")
    with sync_playwright() as p:
        args=  []
        args.append("--disable-blink-features=AutomationControlled")
        args.append("--use-fake-ui-for-media-stream")

        browser = p.chromium.launch(headless=False,slow_mo=60,args=args)
        context = browser.new_context(no_viewport=True)
        page = context.new_page()
        
        try:
            page.goto(meeting_link)
            time.sleep(2)
            page.click('button:has-text("Got it")');
            time.sleep(1);
            page.locator('.qdOxv-fmcmS-wGMbrd').fill("Pr-bot");#Name of the bot attending

            mic_class = ".Pr6Uwe"
            cam_class = ".utiQxe"
            transcript_class = ".VbkSUe"
            page.locator(cam_class).click();
            time.sleep(2);
            page.locator('.UywwFc-vQzf8d').click(); #clicking the join now button
            page.wait_for_load_state('domcontentloaded')
            page.click('button:has-text("Got it")')
            page.locator('.juFBl').click() #turn on captions button
            page.wait_for_load_state('domcontentloaded')
            while True:
                time.sleep(5)
                l = page.locator(transcript_class).all_text_contents()
                if "bot" in l[0].lower():
                    print("Call to you is made")
                    #need to make a call to llm here
                    break
                else:
                    print(l[0].lower())
                time.sleep(7)

            
        
        except Exception as e:
            print(e)
        finally:
            page.close()        
            browser.close()

if __name__ == "__main__":
    main()