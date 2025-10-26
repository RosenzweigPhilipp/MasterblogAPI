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
    """Get all blog posts with optional sorting"""
    # Get query parameters for sorting
    sort_field = request.args.get('sort')
    sort_direction = request.args.get('direction')
    
    # Define valid parameters
    valid_sort_fields = ['title', 'content']
    valid_directions = ['asc', 'desc']
    
    # Validate sort parameters if provided
    if sort_field and sort_field not in valid_sort_fields:
        return jsonify({
            "error": f"Invalid sort field '{sort_field}'. Valid options are: {', '.join(valid_sort_fields)}"
        }), 400
    
    if sort_direction and sort_direction not in valid_directions:
        return jsonify({
            "error": f"Invalid direction '{sort_direction}'. Valid options are: {', '.join(valid_directions)}"
        }), 400
    
    # If sort field is provided but direction is not, default to ascending
    if sort_field and not sort_direction:
        sort_direction = 'asc'
    
    # If direction is provided but sort field is not, return error
    if sort_direction and not sort_field:
        return jsonify({
            "error": "Direction parameter requires a sort field. Please provide both 'sort' and 'direction' parameters."
        }), 400
    
    # Make a copy of POSTS to avoid modifying the original list
    posts_to_return = POSTS.copy()
    
    # Apply sorting if parameters are provided
    if sort_field:
        reverse_order = (sort_direction == 'desc')
        posts_to_return.sort(key=lambda post: post[sort_field].lower(), reverse=reverse_order)
    
    return jsonify(posts_to_return)


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


@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    """Update a blog post by ID"""
    # Get JSON data from request
    data = request.get_json()
    
    # Find the post with the given ID
    post_to_update = None
    for post in POSTS:
        if post['id'] == post_id:
            post_to_update = post
            break
    
    # Check if post was found
    if not post_to_update:
        return jsonify({
            "error": f"Post with id {post_id} not found."
        }), 404
    
    # Update the post (keep existing values if not provided)
    if data and 'title' in data and data['title']:
        post_to_update['title'] = data['title']
    
    if data and 'content' in data and data['content']:
        post_to_update['content'] = data['content']
    
    # Return the updated post with 200 OK status
    return jsonify(post_to_update), 200


@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    """Search for blog posts by title or content"""
    # Get query parameters
    title_query = request.args.get('title', '').lower()
    content_query = request.args.get('content', '').lower()
    
    # If no search parameters provided, return empty list
    if not title_query and not content_query:
        return jsonify([])
    
    # Filter posts based on search criteria
    matching_posts = []
    
    for post in POSTS:
        # Check if post matches search criteria
        title_match = title_query and title_query in post['title'].lower()
        content_match = content_query and content_query in post['content'].lower()
        
        # Add post if it matches any of the search criteria
        if title_match or content_match:
            matching_posts.append(post)
    
    return jsonify(matching_posts)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
