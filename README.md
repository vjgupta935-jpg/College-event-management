# 🎉 College Event Management System

## ✅ COMPLETELY WORKING SYSTEM

This is a **fully functional** College Event Management System built with Flask, SQLAlchemy, and modern web technologies. All features work perfectly!

### 🚀 Features

✅ **User Authentication** - Secure login/registration with password hashing  
✅ **Event Management** - Browse, search, filter, and register for events  
✅ **Student Dashboard** - Personal event management and registration tracking  
✅ **Admin Panel** - Complete administrative control with user management  
✅ **Login Tracking** - Monitor user activity with detailed session tracking  
✅ **Modern UI** - Beautiful, responsive design with smooth animations  
✅ **Real-time Search** - Instant event filtering and search  
✅ **Category System** - Organized events by technology, cultural, career, etc.  

### 🛠️ Technologies Used

- **Backend:** Flask 2.3.3 with SQLAlchemy ORM
- **Frontend:** Modern HTML5, CSS3, JavaScript (ES6+)
- **Database:** SQLite (auto-created)
- **Authentication:** Session-based with secure password hashing
- **UI Framework:** Custom CSS with modern design patterns
- **Icons:** Font Awesome 6.4.0
- **Fonts:** Google Fonts (Inter)

### 📋 Requirements

- Python 3.8 or higher
- All dependencies listed in `requirements.txt`

## 🚀 Setup Instructions for VS Code

### Step 1: Extract and Open Project

1. **Extract the ZIP file** to your desired location
2. **Open VS Code**
3. **File → Open Folder** → Select the `college_event_management` folder
4. **Open Terminal** in VS Code (`View → Terminal` or `` Ctrl+` ``)

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate

# Activate virtual environment (Mac/Linux)
source venv/bin/activate
```

**Note for Windows Users:** If you get an execution policy error, run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Run the Application

```bash
python app.py
```

### Step 5: Access the System

1. **Open your browser** and go to: `http://localhost:5000`
2. **Admin Access:** Username: `admin`, Password: `admin123`
3. **Student Access:** Register a new account or use existing credentials

## 🎯 System Overview

### For Students:
- **Browse Events:** View all available events with search and filtering
- **Register:** One-click event registration with capacity tracking
- **Dashboard:** Personal overview of registered and available events
- **Profile:** Secure account management

### For Administrators:
- **User Management:** View all users and their activity
- **Login Tracking:** Monitor user sessions with detailed analytics
- **Event Creation:** Add new events with full details
- **System Analytics:** Comprehensive dashboard with statistics

## 📊 Database Structure

The system uses SQLite with the following tables:
- **Users:** Student and admin accounts with role-based access
- **Events:** Event details with categories and capacity management
- **Registrations:** Event registration tracking
- **LoginActivity:** Detailed user session monitoring

## 🎨 UI/UX Features

- **Modern Design:** Clean, professional interface with gradient backgrounds
- **Responsive Layout:** Works perfectly on desktop, tablet, and mobile
- **Interactive Elements:** Smooth hover effects and transitions
- **Real-time Feedback:** Instant validation and success/error messages
- **Accessibility:** Keyboard navigation and screen reader friendly

## 🔧 Development Features

- **Hot Reload:** Debug mode for development
- **Error Handling:** Comprehensive 404/500 error pages
- **Security:** CSRF protection and secure password storage
- **Logging:** Detailed user activity tracking
- **Scalable:** Easy to extend with additional features

## 📁 Project Structure

```
college_event_management/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── templates/            # HTML templates
│   ├── base.html         # Base layout
│   ├── index.html        # Homepage
│   ├── login.html        # Login page
│   ├── register.html     # Registration page
│   ├── dashboard.html    # Student dashboard
│   ├── events.html       # Events listing
│   ├── event_detail.html # Event details
│   ├── admin.html        # Admin dashboard
│   ├── admin_users.html  # User management
│   ├── create_event.html # Event creation
│   ├── 404.html          # Error pages
│   └── 500.html          # Error pages
└── static/               # Static assets
    ├── css/
    │   └── style.css     # Modern CSS styles
    └── js/
        └── main.js       # Interactive JavaScript
```

## 🎉 Success Indicators

If everything is working correctly, you should see:
- ✅ Server starts without errors
- ✅ Homepage loads with modern design
- ✅ Navigation buttons work perfectly
- ✅ Login/registration functions properly
- ✅ Events can be browsed and registered for
- ✅ Admin panel shows user activity tracking
- ✅ Database auto-creates with sample data

## 🐛 Troubleshooting

### Common Issues:

**Virtual Environment Issues:**
```bash
# Windows PowerShell execution policy
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Alternative activation (Windows)
venv\Scripts\python.exe app.py
```

**Port Already in Use:**
```bash
# Change port in app.py (line 582)
app.run(debug=True, host='0.0.0.0', port=5001)  # Use different port
```

**Database Issues:**
```bash
# Delete existing database and restart
rm college_events_new.db  # Linux/Mac
del college_events_new.db  # Windows
python app.py
```

## 🤝 Support

If you encounter any issues:
1. Check the terminal for error messages
2. Ensure all dependencies are installed correctly
3. Verify Python version is 3.8 or higher
4. Make sure the virtual environment is activated

---

**🎊 Your college event management system is ready to use!**

All features work perfectly - login, registration, event management, admin panel, and user tracking! 🚀
