
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
import csv


# Function to save listings to a CSV file
def save_to_csv(listings, filename):
    # Define the header/column names
    fieldnames = ['address', 'price', 'square_footage']

    # Open the file for writing
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        # Create a writer object
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write the header row
        writer.writeheader()

        # Write the listing data
        for listing in listings:
            writer.writerow(listing)

# Set up the web driver
DRIVER_PATH = '/usr/local/bin/chromedriver'
service = Service(DRIVER_PATH)
driver = webdriver.Chrome(service=service)
driver.get('https://www.forsalebyowner.com/search/list/los-angeles-county-california')

wait = WebDriverWait(driver, 20)

# Initialize a list to store all listings
listings = []

try:
    previous_listing_count = 0
    while len(listings) < 500:  # Keep scraping until you have 500 listings
        # XPath that targets the container of each listing
        listings_xpath = '//div[contains(@class, "flex flex-col items-center md:h-70 md:w-1/2 relative")]'
        listings_elements = wait.until(EC.visibility_of_all_elements_located((By.XPATH, listings_xpath)))

        # Scrape only new listings by skipping the ones already scraped
        new_listings_elements = listings_elements[previous_listing_count:]

        for listing_element in new_listings_elements:
            # Extract individual data points for each listing
            address = listing_element.find_element(By.XPATH, './/span[contains(@class, "block text-xs font-normal text-gray-400")]').text
            price = listing_element.find_element(By.XPATH, './/div[contains(@class, "flex items-center justify-center gap-x-1.5 font-bold")]//span[contains(@class, "text-xl")]').text
            
            # Handle missing square footage
            sqft_elements = listing_element.find_elements(By.XPATH, './/span[contains(@class, "border-l border-gray-light px-3")][2]//span[contains(@class, "font-medium")]')
            sqft = sqft_elements[0].text if sqft_elements else None

            # Append the data to the listings list
            listings.append({'address': address, 'price': price, 'square_footage': sqft})

        # Update the count of listings already scraped
        previous_listing_count = len(listings)

        # Click the "View More Listings" button, if present
        try:
            view_more_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'mt-6') and contains(@href, 'page')]/div/button[contains(@class, 'flex items-center justify-center')]")))
            driver.execute_script("arguments[0].scrollIntoView(true);", view_more_button)  # Scroll to the button
            time.sleep(1)  # Ensure the scroll and any animations have completed
            driver.execute_script("arguments[0].click();", view_more_button)  # Use JavaScript to click the button
            # Wait for the new listings to load
            wait.until(EC.visibility_of_all_elements_located((By.XPATH, listings_xpath)))  # Wait for new listings to be visible
        except (NoSuchElementException, TimeoutException):
            print("No more 'View More Listings' button found or reached the end of listings.")
            break  # Break the loop if no more listings are available
     # Use an OS-independent path to save the CSV in the current directory
    current_directory = os.getcwd()
    csv_file_path = os.path.join(current_directory, 'listings.csv')
    
    # Save the listings to a CSV file after scraping
    save_to_csv(listings, csv_file_path)
    print(f"Data has been written to {csv_file_path}")

except Exception as e:
    print("An error occurred:", e)

finally:
    driver.quit()

# Output the data
for listing in listings[:500]:  # Ensure only the first 500 are printed
    print(listing)
