import google.generativeai as genai
import io
from PIL import Image
from flask import Flask, request, render_template, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configure Gemini
genai.configure(api_key="AIzaSyAV4g4LIPbwTIb6zMr1xBaHkRwwPdlDY5I")  # replace with your actual Gemini API key
model = genai.GenerativeModel(model_name="gemini-2.5-flash")

@app.route('/')
def index():
    return render_template('index.html', answer1=None)

@app.route('/que', methods=['POST'])
def ai_response():
    file = request.files.get('bill')
    question = request.form.get('question')

    if not question:
        return jsonify({"success": False, "error": "Missing question. Please type a question."})
    
    try:
        if file:
            # Process with image
            img = Image.open(file).convert("RGB")
            img_bytes = io.BytesIO()
            img.save(img_bytes, format='JPEG')
            image_data = img_bytes.getvalue()
            
            response = model.generate_content([
                question,
                {"mime_type": "image/jpeg", "data": image_data}
            ])
        else:
            # Process without image
            response = model.generate_content(question)
            
        return jsonify({"success": True, "answer": response.text})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
