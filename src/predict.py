# src/predict.py - SIMPLE VERSION
import pickle
import os
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models", "phishing_detector.pkl")

# Load model once
def load_model():
    try:
        if not os.path.exists(MODEL_PATH):
            print(f"Model not found at {MODEL_PATH}")
            return None
        
        with open(MODEL_PATH, "rb") as f:
            model = pickle.load(f)
        
        print(f"✅ Model loaded successfully")
        return model
        
    except Exception as e:
        print(f"Error loading model: {e}")
        return None

# Load the model
model = load_model()

def predict_email(email_text):
    """
    Predict whether an email is phishing or legitimate.
    """
    if model is None:
        return {
            "label": "❌ Error: Model not loaded. Please run training first.",
            "confidence": 0.0
        }
    
    if not email_text or not email_text.strip():
        return {
            "label": "⚠️ Please enter email text",
            "confidence": 0.0
        }
    
    try:
        # Make sure email_text is a string
        email_text = str(email_text).strip()
        
        # Make prediction
        prediction = model.predict([email_text])[0]
        
        # Get confidence score
        if hasattr(model, "predict_proba"):
            proba = model.predict_proba([email_text])[0]
            confidence = max(proba) * 100
        else:
            confidence = 0.0
        
        # Create label based on prediction
        if prediction == 1:
            label = "⚠️ PHISHING EMAIL"
        else:
            label = "✅ LEGITIMATE EMAIL"
        
        return {
            "label": label,
            "confidence": round(float(confidence), 2)
        }
        
    except Exception as e:
        print(f"Prediction error: {e}")
        return {
            "label": f"❌ Error: {str(e)[:100]}",
            "confidence": 0.0
        }