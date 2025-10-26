from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


@app.route('/api/posts', methods=['GET'])
def get_posts():
    return jsonify(POSTS)


@app.route('/api/posts', methods=['POST'])
def add_post():
    """Add a new blog post"""
    # Get JSON data from request
    data = request.get_json()
    
    # Validate input - check if JSON was provided
    if data is None:
        return jsonify({"error": "No JSON data provided"}), 400
    
    # Check for required fields
    missing_fields = []
    if 'title' not in data or not data['title']:
        missing_fields.append('title')
    if 'content' not in data or not data['content']:
        missing_fields.append('content')
    
    if missing_fields:
        return jsonify({
            "error": f"Missing required fields: {', '.join(missing_fields)}"
        }), 400
    
    # Generate new unique ID
    new_id = max([post['id'] for post in POSTS]) + 1 if POSTS else 1
    
    # Create new post
    new_post = {
        "id": new_id,
        "title": data['title'],
        "content": data['content']
    }
    
    # Add to posts list
    POSTS.append(new_post)
    
    # Return the new post with 201 Created status
    return jsonify(new_post), 201


@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    """Delete a blog post by ID"""
    # Find the post with the given ID
    post_to_delete = None
    for i, post in enumerate(POSTS):
        if post['id'] == post_id:
            post_to_delete = POSTS.pop(i)
            break
    
    # Check if post was found and deleted
    if post_to_delete:
        return jsonify({
            "message": f"Post with id {post_id} has been deleted successfully."
        }), 200
    else:
        return jsonify({
            "error": f"Post with id {post_id} not found."
        }), 404


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
