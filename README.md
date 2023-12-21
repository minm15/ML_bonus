# How to use 
---
## set the chromeDriver
Download the chromeDriver [here](https://googlechromelabs.github.io/chrome-for-testing/)

## subject
Currently, there is a need to manually adjust the subject.
Replace the target_subject at line 54 in `main.py`

## Tips
- For test, you can revise the model as gpt-3.5-turbo in `config.json`
- You are free to cunstomize your prompt in `prompt.txt`, remember to revise the `chat()` function in `main.py` to fit your change. 

## TODO
- Automatic for several subjects
- Automatically handle the csv file generation and evaluation