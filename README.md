# 📚 Enhanced Blog API

A powerful RESTful API for managing blog posts with advanced features including search and sorting capabilities.

## 🚀 Features

### Core CRUD Operations
- ✅ **CREATE** - Add new blog posts with validation
- ✅ **READ** - Retrieve all posts with optional sorting
- ✅ **UPDATE** - Modify existing posts (full or partial updates)
- ✅ **DELETE** - Remove posts by ID

### Advanced Features
- 🔍 **Search** - Find posts by title or content with case-insensitive matching
- 📊 **Sorting** - Organize posts by title or content in ascending/descending order
- ⚠️ **Error Handling** - Comprehensive validation with descriptive error messages
- 🌐 **CORS Support** - Cross-origin requests enabled for frontend integration

## 🛠 Tech Stack

- **Backend**: Python Flask
- **Dependencies**: flask, flask-cors
- **Testing**: Custom test suite with comprehensive coverage
- **Environment**: Python virtual environment

## 📋 API Endpoints

### 1. Get All Posts (with optional sorting)
```http
GET /api/posts
GET /api/posts?sort=title&direction=asc
GET /api/posts?sort=content&direction=desc
```

**Query Parameters:**
- `sort` (optional): `title` or `content`
- `direction` (optional): `asc` or `desc` (defaults to `asc`)

**Response:**
```json
[
  {
    "id": 1,
    "title": "First post",
    "content": "This is the first post."
  },
  {
    "id": 2,
    "title": "Second post", 
    "content": "This is the second post."
  }
]
```

### 2. Create New Post
```http
POST /api/posts
Content-Type: application/json

{
  "title": "My New Post",
  "content": "This is the content of my new post."
}
```

**Response (201 Created):**
```json
{
  "id": 3,
  "title": "My New Post",
  "content": "This is the content of my new post."
}
```

### 3. Update Post
```http
PUT /api/posts/{id}
Content-Type: application/json

{
  "title": "Updated Title",
  "content": "Updated content"
}
```

**Features:**
- Supports partial updates (title only, content only, or both)
- Returns updated post object

### 4. Delete Post
```http
DELETE /api/posts/{id}
```

**Response (200 OK):**
```json
{
  "message": "Post with id 1 has been deleted successfully."
}
```

### 5. Search Posts
```http
GET /api/posts/search?title=flask
GET /api/posts/search?content=tutorial
GET /api/posts/search?title=python&content=guide
```

**Query Parameters:**
- `title` (optional): Search term for post titles
- `content` (optional): Search term for post content
- Uses OR logic: matches posts containing ANY search criteria
- Case-insensitive substring matching

## 🔧 Setup & Installation

### Prerequisites
- Python 3.7+
- pip (Python package manager)

### Installation Steps

1. **Clone the repository:**
```bash
git clone https://github.com/RosenzweigPhilipp/MasterblogAPI.git
cd MasterblogAPI
```

2. **Create and activate virtual environment:**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install flask flask-cors
```

4. **Run the application:**
```bash
python backend/backend_app.py
```

The API will be available at `http://localhost:5002`

## 🧪 Testing

### Automated Testing

Run the comprehensive test suite:
```bash
python test_api.py
```

Run quick tests:
```bash
python quick_test.py
```

### Manual Testing with curl

```bash
# Get all posts
curl -s "http://localhost:5002/api/posts" | python3 -m json.tool

# Sort by title ascending
curl -s "http://localhost:5002/api/posts?sort=title&direction=asc" | python3 -m json.tool

# Sort by title descending
curl -s "http://localhost:5002/api/posts?sort=title&direction=desc" | python3 -m json.tool

# Create a new post
curl -X POST "http://localhost:5002/api/posts" \
  -H "Content-Type: application/json" \
  -d '{"title": "Test Post", "content": "Testing the API"}' | python3 -m json.tool

# Search for posts
curl -s "http://localhost:5002/api/posts/search?title=test" | python3 -m json.tool

# Update a post
curl -X PUT "http://localhost:5002/api/posts/1" \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated Title"}' | python3 -m json.tool

# Delete a post
curl -X DELETE "http://localhost:5002/api/posts/1" | python3 -m json.tool
```

