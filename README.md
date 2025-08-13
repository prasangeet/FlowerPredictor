# 🌸 Flower Image Classification Project

A full-stack application for classifying flower images using a deep learning model. Built with Django backend (PyTorch model) and Next.js frontend, providing an API for image prediction and a user-friendly web interface.

---

## Features

- **AI-Powered Classification**: Trained PyTorch model for flower recognition
- **REST API**: Django backend with image prediction endpoints
- **Modern Web Interface**: Next.js frontend with responsive design
- **Real-Time Predictions**: Instant classification with confidence scores
- **Easy Integration**: Clean API for external applications

---

## Project Structure

```
flower-classification/
├── backend/
│   ├── requirements.txt          # Python dependencies
│   └── core/
│       ├── db.sqlite3           # SQLite database
│       ├── manage.py            # Django management
│       ├── core/                # Django settings
│       └── flowerapi/           # API application
│           ├── best_flower_model.pth    # Trained model
│           ├── class_mapping.json       # Class mappings
│           ├── idx_to_class.json        # Index mappings
│           ├── predict.py               # Prediction logic
│           ├── training.ipynb           # Training notebook
│           └── views.py                 # API endpoints
├── data/
│   ├── flower_data.zip          # Dataset archive
│   └── flower_data/
│       ├── cat_to_name.json     # Category names
│       ├── train/               # Training images
│       ├── valid/               # Validation images
│       └── test_flat/           # Test images
├── frontend/
│   ├── package.json             # Node dependencies
│   ├── app/                     # Next.js pages
│   ├── components/              # React components
│   └── public/                  # Static assets
└── README.md
```

---

## Technology Stack

**Backend:**

- Django 4.0+ - Web framework and REST API
- PyTorch 2.0+ - Deep learning model
- Python 3.8+ - Core language

**Frontend:**

- Next.js 13+ - React framework
- Tailwind CSS - Styling
- JavaScript/React - UI components

---

## Setup Instructions

### Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create and activate virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup Django
cd core
python manage.py migrate
python manage.py runserver
```

Backend runs at: `http://localhost:8000`

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend runs at: `http://localhost:3000`

---

## API Documentation

### Base URL

```
http://localhost:8000/api/
```

### Endpoints

**POST /predict/**

- Upload flower image for classification
- Request: `multipart/form-data` with `image` field
- Response:

```json
{
  "success": true,
  "prediction": {
    "class": "rose",
    "confidence": 0.95,
    "class_name": "Rose"
  }
}
```

---

## Usage

1. Start both backend and frontend servers
2. Open `http://localhost:3000` in your browser
3. Upload a flower image to get instant classification results
4. View prediction confidence and alternative classifications

---

## Dataset

The `data/flower_data/` directory contains:

- **Training set**: ~6,000 categorized flower images
- **Validation set**: ~1,000 images for model validation
- **Test set**: ~1,000 images for evaluation
- **Categories**: Multiple flower species (Rose, Tulip, Daisy, etc.)
- **Mappings**: JSON files linking categories to readable names

---

## Model Information

- **Architecture**: Fine-tuned ResNet-50
- **Accuracy**: ~92% on validation set
- **Input**: 224x224 RGB images
- **Output**: Softmax probabilities for flower classes
- **Size**: ~100MB model file

---

## Development

### Running Tests

```bash
# Backend tests
cd backend/core
python manage.py test

# Frontend tests
cd frontend
npm test
```

### API Testing

```bash
curl -X POST -F "image=@flower.jpg" http://localhost:8000/api/predict/
```

---

## Deployment

### Production Backend

```bash
pip install gunicorn
gunicorn core.wsgi:application --bind 0.0.0.0:8000
```

### Production Frontend

```bash
npm run build
npm start
```

---

## License

This project is for educational and research purposes.

---

## Acknowledgements

- PyTorch for deep learning framework
- Django for backend API development
- Next.js and Tailwind CSS for modern frontend
- Open source flower datasets for training data
