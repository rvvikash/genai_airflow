from openai import OpenAI

def main():
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key="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",  # Your API key here
        default_headers={
            "Referer": "http://localhost",
            "X-Title": "LLM Token Validator"
        }
    )

    response = client.chat.completions.create(
        model="openai/gpt-4o",
        messages=[{"role": "user", "content": "trigger this dag cli command llm_fix_suggestion ?"}],
        max_tokens=1500
    )

    print("✅ LLM Response:", response.choices[0].message.content)

if __name__ == "__main__":
    main()
