import openai

def get_car_ai_bio(model, brand, year):
    prompt = f"Escreva uma breve biografia para o carro da marca {brand}, modelo {model}, do ano {year}."
    openai.api_key = "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"  # Replace
    responde = openai.Completion.create(
        model='text-davinci-003',
        prompt=prompt,
        max_tokens=1000
    )
    return responde.choices[0].text.strip()