from flask import Flask, render_template, send_from_directory, abort
import os
import markdown
import re

BLOGS_DIR = 'blogs'

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

@app.route("/")
def index():
    return render_template('index.html')

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

if __name__ == '__main__':
    # Allow connections from any IP address
    app.run(host='0.0.0.0', port=5000, debug=True)