from flask import Flask, jsonify
import psycopg2
import json
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

conn = psycopg2.connect(
    host="localhost",
    database="treedetect",
    user="postgres",
    password="Lfz19891011!",
    port = "5432"
)
@app.route('/data', methods=['GET'])
def get_trees():
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT jsonb_build_object(               
                    'type', 'FeatureCollection',
                    'features', jsonb_agg(
                    jsonb_build_object(
                    'type', 'Feature',
                    'properties', jsonb_build_object(
                    'score', score
                    ),
                    'geometry', ST_AsGeoJSON(ST_Transform(geometry, 4326))::jsonb
                )
            )
        )
        FROM tree_predictions;  
    """)

    
        geojson_result = cur.fetchone()[0]
        cur.close() 
        return jsonify(geojson_result)
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)