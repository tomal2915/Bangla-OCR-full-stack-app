# বাংলা OCR — Bangla Handwritten Text Recognition

A full-stack web application that recognises handwritten Bangla characters using a CNN-based deep learning model. Upload an image and get the predicted character with a confidence score instantly.

---

## Features

- Handwritten Bangla character recognition across 50 character classes
- CNN model trained on the CMATERdb 3.1.2 dataset using TensorFlow/Keras
- REST API backend built with Django REST Framework
- React frontend with drag-and-drop image upload
- Prediction history stored in PostgreSQL
- Confidence score displayed with a visual progress bar

---

## Tech Stack

| Layer     | Technology                          |
|-----------|-------------------------------------|
| ML Model  | Python, TensorFlow, Keras (CNN)     |
| Backend   | Django, Django REST Framework       |
| Database  | PostgreSQL                          |
| Frontend  | React, Axios                        |

---

## Project Structure
bangla-ocr-app/
├── ml/                   # Model training and inference
│   ├── train.py          # CNN training script
│   ├── predict.py        # Single image prediction test
│   └── class_map.json    # Class index to label mapping
├── backend/              # Django REST API
│   ├── manage.py
│   ├── backend/          # Project settings and URLs
│   └── ocr/              # OCR app — models, views, serializers
└── frontend/             # React application
└── src/
├── components/
│   ├── Uploader.jsx
│   └── History.jsx
└── App.jsx

---

## Getting Started

### Prerequisites

- Python 3.11
- Node.js 18+
- PostgreSQL 18
- Git

---

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/bangla-ocr-app.git
cd bangla-ocr-app
```

---

### 2. Set up environment variables

Copy the example env file and fill in your values:
```bash
copy .env.example .env
```

Open `.env` and set:
```env
SECRET_KEY=your-django-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=bangla_ocr
DB_USER=postgres
DB_PASSWORD=your_postgres_password
DB_HOST=localhost
DB_PORT=5432

ML_MODEL_PATH=../ml/bangla_ocr.h5
ML_CLASS_MAP=../ml/class_map.json
```

Generate a secure `SECRET_KEY`:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

### 3. Train the ML model

Download the [CMATERdb 3.1.2 dataset](https://www.kaggle.com/datasets/debdoot/cmaterdb) and place the folders inside `ml/dataset/`.
```bash
pip install tensorflow matplotlib
python ml/train.py
```

Training completes automatically when validation accuracy stops improving. The model is saved to `ml/bangla_ocr.h5`.

---

### 4. Set up the backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

Create the PostgreSQL database:
```bash
psql -U postgres -c "CREATE DATABASE bangla_ocr;"
```

Run migrations and start the server:
```bash
python manage.py migrate
python manage.py runserver
```

Django runs at **http://localhost:8000**

---

### 5. Set up the frontend

Open a new terminal:
```bash
cd frontend
```

Create `frontend/.env`:
```env
REACT_APP_API_URL=http://localhost:8000/api
```

Install dependencies and start:
```bash
npm install
npm start
```

React runs at **http://localhost:3000**

---

## API Endpoints

| Method | Endpoint           | Description                        |
|--------|--------------------|------------------------------------|
| POST   | `/api/predict/`    | Upload an image, get OCR result    |
| GET    | `/api/predictions/`| Retrieve last 20 predictions       |

### Example request
```bash
curl -X POST http://localhost:8000/api/predict/ \
  -F "image=@handwritten_character.png"
```

### Example response
```json
{
  "id": 1,
  "image": "http://localhost:8000/media/uploads/handwritten_character.png",
  "predicted": "ক",
  "confidence": 94.73,
  "created_at": "2026-04-03T10:22:00Z"
}
```

---

## Environment Variables Reference

| Variable         | Description                        | Example               |
|------------------|------------------------------------|-----------------------|
| `SECRET_KEY`     | Django secret key                  | `django-insecure-...` |
| `DEBUG`          | Enable debug mode                  | `True`                |
| `ALLOWED_HOSTS`  | Comma-separated allowed hosts      | `localhost,127.0.0.1` |
| `DB_NAME`        | PostgreSQL database name           | `bangla_ocr`          |
| `DB_USER`        | PostgreSQL username                 | `postgres`            |
| `DB_PASSWORD`    | PostgreSQL password                 | `yourpassword`        |
| `DB_HOST`        | Database host                      | `localhost`           |
| `DB_PORT`        | Database port                      | `5432`                |
| `ML_MODEL_PATH`  | Path to trained `.h5` model        | `../ml/bangla_ocr.h5` |
| `ML_CLASS_MAP`   | Path to class map JSON             | `../ml/class_map.json`|

---

## Notes

- The trained model file `bangla_ocr.h5` is excluded from this repository due to its size. Train it locally using the instructions above.
- The dataset folder `ml/dataset/` is also excluded. Download it from Kaggle.
- Never commit your `.env` file. Use `.env.example` as a reference template.

---

## License

This project is for educational purposes.
