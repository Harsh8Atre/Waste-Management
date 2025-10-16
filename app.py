# Python In-built packages
from pathlib import Path
import PIL

# External packages
import streamlit as st
from streamlit_option_menu import option_menu

# Local Modules
import settings
import helper

# 1. SET PAGE CONFIG - MUST BE FIRST STREAMLIT COMMAND
st.set_page_config(
    page_title="Waste Classification using YOLOv8",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "Waste Classification System using YOLOv8"
    }
)

# 2. LOAD CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("styles.css")

# 3. NAVIGATION MENU
selected = option_menu(
    menu_title=None,
    options=["Home", "Detection", "Statistics", "About"],
    icons=["house", "camera", "bar-chart", "info-circle"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "rgba(0,0,0,0.7)"},
        "icon": {"color": "#4CAF50", "font-size": "18px"},
        "nav-link": {
            "font-size": "16px",
            "text-align": "center",
            "margin": "0px",
            "color": "white",
            "border-radius": "20px",
            "padding": "8px 15px",
        },
        "nav-link-selected": {"background-color": "#4CAF50"},
    }
)

# 4. MAIN PAGE CONTENT
st.title("Waste Classification using YOLOv8")

# Sidebar Configuration
st.sidebar.header("ML Model Config")

# Model Options
model_type = st.sidebar.radio(
    "Select Task", ['Detection'],
    help="Choose between object detection or segmentation"
)

confidence = float(st.sidebar.slider(
    "Select Model Confidence", 25, 100, 25)) / 100

# Model selection
if model_type == 'Detection':
    model_path = Path(settings.DETECTION_MODEL)
elif model_type == 'Segmentation':
    model_path = Path(settings.SEGMENTATION_MODEL)

# Load model
try:
    model = helper.load_model(model_path)
except Exception as ex:
    st.error(f"Unable to load model. Check the specified path: {model_path}")
    st.error(ex)

# Source selection
st.sidebar.header("Image/Video Config")
source_radio = st.sidebar.radio(
    "Select Source", settings.SOURCES_LIST,
    help="Choose between image upload or webcam"
)

# Page Routing
if selected == "Detection":
    if source_radio == settings.IMAGE:
        source_img = st.sidebar.file_uploader(
            "Choose an image...", 
            type=("jpg", "jpeg", "png", 'bmp', 'webp'),
            help="Upload an image for waste classification"
        )

        col1, col2 = st.columns(2)

        with col1:
            try:
                if source_img is None:
                    default_image_path = str(settings.DEFAULT_IMAGE)
                    default_image = PIL.Image.open(default_image_path)
                    st.image(default_image_path, caption="Default Image",
                             use_column_width=True)
                else:
                    uploaded_image = PIL.Image.open(source_img)
                    st.image(source_img, caption="Uploaded Image",
                             use_column_width=True)
            except Exception as ex:
                st.error("Error occurred while opening the image.")
                st.error(ex)

        with col2:
            if source_img is None:
                default_detected_image_path = str(settings.DEFAULT_DETECT_IMAGE)
                default_detected_image = PIL.Image.open(
                    default_detected_image_path)
                st.image(default_detected_image_path, caption='Detected Image',
                         use_column_width=True)
            else:
                if st.sidebar.button('Detect Objects'):
                    res = model.predict(uploaded_image,
                                        conf=confidence
                                        )
                    boxes = res[0].boxes
                    res_plotted = res[0].plot()[:, :, ::-1]
                    st.image(res_plotted, caption='Detected Image',
                             use_column_width=True)
                    try:
                        with st.expander("Detection Results"):
                            for box in boxes:
                                st.write(box.data)
                    except Exception as ex:
                        st.write("No image is uploaded yet!")

    elif source_radio == settings.WEBCAM:
        helper.play_webcam(confidence, model)

    else:
        st.error("Please select a valid source type!")

elif selected == "Statistics":
    st.header("Waste Statistics Dashboard")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
            <div class="stat-card">
                <h3>Total Waste Detected</h3>
                <div class="stat-value">1,248</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="stat-card">
                <h3>Recyclable Waste</h3>
                <div class="stat-value">856</div>
            </div>
        """, unsafe_allow_html=True)

elif selected == "About":
    st.header("About This Project")
    st.markdown("""
        <div class="about-content">
            <p>This waste classification system uses YOLOv8 to identify and categorize different types of waste materials.</p>
            <p>The system helps in automating waste management processes and improving recycling efficiency.</p>
        </div>
    """, unsafe_allow_html=True)