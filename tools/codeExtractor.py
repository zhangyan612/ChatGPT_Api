from bs4 import BeautifulSoup

# Replace 'input_file.html' with the name of your HTML file

def extractCode(html_file):
    try:
        soup = BeautifulSoup(html_file, 'html.parser')

        # Find all <code> tags in the HTML
        code_tags = soup.find_all('code')

        # Create a list to store the extracted code
        extracted_code = []

        # Extract the code from <code> tags and add it to the list
        for tag in code_tags:
            code = tag.get_text()
            extracted_code.append(code)

        return extracted_code

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ =='__main__':
    input_file = 'ChatResponse.html'
    import json
    from tools import saveFile

    with open(input_file, 'r', encoding='utf-8') as html_file:
        code = extractCode(html_file)
        # print(code)
    
        result = {
            "choices": [
                {
                    "finish_reason": "stop",
                    "index": 0,
                    "message": {
                        "code": code,
                        "role": "assistant"
                    }
                }
            ],
            "id": "chatcmpl-7QyqpwdfhqwajicIEznoc6Q47XAyW",
            "object": "chat.completion",
        }

        json_str = json.dumps(result)
        print(json_str)
        response = json_str.json()
        saveFile('responses', str(response["created"]), response)