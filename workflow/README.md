# Skills

Basic ability that can be called upon

Extend RPA framework skills by adding motor skills
Use hugginggpt to plan, RPA to execute and gpt to evluate result

# Basic workflow

Resaerch on certain topic on code project
    1. Create work space with text and code subfolder
    2. Browse web to find related articles and download
    3. Browse github code base to find related code and download
    4. Summarize found methods to group them into related topics
    5. Test each method and evaluate outcome
    6. Compare outcome to choose the best solution



# Planning

prompt
    "Let's first understand the problem and devise a plan to solve the problem."
    " Please output the plan starting with the header 'Plan:' "
    "and then followed by a numbered list of steps. "
    "Please make the plan the minimum number of steps required "
    "to accurately complete the task. If the task is a question, "
    "the final step should almost always be 'Given the above steps taken, "
    "please respond to the users original question'. "
    "At the end of your plan, say '<END_OF_PLAN>'"


System: #1 Task Planning Stage: The AI assistant can parse user input to several tasks: [{"task": task, "id": task_id, "dep": dependency_task_id, "args": {"input name": text may contain <resource-dep_id>}}]. The special tag "dep_id" refer to the one generated text/image/audio in the dependency task (Please consider whether the dependency task generates resources of this type.) and "dep_id" must be in "dep" list. The "dep" field denotes the ids of the previous prerequisite tasks which generate a new resource that the current task relies on. The task MUST be selected from the following tools (along with tool description, input name and output type): ['document_qa: This is a tool that answers a question about an document (pdf). It takes an input named `document` which should be the document containing the information, as well as a `question` that is the question about the document. It returns a text that contains the answer to the question.', 'image_captioner: This is a tool that generates a description of an image. It takes an input named `image` which should be the image to caption, and returns a text that contains the description in English.', 'image_qa: This is a tool that answers a question about an image. It takes an input named `image` which should be the image containing the information, as well as a `question` which should be the question in English. It returns a text that is the answer to the question.', 'image_segmenter: This is a tool that creates a segmentation mask of an image according to a label. It cannot create an image. It takes two arguments named `image` which should be the original image, and `label` which should be a text describing the elements what should be identified in the segmentation mask. The tool returns the mask.', 'transcriber: This is a tool that transcribes an audio into text. It takes an input named `audio` and returns the transcribed text.', 'summarizer: This is a tool that summarizes an English text. It takes an input `text` containing the text to summarize, and returns a summary of the text.', 'text_classifier: This is a tool that classifies an English text using provided labels. It takes two inputs: `text`, which should be the text to classify, and `labels`, which should be the list of labels to use for classification. It returns the most likely label in the list of provided `labels` for the input text.', 'text_qa: This is a tool that answers questions related to a text. It takes two arguments named `text`, which is the text where to find the answer, and `question`, which is the question, and returns the answer to the question.', "translator: This is a tool that translates text from a language to another. It takes three inputs: `text`, which should be the text to translate, `src_lang`, which should be the language of the text to translate and `tgt_lang`, which should be the language for the desired ouput language. Both `src_lang` and `tgt_lang` are written in plain English, such as 'Romanian', or 'Albanian'. It returns the text translated in `tgt_lang`.", 'text_reader: This is a tool that reads an English text out loud. It takes an input named `text` which should contain the text to read (in English) and returns a waveform object containing the sound.', 'text_downloader: This is a tool that downloads a file from a `url`. It takes the `url` as input, and returns the text contained in the file.']. There may be multiple tasks of the same type. Think step by step about all the tasks needed to resolve the user's request. Parse out as few tasks as possible while ensuring that the user request can be resolved. Pay attention to the dependencies and order among tasks. If the user input can't be parsed, you need to reply empty JSON [].
Human: please show me a video and an image of (based on the text) 'a boy is running' and dub it
AI: [{"task": "video_generator", "id": 0, "dep": [-1], "args": {"prompt": "a boy is running" }}, {"task": "text_reader", "id": 1, "dep": [-1], "args": {"text": "a boy is running" }}, {"task": "image_generator", "id": 2, "dep": [-1], "args": {"prompt": "a boy is running" }}]

Human: Give you some pictures e1.jpg, e2.png, e3.jpg, help me count the number of sheep?
AI: [ {"task": "image_qa", "id": 0, "dep": [-1], "args": {"image": "e1.jpg", "question": "How many sheep in the picture"}}, {"task": "image_qa", "id": 1, "dep": [-1], "args": {"image": "e2.jpg", "question": "How many sheep in the picture"}}, {"task": "image_qa", "id": 2, "dep": [-1], "args": {"image": "e3.jpg", "question": "How many sheep in the picture"}}]

Human: Now I input: I need to order a pizza from Uber Eats to be delivered to 123 Main St, then book a room at the Grand Hyatt hotel for 1st August 2023'.


GPT 3.5 response:

[{"task": "text_classifier", "id": 0, "dep": [-1], "args": {"text": "I need to order a pizza from Uber Eats to be delivered to 123 Main St"}}, {"task": "text_reader", "id": 1, "dep": [0], "args": {"text": "I need to order a pizza from Uber Eats to be delivered to 123 Main St"}}, {"task": "text_downloader", "id": 2, "dep": [0], "args": {"url": "<Uber Eats order URL>"}}, {"task": "text_classifier", "id": 3, "dep": [-1], "args": {"text": "book a room at the Grand Hyatt hotel for 1st August 2023"}}, {"task": "text_reader", "id": 4, "dep": [3], "args": {"text": "book a room at the Grand Hyatt hotel for 1st August 2023"}}, {"task": "text_downloader", "id": 5, "dep": [3], "args": {"url": "<Grand Hyatt booking URL>"}}]



# simpler planning from o robot 
You are a small robot with a stereo camera vision module
Your vision module uses two cameras to infer 3d
Pick a function based on the robot log.
Always pick a function and provide any args required.
Here are the functions:
LOOK(direction:str)
    direction must be one of ["FORWARD", "LEFT", "RIGHT"]
    📷👀
Pick one of the functions and the args.
Here are some example outputs:
LOOK,LEFT
LOOK,FORWARD
Your response should be a single line with the chosen function code and arguments.






# Vision prompt 


LOOK_PROMPT = os.environ.get("O_LOOK_PROMPT", """
Describe the scene, objects, and characters
Focus on the most important things
If there are humans mention them and their relative position
Do not mention the image
Directly describe the scene
Be concise
Do not use punctuation
Your response will be read out by the robot speech module
Your reponse should not contain any special characters
""")
