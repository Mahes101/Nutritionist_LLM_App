import streamlit as st 
import google.generativeai as genai
from dotenv import load_dotenv
from PIL import Image
import base64
import os
import io

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(prompt_input, image):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content([prompt_input, image[0]])
    return response.text 

def input_image_setup(uploaded_file):
    
    if uploaded_file is not None:
        #Convert into bytes
        img_byte_arr = uploaded_file.getvalue()
        
        pdf_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": img_byte_arr #img_byte_arr
            }
        ]
        return pdf_parts
    else:
        raise Exception("PDF File does not uploaded")


## Streamlit App
st.set_page_config(
    page_title="Calories Calculator",
    page_icon=":material/track_changes:"
)

st.title("Gemini Health App")

uploaded_file = st.file_uploader("Upload an Image: ", type=['jpg','jpeg','png'])

image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded_Image", use_container_width=True)
    
submit = st.button("Tell Me about the calories")    

input_prompt = """
    You are an expert in nutritionist, yoou need to see the food items from the image
    and calculate the total calories, and also provide the details of each food items with calories from the given image 
    intake in the below format
    1.Item1 : calories,
    2.Item2 : calories,
    .......
    Finally you can also mention whether the food is healthy or not and mention the percentage split of the ratio of 
    carbohydrates, fats, fibre, sugar and other things in our diet.
    
"""
if submit:
    image_data = input_image_setup(uploaded_file)
    response = get_gemini_response(input_prompt, image_data)
    st.subheader("The Response is: ")
    st.write(response)
        