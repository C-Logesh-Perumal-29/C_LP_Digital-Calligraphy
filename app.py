import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import textwrap
import os
from io import BytesIO
import base64  # Don't forget to import base64

# Preprocess text (split into lines)
def preprocess_text(text, line_length=50):
    lines = textwrap.wrap(textwrap.dedent(text), line_length)
    return '\n'.join(lines)

# Function to get a list of font files in the 'Fonts' folder
def get_font_files():
    font_folder_path = "Fonts"  # Update this path to match your folder structure
    return [f for f in os.listdir(font_folder_path) if f.endswith('.ttf')]

# Create an image with handwritten-style text
def create_handwritten_image(text, font_size, font_color, font_family, background_color, background_size):
    # Create an image with the specified background size and color
    image = Image.new('RGB', background_size, color=background_color)
    
    # Load the specified font
    font_path = os.path.join("Fonts", font_family)  # Assuming 'Fonts' is a subfolder in the current directory
    font = ImageFont.truetype(font_path, size=font_size)
    
    # Create a drawing context
    draw = ImageDraw.Draw(image)
    
    # Define the starting position
    x, y = 50, 50
    
    # Define the line height
    line_height = font_size + 10
    
    # Draw text on the image
    for line in text.split('\n'):
        draw.text((x, y), line, fill=font_color, font=font)
        y += line_height
    
    # Save the image
    return image

def get_image_download_link(image_buffer):
    # Generate a download link for the image
    href = f'<a href="data:file/png;base64,{base64.b64encode(image_buffer.read()).decode()}" download="handwritten_image.png">Click here to download</a>'
    return href

# Streamlit app
def main():
    st.set_page_config(
        page_title="Handwritten Text Generator",
        page_icon="✍️",
        layout="wide",)

    # Hide Menu_Bar & Footer :
    hide_menu_style = """
        <style>
        #MainMenu {visibility : hidden;}
        footer {visibility : hidden;}
        </style>
    """
    st.markdown(hide_menu_style , unsafe_allow_html=True)

    st.sidebar.image("Logo.jpg")
    
    # Get user input
    user_text = st.sidebar.text_area("Enter the text you want to convert to handwritten style:")

    st.sidebar.subheader("Customization")

    # Get a list of font files
    font_files = get_font_files()

    font_size = st.sidebar.slider("Font Size", 10, 100, 34, key="font_size", help="Font Size Slider")
    font_color = st.sidebar.color_picker("Font Color", "#0000FF", key="font_color")
    font_family_index = st.sidebar.slider("Select Font Family", 0, len(font_files) - 1, 0, key="font_family_index")
    font_family = font_files[font_family_index]
    background_color = st.sidebar.color_picker("Background Color", "#FFFFFF", key="background_color")
    background_width = st.sidebar.slider("Background Width", 100, 2000, 1000, key="background_width")
    background_height = st.sidebar.slider("Background Height", 100, 2000, 1200, key="background_height")
    line_length = st.sidebar.slider("Line Length", 10, 150, 50, key="line_length")

    title_html = f'<h1 style="color:#FF5733; text-align:center;font-family:Edwardian Script ITC;font-size:96px;">Handwritten Text Generator</h1>'
    st.markdown(title_html, unsafe_allow_html=True)

    # Create two columns for input and output
    col1, col2 = st.columns([2, 3])

    # Preprocess user input (split into lines)
    processed_text = preprocess_text(user_text, line_length)

    # Check if the content fits within the background size
    if len(processed_text.split('\n')) * (font_size + 10) > background_height:
        st.error("The content exceeds the background height. Please reduce the text or increase the background size.")
    else:
        # Generate the handwritten-style text image
        Handwritten_Image = create_handwritten_image(processed_text, font_size, font_color, font_family, background_color, (background_width, background_height))

        # Display the image
        st.image(Handwritten_Image, caption="Handwritten Text", use_column_width=True)

        # Save Image button
        col1, col2 = st.columns([2.7, 3.3])

        st.write("\n\n\n\n")

        # Center align the Save Image button
        with col2:
            # Save Image button
            if st.button("Download", key="save_button", help="Save Image"):
                # Save the image to BytesIO buffer
                image_buffer = BytesIO()
                Handwritten_Image.save(image_buffer, format="PNG")
                image_buffer.seek(0)

                # Offer the image for download
                st.markdown(get_image_download_link(image_buffer), unsafe_allow_html=True)
                st.balloons()
                
if __name__ == "__main__":
    main()
