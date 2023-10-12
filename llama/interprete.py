import interpreter

interpreter.model = "gpt-3.5-turbo"

interpreter.chat("Plot AAPL and META's normalized stock prices") # Executes a single command
interpreter.chat() # Starts an interactive chat

# how to run 
# conda activate huggingface
# interpreter -y