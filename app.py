import os
import json
from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import gemini_helper

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['STORYBOOK_FOLDER'] = 'static/storybooks'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['STORYBOOK_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate', methods=['POST'])
def generate_storybook():
    try:
        character_info = {
            'name': request.form.get('name', ''),
            'age': request.form.get('age', ''),
            'interests': request.form.get('interests', ''),
            'theme': request.form.get('theme', ''),
            'art_style': request.form.get('art_style', 'anime art style')
        }
        
        uploaded_images = []
        if 'photos' in request.files:
            files = request.files.getlist('photos')
            for file in files:
                if file and allowed_file(file.filename):
                    img_bytes = file.read()
                    uploaded_images.append(img_bytes)
        
        storybook_data = gemini_helper.generate_storybook(character_info, uploaded_images)
        
        import time
        storybook_id = f"story_{int(time.time())}"
        storybook_dir = os.path.join(app.config['STORYBOOK_FOLDER'], storybook_id)
        os.makedirs(storybook_dir, exist_ok=True)
        
        pages_with_images = []
        for page in storybook_data['pages']:
            if page['type'] == 'image':
                image_filename = f"page_{page['page']}.png"
                image_path = os.path.join(storybook_dir, image_filename)
                
                success = gemini_helper.generate_storybook_image(
                    page['description'],
                    page['page'],
                    image_path
                )
                
                page['image_url'] = f"/static/storybooks/{storybook_id}/{image_filename}" if success else None
            
            pages_with_images.append(page)
        
        storybook_json_path = os.path.join(storybook_dir, 'storybook.json')
        with open(storybook_json_path, 'w') as f:
            json.dump({'pages': pages_with_images, 'info': character_info}, f)
        
        return jsonify({
            'success': True,
            'storybook_id': storybook_id,
            'pages': pages_with_images
        })
    
    except Exception as e:
        print(f"Error generating storybook: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/storybook/<storybook_id>')
def view_storybook(storybook_id):
    storybook_path = os.path.join(app.config['STORYBOOK_FOLDER'], storybook_id, 'storybook.json')
    
    if not os.path.exists(storybook_path):
        return "Storybook not found", 404
    
    with open(storybook_path, 'r') as f:
        storybook_data = json.load(f)
    
    return render_template('storybook.html', storybook=storybook_data, storybook_id=storybook_id)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
