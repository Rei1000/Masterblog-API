// Function that runs once the window is fully loaded
window.onload = function() {
    // Attempt to retrieve the API base URL from the local storage
    var savedBaseUrl = localStorage.getItem('apiBaseUrl');
    // If a base URL is found in local storage, load the posts
    if (savedBaseUrl) {
        document.getElementById('api-base-url').value = savedBaseUrl;
        loadPosts();
    }
}

/**
 * Shows an error message to the user.
 * Message disappears automatically after 5 seconds.
 * @param {string} message - The error message to display
 */
function showError(message) {
    const errorDiv = document.getElementById('error-message');
    errorDiv.textContent = message;
    errorDiv.style.display = 'block';
    setTimeout(() => {
        errorDiv.style.display = 'none';
    }, 5000);
}

/**
 * Fetches and displays all blog posts from the API.
 * Includes optional sorting functionality.
 */
function loadPosts() {
    // Retrieve the base URL from the input field and save it to local storage
    var baseUrl = document.getElementById('api-base-url').value;
    localStorage.setItem('apiBaseUrl', baseUrl);

    // Use the Fetch API to send a GET request to the /posts endpoint
    fetch(baseUrl + '/posts')
        .then(response => {
            if (!response.ok) {
                throw new Error('Error loading posts');
            }
            return response.json();
        })
        .then(data => {
            // Clear out the post container first
            const postContainer = document.getElementById('post-container');
            postContainer.innerHTML = '';

            // For each post in the response, create a new post element and add it to the page
            data.forEach(post => {
                const postDiv = document.createElement('div');
                postDiv.className = 'post';
                postDiv.innerHTML = `<h2>${post.title}</h2><p>${post.content}</p>
                <button onclick="deletePost(${post.id})">Delete</button>`;
                postContainer.appendChild(postDiv);
            });
        })
        .catch(error => {
            console.error('Error:', error);
            showError('Error loading posts: ' + error.message);
        });
}

/**
 * Creates a new blog post.
 * Validates input fields before sending to the API.
 */
function addPost() {
    // Retrieve the values from the input fields
    var baseUrl = document.getElementById('api-base-url').value;
    var postTitle = document.getElementById('post-title').value;
    var postContent = document.getElementById('post-content').value;

    // Validierung der Eingabefelder
    if (!postTitle.trim()) {
        showError('Title cannot be empty');
        return;
    }
    if (!postContent.trim()) {
        showError('Content cannot be empty');
        return;
    }

    // Use the Fetch API to send a POST request to the /posts endpoint
    fetch(baseUrl + '/posts', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title: postTitle, content: postContent })
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(err => {
                throw new Error(err.error || 'Error creating post');
            });
        }
        return response.json();
    })
    .then(post => {
        console.log('Post added:', post);
        document.getElementById('post-title').value = '';
        document.getElementById('post-content').value = '';
        loadPosts(); // Reload the posts after adding a new one
    })
    .catch(error => {
        console.error('Error:', error);
        showError(error.message);
    });
}

/**
 * Deletes a blog post by its ID.
 * Asks for confirmation before deletion.
 * 
 * @param {number} postId - The ID of the post to delete
 */
function deletePost(postId) {
    // Ask for confirmation before deleting
    if (!confirm('Are you sure you want to delete this post?')) {
        return;
    }

    var baseUrl = document.getElementById('api-base-url').value;

    // Use the Fetch API to send a DELETE request to the specific post's endpoint
    fetch(baseUrl + '/posts/' + postId, {
        method: 'DELETE'
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Error deleting post');
        }
        return response.json();
    })
    .then(data => {
        console.log('Post deleted:', postId);
        loadPosts(); // Reload the posts after deleting one
    })
    .catch(error => {
        console.error('Error:', error);
        showError('Error deleting post: ' + error.message);
    });
}
