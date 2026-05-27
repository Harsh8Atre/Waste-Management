from pathlib import Path
import sys

# 1. Get the absolute path of this settings.py file
file_path = Path(__file__).resolve()

# 2. Get the root directory folder (E:\Waste-Management-main)
ROOT = file_path.parent

# Add the root path to the sys.path list if it is not already there
if ROOT not in sys.path:
    sys.path.append(str(ROOT))

# Sources Configuration
IMAGE = 'Image'
WEBCAM = 'Webcam'
SOURCES_LIST = [IMAGE, WEBCAM]

# Images Configuration (Looks directly inside your local 'images' folder)
IMAGES_DIR = ROOT / 'images'
DEFAULT_IMAGE = IMAGES_DIR / 'def.jfif'
DEFAULT_DETECT_IMAGE = IMAGES_DIR / 'def1.jpg'

# Videos Configuration
VIDEO_DIR = ROOT / 'videos'
VIDEO_1_PATH = VIDEO_DIR / 'video_1.mp4'
VIDEO_2_PATH = VIDEO_DIR / 'video_2.mp4'
VIDEO_3_PATH = VIDEO_DIR / 'video_3.mp4'
VIDEO_4_PATH = VIDEO_DIR / 'video_4.mp4'
VIDEO_5_PATH = VIDEO_DIR / 'video_5.mp4'
VIDEOS_DICT = {
    'video_1': VIDEO_1_PATH,
    'video_2': VIDEO_2_PATH,
    'video_3': VIDEO_3_PATH,
    'video_4': VIDEO_4_PATH,
    'video_5': VIDEO_5_PATH,
}

# 3. Model Weight Configuration Paths
MODEL_DIR = ROOT / "weights"

# Points directly to 'best.pt' sitting in your root directory folder
DETECTION_MODEL = ROOT / 'best.pt'

# Webcam Configuration
WEBCAM_PATH = 0