import requests
from bs4 import BeautifulSoup

# extract base web content
def get_website_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup.text

url = 'https://www.example.com'  # replace with your url
content = get_website_content(url)
print(content)
