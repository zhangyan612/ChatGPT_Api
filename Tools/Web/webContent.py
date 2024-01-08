import requests
from bs4 import BeautifulSoup

# Description: This function extract web content based on url
# Parameters: URL of website
# Result: text string
def get_website_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup.text

# Test to validate result
if __name__ == '__main__':
    url = 'https://github.com/MarkFzp/mobile-aloha/tree/main'
    content = get_website_content(url)
    print(content)
