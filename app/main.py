from flask import Flask, jsonify
from inference import get_clip_embedding
from vectordb import VectorDatabase
from product_queries import get_product_by_id
import os
from db import load_metadata_from_disk, load_logs_from_disk, save_logs_to_disk, log_event
load_metadata_from_disk()
load_logs_from_disk()

app = Flask(__name__)
vectordb = VectorDatabase(dimension=512)
vectordb.load("faiss/vector.index", "faiss/product_ids.json")

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome! Goto /batch_match for results."})

@app.route("/batch_match", methods=["GET"])
def batch_match():
    image_dir = os.environ.get("IMAGE_DIR", "/app/input_images")
    if not os.path.exists(image_dir):
        log_event("ERROR", "Image directory not found", {"path": image_dir})
        return jsonify({"error": f"Image directory '{image_dir}' not found."}), 400

    results = []
    for filename in os.listdir(image_dir):
        if not filename.lower().endswith((".jpg", ".jpeg", ".png")):
            continue

        path = os.path.join(image_dir, filename)
        emb = get_clip_embedding(path)
        if emb is None:
            log_event("WARNING", "Embedding failed", {"image": filename})
            continue

        matches = vectordb.search(emb, k=1)
        if not matches:
            log_event("INFO", "No match found", {"image": filename})
            continue

        prod_id, score = matches[0]
        product = get_product_by_id(prod_id)

        if product:
            product["similarity"] = score
            product["image"] = filename
            results.append(product)
            log_event("INFO", "Match found", {
                "image": filename,
                "product_id": str(prod_id),
                "score": score
            })
    
    log_event("INFO", "Batch match completed", {"results_count": len(results)})
    save_logs_to_disk()
    return jsonify(results)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
