# you have to install openai via: pip install openai
# then import this bibleothek

import openai
openai.api_key = "YOUR_API_KEY"

while True:
    question = input("Enter Question: ")

    answer = openai.Completion.create(
        model="text-davinci-003",
        prompt=question,
        temperature=0.9,
        max_tokens=1500,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.6,
    )
    text = answer['choices'][0]['text']
    print("ChatGPT : " + text)
