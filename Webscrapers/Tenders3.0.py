import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException

# Function to scrape data from a company page
def scrape_company_page(driver):
    try:
        # Extract website
        website_element = driver.find_element(By.XPATH, '//*[contains(text(),"address")]//following-sibling::a')
        website = website_element.text.strip()
    except NoSuchElementException:
        website = "N/A"

    try:
        # Extract email
        email_element = driver.find_element(By.XPATH, '//a[contains(@href, "mailto")]')
        email = re.search(r'[\w\.-]+@[\w\.-]+', email_element.get_attribute("href")).group()
    except NoSuchElementException:
        email = "N/A"

    try:
        # Extract company name
        company_name_element = driver.find_element(By.XPATH, '//div[@class="grseq"]')
        company_name_text = company_name_element.text.strip()
        # Extract the company name using a regular expression
        company_name_match = re.search(r'Official name:\s*(.*)', company_name_text)
        company_name = company_name_match.group(1) if company_name_match else ""
    except NoSuchElementException:
        company_name = "N/A"
    
    

    try:
        # Extract description
        description_element = driver.find_element(By.XPATH, '//div[@class="stdoc"]')
        description = description_element.text.strip()
    except NoSuchElementException:
        description = "N/A"

    # Print extracted information
    print("Email:", email)
    print("Company Name:", company_name)
    print("Description:", description)
    print("Website:", website)
    print()


# URL of the RSS feed
rss_feed_url = "https://ted.europa.eu/TED/rss/en/RSS_dese_all.xml"

# Configure Selenium WebDriver
driver = webdriver.Chrome()  # Replace with the appropriate WebDriver for your browser
driver.implicitly_wait(10)
wait = WebDriverWait(driver, 10)

# Open the RSS feed
driver.get(rss_feed_url)

# Find and click on each company link containing "2023"
company_links = driver.find_elements(By.XPATH, '//a[contains(@href, "2023")]')
for index, company_link in enumerate(company_links):
    if index < 2:
        continue
    
    company_url = company_link.get_attribute("href")

    # Open the company page in a new tab
    driver.execute_script("window.open();")
    driver.switch_to.window(driver.window_handles[1])
    driver.get(company_url)

    try:
        # Wait for the company page to load
        company_name_element = wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@class="grseq"]')))
        scrape_company_page(driver)
    except TimeoutException:
        print("Error: Timed out waiting for the company page to load")

    # Close the company tab
    driver.close()
    driver.switch_to.window(driver.window_handles[0])

# Close the browser
driver.quit()
