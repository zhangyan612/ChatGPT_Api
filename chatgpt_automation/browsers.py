# from helpers import detect_chrome_version
# import undetected_chromedriver as uc
# from selenium.webdriver.common.keys import Keys
# import os
# import time

# options = uc.ChromeOptions()
# options.add_argument('--incognito')

# browser = uc.Chrome(
#             driver_executable_path="",
#             options=options,
#             headless=False,
#             version_main=detect_chrome_version(None),
#             log_level=10,
#         )

# # driver = webdriver.Firefox()  #python

# # extract to session_id and _url from driver object.
# url = browser.command_executor._url       #"http://127.0.0.1:60622/hub"
# session_id = browser.session_id            #'4e167f26-dc1d-4f51-a207-f761eaf73c31'

# print(url)
# print(session_id)

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import os
import parseResult

# Set the path to the WebDriver executable
webdriver_path = 'C:/Users/JohnSong/Desktop/chromedriver_win32/chromedriver.exe'  # Change this to your WebDriver path

# Initialize the Chrome driver with the Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(f"executable_path={webdriver_path}")
browser = webdriver.Chrome(options=chrome_options)


# Navigate to Google
browser.get("https://www.google.com")

# Wait for the search input field to be present
wait = WebDriverWait(browser, 10)
search_input = wait.until(EC.presence_of_element_located((By.NAME, "q")))

# Enter your search query and submit
search_query = "how to train LLM"  # Change this to your desired query
search_input.send_keys(search_query)
search_input.send_keys(Keys.RETURN)

# Wait for the search results to load
time.sleep(5)  # Adjust the sleep time as needed

# Create a folder with a timestamp
timestamp = time.strftime("%Y%m%d%H%M%S")
folder_name = f"responses/search_results_{timestamp}"
os.makedirs(folder_name)

# Initialize an empty string to store the concatenated HTML content
html_content = ''
search_results = browser.find_elements(By.ID, "search")
for element in search_results:
    html_content += element.get_attribute('outerHTML') + '\n'

# Find and save the search result links to a file within the folder
filename = os.path.join(folder_name, "search_results.html")

with open(filename, 'w', encoding='utf-8') as file:
    file.write(html_content)

parseResult.parseHtmlSearchResult(folder_name, filename)
# Close the browser when done

#for each result visit the link and download the article




browser.quit()