### Testing with Postman

Import the following endpoints into Postman:
- `GET http://localhost:5002/api/posts`
- `POST http://localhost:5002/api/posts`
- `PUT http://localhost:5002/api/posts/{id}`
- `DELETE http://localhost:5002/api/posts/{id}`
- `GET http://localhost:5002/api/posts/search`

## 📊 Sorting Examples

### Sort by Title
```bash
# A to Z (ascending)
GET /api/posts?sort=title&direction=asc

# Z to A (descending)  
GET /api/posts?sort=title&direction=desc

# Default to ascending
GET /api/posts?sort=title
```

### Sort by Content
```bash
# Content A to Z
GET /api/posts?sort=content&direction=asc

# Content Z to A
GET /api/posts?sort=content&direction=desc
```

## 🔍 Search Examples

### Search by Title
```bash
GET /api/posts/search?title=python
# Returns posts with "python" in the title
```

### Search by Content
```bash
GET /api/posts/search?content=tutorial
# Returns posts with "tutorial" in the content
```

### Combined Search
```bash
GET /api/posts/search?title=flask&content=guide
# Returns posts with "flask" in title OR "guide" in content
```

## ⚠️ Error Handling

The API returns appropriate HTTP status codes and error messages:

### 400 Bad Request
- Missing required fields (title, content)
- Invalid sort field or direction
- Direction parameter without sort field

### 404 Not Found
- Post with specified ID doesn't exist

### Example Error Response
```json
{
  "error": "Invalid sort field 'invalid'. Valid options are: title, content"
}
```

## 📁 Project Structure

```
MasterblogAPI/
├── backend/
│   └── backend_app.py          # Main Flask application
├── frontend/                   # Frontend files (if applicable)
│   ├── frontend_app.py
│   ├── static/
│   └── templates/
├── test_api.py                 # Comprehensive test suite
├── quick_test.py               # Quick testing utility
├── .venv/                      # Virtual environment
└── README.md                   # This file
```

## 🚀 Development Roadmap

### Completed Features ✅
- [x] Basic CRUD operations
- [x] Input validation and error handling  
- [x] Search functionality (title & content)
- [x] Sorting functionality (title & content, asc/desc)
- [x] Comprehensive test suite
- [x] CORS support

### Future Enhancements 🔮
- [ ] Database integration (SQLite/PostgreSQL)
- [ ] User authentication and authorization
- [ ] Pagination for large datasets
- [ ] Rate limiting
- [ ] API documentation with Swagger
- [ ] Docker containerization
- [ ] Category/tag system for posts

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 API Testing Status

| Endpoint | Method | Status | Features |
|----------|--------|--------|----------|
| `/api/posts` | GET | ✅ | List all posts + sorting |
| `/api/posts` | POST | ✅ | Create with validation |
| `/api/posts/{id}` | PUT | ✅ | Full & partial updates |
| `/api/posts/{id}` | DELETE | ✅ | Delete by ID |
| `/api/posts/search` | GET | ✅ | Search by title/content |

**Test Coverage:** 9/9 tests passing ✅

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🏗️ Built With

- [Flask](https://flask.palletsprojects.com/) - The web framework used
- [Flask-CORS](https://flask-cors.readthedocs.io/) - Cross-origin resource sharing
- Python 3.7+ - Programming language

## 👨‍💻 Author

**Philipp Rosenzweig** - [RosenzweigPhilipp](https://github.com/RosenzweigPhilipp)

---

⭐ **Star this repository if you find it helpful!**

🐛 **Found a bug?** [Create an issue](https://github.com/RosenzweigPhilipp/MasterblogAPI/issues)

📧 **Questions?** Feel free to reach out!