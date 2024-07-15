from googlesearch import search

# Define the search query and the number of results to fetch
query = "top trending fashion blogs 2022 "
num_results = 10

# Perform the search and save the URLs in a list
urls = []
for url in search(query, num_results=num_results):
    urls.append(url)

# Save the URLs to a file
with open("2022_search_results.txt", "w") as file:
    for url in urls:
        file.write(url + "\n")

print(f"Saved {len(urls)} URLs to 2022_search_results.txt")
