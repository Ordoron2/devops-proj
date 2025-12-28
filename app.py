import docker
from flask import Flask, render_template, redirect, url_for, jsonify

app = Flask(__name__)


try:
    client = docker.from_env()
except Exception as e:
    client = None
    print(f"Error: Could not connect to Docker. {e}")

@app.route('/')
def index():
    if not client:
        return "Docker is not connected. Make sure /var/run/docker.sock is mounted.", 500
    
 
    images = client.images.list()
    return render_template('index.html', images=images)

@app.route('/delete/<image_id>')
def delete_image(image_id):
    try:
    
        client.images.remove(image=image_id, force=True)
        return redirect(url_for('index'))
    except Exception as e:
        return f"Error deleting image: {e}", 400

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "docker_connected": client is not None}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
