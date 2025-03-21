import openai
def recommend_dermatologist(condition):
    prompt = f"Suggest the best dermatologist in Lucknow for treating {condition}."
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": prompt}]
    )
    return response['choices'][0]['message']['content']
