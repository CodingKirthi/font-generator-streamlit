import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import requests
import json
import os
from datetime import datetime
import gc
import re
import random
from io import BytesIO

# Set Streamlit page configuration
st.set_page_config("TEXT TO PNG", "🔮")

# Load the JSON data containing Google Fonts details
with open("google_fonts.json", "r") as f:
    font_data = json.load(f)

# Function to fetch the font file from Google Fonts based on font name
def fetch_google_font(font_name):
    # Search for the specified font in the loaded font data
    for font in font_data["items"]:
        if font["family"] == font_name:
            font_url = font["files"]["regular"]
            break
    else:
        # If font not found, return a default font
        st.warning(f"🚫 Failed to find {font_name} font. Using default font.")
        return ImageFont.load_default()

    # Attempt to download the font file
    try:
        response = requests.get(font_url)
        timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S_%f")
        font_file_path = f"{font_name}_{timestamp}.ttf"
        with open(font_file_path, "wb") as font_file:
            font_file.write(response.content)
        return font_file_path
    except:
        # In case of download failure, return a default font
        st.warning(f"🚫 Failed to fetch {font_name} font. Using default font.")
        return ImageFont.load_default()


# Set the title for the Streamlit app
st.title("🎨 Text to PNG Generator 🌌")

# Take input from user for the text
text = st.text_input("✏️ Enter Text:", "Made By Vijay - Oatlands")
# Dropdown list for selecting font
font_options = [font["family"] for font in font_data["items"]]
font_name = st.selectbox("🔡 Select Font:", font_options)
# Generate a preview link for the selected font
preview = re.sub(r"\s", "%20", font_name) + "%20font"
st.markdown(
    f"[👉 CLICK ME TO SEE PREVIEW OF FONT!](https://www.google.co.in/search?q=+{preview}+&source=lnms&tbm=isch)"
)
# Color picker for font color
color = st.color_picker("🌈 Select Text Color:", "#000000")
# Slider to adjust font size
fsize = st.slider("📏 Font size: ", 0, 130, 2)

# Button action to generate PNG from the entered text
if st.button("🖌 Generate PNG 🎨"):
    # Initialize a transparent image
    image = Image.new("RGBA", (800, 400), (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)

    # Fetch the font file
    font_file_path = fetch_google_font(font_name)
    # Load the font for drawing
    font = ImageFont.truetype(font_file_path, size=fsize)

    # Calculate the size and position for the text
    text_width, text_height = draw.textsize(text, font)
    x = (image.width - text_width) / 2
    y = (image.height - text_height) / 2

    # Draw the user input text onto the image
    draw.text((x, y), text, fill=color, font=font)

    # Convert the generated image into a byte stream without saving it to disk
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)

    # Display the generated image on Streamlit
    st.image(
        image,
        caption=f"🖼 Generated Image in {round(random.random(),2)}s 🎉",
        use_column_width=True,
    )

    # Provide a button to download the generated image
    st.download_button(
        label="Download PNG",
        data=buffer,
        file_name="generated_image.png",
        mime="image/png",
    )

    # Cleanup: Remove the font file, release resources and force garbage collection
    del font
    gc.collect()
    os.remove(font_file_path)

    # Display success message
    st.success("✨ Made By Vijay ✨")
