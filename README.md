# Workflow Automation of Tree Detection Visualization Comparison 
## -by DeepForest Model
## 1. Introduction
### This project aims to...

## 2. Tech tags
### <div style="color:red;">Python</div> <div style="color:red;">Jupyter Notebook</div> <div style="color:red;">Jave Script</div> <div style="color:red;">PostgresSQL</div> <div style="color:red;">HTML</div> <div style="color:red;">Geopandas</div> <div style="color:red;">Leaflet</div> <div style="color:red;">Geojson</div> <div style="color:red;">QGIS</div> <div style="color:red;">Deep Learing Model</div> <div style="color:red;">Workflow Automation</div>

## 3. Project Folder
- data
  - TreeAOIWGS84.tif
- Output
  - run1_predictions.geojson
  - run2_predictions.geojson
  - run1_predictions.csv
  - run2_predictions.cvs
  - settings.csv
  - ComparisonReport.pdf
- run_tile.py
- settingGUI.py
- ObjectDetectVisualComp.ipynb
- ComparisonWebpage.html

## 4. Results
Settings.csv (Relational Table)
|  | patch_size | patch_overlap | score_threshold | iou_threshold | batch_size |file_name |
| -------- | -------- | -------- | -------- | -------- | -------- | -------- |
| Run 1   | 1200   | 0.25   | 0.2 | 0.15 | 4 |run1_predictions |
| Run 2   | 800   | 0.25   | 0.4 | 0.15 | 4 | run2_predictions |

Geojson file attribute Table

| xmin | ymin | xmax | ymax | label | score | image_path | geometry | 
| -------- | -------- | -------- |-------- | -------- | -------- |-------- | -------- |
| 4733   | 1802   | 4799   |1876   | Tree  | 0.560285925865173   |TreeAOIWGS84.tif   | POLYGON ((4799 1802, 4799 1876, 4733 1876, 4733 1802, 4799 1802))   |
| 4532   | 2385   | 4775   |2608   | Tree   | 0.53722459077835   | TreeAOIWGS84.tif   | POLYGON ((4775 2385, 4775 2608, 4532 2608, 4532 2385, 4775 2385))   |
