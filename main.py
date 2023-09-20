import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import requests
import json
import os
from datetime import datetime
import gc
import re

st.set_page_config(
    "TEXT TO PNG",
    "🔮"
)
# Load the JSON data for Google Fonts
with open('google_fonts.json', 'r') as f:
    font_data = json.load(f)

# Fetch the font file from the provided URL
def fetch_google_font(font_name):
    # Extract the font file URL from JSON data
    for font in font_data['items']:
        if font['family'] == font_name:
            font_url = font['files']['regular']
            break
    else:
        st.warning(f"🚫 Failed to find {font_name} font. Using default font.")
        return ImageFont.load_default()

    # Download font file and save to local directory with a timestamp
    try:
        response = requests.get(font_url)
        timestamp = datetime.now().strftime('%Y_%m_%d_%H_%M_%S_%f')
        font_file_path = f"{font_name}_{timestamp}.ttf"
        with open(font_file_path, 'wb') as font_file:
            font_file.write(response.content)
        return font_file_path
    except:
        st.warning(f"🚫 Failed to fetch {font_name} font. Using default font.")
        return ImageFont.load_default()

# Streamlit app
st.title("🎨 Text to PNG Generator 🌌")

# Input for text
text = st.text_input("✏️ Enter Text:", "Hello, Streamlit!")

# Dropdown to select font
font_options = [font['family'] for font in font_data['items']]
font_name = st.selectbox("🔡 Select Font:", font_options)
preview = re.sub(r'\s', '%20', font_name) + "%20font"
st.markdown(f"[CLICK ME TO SEE PREVIEW OF FONT!](https://www.google.com/search?q=+{preview}+&source=lnms&tbm=isch)")

# Color picker for foreground text color
color = st.color_picker("🌈 Select Text Color:", "#000000")

# Font size
fsize = st.slider('📏 Font size: ', 0, 130, 2)

# Button to generate PNG
if st.button("🖌 Generate PNG 🎨"):
    # Create an image with a transparent background
    image = Image.new("RGBA", (800, 400), (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)

    # Fetch the selected Google Font
    font_file_path = fetch_google_font(font_name)

    # Load the font
    font = ImageFont.truetype(font_file_path, size=fsize)

    # Calculate text size and position
    text_width, text_height = draw.textsize(text, font)
    x = (image.width - text_width) / 2
    y = (image.height - text_height) / 2

    # Draw text with the selected color
    draw.text((x, y), text, fill=color, font=font)

    # Display the generated image
    st.image(image, caption=f"🖼 Generated Image with {font_name} Font 🎉", use_column_width=True)

    # Release the font object and force garbage collection
    del font
    gc.collect()

    # Delete the downloaded font file
    os.remove(font_file_path)

    # Provide a sign-off note
    st.success("✨ Made By Vijay 🌟")
