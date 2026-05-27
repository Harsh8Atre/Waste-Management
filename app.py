import os
import sys

# Forces Windows to accept the low-level C++ DLL initialization routine safely
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
os.environ["OMP_NUM_THREADS"] = "1"

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
    try:
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        pass # Prevents crashing if styles.css is missing temporarily

local_css("styles.css")

# 3. NAVIGATION MENU (Reverted back to original tabs)
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
    st.sidebar.error(f"Unable to load model from: {model_path}")
    model = None

# Source selection
st.sidebar.header("Image/Video Config")
source_radio = st.sidebar.radio(
    "Select Source", settings.SOURCES_LIST,
    help="Choose between image upload or webcam"
)

# --- PAGE ROUTING ---

if selected == "Home":
    st.subheader("Welcome to the AI Waste Management System")
    st.markdown("""
    This intelligent platform leverages real-time computer vision processing to detect, classify, and sort recyclable versus non-recyclable materials.
    
    ### How to start:
    1. Select the **Detection** tab from the top navigation bar.
    2. Choose your inputs from the sidebar selection menu (Static Image uploads or active Webcam processing streams).
    3. Monitor accuracy yields and distributions inside the live tracking charts on the **Statistics** page.
    """)

elif selected == "Detection":
    if model is None:
        st.error("Model engine is uninitialized. Verify file configurations inside settings.py.")
    else:
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
                        st.image(default_image_path, caption="Default Image", use_column_width=True)
                    else:
                        uploaded_image = PIL.Image.open(source_img)
                        st.image(source_img, caption="Uploaded Image", use_column_width=True)
                except Exception as ex:
                    st.error("Error occurred while opening the image.")

            with col2:
                if source_img is None:
                    default_detected_image_path = str(settings.DEFAULT_DETECT_IMAGE)
                    st.image(default_detected_image_path, caption='Detected Image', use_column_width=True)
                else:
                    if st.sidebar.button('Detect Objects'):
                        res = model.predict(uploaded_image, conf=confidence)
                        boxes = res[0].boxes
                        res_plotted = res[0].plot()[:, :, ::-1]
                        st.image(res_plotted, caption='Detected Image', use_column_width=True)
                        
                        with st.expander("Detection Results"):
                            if len(boxes) == 0:
                                st.write("No distinct items detected matching the targeted categories.")
                            for box in boxes:
                                st.write(box.data)

        elif source_radio == settings.WEBCAM:
            helper.play_webcam(confidence, model)
        else:
            st.error("Please select a valid source type!")

elif selected == "Statistics":
    st.header("Waste Statistics Dashboard")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
            <div class="stat-card" style="padding:20px; border-radius:10px; background-color:rgba(0,0,0,0.1); border-left:5px solid #4CAF50;">
                <h3 style="margin:0;">Total Waste Detected</h3>
                <div class="stat-value" style="font-size:32px; font-weight:bold; color:#4CAF50;">1,248</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="stat-card" style="padding:20px; border-radius:10px; background-color:rgba(0,0,0,0.1); border-left:5px solid #2196F3;">
                <h3 style="margin:0;">Recyclable Waste</h3>
                <div class="stat-value" style="font-size:32px; font-weight:bold; color:#2196F3;">856</div>
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