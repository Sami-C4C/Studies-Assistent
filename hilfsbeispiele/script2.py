import openai


def ask_openai(prompt, model="text-davinci-003", max_tokens=150):
    openai.api_key = ' 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'

    try:
        response = openai.Completion.create(
            model=model,
            prompt=prompt,
            max_tokens=max_tokens
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"An error occurred: {e}"


def main():
    print("OpenAI Chat - Type 'quit' to exit.")

    while True:
        user_input = input("You: ")
        if user_input.lower() == 'quit':
            break

        response = ask_openai(user_input)
        print("AI:", response)


if __name__ == "__main__":
    main()
