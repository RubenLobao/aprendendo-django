import openai


client = OpenAI(api_key='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')  # Substitua "YOUR_API_KEY" pela sua chave de API real do OpenAI.

def get_car_ai_bio(model, brand, year):
    prompt = f"Escreva uma breve biografia para o carro da marca {brand}, modelo {model}, do ano {year}." 
    message = prompt
    response = client.ChatCompletion.create(
        messages = [
            {
                "role": "user",
                "content": message
            }
        ],
        model="gpt-3.5-turbo",
        max_tokens=100, 
    )
    return response.choices[0].message.content.strip()