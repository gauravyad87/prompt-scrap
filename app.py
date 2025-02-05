from fastapi import FastAPI
from pydantic import BaseModel
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

CHROME_PATH = "/usr/bin/google-chrome-stable"
CHROMEDRIVER_PATH = "/usr/bin/chromedriver"

app = FastAPI()

class URLRequest(BaseModel):
    url: str

def extract_chatgpt_prompts(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.binary_location = CHROME_PATH

    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.get(url)
    time.sleep(5)

    prompts = [elem.text for elem in driver.find_elements(By.CLASS_NAME, "whitespace-pre-wrap")]

    driver.quit()
    return {"prompts": prompts if prompts else ["No prompts found"]}

@app.post("/extract-prompts")
async def get_prompts(request: URLRequest):
    return extract_chatgpt_prompts(request.url)
