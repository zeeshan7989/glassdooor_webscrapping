from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import numpy as np

driver = webdriver.Chrome()


url = 'https://www.glassdoor.com/Job/united-states-data-engineer-jobs-SRCH_IL.0,13_IN1_KO14,27.htm'
driver.get(url)

try:
    videos = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.ID, 'dismissible'))
    )
    print(f"Found {len(videos)} videos!")
except Exception as e:
    print(f"Error loading videos: {e}")
    driver.quit()

video_list = []

for video in videos:
    try:
        title = video.find_element(By.XPATH, './/*[@id="video-title"]').text

        views = video.find_element(By.XPATH, './/*[@id="metadata-line"]/span[1]').text
        when = video.find_element(By.XPATH, './/*[@id="metadata-line"]/span[2]').text

        video_list.append({
            'Title': title,
            'Views': views,
            'Posted': when
        })
    except Exception as e:
        print(f"Error extracting data from video: {e}")

df = pd.DataFrame(video_list)

print(df)

df.to_csv('youtube_videos.csv')

driver.quit()