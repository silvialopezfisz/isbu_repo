import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

# Function to scrape data from a company page
def scrape_company_page(driver):
    try:
        # Extract website
        website_element = driver.find_element(By.XPATH, '//*[@id="js-vue-onlinecontacts"]/ul/li[1]/a')
        website = website_element.text.strip()
    except NoSuchElementException:
        website = "N/A"

    try:
        # Extract company name
        company_name_element = driver.find_element(By.XPATH, '//*[@id="showroomTopContentDiv"]/div/div[1]/div[2]/div[1]/h1')
        company_name_text = company_name_element.text.strip()
    except NoSuchElementException:
        company_name_text = "N/A"

    try:
        # Extract phone number
        phone_element = driver.find_element(By.XPATH, '//*[@id="js-vue-onlinecontacts"]/ul/li[2]')
        phone = phone_element.text.strip()

        # phone_element_match = re.search(r'\b(?:\+?1[-.]?)?(?:\(\d{3}\)|\d{3})[-.]?\d{3}[-.]?\d{4}\b', phone)
        # phone_number = phone_element_match.group(0) if phone_element_match else ""

    except NoSuchElementException:
        phone = "N/A"

    try:
        # Extract description
        description_element = driver.find_element(By.XPATH, '//*[@id="js-vue-description"]/div/div[1]/div/p')
        description = description_element.text.strip()
    except NoSuchElementException:
        description = "N/A"

    # Print extracted information
    print( phone)
    print("Company Name:", company_name_text)
    print("Description:", description)
    print("Website:", website)
    print()


# URL of the RSS feed
rss_feed_url = "https://bse23.mapyourshow.com/8_0/explore/exhibitor-gallery.cfm?featured=false"

# Configure Selenium WebDriver
driver = webdriver.Chrome()  # Replace with the appropriate WebDriver for your browser
driver.implicitly_wait(10)
wait = WebDriverWait(driver, 10)

# Open the RSS feed
driver.get(rss_feed_url)

# Find and click the "Load More" button three times
load_more_button = None
for _ in range(3):
    try:
        load_more_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[contains(text(), "Load More Results")]')))
        load_more_button.click()
        time.sleep(2)  # Wait for the new content to load
    except TimeoutException:
        break

# Find and click on each company link
company_links = driver.find_elements(By.XPATH, '//a[contains(@href, "exhibitor-details")]')
visited_urls = set()  # Track visited company URLs
for company_link in company_links:
    company_url = company_link.get_attribute("href")

    if company_url in visited_urls:
        continue

    visited_urls.add(company_url)

    # Open the company page in a new tab
    driver.execute_script("window.open();")
    driver.switch_to.window(driver.window_handles[1])
    driver.get(company_url)

    # Scrape data from the company page
    scrape_company_page(driver)

    # Close the company tab
    driver.close()
    driver.switch_to.window(driver.window_handles[0])

# Close the browser
driver.quit()
