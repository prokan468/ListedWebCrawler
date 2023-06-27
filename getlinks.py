from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
from selenium.webdriver.common.by import By

def main():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=chrome_options)

    driver.get("https://www.google.com/search?q=site:youtube.com+openinapp.co&num=100000")
    links= driver.find_elements(By.TAG_NAME, 'a')

    newlinks=[]
    for lnk in links:
        a= lnk.get_attribute("jscontroller")
        if a=="M9mgyc":
            newlinks.append(lnk.get_attribute("href"))

    with open("youtube_links.json", "w") as file:
        json.dump(newlinks, file, indent=4)

    print(f"Scraped {len(newlinks)} YouTube links.")
    driver.quit()
