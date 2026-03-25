from deepforest import main
import argparse
import os
from dotenv import load_dotenv

#Load Hugging Face token from .env file
load_dotenv()
hf_token = os.getenv("HF_TOKEN")
os.environ["HUGGINGFACE_HUB_TOKEN"] = hf_token

#Settings
parser = argparse.ArgumentParser()
parser.add_argument("--image_path", type=str, required=True, help="Path to the input image")
parser.add_argument("--patch_size", type=int, default=400, help="Size of the patches to split the image into")
parser.add_argument("--patch_overlap", type=float, default=0.0, help="Overlap between patches (0-1)")  
parser.add_argument("--score_threshold", type=float, default=0.0, help="Minimum score threshold for predictions (0-1)")
parser.add_argument("--iou_threshold", type=float, default=0.0, help="IOU threshold for non-max suppression (0-1)") 
parser.add_argument("--batch_size", type=int, default=16, help="Batch size for prediction")
parser.add_argument("--output_gdf", type=str, help="Path to the output GeoDataFrame file")
args = parser.parse_args()

model = main.deepforest()
gdf = model.predict_tile(
    path=args.image_path,
    patch_size=args.patch_size,
    patch_overlap=args.patch_overlap,
    iou_threshold=args.iou_threshold,
#    score_threshold=args.score_threshold,
#    batch_size=args.batch_size
)
# Filter predictions by score threshold
gdf = gdf[gdf['score'] >= args.score_threshold]
#Force overwrite if file exists
if os.path.exists(args.output_gdf):
    os.remove(args.output_gdf)

gdf.to_csv(args.output_gdf, index=False)
print(f"\nSaved predictions to {args.output_gdf}")