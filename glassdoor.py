from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import numpy as np

driver = webdriver.Chrome()

url = 'https://www.glassdoor.com/Job/united-states-data-engineer-jobs-SRCH_IL.0,13_IN1_KO14,27.htm?employerSizes=1'
driver.get(url)

try:
    jobs = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.XPATH, '//li[contains(@class,"JobsList_jobListItem")]'))
    )
    print(f"Found {len(jobs)} jobs!")
except Exception as e:
    print(f"Error loading jobs: {e}")
    driver.quit()

jobs_list = []

for job in jobs:
    try:
        job_title = job.find_element(By.XPATH, './/a[@data-test="job-title"]').text
        job_company = job.find_element(By.XPATH, './/span[@class="EmployerProfile_compactEmployerName__LE242"]').text
        job_location = job.find_element(By.XPATH, './/div[@data-test="emp-location"]').text
        job_salary = job.find_element(By.XPATH, './/div[@data-test="detailSalary"]').text
        job_description = "Description not available"
        job_postedDate = job.find_element(By.XPATH, './/div[@data-test="job-age"]').text
        job_link = job.find_element(By.XPATH, './/a[@data-test="job-title"]').get_attribute('href')

        jobs_list.append({
            'Job_Title': job_title,
            'Job_Company': job_company,
            'Job_Location': job_location,
            'Job_Salary': job_salary,
            'Job_Description': job_description,
            'Job_PostedDate': job_postedDate,
            'Job_Link': job_link
        })

    except Exception as e:
        print(f"Error extracting data from job listing: {e}")

# Creating a DataFrame from the job list
df = pd.DataFrame(jobs_list)

print(df)

# Saving to CSV file
df.to_csv('glassworld_.csv', index=False)

driver.quit()
