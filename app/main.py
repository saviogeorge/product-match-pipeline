from flask import Flask, jsonify
from inference import get_clip_embedding
from vectordb import VectorDatabase
from product_queries import get_product_by_id
import os
from db import load_metadata_from_disk
load_metadata_from_disk()

app = Flask(__name__)
vectordb = VectorDatabase(dimension=512)
vectordb.load("faiss/vector.index", "faiss/product_ids.json")

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome! Use /match for one image or /batch_match for a folder of images."})

@app.route("/match", methods=["GET"])
def match():
    image_name = os.environ.get("IMAGE_NAME", "airmax90.jpg")
    image_path = f"/app/images/{image_name}"

    if not os.path.exists(image_path):
        return jsonify({"error": f"Image not found: {image_path}"}), 404

    emb = get_clip_embedding(image_path)
    matches = vectordb.search(emb, k=1)

    if not matches:
        return jsonify({"message": "No match found"}), 404

    prod_id, score = matches[0]
    product = get_product_by_id(prod_id)
    if not product:
        return jsonify({"error": f"No metadata found for product ID: {prod_id}"}), 404

    product["similarity"] = score
    return jsonify(product)

@app.route("/batch_match", methods=["GET"])
def batch_match():
    image_dir = os.environ.get("IMAGE_DIR", "/app/input_images")
    if not os.path.exists(image_dir):
        return jsonify({"error": f"Image directory '{image_dir}' not found."}), 400

    results = []
    for filename in os.listdir(image_dir):
        if not filename.lower().endswith((".jpg", ".jpeg", ".png")):
            continue

        path = os.path.join(image_dir, filename)
        emb = get_clip_embedding(path)
        if emb is None:
            continue

        matches = vectordb.search(emb, k=1)
        if not matches:
            continue

        prod_id, score = matches[0]
        product = get_product_by_id(prod_id)

        if product:
            product["similarity"] = score
            product["image"] = filename
            results.append(product)

    return jsonify(results)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
