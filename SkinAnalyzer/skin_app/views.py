from django.shortcuts import render, redirect
from .models import SkinAnalysis
from .ai_skin_analysis import analyze_skin
import openai
import os 
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import google.generativeai as genai
from django.conf import settings

# Configure Gemini API
import os
import google.generativeai as genai
from django.conf import settings

# ✅ Configure Gemini API key globally (do this only once)
genai.configure(api_key=settings.GEMINI_API_KEY)

import os
import google.generativeai as genai
from django.conf import settings

def analyze_skin_condition(image_path):
    """Processes an uploaded image and analyzes skin conditions using Gemini AI."""
    
    # ✅ Ensure MEDIA_ROOT is properly joined
    full_path = os.path.join(settings.MEDIA_ROOT, image_path.strip("/").replace("media/", ""))
    
    print(f"🔍 Checking file at: {full_path}")  # Debugging

    # ✅ Check if file exists
    if not os.path.exists(full_path):
        print(f"❌ File not found at: {full_path}")
        return {'error': 'File not found. Please upload the image again.'}

    print(f"✅ File found! Proceeding with AI analysis...")

    try:
        # ✅ Read image file in binary mode
        with open(full_path, "rb") as image_file:
            image_data = image_file.read()

        # ✅ Ensure Gemini API Key is set correctly
        if not settings.GEMINI_API_KEY:
            print("❌ Gemini API key is missing!")
            return {'error': 'Gemini API key is missing. Please check your settings.'}

        # ✅ Initialize Gemini AI Model
        model = genai.GenerativeModel("gemini-1.5-flash")

        # ✅ Define AI prompt
        prompt = """Analyze this image for any visible skin conditions such as acne, hyperpigmentation, dryness, redness, or irritation.
                   - Identify possible skin issues.
                   - Provide potential causes.
                   - Suggest skincare recommendations & remedies.
                   - If necessary, mention whether a dermatologist consultation is needed."""

        # ✅ Send image to Gemini for analysis
        response = model.generate_content([
            prompt,
            {"mime_type": "image/jpeg", "data": image_data}
        ])

        # ✅ Extract and return AI insights
        if response and hasattr(response, "text"):
            print(f"✅ AI Analysis Result: {response.text}")
            
            # ✅ Convert Markdown formatting to HTML-compatible format
            formatted_text = response.text.replace("\n", "<br>").replace("**", "<strong>").replace("* ", "- ")

            return {'insights': formatted_text}
        else:
            print("⚠️ AI did not return any insights.")
            return {'error': 'AI did not return any insights.'}

    except FileNotFoundError:
        print(f"❌ File not found at: {full_path}")
        return {'error': 'File not found. Please upload the image again.'}

    except genai.ApiException as api_error:
        print(f"⚠️ API Error: {api_error}")
        return {'error': 'AI service error. Please try again later.'}

    except Exception as e:
        print(f"⚠️ Unexpected Error: {e}")
        return {'error': f'An error occurred: {str(e)}'}





def upload_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save(f'skin_images/{image.name}', image)
        uploaded_file_url = fs.url(filename)

        # Analyze the image using AI
        analysis_result = analyze_skin_condition(uploaded_file_url)

        # Save result in database
        skin_analysis = SkinAnalysis(image=filename, condition=analysis_result, recommendations="Use mild skincare products.")
        skin_analysis.save()

        return render(request, 'skin_app/upload_skin.html', {'uploaded_file_url': uploaded_file_url, 'analysis_result': analysis_result})
    
    return render(request, 'skin_app/upload_skin.html')

def skin_results(request, analysis_id):
    analysis = SkinAnalysis.objects.get(id=analysis_id)
    return render(request, 'skin_results.html', {"analysis": analysis})

from .ai_doctor_recommend import recommend_dermatologist

def skin_results(request, analysis_id):
    analysis = SkinAnalysis.objects.get(id=analysis_id)
    dermatologist = recommend_dermatologist(analysis.condition)
    
    return render(request, 'skin_results.html', {
        "analysis": analysis, "dermatologist": dermatologist
    })
def user_history(request):
    analyses = SkinAnalysis.objects.all()
    return render(request, 'history.html', {"analyses": analyses})

# Create your views here.
