from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Initialize WebDriver
driver = webdriver.Chrome()

url = 'https://www.glassdoor.com/Job/united-states-data-engineer-jobs-SRCH_IL.0,13_IN1_KO14,27.htm?employerSizes=3&remoteWorkType=1'
driver.get(url)

# Function to load jobs, clicking 'Show More' up to 50 times
def load_jobs(max_clicks=50):
    jobs = []
    prev_job_count = 0
    clicks = 0
    
    while clicks < max_clicks:
        try:
            # Load current job listings
            jobs = driver.find_elements(By.XPATH, '//li[contains(@class,"JobsList_jobListItem")]')
            
            # Check if new jobs have been loaded
            if len(jobs) > prev_job_count:
                prev_job_count = len(jobs)
            else:
                print("No more new jobs loaded.")
                break  # If no new jobs are loaded, exit the loop

            # Click 'Show More' button if it's still there
            show_more_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="left-column"]/div[2]/div/button'))
            )
            show_more_button.click()
            clicks += 1
            print(f"Clicked 'Show More' {clicks} times")
            time.sleep(2)  

        except Exception as e:
            print(f"No more 'Show More' button found or an error occurred: {e}")
            break

    return jobs

def scrape_jobs(jobs):
    jobs_list = []

    for job in jobs:
        try:
            
            job.click()
            time.sleep(2)  
            
            job_title = job.find_element(By.XPATH, './/a[@data-test="job-title"]').text
            job_company = job.find_element(By.XPATH, './/span[@class="EmployerProfile_compactEmployerName__LE242"]').text
            job_location = job.find_element(By.XPATH, './/div[@data-test="emp-location"]').text
            job_salary = job.find_element(By.XPATH, './/div[@data-test="detailSalary"]').text
            
            # Extract the job description after clicking on the job
            job_description = driver.find_element(By.CSS_SELECTOR, "div[class*='JobDetails_jobDescription']").text
            job_email = "N/A"
            job_postedDate = job.find_element(By.XPATH, './/div[@data-test="job-age"]').text
            job_link = job.find_element(By.XPATH, './/a[@data-test="job-title"]').get_attribute('href')

            # Append the extracted data to the jobs_list
            jobs_list.append({
                'Job_Title': job_title,
                'Job_Company': job_company,
                'Job_Location': job_location,
                'Job_Salary': job_salary,
                'Job_Description': job_description,
                'Job_Email': job_email,
                'Job_PostedDate': job_postedDate,
                'Job_Link': job_link
            })

        except Exception as e:
            print(f"Error extracting data from job listing: {e}")

    return jobs_list


# Main logic
try:
    # Load the jobs by clicking 'Show More' up to 50 times
    jobs = load_jobs(max_clicks=50)
    print(f"Found {len(jobs)} jobs!")

    # Scrape the jobs
    jobs_list = scrape_jobs(jobs)

    # Creating a DataFrame from the job list
    df = pd.DataFrame(jobs_list)

    print(df)

    # Saving to CSV file
    df.to_csv('glassdoor_dataengineer(501-1000)REMOTE.csv', index=False)

except Exception as e:
    print(f"Error during scraping: {e}")
finally:
    driver.quit()


