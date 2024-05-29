from flask import Flask
from flask import render_template
from flask import send_file

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/blog")
def blog():
    # Placeholder for blog logic
    return render_template('blog.html')

@app.route("/projects")
def projects():
    # Placeholder for projects logic
    return render_template('projects.html')

if __name__ == '__main__':
    # Allow connections from any IP address
    app.run(host='0.0.0.0', port=5000, debug=True)