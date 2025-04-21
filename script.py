from playwright.sync_api import sync_playwright
import time
import google.generativeai as genai
import os
from dotenv import load_dotenv
load_dotenv()
from taskalloc import find_users_for_tasks
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

def main():
    meeting_link = input("Enter meeting link for me to join:")
    with sync_playwright() as p:
        args=  []
        args.append("--disable-blink-features=AutomationControlled")
        args.append("--use-fake-ui-for-media-stream")
        args.append("--mute-audio")

        browser = p.chromium.launch(headless=False,slow_mo=60,args=args)
        context = browser.new_context(no_viewport=True)
        page = context.new_page()

        try:
            page.goto(meeting_link)
            time.sleep(2)
            page.click('button:has-text("Got it")');
            # time.sleep(1);
            page.locator('.qdOxv-fmcmS-wGMbrd').fill("Pr-bot");#Name of the bot attending

            mic_class = ".Pr6Uwe"
            cam_class = ".utiQxe"
            transcript_xpath = '''//*[@id="yDmH0d"]/c-wiz/div/div/div[63]/div[3]/div/div[3]/div/div[2]/div/div'''
            endcall_xpath='.VYBDae-Bz112c-RLmnJb'
            chat_xpath='''//*[@id="yDmH0d"]/c-wiz/div/div/div[63]/div[3]/div/div[8]/div/div/div[3]/nav/div[3]/div/div/span/button/div'''
            page.locator(cam_class).click();
            page.locator(mic_class).click();
            time.sleep(2);
            page.locator('.UywwFc-vQzf8d').click(); #clicking the join now button
            page.wait_for_load_state('domcontentloaded')
            # page.click('button:has-text("Got it")')
            page.locator('.juFBl').click() #turn on captions button
            # page.wait_for_load_state('domcontentloaded')
            genai.configure(api_key=os.getenv("GOOGLE_APIKEY"))
            with open('prompt.txt','r') as f:
                    prompts = f.read().split('/')#different prompts are stored as list
            counter=1 #No.of times the users call it(To prevent infinite responses)
            time.sleep(5)
            def chatwithuser(text):
                page.locator(chat_xpath).click()
                time.sleep(2)
                page.keyboard.type(text)
                time.sleep(3)
                page.keyboard.press('Enter')
                time.sleep(1)
                page.locator(chat_xpath).click()
                time.sleep(1)
            
            chatwithuser("Hello. I am your Assistant for this meeting.")

            while True:
                time.sleep(3)
                l = page.locator(transcript_xpath).all_text_contents()
                print(l)
                if len(l)==0:
                    continue
                print(l)
                if "bot" in l[0].lower() and l[0].count("bot")>counter:
                    counter+=1
                    #Making call to llm here
                    model = genai.GenerativeModel('gemini-2.0-flash')
                    response = model.generate_content(prompts[0]+l[0].lower())
                    output = response.text.replace('*','').replace('#','')
                    chatwithuser(output)

                elif "end" in l[0].lower() or "bye" in l[0].lower():
                    model = genai.GenerativeModel('gemini-2.0-flash')
                    response = model.generate_content(prompts[1]+l[0].lower())
                    output = response.text.replace('#','').replace('*','')
                    chatwithuser(output)


                    #Plan on how to proceed(Visualizations plan)
                    #Assigning tasks to users
                    response = model.generate_content(prompts[2]+l[0].lower())
                    output = response.text.replace('#','').replace('*','')
                    li = find_users_for_tasks(output.split(","))
                    chatwithuser(str(li))
                    time.sleep(2)
                    print(output)
                    break
                else:
                    print(l[0].lower())
                time.sleep(8)

            
        
        except Exception as e:
            print(e)
        finally:
            chatwithuser("Thank you for joining the meeting")
            page.locator(endcall_xpath).click()
            page.close()        
            browser.close()

if __name__ == "__main__":
    main()