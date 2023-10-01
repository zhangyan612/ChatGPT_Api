import json
from bs4 import BeautifulSoup

# Read the local HTML file

def parseHtmlSearchResult(folder, fileName):
    with open(fileName, 'r', encoding='utf-8') as html_file:
        html_content = html_file.read()

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all elements with class "MjjYud"
    elements = soup.find_all(class_='MjjYud')

    # Initialize a list to store the extracted data
    data_list = []


    # Loop through the elements and extract data
    for element in elements:
        link = element.find('a')
        title = element.find('h3')

        # Find the second child of the element with class "MjjYud"
        first_child = element.find_all('div')[0]
        second_child = first_child.find_all('div')[0]

        # Find the second <div> element within the second child
        second_div = second_child.find_all('div')[1]

        description = second_div

        # Check if any of the fields is missing and skip the element
        if link is None or title is None or description is None:
            continue

        # Extract data if all fields are present
        link = link['href']
        title = title.text
        description = description.text

        # Create a dictionary for each item
        item = {
            'link': link,
            'title': title,
            'description': description
        }

        # Append the item to the data list
        data_list.append(item)

    print(data_list)
    # Save the list of data as a JSON file
    with open(folder +'/search_result.json', 'w', encoding='utf-8') as json_file:
        json.dump(data_list, json_file, ensure_ascii=False, indent=4)

    print('Data has been extracted and saved to "output.json".')


if __name__ == '__main__':
    parseHtmlSearchResult(r'D:\AI\ChatGPT_Api\search_results_20231001005217', r'D:\AI\ChatGPT_Api\search_results_20231001005217\search_results.html')