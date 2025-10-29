# --------------------------------------------------------------

# import sys, types
# sys.modules['cgi'] = types.ModuleType('cgi')





import requests
from io import BytesIO
from dotenv import load_dotenv
import google.generativeai as genai
from googletrans import Translator
from PIL import Image
import os

# Load environment variable:
load_dotenv()

# Configure the API key for Google Generative AI:
API_KEY = "AIzaSyB6IPWiMtU5XXtkRlTlFKxR-b8cvMTHACM"
genai.configure(api_key=API_KEY)
# genai.configure(api_key=API_KEY, api_version='v1beta')


# Initialize the translator:
translator = Translator()

# Function to download an image from URL:
def download_image_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        return Image.open(BytesIO(response.content))
    else:
        raise ValueError(f"Failed to download image. Status code: {response.status_code}")


def get_gemini_response(input_prompt, image_urls):
    # Use the stable multimodal model
    # model_name = "gemini-1.5-flash-002"
    # model_name = "gemini-1.5-flash"
    # model_name = genai.GenerativeModel("gemini-1.5-flash")
    # Correct
    model_name = "gemini-2.5-pro"



    responses = []
    for url in image_urls:
        image = download_image_from_url(url)

        # Initialize the multimodal model
        # Correct way:
        model = genai.GenerativeModel(model_name)

        if input_prompt.strip():
            response = model.generate_content([input_prompt, image])
        else:
            # response = model.generate_content(image)
            response = model.generate_content([image])


        generated_text = response.text

        # Translate to Marathi
        translated_text = translator.translate(generated_text, src='en', dest='mr').text

        responses.append({
            'english': generated_text,
            'marathi': translated_text
        })

    return responses




# # Function to process the image and generate text:
# def get_gemini_response(input_prompt, image_urls):
#     # model = genai.GenerativeModel('gemini-1.5-flash')
#     # model = genai.GenerativeModel('gemini-1.5')
#     # model = genai.GenerativeModel('gemini-2.0-flash')
#     # model = genai.GenerativeModel('gemini-1.5')
#     model = genai.GenerativeModel("models/gemini-1.5-flash-002")
    




    
#     responses = []
#     for url in image_urls:
#         image = download_image_from_url(url)
        
#         # Generate content using the image & prompt:
#         if input_prompt.strip():
#             response = model.generate_content([input_prompt, image])
#         else:
#             response = model.generate_content(image)
        
#         # Extract the generated text:
#         generated_text = response.text
        
#         # Translate the generated text to Marathi:
#         translated_text = translator.translate(generated_text, src='en', dest='mr').text
        
#         # Append both English and Marathi translations:
#         responses.append({
#             'english': generated_text,
#             'marathi': translated_text
#         })
    
#     return responses

# User input:
# input_prompt = "describe the given image in 150 letters"
input_prompt = (
    # "Look at the accident image. Give output in JSON with two parts: "
    # "'description' = short summary (4-5 lines, max 450 characters). "
    # "'instructions' = short numbered rescue steps, clear and simple."

   
    "Look at the accident image. Give output in JSON with two parts: "
    "'description' = short summary of the accident scene (max 400-500 characters). "
    "'instructions' = 3-5 short simple steps combining how to manage the scene and how to help victims, "
    # "written in clear language that normal people can follow. Avoid medical jargon."
    "written in clear language that normal people can follow. Use Indian context: call 108 for ambulance and emergency services. "
    "Avoid medical jargon."



)

image_urls = [
    # "https://resize.indiatvnews.com/en/resize/newbucket/1200_-/2025/04/maharashtra-accident-1743564838.jpg"
    "https://media.newscentermaine.com/assets/NCM/images/5ed53771-23bf-470c-8fd2-5b14b674fb3c/5ed53771-23bf-470c-8fd2-5b14b674fb3c_1920x1080.jpg"
]

# image_urls = input("Enter image URLs: ").split(',')

# Remove any extra spaces from the URLs:
image_urls = [url.strip() for url in image_urls]

try:
    # Get the AI-generated response:
    results = get_gemini_response(input_prompt, image_urls)
    for idx, result in enumerate(results, 1):
        print(f"\nGenerated Text from Image {idx} (English):")
        print(result['english'])
        print(f"\nGenerated Text from Image {idx} (Marathi):")
        print(result['marathi'])
        
except Exception as e:
    print(f"An error occurred: {e}")






