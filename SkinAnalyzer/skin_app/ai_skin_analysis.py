import openai
from PIL import Image

openai.api_key = "your_openai_api_key"

def analyze_skin(image_path):
    with open(image_path, "rb") as image_file:
        response = openai.Image.create(
            model="gpt-4-vision-preview",
            file=image_file,
            prompt="Analyze this skin image and provide possible skin conditions like acne, eczema, or fungal infections. Also, suggest treatments."
        )
    return response["choices"][0]["text"]
