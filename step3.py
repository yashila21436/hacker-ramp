from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import csv
from collections import Counter

# Setup Selenium with headless Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run Chrome in headless mode
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Initialize the Chrome driver
service = ChromeService(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Read URLs from the file
file_path = '2022_collected_blog_post_links.txt' # Change the file name if necessary
with open(file_path, 'r') as file:
    urls = file.readlines()

# Dictionaries to store the count of trending words, categories, and hashtags
trending_words_count = Counter()
categories_count = Counter()
hashtags_count = Counter()

# Open a file to save image URLs
with open('2022_image_urls.txt', 'w') as img_file: # Change the file name if necessary
    # Process each URL
    for url in urls:
        url = url.strip()  # Remove any leading/trailing whitespace
        if url:
            try:
                driver.get(url)

                # Wait for the page to load
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

                # Extracting post titles
                post_titles = driver.find_elements(By.CSS_SELECTOR, 'h2.entry-title a')
                for title in post_titles:
                    print("Post Title:", title.text)

                # Extracting post content
                post_contents = driver.find_elements(By.CSS_SELECTOR, 'div.entry-content p')
                for content in post_contents:
                    print("Post Content:", content.text)

                # Extracting categories and tags
                categories = driver.find_elements(By.CSS_SELECTOR, 'span.cat-links a')
                tags = driver.find_elements(By.CSS_SELECTOR, 'span.tag-links a')

                category_list = [category.text for category in categories]
                tag_list = [tag.text for tag in tags]

                print("Categories:", category_list)
                print("Tags:", tag_list)

                # Update category and hashtag counts
                categories_count.update(category_list)
                hashtags_count.update(tag_list)

                # Extracting images
                images = driver.find_elements(By.CSS_SELECTOR, 'div.entry-content img')
                image_urls = [image.get_attribute('src') for image in images]
                for img_url in image_urls:
                    img_file.write(img_url + '\n')

                # Extracting hashtags and trending words from the full body text
                text = driver.find_element(By.TAG_NAME, 'body').text

                # Using regular expressions to find trending words (capitalized words)
                trending_words = re.findall(r'\b[A-Z][a-z]*\b', text)
                trending_words_count.update(trending_words)

            except Exception as e:
                print(f"Error processing {url}: {e}")

# Close the browser
driver.quit()

# Write the trending words, categories, and hashtags and their frequencies to a CSV file
with open(r'C:\Users\yaror\OneDrive\Desktop\Myntra 13th July\2022_trending_words.csv', 'w', newline='') as csvfile: # Change the file name if necessary
    writer = csv.writer(csvfile)
    writer.writerow(['Word', 'Frequency', 'Type'])

    for word, frequency in trending_words_count.most_common():
        writer.writerow([word, frequency, 'Trending Word'])

    for category, frequency in categories_count.most_common():
        writer.writerow([category, frequency, 'Category'])

    for hashtag, frequency in hashtags_count.most_common():
        writer.writerow([hashtag, frequency, 'Hashtag'])
