from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__, static_folder='../static')
CORS(app)

POSTS_FILE = 'posts.json'

def load_posts():
    """
    Loads blog posts from the JSON file. Initializes the file if it is empty or faulty.

    Returns:
        list: A list of blog posts as dictionaries.
    """
    try:
        if not os.path.exists(POSTS_FILE):
            # File does not exist – create empty file
            with open(POSTS_FILE, 'w', encoding='utf-8') as file:
                json.dump([], file)
            return []

        with open(POSTS_FILE, 'r+', encoding='utf-8') as file:
            content = file.read().strip()
            if not content:
                # File is empty – initialize with empty list
                file.seek(0)
                json.dump([], file)
                file.truncate()
                return []
            file.seek(0)
            return json.load(file)

    except (json.JSONDecodeError, IOError) as e:
        print(f"Error loading the file: {e}")
        try:
            # On JSON error – overwrite file with empty list
            with open(POSTS_FILE, 'w', encoding='utf-8') as file:
                json.dump([], file)
        except IOError as write_error:
            print(f"Error resetting the file: {write_error}")
        return []

def save_posts(posts):
    """
    Saves blog posts to the JSON file.

    Args:
        posts (list): A list of blog post dictionaries.
    """
    try:
        with open(POSTS_FILE, 'w', encoding='utf-8') as file:
            json.dump(posts, file, ensure_ascii=False, indent=4)
    except IOError as e:
        print(f"Error saving the file: {e}")

def validate_post_data(data):
    """
    Validates the data for a new or updated blog post.

    Args:
        data (dict): The post data to validate.

    Returns:
        tuple: (bool, str) - (is_valid, error_message)
    """
    if not isinstance(data, dict):
        return False, "Invalid data format"
    
    title = data.get('title', '').strip()
    content = data.get('content', '').strip()
    
    if not title:
        return False, "Title must not be empty"
    if not content:
        return False, "Content must not be empty"
    
    return True, ""

@app.route('/api/posts', methods=['GET'])
def get_posts():
    """
    Returns all blog posts as JSON.
    
    Query Parameters:
        sort (str): Field to sort by ('title' or 'content')
        direction (str): Sort direction ('asc' or 'desc')
    
    Returns:
        JSON response with list of all posts and appropriate HTTP status code
    """
    try:
        posts = load_posts()
        
        # Optional sorting
        sort_key = request.args.get('sort')
        direction = request.args.get('direction', 'asc')

        if sort_key in ('title', 'content'):
            reverse = direction == 'desc'
            posts.sort(key=lambda x: x.get(sort_key, '').lower(), reverse=reverse)
        
        return jsonify(posts), 200
    except Exception as e:
        print(f"Error retrieving posts: {e}")
        return jsonify({"error": "An error occurred while retrieving posts"}), 500

@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    """
    Searches for posts by title and/or content.
    
    Query Parameters:
        title (str): Search term for title
        content (str): Search term for content
    
    Returns:
        JSON response with matching posts and appropriate HTTP status code
    """
    try:
        title_query = request.args.get('title', '').strip().lower()
        content_query = request.args.get('content', '').strip().lower()

        posts = load_posts()
        filtered = []

        for post in posts:
            title_match = title_query in post['title'].lower() if title_query else True
            content_match = content_query in post['content'].lower() if content_query else True

            if title_match and content_match:
                filtered.append(post)

        return jsonify(filtered), 200
    except Exception as e:
        print(f"Error searching posts: {e}")
        return jsonify({"error": "An error occurred while searching posts"}), 500

@app.route('/api/posts', methods=['POST'])
def add_post():
    """
    Adds a new blog post.
    
    Expected JSON body:
        title (str): Post title
        content (str): Post content
    
    Returns:
        JSON response with the new post data and appropriate HTTP status code
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        is_valid, error_message = validate_post_data(data)
        if not is_valid:
            return jsonify({"error": error_message}), 400

        posts = load_posts()
        new_id = max((post['id'] for post in posts), default=0) + 1
        
        new_post = {
            "id": new_id,
            "title": data['title'].strip(),
            "content": data['content'].strip()
        }
        
        posts.append(new_post)
        save_posts(posts)
        
        return jsonify(new_post), 201
    except Exception as e:
        print(f"Error adding post: {e}")
        return jsonify({"error": "An error occurred while adding the post"}), 500

@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    """
    Deletes a blog post by ID.
    
    Args:
        post_id (int): The ID of the post to delete
    
    Returns:
        JSON response with success/error message and appropriate HTTP status code
    """
    try:
        posts = load_posts()
        post_to_delete = next((post for post in posts if post['id'] == post_id), None)

        if not post_to_delete:
            return jsonify({"error": f"Post with id {post_id} not found"}), 404

        posts.remove(post_to_delete)
        save_posts(posts)
        
        return jsonify({"message": f"Post with id {post_id} has been deleted successfully"}), 200
    except Exception as e:
        print(f"Error deleting post {post_id}: {e}")
        return jsonify({"error": f"An error occurred while deleting post {post_id}"}), 500

@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    """
    Updates an existing blog post.
    
    Args:
        post_id (int): The ID of the post to update
    
    Expected JSON body:
        title (str, optional): New post title
        content (str, optional): New post content
    
    Returns:
        JSON response with updated post data and appropriate HTTP status code
    """
    try:
        posts = load_posts()
        post_to_update = next((post for post in posts if post['id'] == post_id), None)

        if not post_to_update:
            return jsonify({"error": f"Post with id {post_id} not found"}), 404

        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        # Update only provided fields
        title = data.get('title', '').strip() if 'title' in data else post_to_update['title']
        content = data.get('content', '').strip() if 'content' in data else post_to_update['content']

        # Validate updated data
        is_valid, error_message = validate_post_data({"title": title, "content": content})
        if not is_valid:
            return jsonify({"error": error_message}), 400

        post_to_update['title'] = title
        post_to_update['content'] = content

        save_posts(posts)
        return jsonify(post_to_update), 200
    except Exception as e:
        print(f"Error updating post {post_id}: {e}")
        return jsonify({"error": f"An error occurred while updating post {post_id}"}), 500

# Swagger UI Configuration
SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.json'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Masterblog API"
    }
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

if __name__ == '__main__':
    app.run(debug=True, port=5002)