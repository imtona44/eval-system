# TEST Evaluation System - Trainee's Evaluation, Statement and Testimonies
https://img.shields.io/badge/Python-3.7+-blue.svg
https://img.shields.io/badge/Flask-2.0+-green.svg
https://img.shields.io/badge/MySQL-8.0+-orange.svg
https://img.shields.io/badge/Bootstrap-5.0+-purple.svg
https://img.shields.io/badge/License-MIT-yellow.svg
https://img.shields.io/badge/PRs-welcome-brightgreen.svg

TEST (Trainee's Evaluation, Statement and Testimonies) is a comprehensive digital platform for collecting, managing, and analyzing trainee feedback on instructor performance. Built for TESDA Region II, this system streamlines the entire evaluation process with dynamic search, batch management, and powerful reporting tools.

📱 Overview
TEST transforms the traditional paper-based evaluation process into a modern, efficient digital experience. Trainees can submit evaluations instantly, administrators gain real-time insights, and trainers receive actionable feedback to improve their performance.

Key Features
📝 Digital Evaluation Forms: Trainees submit ratings and comments with ease

📊 Admin Dashboard: Comprehensive overview of all submissions with batch management

🏆 Trainer Ratings: Performance metrics broken down by qualification

📈 Leaderboard: Top performers across all qualifications

🔍 Advanced Search & Filter: Search by student, trainer, qualification, or date range

📤 Export to Excel: One-click export of evaluation data

📁 Batch Management: Group and analyze evaluations by training batch

🔐 User Authentication: Secure role-based access for administrators and trainers

📱 Responsive Design: Works on desktop, tablet, and mobile devices

🏗️ System Architecture
text
┌─────────────────────────────────────────────────────────────────┐
│                    TEST Evaluation System                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐     │
│  │   Frontend   │    │   Backend    │    │   Database   │     │
│  │  HTML/CSS/JS │◄──►│   Flask      │◄──►│   MySQL      │     │
│  │  Bootstrap 5 │    │              │    │              │     │
│  └──────────────┘    └──────────────┘    └──────────────┘     │
│         │                   │                   │              │
│         └───────────────────┼───────────────────┘              │
│                             │                                  │
│                    ┌────────▼────────┐                         │
│                    │   JSON Backup   │                         │
│                    │  (Fallback)     │                         │
│                    └─────────────────┘                         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
🚀 Quick Start
Prerequisites
Python 3.7+

MySQL Server 8.0+

pip (Python package manager)

1. Clone the Repository
bash
git clone https://github.com/imtona44/eval-system.git
cd eval-system
2. Database Setup
bash
# Import the database structure
mysql -u root -p < database_structure.sql

# Or manually create the database
mysql -u root -p
CREATE DATABASE eval;
USE eval;
SOURCE database_structure.sql;
3. Configure Database Credentials
Update eval.py with your database credentials:

python
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'your_password'
app.config['MYSQL_DB'] = 'eval'
4. Install Dependencies
bash
pip install -r requirements.txt
5. Run the Application
bash
python eval.py
The application will be available at http://localhost:5000

🎯 Usage Guide
For Trainees
Access the Evaluation Form

Open the homepage

Fill in your personal information

Select your training batch

Complete the Evaluation

Select the trainer you're evaluating

Rate each criterion from 1-3:

1 = Disagree

2 = Agree

3 = Very Much Agree

Add comments (optional)

Submit Your Evaluation

Review your ratings

Click Submit

Confirmation message will appear

For Administrators
Access the Dashboard

Login with ADMIN credentials

View summary statistics

See recent submissions

Manage Evaluations

View all submissions

Search and filter results

Export data to Excel

Manage training batches

Generate Reports

View trainer performance ratings

Access qualification-based reports

Export comprehensive data

For Trainers
Login to Your Account

Use your trainer credentials

View your personal dashboard

Review Feedback

See evaluation ratings

Read trainee comments

Track performance over time

Export Your Data

Download your evaluation results

Generate reports for self-improvement

📁 Project Structure
text
eval-system/
├── eval.py                     # Main Flask application
├── requirements.txt            # Python dependencies
├── database_structure.sql      # MySQL database schema
├── README.md                   # This file
├── LICENSE                     # MIT License
│
├── templates/                  # HTML templates
│   ├── base.html              # Base template with common layout
│   ├── index.html             # Home page / Evaluation form
│   ├── dashboard.html         # Admin dashboard
│   ├── trainer_dashboard.html # Trainer dashboard
│   ├── login.html             # Login page
│   ├── ratings.html           # Trainer ratings view
│   ├── leaderboard.html       # Top performers leaderboard
│   ├── batch_management.html  # Batch management interface
│   └── export.html            # Export options
│
├── static/                     # Static assets
│   ├── styles.css             # Custom CSS styles
│   └── images/                # Image assets
│
├── docs/                       # Documentation
│   ├── api.md                 # API documentation
│   ├── database.md            # Database schema documentation
│   └── deployment.md          # Deployment guide
│
└── tests/                      # Test files
    ├── test_eval.py           # Unit tests
    └── test_api.py            # API tests
🔧 API Endpoints
Route	Method	Description
/	GET	Home page / Evaluation form
/login	GET/POST	User authentication
/logout	GET	Logout user
/dashboard	GET	Admin dashboard
/trainer-dashboard	GET	Trainer dashboard
/submit-evaluation	POST	Submit trainee evaluation
/get-evaluations	GET	Get evaluations with filters
/get-trainer-ratings	GET	Get trainer performance ratings
/get-leaderboard	GET	Get top performers
/export-excel	GET	Export data to Excel
/manage-batches	GET/POST	Batch management
/api/evaluations	GET	API endpoint for evaluations
/api/trainers	GET	API endpoint for trainers
🗄️ Database Schema
Core Tables
Table	Description
admin_users	User accounts (admins and trainers)
sections	Evaluation sections/categories
criteria	Individual evaluation questions
participants	Trainee information
responses_master	Submission tracking
responses	Individual rating responses
qualifications	Trainer qualifications
batches	Training batch information
ER Diagram
text
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   admin_users   │     │   participants  │     │    batches     │
├─────────────────┤     ├─────────────────┤     ├─────────────────┤
│ id (PK)         │     │ id (PK)         │     │ id (PK)         │
│ username        │     │ name            │     │ batch_name      │
│ password        │     │ email           │     │ created_at      │
│ role            │     │ batch_id (FK)   │     └─────────────────┘
└─────────────────┘     └─────────────────┘
         │                       │
         │                       │
         ▼                       ▼
┌─────────────────┐     ┌─────────────────┐
│  responses_     │     │    responses    │
│     master      │     │                 │
├─────────────────┤     ├─────────────────┤
│ id (PK)         │◄────│ response_id(FK) │
│ trainer_id(FK)  │     │ criteria_id(FK) │
│ participant_id  │     │ rating          │
│ created_at      │     │ comment         │
└─────────────────┘     └─────────────────┘
📊 Rating Scale
Rating	Description	Interpretation
1	Disagree	Needs Improvement
2	Agree	Satisfactory
3	Very Much Agree	Excellent
🔐 Default Login Credentials
Role	Username	Password
Administrator	ADMIN	admin123
Trainer 1	TRAINER1	trainer123
Trainer 2	TRAINER2	trainer123
Trainer 3	TRAINER3	trainer123
Trainer 4	TRAINER4	trainer123
📦 Installation Options
Standard Installation
bash
pip install -r requirements.txt
python eval.py
Development Installation
bash
# Clone repository
git clone https://github.com/yourusername/eval-system.git
cd eval-system

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements-dev.txt

# Run in development mode
python eval.py --debug
Production Deployment
bash
# Using Gunicorn (Linux/Mac)
pip install gunicorn
gunicorn -w 4 eval:app

# Using Waitress (Windows)
pip install waitress
waitress-serve --port=5000 eval:app

# Using Nginx + Gunicorn (Production)
# See docs/deployment.md for detailed instructions
🧪 Testing
bash
# Run unit tests
python -m pytest tests/

# Run with coverage
python -m pytest --cov=. tests/

# Run specific test file
python -m pytest tests/test_eval.py
🐛 Troubleshooting
Common Issues
Issue	Solution
MySQL connection failed	Check credentials in eval.py
Database not found	Run database_structure.sql
Port 5000 already in use	Change port: python eval.py --port=5001
Missing dependencies	Run: pip install -r requirements.txt
JSON fallback mode	Check MySQL connection, verify database exists
Database Fallback
If MySQL is unavailable, the system automatically falls back to JSON storage:

python
# Data is saved to data_store.json
# No data loss during database issues
Logs
bash
# View application logs
tail -f logs/eval.log
🤝 Contributing
Fork the repository

Create a feature branch: git checkout -b feature/amazing-feature

Commit your changes: git commit -m 'Add amazing feature'

Push to the branch: git push origin feature/amazing-feature

Open a Pull Request

Development Guidelines
bash
# Install pre-commit hooks
pip install pre-commit
pre-commit install

# Run linter
flake8 eval.py

# Run formatter
black eval.py
📄 License
Developed for TESDA Region II. See LICENSE for more information.

📞 Support
📧 Email: region2@tesda.gov.ph

📞 Telephone: (078) 846-1618

📍 Address: Bldg 1 TESDA Compound, Carig Norte, Tuguegarao, Cagayan

🙏 Acknowledgments
TESDA Region II - Project sponsor and support

Bootstrap - Frontend framework

Font Awesome - Icons

Community Contributors - Testing and feedback

🌟 Star Us
If you find this project useful, please give it a star on GitHub! ⭐


Built with ❤️ for TESDA Region II - Empowering Filipino learners through technology.
