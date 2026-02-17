# app.py - FIXED VERSION
from flask import Flask, render_template, request, jsonify
from src.predict import predict_email
import os

app = Flask(__name__)

@app.route("/")
def home():
    """Home page with the email input form"""
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    """Handle email prediction"""
    try:
        # Get email text from form
        email_text = request.form.get("email", "").strip()
        
        # Debug: Print what we received
        print(f"\n{'='*60}")
        print(f"Received email text (length: {len(email_text)})")
        print(f"First 100 chars: {email_text[:100]}")
        print(f"{'='*60}\n")
        
        # Validate input
        if not email_text:
            return render_template(
                "index.html",
                label="⚠️ ERROR: Please enter email text",
                confidence=0,
                email_text=""
            )
        
        if len(email_text) < 10:
            return render_template(
                "index.html",
                label="⚠️ ERROR: Email text too short (minimum 10 characters)",
                confidence=0,
                email_text=email_text
            )
        
        # Get prediction from the model
        result = predict_email(email_text)
        
        # Debug: Print the result
        print(f"\n{'='*60}")
        print(f"Prediction Result:")
        print(f"Label: {result['label']}")
        print(f"Confidence: {result['confidence']}%")
        print(f"{'='*60}\n")
        
        # Return result to template
        return render_template(
            "index.html",
            label=result["label"],
            confidence=result["confidence"],
            email_text=email_text  # Keep the text in form
        )
        
    except Exception as e:
        print(f"\n❌ ERROR in /predict route: {str(e)}")
        import traceback
        traceback.print_exc()
        
        return render_template(
            "index.html",
            label=f"❌ ERROR: {str(e)}",
            confidence=0,
            email_text=email_text if 'email_text' in locals() else ""
        )

@app.route('/api/check', methods=['POST'])
def api_check():
    """API endpoint for AJAX requests"""
    try:
        data = request.get_json()
        email_text = data.get("email", "").strip()
        
        if not email_text:
            return jsonify({
                "label": "⚠️ Please enter email text",
                "confidence": 0
            })
        
        result = predict_email(email_text)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            "label": f"❌ Error: {str(e)}",
            "confidence": 0
        })

@app.route('/test')
def test():
    """Test route to verify Flask is working"""
    return "Flask app is running! ✅"

@app.route('/check-model')
def check_model():
    """Check if model is loaded"""
    from src.predict import model
    model_path = os.path.join("models", "phishing_detector.pkl")
    
    return f"""
    <h1>Model Status Check</h1>
    <p><strong>Model Path:</strong> {model_path}</p>
    <p><strong>Model Exists:</strong> {os.path.exists(model_path)}</p>
    <p><strong>Model Loaded:</strong> {model is not None}</p>
    <p><strong>Model Type:</strong> {type(model)}</p>
    """

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🌐 STARTING PHISHING DETECTION WEB APP")
    print("="*60)
    
    # Check if model exists
    model_path = os.path.join("models", "phishing_detector.pkl")
    if not os.path.exists(model_path):
        print("⚠️  WARNING: Model file not found!")
        print(f"   Expected location: {model_path}")
        print("   Please run: python train.py")
        print("="*60)
    else:
        print(f"✅ Model found at: {model_path}")
    
    print("✅ Open your browser and go to: http://localhost:5000")
    print("✅ Test endpoint: http://localhost:5000/test")
    print("✅ Check model: http://localhost:5000/check-model")
    print("✅ Press CTRL+C to stop the server")
    print("="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
    