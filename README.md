# Full Stack Web Application - Setup Guide

A modern full-stack web application built with **Python (Flask)**, **HTML**, **CSS**, **JavaScript**, and **MongoDB**.

## 🎯 Features

- ✅ Responsive web interface with modern UI
- ✅ User management system
- ✅ Message board functionality
- ✅ Real-time dashboard with statistics
- ✅ MongoDB database integration
- ✅ RESTful API endpoints
- ✅ Beautiful CSS styling with gradient effects
- ✅ Auto-refreshing data every 30 seconds

## 📁 Project Structure

```
new project/
├── app.py                      # Flask backend application
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── README.md                  # This file
├── templates/
│   └── index.html            # Main HTML template
└── static/
    ├── css/
    │   └── style.css         # Main CSS stylesheet
    └── js/
        └── script.js         # Frontend JavaScript
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- MongoDB (local or MongoDB Atlas cloud)
- pip (Python package manager)

### Installation

1. **Clone/Navigate to project directory:**
   ```bash
   cd "c:\Users\Admin\Desktop\new project"
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate
   
   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup environment variables:**
   ```bash
   # Copy the example file
   copy .env.example .env
   
   # Edit .env with your MongoDB connection string
   ```

5. **Run the application:**
   ```bash
   python app.py
   ```

6. **Open in browser:**
   ```
   http://localhost:5000
   ```

## 🗄️ MongoDB Setup

### Option 1: Local MongoDB
- Install MongoDB Community Edition from https://www.mongodb.com/try/download/community
- Start MongoDB service
- Connection string: `mongodb://localhost:27017/`

### Option 2: MongoDB Atlas (Cloud)
1. Create account at https://www.mongodb.com/cloud/atlas
2. Create a free cluster
3. Get connection string
4. Update `.env` file with your connection string:
   ```
   MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
   ```

## 📚 API Endpoints

### Users
- `GET /api/users` - Get all users
- `POST /api/users` - Create new user
  - Body: `{ "name": "string", "email": "string" }`

### Messages
- `GET /api/messages` - Get all messages (latest 50)
- `POST /api/messages` - Post new message
  - Body: `{ "text": "string", "author": "string" }`

### Stats
- `GET /api/stats` - Get dashboard statistics

## 🎨 Frontend Features

### Dashboard
- View total users count
- View total messages count
- Connection status indicator
- Real-time statistics

### Users Section
- Add new users with name and email
- Display all users in a formatted list
- User creation timestamp
- Delete user functionality

### Messages Section
- Post messages with author name
- Display all messages with timestamps
- Real-time message feed
- Message formatting and escaping (XSS protection)

## 🔧 Technology Stack

| Layer | Technology |
|-------|------------|
| **Backend** | Flask (Python) |
| **Frontend** | HTML5, CSS3, Vanilla JavaScript |
| **Database** | MongoDB |
| **API** | RESTful API with JSON |

## 📝 Python Dependencies

- **Flask** - Web framework
- **pymongo** - MongoDB driver
- **python-dotenv** - Environment variable management
- **Werkzeug** - WSGI utilities

## 🛠️ Development

### Adding New Features

1. **Add backend route in app.py:**
   ```python
   @app.route('/api/newfeature', methods=['GET'])
   def new_feature():
       return jsonify({'message': 'New feature'})
   ```

2. **Add frontend JavaScript in static/js/script.js:**
   ```javascript
   function loadNewFeature() {
       fetch('/api/newfeature')
           .then(response => response.json())
           .then(data => console.log(data));
   }
   ```

3. **Add HTML section in templates/index.html**

4. **Style with CSS in static/css/style.css**

## 🐛 Troubleshooting

### MongoDB Connection Error
- Check if MongoDB service is running
- Verify connection string in `.env`
- Check firewall settings (for cloud MongoDB)

### Port 5000 Already in Use
```bash
python app.py --port 5001
```

### Module Not Found Errors
```bash
pip install -r requirements.txt
```

## 📦 Database Schema

### Users Collection
```json
{
  "_id": ObjectId,
  "name": "string",
  "email": "string",
  "created_at": ISODate
}
```

### Messages Collection
```json
{
  "_id": ObjectId,
  "text": "string",
  "author": "string",
  "created_at": ISODate
}
```

## 🔒 Security Notes

- Input validation implemented on frontend and backend
- XSS protection with HTML escaping
- CSRF tokens can be added for production
- Use environment variables for sensitive data
- Never commit `.env` file to version control

## 📄 License

This project is open source and available for educational purposes.

## 🤝 Support

For issues or questions, please refer to:
- Flask Documentation: https://flask.palletsprojects.com
- MongoDB Documentation: https://docs.mongodb.com
- PyMongo Documentation: https://pymongo.readthedocs.io

---

Happy coding! 🚀
