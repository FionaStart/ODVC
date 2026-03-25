import warnings
warnings.filterwarnings("ignore",category=DeprecationWarning)
import streamlit as st
from deepforest import main 
from deepforest import utilities
import os
import subprocess
import sys
from pyproj import CRS
import time



st.title("DeepForest Model Settings")
st.header("Select Local Tiff File")
image_path = st.text_input("Enter the path to your local TIFF file:") #   D:\Thesis2026\ProjectCode\Data\TreeAOIWGS84.tif
if st.button("Load Image"):
    if os.path.isfile(image_path):
        st.success("Image loaded successfully!")
    else:
        st.error("File not found. Please check the path and try again.")

col_left, col_right = st.columns(2)
#--- Model Settings 1---
with col_left:

    st.header("Settings for 1st Run")
    patch_size_1 = st.slider("Patch Size (1st Run)", min_value=400, max_value=2000, value=1200, step=100)
    patch_overlap_1 = st.slider("Patch Overlap (1st Run)", min_value=0.0, max_value=1.0, value=0.25, step=0.05)
    score_threshold_1 = st.slider("Score Threshold (1st Run)", min_value=0.0, max_value=1.0, value=0.2, step=0.05)
    iou_threshold_1 = st.slider("NMS IOU Threshold (1st Run)", min_value=0.0, max_value=1.0, value=0.15, step=0.05)
    batch_size_1= st.slider("Batch Size (1st Run)", min_value=1, max_value=32, value=4)

#--- Model Settings 2---
with col_right:
    st.header("Settings for 2nd Run")
    patch_size_2 = st.slider("Patch Size (2nd Run)", min_value=400, max_value=2000, value=1200, step=100)
    patch_overlap_2 = st.slider("Patch Overlap (2nd Run)", min_value=0.0, max_value=1.0, value=0.25, step=0.05)
    score_threshold_2 = st.slider("Score Threshold (2nd Run)", min_value=0.0, max_value=1.0, value=0.4, step=0.05)
    iou_threshold_2 = st.slider("NMS IOU Threshold (2nd Run)", min_value=0.0, max_value=1.0, value=0.15, step=0.05)
    batch_size_2 = st.slider("Batch Size (2nd Run)", min_value=1, max_value=32, value=4)

run_button = st.button("Run Both Settings")
#Define settings dictionaries for both runs
settings_1 = {
    'patch_size': patch_size_1,
    'patch_overlap': patch_overlap_1,
    'score_threshold': score_threshold_1,
    'iou_threshold': iou_threshold_1,
    'batch_size': batch_size_1
}
settings_2 = {
    'patch_size': patch_size_2,
    'patch_overlap': patch_overlap_2,
    'score_threshold': score_threshold_2,
    'iou_threshold': iou_threshold_2,
    'batch_size': batch_size_2
}

#Define model running progress bar function
def run_deepforest_with_progress(image_path,settings,output_gdf_name):
    st.write("Running DeepForest with tracking...")
    progress_box = st.empty()
    progress_bar = st.progress(0)

    # Build DeepForest command
    cmd = [
        sys.executable, "-m", "run_tile",
        "--image_path",image_path,
        "--patch_size", str(settings['patch_size']),
        "--patch_overlap", str(settings['patch_overlap']),
        "--score_threshold", str(settings['score_threshold']),
        "--iou_threshold", str(settings['iou_threshold']),  
        "--batch_size", str(settings['batch_size']),
        "--output_gdf", output_gdf_name
    ]
    # Run DeepForest as subprocess so we can capture its progress
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,bufsize=1)

    #  Stream DeepForest progress into Streamlit

    logs = ""
    
    for line in iter(process.stdout.readline, ''):
        if line == '':
             break

        logs += line
        progress_box.code(logs) #show full terminal log

    total_seconds=10
    for i in range(total_seconds+1):
        percent = int((i / total_seconds) * 100)
        progress_bar.progress(percent)
        time.sleep(1)


    process.wait()
    progress_bar.progress(100)
    st.success("DeepForest prediction completed!")
    return output_gdf_name
    
#--- Run Model ---
if run_button and image_path is not None:



    gdf1 = run_deepforest_with_progress(image_path,settings_1, "run1_predictions.csv")
    gdf2 = run_deepforest_with_progress(image_path,settings_2, "run2_predictions.csv")

