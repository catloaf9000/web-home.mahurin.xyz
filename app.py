from flask import Flask, render_template, send_from_directory, abort
import os
import markdown
import re
import json

BLOGS_DIR = 'blogs'
CONTACT_JSON = 'contact_info.json'

app = Flask(__name__)

def get_blog_metadata(filepath):
    with open(filepath, 'r') as file:
        lines = file.readlines()
    
    metadata = {}
    content_lines = []
    in_metadata_section = False
    in_content_section = False

    for line in lines:
        if line.strip() == '---':
            if in_metadata_section:
                in_metadata_section = False
                in_content_section = True
            else:
                in_metadata_section = True
            continue

        if in_metadata_section:
            key, value = line.split(':', 1)
            metadata[key.strip()] = value.strip().strip("'\"")
        elif in_content_section:
            content_lines.append(line)
    
    content = ''.join(content_lines).strip()
    return metadata, content

def json_to_dict(file):
    json_file = os.path.join(os.path.dirname(__file__), file)
    # Read the JSON file
    with open(json_file, 'r') as f:
        return json.load(f)

@app.route("/")
def index():
    contact_info = json_to_dict(CONTACT_JSON)
    return render_template('index.html', contact_info=contact_info)

@app.route("/blogs")
def blogs():
    blog_list = []
    for filename in os.listdir(BLOGS_DIR):
        if filename.endswith('.md'):
            filepath = os.path.join(BLOGS_DIR, filename)
            metadata, _ = get_blog_metadata(filepath)
            blog_list.append(metadata)
    blog_list.sort(key=lambda x: x['Date'], reverse=True)
    return render_template('blogs.html', blogs=blog_list)

@app.route("/blog/<slug>")
def blog(slug):
    for filename in os.listdir(BLOGS_DIR):
        if filename.endswith('.md'):
            filepath = os.path.join(BLOGS_DIR, filename)
            metadata, content = get_blog_metadata(filepath)
            blog_slug = re.sub(r'\s+', '-', metadata['Title']).lower()
            if blog_slug == slug:
                html_content = markdown.markdown(content)
                return render_template('blog.html', title=metadata['Title'], content=html_content, path=slug)
    abort(404)

@app.route("/projects")
def projects():
    return render_template('projects.html')

@app.route("/contact")
def contact():
    contact_info = json_to_dict(CONTACT_JSON)
    return render_template('contact.html', contact_info=contact_info)

if __name__ == '__main__':
    # Allow connections from any IP address
    app.run(host='0.0.0.0', port=5000)