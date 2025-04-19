import openai

def ask_ai(prompt):
    client = openai.OpenAI(api_key="pypi-AgEIcHlwaS5vcmcCJGUwM2E5ODljLTU3YTctNDk0ZC1iNDYzLWFjMmRkNzZkMjliOAACKlszLCIyZWU5ZjA3ZC0yMTUzLTQ2YmEtYTA4Zi01N2EwMTY4N2Y0ODQiXQAABiCcWyHcC-IHmrwqZn3qxWROcbMqdDyFEY6ad8cqVUvo0g")  # Replace with your actual key
    response = client.chat.completions.create(
        model="gpt-3.5",  # or "gpt-3.5-turbo"
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content
