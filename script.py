from playwright.sync_api import sync_playwright
import time
from RealtimeSTT import AudioToTextRecorder
import google.generativeai as genai
import os
from dotenv import load_dotenv
load_dotenv()

def main():
    meeting_link = input("Enter meeting link for me to join:")
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
            genai.configure(api_key=os.getenv("GOOGLE_APIKEY"))#adding the API key before itself
            with open('prompt.txt','r') as f:
                    prompts = f.read().split('/')#different prompts are stored as list
            counter=0 #No.of times the users call it(To prevent infinite responses)
            time.sleep(5)
            while True:
                time.sleep(5)
                l = page.locator(transcript_class).all_text_contents()
                if "bot" in l[0].lower() and l[0].count("bot")>counter:
                    counter+=1
                    #Making call to llm here
                    print(l[0].lower())
                    model = genai.GenerativeModel('gemini-2.0-flash')
                    response = model.generate_content(prompts[0]+l[0].lower())
                    output = response.text.replace('*','').replace('#','')
                    print(output)
                elif "end" in l[0].lower() or "bye" in l[0].lower():
                    model = genai.GenerativeModel('gemini-2.0-flash')
                    response = model.generate_content(prompts[1]+l[0].lower())
                    output = response.text.replace('#','').replace('*','')
                    print(output)
                    #Plan on how to proceed
                    response = model.generate_content(prompts[2]+l[0].lower())
                    output = response.text.replace('#','').replace('*','')
                    print(output)
                    break
                else:
                    print(l[0].lower())
                time.sleep(8)

            
        
        except Exception as e:
            print(e)
        finally:
            page.close()        
            browser.close()

if __name__ == "__main__":
    main()