import requests
import numpy as np
from PIL import Image
from transformers import BertTokenizer

# Triton model endpoints
CLIP_URL = "http://triton:8000/v2/models/clip_visual/infer"



# Load tokenizer
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

def get_clip_embedding(image_path):
    image = Image.open(image_path).resize((224, 224)).convert("RGB")
    image_np = np.array(image).astype(np.float32).transpose(2, 0, 1) / 255.0
    image_np = image_np[np.newaxis, ...]  # Add batch dimension

    payload = {
        "inputs": [{
            "name": "input",
            "shape": list(image_np.shape),
            "datatype": "FP32",
            "data": image_np.flatten().tolist()
        }]
    }

    response = requests.post(CLIP_URL, json=payload)
    result = response.json()

    if "outputs" not in result:
        print("CLIP Error:", result)
        return None

    return np.array(result["outputs"][0]["data"], dtype=np.float32)

def get_bert_embedding(text):
    inputs = tokenizer(text, padding="max_length", truncation=True, max_length=16, return_tensors="np")
    input_ids = inputs["input_ids"][0].astype(np.int64)

    payload = {
        "inputs": [{
            "name": "input_ids",
            "shape": list(input_ids.shape),
            "datatype": "INT64",
            "data": input_ids.tolist()
        }]
    }

    response = requests.post(BERT_URL, json=payload)
    result = response.json()

    if "outputs" not in result:
        print("BERT Error:", result)
        return None

    output = np.array(result["outputs"][0]["data"], dtype=np.float32).reshape(1, 16, 768)
    return output.mean(axis=1).squeeze()  # Mean pooling
