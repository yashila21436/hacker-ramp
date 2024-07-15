import requests
from bs4 import BeautifulSoup

# Function to read URLs from search_results.txt file
def read_urls_from_file(file_path):
    with open(file_path, 'r') as file:
        urls = [line.strip() for line in file if line.strip()]  # Read all non-empty lines and remove any leading/trailing whitespace
    return urls

# Function to write URLs to a file
def write_urls_to_file(file_path, urls):
    with open(file_path, 'w') as file:
        for url in urls:
            file.write(f"{url}\n")

# Read the URLs from search_results.txt
urls = read_urls_from_file('2022_search_results.txt') #change krna h file name

# Check if URLs were successfully read
if urls:
    all_blog_post_links = []  # List to store all collected blog post links

    for url in urls:
        print(f"{url}")
        
        # Send a GET request to the webpage
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the page content with BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')

            # Initialize an empty list to store blog post links
            blog_post_links = []

            # Find all h2 tags which are likely to contain blog links
            h2_tags = soup.find_all('h2')
            print(f"{len(h2_tags)} {url}")

            for h2 in h2_tags:
                # Find all anchor tags within the h2 tag
                a_tag = h2.find('a', href=True)
                if a_tag:
                    href = a_tag['href']
                    blog_post_links.append(href)
                    print(f"{href}")

            # Find all a tags with class 'ext' to get additional blog URLs
            ext_links = soup.find_all('a', class_='ext', href=True)
            print(f"{len(ext_links)} {url}")

            for a_tag in ext_links:
                href = a_tag['href']
                blog_post_links.append(href)
                print(f"{href}")

            # Find all a tags with class 'DiscoverFeed__source-link' to get additional blog URLs
            discover_feed_links = soup.find_all('a', class_='DiscoverFeed__source-link', href=True)
            print(f"{len(discover_feed_links)} {url}")

            for a_tag in discover_feed_links:
                href = a_tag['href']
                blog_post_links.append(href)
                print(f"{href}")

            # Find all a tags with class 'af pb' to get additional blog URLs
            af_pb_links = soup.find_all('a', class_='af pb', href=True)
            print(f"{len(af_pb_links)} {url}")

            for a_tag in af_pb_links:
                href = a_tag['href']
                blog_post_links.append(href)
                print(f"{href}")

            # Find all span tags with class 'blog-url' to get additional blog URLs
            blog_url_spans = soup.find_all('span', class_='blog-url')
            print(f"{len(blog_url_spans)} {url}")

            for span in blog_url_spans:
                a_tag = span.find('a', href=True)
                if a_tag:
                    href = a_tag['href']
                    blog_post_links.append(href)
                    print(f"{href}")

            # Find all a tags with class 'external-link' to get additional blog URLs
            external_links = soup.find_all('a', class_='external-link', href=True)
            print(f"{len(external_links)} {url}")

            for a_tag in external_links:
                href = a_tag['href']
                blog_post_links.append(href)
                print(f"{href}")

            # Print the collected blog post links
            print("\nCollected blog post links:")
            for blog_link in blog_post_links:
                print(blog_link)

            # Add the collected blog post links to the main list
            all_blog_post_links.extend(blog_post_links)
        else:
            print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

    # Write all collected blog post links to a file
    write_urls_to_file('2022_collected_blog_post_links.txt', all_blog_post_links) #change krna h file name
else:
    print("Failed to read URLs from search_results.txt")
