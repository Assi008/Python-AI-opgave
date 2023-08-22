import requests
from bs4 import BeautifulSoup
#Importing Libraries: The code starts by importing the necessary libraries: requests for making HTTP requests and BeautifulSoup for parsing HTML content.

# Define a function to fetch XBRL links from HTML content
def fetch_xbrl_links(html_content):
 # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    # Find all <a> elements with a title containing "XBRL"
    return soup.find_all('a', title=lambda value: value and 'XBRL' in value)
    

# Define a function to read existing URLs from a file
def read_existing_urls(filename):
    try:
        with open(filename, 'r') as file:
            return set(line.strip() for line in file)
    except FileNotFoundError:
        return set()

# Define a function to save new URLs to a file
def save_new_urls_to_file(filename, new_urls):
    with open(filename, 'a') as file:
        for url in new_urls:
            file.write(url + '\n')

# Define a function to fetch and save XBRL data from URLs
def fetch_and_save_xbrl_data(urls):
    for xbrl_url in urls:
        print("Processing link:", xbrl_url)
        response = requests.get(xbrl_url)
        
        if response.status_code == 200:
            xbrl_data = response.content
            filename = xbrl_url.split("/")[-1]
            
            with open(filename, 'wb') as file:
                file.write(xbrl_data)
            
            print(f"XBRL data saved to {filename}")
        else:
            print(f"Failed to fetch XBRL data from {xbrl_url}")
        print("Writing URL to file:", xbrl_url)

# Main function
def main():
    html = '<a href="https://datacvr.virk.dk/gateway/dokument/downloadDokumentForVirksomhed?dokumentId=amNsb3VkczovLzAzLzBlL2M4LzEzLzIyLzcxNzctNDM4Ni04NGYyLTgyODBmZjA3MDhhMA&amp;cvrNummer=39588072" target="_blank" rel="noopener" class="d-block" title="Download regnskab fra 02.01.2023 i format XBRL" data-v-b882a22c="" data-v-d15255b8=""><span data-v-b882a22c="">XBRL</span><!----></a>'

    # Fetch XBRL links from the HTML content
    xbrl_links = fetch_xbrl_links(html)
    
    # Read existing URLs from the file
    existing_urls = read_existing_urls('xbrl_urls.txt')
    
    # Identify new URLs that are not in the existing list
    new_urls = [link['href'] for link in xbrl_links if link['href'] not in existing_urls]
    
    if new_urls:
        # Save new URLs to the file
        save_new_urls_to_file('xbrl_urls.txt', new_urls)
        print(f"Total {len(new_urls)} new XBRL URLs appended to xbrl_urls.txt.")
        print("New URLs:", new_urls)
        # Fetch and save XBRL data from the new URLs
        fetch_and_save_xbrl_data(new_urls)
    else:
        print("No new XBRL links found in the HTML.")

# Execute the main function if this script is run
if __name__ == "__main__":
    main()
