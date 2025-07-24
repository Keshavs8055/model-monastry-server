# AutoML Backend API 🧠🔧

A modular Python Flask backend for training machine learning models via API. Built with MongoDB, supports CSV upload, model training, clustering, and more - In progress.

---

## 🛠 Tech Stack

- Python 3.x
- Flask
- MongoDB (PyMongo)
- Pandas, NumPy, Scikit-learn
- Joblib (for model saving)

---

## 🚀 Getting Started

```bash
git clone https://github.com/Keshavs8055/model-monastry-server
cd model-monastry-server
pip install -r requirements.txt
python app.py
```

---

## 📁 Folder Structure

- `controllers/`: Route logic
- `routes/`: API route mappings
- `models/`: MongoDB schema models
- `services/`: ML processing logic
- `utils/`: Logging and helper tools
- `db/`: MongoDB setup
- `uploads/`: Uploaded CSVs
- `models/`: Saved model files
- `logs/`: Request and error logs

---

## 📡 API (Planned)

- `POST /upload` → Upload dataset
- `GET /data-summary` → Get data stats
- `POST /train-model` → Train selected ML model
- `POST /cluster` → Run unsupervised clustering
- `POST /predict` → Predict using saved model
