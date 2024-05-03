from selenium import webdriver
import time
import pandas as pd

def scroll_to_end(driver):
    # Scroll to the end of the page.
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Add a short sleep to allow content to load
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def scrape_job_links(driver):
    # Scrape job links from the current page.
    job_links = driver.find_elements_by_css_selector('a.base-card__full-link')
    href_list = [link.get_attribute('href') for link in job_links]
    return href_list

def scrape_jobs_data(driver):
    """Scrape job data (company name and title) from the current page."""
    companies = driver.find_elements_by_css_selector('h3.base-search-card__subtitle')
    titles = driver.find_elements_by_css_selector('h2.base-search-card__title')

    companies_list = [company.text for company in companies]
    titles_list = [title.text for title in titles]

    return companies_list, titles_list

def scrape_linkedin_jobs(url, output_file):
    # Scrape job data from LinkedIn.
    # Set ChromeDriver options
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')  # To run Chrome in headless mode (without opening browser window)
    chrome_options.add_argument('--disable-gpu')  # To avoid GPU errors

    # Set ChromeDriver executable path
    chromedriver_path = r'C:\\Users\\Default\\Desktop\\chromedriver.exe'

    # Initialize WebDriver with options and executable path
    driver = webdriver.Chrome(executable_path=chromedriver_path, options=chrome_options)
    driver.get(url)

    # Scroll through all jobs
    scroll_to_end(driver)

    # Scrape job data
    companies, titles = scrape_jobs_data(driver)

    # Save data to DataFrame
    df = pd.DataFrame({'Company': companies, 'Title': titles})

    # Save DataFrame to CSV
    df.to_csv(output_file, index=False)

    driver.quit()

if __name__ == "__main__":
    url = 'https://www.linkedin.com/jobs/search/?currentJobId=3910909430&keywords=developer&origin=SWITCH_SEARCH_VERTICAL'
    output_file = 'linkedin_jobs.csv'
    scrape_linkedin_jobs(url, output_file)