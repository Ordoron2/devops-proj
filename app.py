import docker
from flask import Flask, jsonify, render_template

app = Flask(__name__)

# התחברות ל-Docker Socket של השרת
try:
    client = docker.from_env()
except Exception as e:
    client = None
    print(f"Error connecting to Docker: {e}")

@app.route('/')
def home():
    if not client:
        return jsonify({"error": "Docker not connected"}), 500
    
    # שליפת רשימת ה-Images
    images_list = []
    for img in client.images.list():
        images_list.append({
            "id": img.short_id,
            "tags": img.tags,
            "size_mb": round(img.attrs['Size'] / (1024 * 1024), 2)
        })
    
    return jsonify({
        "message": "Docker Image Cleaner API",
        "images_count": len(images_list),
        "images": images_list
    })

@app.route('/cleanup', methods=['POST'])
def cleanup():
    """מוחק Images מסוג Dangling (ללא שם) שתופסים מקום"""
    try:
        pruned = client.images.prune()
        return jsonify({
            "status": "success",
            "space_reclaimed_mb": round(pruned.get('SpaceReclaimed', 0) / (1024 * 1024), 2)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "docker_connected": client is not None}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
@app.route('/delete/<image_id>')
def delete_image(image_id):
    try:
        # פקודת מחיקה חזקה (Force)
        client.images.remove(image=image_id, force=True)
        return redirect(url_for('index'))
    except Exception as e:
        return f"שגיאה במחיקה: {e}", 400
