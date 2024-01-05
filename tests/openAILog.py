import openai
import datetime
import json
import os


# Get today's date as a string
today = datetime.date.today().strftime("%Y-%m-%d")

# Create a log file with today's date
log_file = open(f"{today}_openai_log.txt", "a")

def log_request_response(r):
    # Get the current time
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Log the request
    log_file.write(f"\n{now} - Request:\n")
    log_file.write(json.dumps(r["request"], indent=4))

    # Log the response
    log_file.write(f"\n{now} - Response:\n")
    log_file.write(json.dumps(r["response"], indent=4))

# Make a request to the OpenAI API
requestMsg = [
        {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
        {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
    ]

completion = openai.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=requestMsg
)

# Log the request and response
log_request_response({
    "request": requestMsg,
    "response": str(completion.choices[0].message)
})

# Close the log file
log_file.close()
