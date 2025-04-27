
# Product Matching Pipeline

This project is a **Dockerized AI-powered product matcher** that uses image embeddings (via CLIP model), FAISS vector similarity search, and mocked MongoDB for metadata and logging.

---

## 🚀 Features

- 🔎 **Image-based product matching** using CLIP embeddings
- 🧠 **FAISS** vector database for similarity search
- 🗃️ **Mocked MongoDB** for metadata and log persistence
- 🐳 **Fully containerized** with Docker Compose
- 📂 **Batch matching** via Flask API
- 🧪 Easily testable and extendable pipeline

---

## 🗂️ Project Structure

```
.
├── app/
│   ├── input_images/           # Input images to be matched
│   ├── faiss/                  # Vector index & product IDs
│   ├── meta/
│   │   ├── products.json       # Product metadata
│   │   └── logs.json           # Logs and errors
│   ├── db.py                   # MongoDB mock logic
│   ├── vectordb.py             # FAISS DB management
│   ├── inference.py            # CLIP model wrapper
│   ├── product_queries.py      # Product lookup logic
│   └── main.py                 # Flask API entrypoint
├── model_repository_onnx/           # Triton model repo
├── model_repository_trt/           # Triton model repo
├── Dockerfile
├── docker-compose.yml
└── README.md
├── requirements.txt
```

---

## 🐳 Running with Docker

### 1. Clone the repo

```bash
git clone https://github.com/your-username/product-match-pipeline.git
cd product-match-pipeline
```

### 2. Add images

Place images to be matched in the `app/input_images/` folder or set a custom directory via `IMAGE_DIR`.

### 3. Start the pipeline

```bash
IMAGE_DIR=$(pwd)/app/input_images docker-compose up --build
```

---

## 📡 API Endpoints

### `GET /`

Simple welcome message.

### `GET /batch_match`

Scans all images in the input directory and returns the best product match with similarity scores.

Response:

```json
[{"_id":"prod_001","category":"Shoes","image":"1.jpeg","name":"Air Max 90","price":129.99,"similarity":107.18307495117188},
{"_id":"prod_001","category":"Shoes","image":"2.jpeg","name":"Air Max 90","price":129.99,"similarity":109.03010559082031}]
```

---

## 📋 Environment Variables

| Variable      | Description                          | Default                |
|---------------|--------------------------------------|------------------------|
| `IMAGE_DIR`   | Folder path for input images         | `/app/input_images`   |

---

## 🧪 Mock MongoDB for Logging

- Logs (e.g. errors or match attempts) are stored in `meta/logs.json`
- Use `logs_collection.insert_one({...})` anywhere in code to persist logs

---

## 🛠️ Future Improvements

- ✅ Parallelize image matching for better throughput
- ✅ Optimize latency by applying batching or caching strategies.

---
