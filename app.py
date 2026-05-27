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
import streamlit.components.v1 as components  # Crucial for rendering HTML/JS files
from streamlit_option_menu import option_menu

# Local Modules
import settings
import helper

# 1. SET PAGE CONFIG
st.set_page_config(
    page_title="Smart Waste Management System",
    page_icon="🚛",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Helper function to safely read and render your frontend HTML files
def render_html_page(html_filename):
    html_path = os.path.join("frontend", html_filename)
    try:
        # 1. Read your raw HTML file code
        with open(html_path, "r", encoding="utf-8") as f:
            html_content = f.read()
        
        # 2. Automatically find and load the matching CSS file if it exists
        # Maps 'index.html' -> 'Styles.css', 'Signin.html' -> 'Signin.css', etc.
        css_filename = "Styles.css" if html_filename == "index.html" else html_filename.replace(".html", ".css")
        css_path = os.path.join("frontend", css_filename)
        
        css_content = ""
        if os.path.exists(css_path):
            with open(css_path, "r", encoding="utf-8") as f:
                css_content = f.read()

        # 3. Inject the CSS content safely into a single runtime string block
        if css_content:
            injected_style = f"<style>{css_content}</style>"
            # Places the CSS code cleanly right before the closing head tag
            if "</head>" in html_content:
                html_content = html_content.replace("</head>", f"{injected_style}</head>")
            else:
                html_content = injected_style + html_content

        # 4. Serve the combined result to the Streamlit UI window frame
        components.html(html_content, height=800, scrolling=True)
        
    except FileNotFoundError:
        st.error(f"Could not locate '{html_filename}' inside your 'frontend' folder.")

# 2. NAVIGATION MENU (Updated to match your actual frontend modules!)
selected = option_menu(
    menu_title=None,
    options=["Home Dashboard", "YOLOv8 Detection", "Active Trucks", "Waste Collected", "Area Wise View", "Team Sign-in"],
    icons=["grid-1x2", "camera", "truck", "bar-chart-line", "map", "person-badge"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "rgba(0,0,0,0.8)"},
        "icon": {"color": "#4CAF50", "font-size": "16px"},
        "nav-link": {
            "font-size": "14px",
            "text-align": "center",
            "margin": "0px",
            "color": "white",
            "padding": "10px 12px",
        },
        "nav-link-selected": {"background-color": "#4CAF50"},
    }
)

# 3. MAIN ROUTING ENGINE
if selected == "Home Dashboard":
    # Renders your static landing page index structure
    render_html_page("index.html")

# elif selected == "Active Trucks":
#     # Renders active truck data panels
#     render_html_page("ActiveTrucks.html")

# elif selected == "Waste Collected":
#     # Renders your custom static analytical summary views
#     render_html_page("WasteCollected.html")

# elif selected == "Area Wise View":
#     # Renders your regional area distribution frameworks
#     render_html_page("areaWise.html")

# elif selected == "Team Sign-in":
#     # Renders your operational login portals
#     render_html_page("Signin.html")

elif selected == "YOLOv8 Detection":
    st.subheader("🤖 Live Object Detection Machine Learning Core")
    
    # Sidebar Configuration
    st.sidebar.header("ML Model Config")
    confidence = float(st.sidebar.slider("Select Model Confidence", 25, 100, 25)) / 100

    # Load model dynamically via path properties
    model_path = Path(settings.DETECTION_MODEL)
    try:
        model = helper.load_model(model_path)
    except Exception as ex:
        model = None

    # Source selection setup
    st.sidebar.header("Image/Video Config")
    source_radio = st.sidebar.radio("Select Source", settings.SOURCES_LIST)

    if model is None:
        st.error("Model engine is uninitialized. Verify file configurations inside settings.py.")
    else:
        if source_radio == settings.IMAGE:
            source_img = st.sidebar.file_uploader("Choose an image...", type=("jpg", "jpeg", "png", "bmp", "webp"))
            col1, col2 = st.columns(2)

            with col1:
                if source_img is None:
                    st.image(str(settings.DEFAULT_IMAGE), caption="Default Sample View", use_column_width=True)
                else:
                    uploaded_image = PIL.Image.open(source_img)
                    st.image(source_img, caption="Uploaded Image", use_column_width=True)

            with col2:
                if source_img is None:
                    st.image(str(settings.DEFAULT_DETECT_IMAGE), caption='Sample Detections Output', use_column_width=True)
                else:
                    if st.sidebar.button('Detect Objects'):
                        res = model.predict(uploaded_image, conf=confidence)
                        boxes = res[0].boxes
                        res_plotted = res[0].plot()[:, :, ::-1]
                        st.image(res_plotted, caption='Processed Detections Output', use_column_width=True)
                        
                        with st.expander("Detection Metrics Metadata"):
                            if len(boxes) == 0:
                                st.write("No items detected matching targeted metric categories.")
                            for box in boxes:
                                st.write(box.data)

        elif source_radio == settings.WEBCAM:
            helper.play_webcam(confidence, model)