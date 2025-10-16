from ultralytics import YOLO
import streamlit as st
import cv2
import pafy
import settings

def load_model(model_path):
    """
    Loads a YOLO object detection model from the specified model_path.
    """
    try:
        model = YOLO(r'C:\Users\chand\OneDrive\Desktop\TEST\Waste-Classification-using-YOLOv8-main\stramlitapp\weights\yoloooo.pt')
        st.toast('Model loaded successfully!', icon='✅')
        return model
    except Exception as e:
        st.error(f"Failed to load model: {e}")
        return None

# [Rest of your existing helper.py code remains exactly the same]
# [Keep all other functions unchanged]

def display_tracker_options():
    st.markdown("""
        <style>
            .stRadio > div {
                background-color: rgba(255, 255, 255, 0.1) !important;
                padding: 10px;
                border-radius: 10px;
            }
                .stRadio div[role="radiogroup"] label {
            color: white !important;
            font-weight: 500;
        }
        </style>
    """, unsafe_allow_html=True)
    
    display_tracker = st.radio("Display Tracker", ('Yes', 'No'))
    is_display_tracker = True if display_tracker == 'Yes' else False
    if is_display_tracker:
        tracker_type = st.radio("Tracker", ("bytetrack.yaml", "botsort.yaml"))
        return is_display_tracker, tracker_type
    return is_display_tracker, None

def _display_detected_frames(conf, model, st_frame, image, is_display_tracking=None, tracker=None):
    """
    Display the detected objects on a video frame using the YOLOv8 model.
    """
    # Resize the image to a standard size
    image = cv2.resize(image, (720, int(720*(9/16))))

    # Display object tracking, if specified
    if is_display_tracking:
        res = model.track(image, conf=conf, persist=True, tracker=tracker)
    else:
        # Predict the objects in the image using the YOLOv8 model
        res = model.predict(image, conf=conf)

    # Plot the detected objects on the video frame
    res_plotted = res[0].plot()
    st_frame.image(res_plotted,
                   caption='Detected Video',
                   channels="BGR",
                   use_column_width=True
                   )

def play_webcam(conf, model):
    """
    Plays a webcam stream with real-time waste detection using YOLOv8.
    """
    # Webcam settings
    source_webcam = settings.WEBCAM_PATH
    is_display_tracker, tracker = display_tracker_options()

    # UI Elements with styling
    stframe = st.empty()
    col1, col2 = st.columns(2)
    with col1:
        stop_button_pressed = st.button("Stop Webcam", key="stop_webcam")
    with col2:
        capture_button = st.button("Capture Image", key="capture_image")

    # Initialize webcam
    cap = cv2.VideoCapture(source_webcam)
    if not cap.isOpened():
        st.error("Failed to access webcam. Please check camera permissions.")
        return

    # Set frame size
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    try:
        while cap.isOpened() and not stop_button_pressed:
            success, frame = cap.read()
            if not success:
                st.warning("Can't receive frame from webcam. Exiting...")
                break

            # Perform detection (with optional tracking)
            if is_display_tracker:
                results = model.track(frame, conf=conf, persist=True, tracker=tracker)
            else:
                results = model.predict(frame, conf=conf)

            # Visualize results
            annotated_frame = results[0].plot()

            # Display the frame with detections
            stframe.image(annotated_frame,
                          channels="BGR",
                          caption="Live Webcam Detection",
                          use_column_width=True)

            if capture_button:
                # Save the captured image
                cv2.imwrite("captured_image.jpg", annotated_frame)
                st.success("Image captured successfully!")
                st.image("captured_image.jpg", caption="Captured Image")
                capture_button = False

    except Exception as e:
        st.error(f"Webcam error: {str(e)}")
    finally:
        cap.release()
        cv2.destroyAllWindows()
        st.info("Webcam session ended.")