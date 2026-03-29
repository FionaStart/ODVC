from asyncio import log
import pandas as pd
import streamlit as st
from deepforest import main 
from deepforest import utilities
import os
import subprocess
import sys
from pyproj import CRS
import time
import csv



st.title("DeepForest Model Settings")
st.header("Select Local Tiff File")
image_path = st.text_input("Enter the path to your local TIFF file:") #   D:\Thesis2026\ProjectCode\Data\TreeAOIWGS84.tif
if st.button("Load Image"):
    if os.path.isfile(image_path):
        st.success("✅ Image loaded successfully!")
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
#Create settings.csv file to store settings for both runs
df = pd.DataFrame([settings_1, settings_2], index=["Run 1", "Run 2"])
df.to_csv("settings.csv", index=True)

#Define model running progress bar function
def run_deepforest_with_progress(image_path,settings,output_gdf_name):
    st.write("⏳ Running Model...")
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
    logs = []
    replace_next = False
    total_lines = 122
    processed_lines = 0

    for line in iter(process.stdout.readline, ''):
        if not line:
            break

        line = line.strip()
        is_predicting = "predicting" in line.lower()

        if is_predicting:
            if replace_next:
                #Replace the last line
               if logs:
                   logs[-1] = line
            else:
                logs.append(line)
                replace_next = True
        else:
            logs.append(line)
            #If this line contains "predicting", mark for replacement

            replace_next = False

        #Update progress box
        with progress_box.container(height=200):
            st.code("\n".join(logs), language="bash")  # Show last 10 lines of log
        
        #Update progress bar
        processed_lines += 1
        progress = int((processed_lines / total_lines) * 100)
        progress_bar.progress(min(progress, 100))  # Cap at 100%

        time.sleep(0.1)  # Small delay to allow UI to update
       
    process.wait()
    progress_bar.progress(100)
    
    return output_gdf_name
    
#--- Run Model & Create settings relational table---
if run_button and image_path is not None:

    gdf1 = run_deepforest_with_progress(image_path,settings_1, "run1_predictions.csv")
    st.success("✅ 1st run completed! Predictions saved to run1_predictions.csv")
    gdf2 = run_deepforest_with_progress(image_path,settings_2, "run2_predictions.csv")
    st.success("✅ 2nd run completed! Predictions saved to run2_predictions.csv")
    #Create new table SettingInfo.csv to store 1st and 2nd run settings and output path



