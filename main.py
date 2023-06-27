import json
import csv
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--log-level=3")
driver = webdriver.Chrome(options=chrome_options)


API_KEY = "SECRETAPI"

def extract_channel_url(video_url):
    video_id = video_url.split("v=")[-1]
    api_url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={API_KEY}"
    response = requests.get(api_url)
    data = response.json()
    if "items" in data and len(data["items"]) > 0:
        channel_id = data["items"][0]["snippet"]["channelId"]
        return f"https://www.youtube.com/channel/{channel_id}"
    return None


def mergedset():
    with open("youtube_links.json", "r") as file:
        vidata = json.load(file)
        
    merged_set = set(vidata)

    return(merged_set)

def checklinks(video):
    if video.startswith("https://www.youtube.com/watch?v"):
        channel_url = extract_channel_url(video)
        if channel_url:
            channels_links.append(channel_url)
    elif video.startswith("https://www.youtube.com/channel") or video.startswith("https://www.youtube.com/c"):
        if video.endswith("featured"):
            video= video[:-9]
        elif video.endswith("community"):
            video= video[:-10]
        channels_links.append(video)
    elif video.startswith("https://www.youtube.com/post"):
        driver.get(video)
        element = driver.find_elements(By.TAG_NAME, 'a')
        for lnk in element:
            a= lnk.get_attribute("href")
            if type(a)==str:
                if a.startswith("https://www.youtube.com/@"):
                    channels_links.append(a)
                    break

video_data= mergedset()

channels_links = []

for video in video_data:
    checklinks(video)

channels_links= set(channels_links)

with open("channels.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Channel Link"])
    writer.writerows([[link] for link in channels_links])

driver.quit()

print("Finished Finding out Channels for", len(channels_links), "links")
