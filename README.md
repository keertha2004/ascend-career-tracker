
# 🧭 Ascend Career Tracker

A full-stack AI-powered career assistant that helps users:
- Upload resumes & job descriptions
- Check match scores
- Improve their resumes with AI
- Track job applications
- Visualize their job search progress with charts

✅ Deployed Live: [View App on Render](https://ascend-career-tracker.onrender.com/)


## 🚀 Features

### 📄 Resume Matching & Improvement
- Upload a resume (`.pdf` or `.docx`) and paste a job description
- AI calculates a **match score** between your resume and the job
- Suggests **resume improvements** based on the job role
- Download the improved resume as a **PDF**

### 📊 Job Application Tracker
- Add jobs with:
  - Company Name
  - Job Title
  - Status (Applied, Interviewing, Offer, etc.)
  - Match Score
  - Deadline
- View and manage all applications in one place

### 📈 Visual Dashboards
- Interactive charts using `matplotlib`:
  - Match scores over time
  - Status distribution (Pie Chart)
  - Applications per company (Bar Chart)

### 🔐 User Authentication
- Register / Login securely using `Flask-Login` and password hashing
- Each user has their **own dashboard and applications**

---

## ⚙️ Tech Stack

| Area         | Tools & Libraries                             |
|--------------|-----------------------------------------------|
| Backend      | Python, Flask                                 |
| Frontend     | HTML, CSS, Jinja2 Templates        |
| Database     | PostgreSQL (deployed on Render)               |
| Auth         | Flask-Login, Werkzeug Security                |
| Resume Logic | `resume_parser.py`, `match_logic.py`          |
| Charts       | Matplotlib                                    |
| PDF Output   | ReportLab                                     |
| Deployment   | Render (Free Tier)                            |
| Version Ctrl | Git + GitHub                                  |

---

## 📁 Project Structure

```

resume\_job\_tracker/
├── app.py                     # Main Flask app
├── requirements.txt           # Python dependencies
├── .env                       # Environment config (not pushed)
├── static/                    # CSS and static files
├── templates/                 # HTML pages
├── uploads/                   # Uploaded resume files
├── utils/
│   ├── auth.py                # User auth logic
│   ├── db\_config.py           # DB connection config
│   ├── match\_logic.py         # Resume-job match score logic
│   └── resume\_parser.py       # Resume text extraction
└── README.md

````

---

## 🛠️ Setup Instructions (Local Development)

1. **Clone the Repository**

```bash
git clone https://github.com/your-username/ascend-career-tracker.git
cd ascend-career-tracker
````

2. **Create a Virtual Environment**

```bash
python -m venv env
source env/bin/activate  # or `env\Scripts\activate` on Windows
```

3. **Install Dependencies**

```bash
pip install -r requirements.txt
```

4. **Add `.env` File**

Create a `.env` file with your configuration:

```env
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your_secret_key
DATABASE_URL=your_postgres_connection_url
```

5. **Run the App**

```bash
flask run
```

Visit: `http://localhost:5000`

---

## 🧠 What You’ll Learn From This Project

* Flask web development (routing, forms, Jinja2 templates)
* PostgreSQL database handling
* User authentication (Flask-Login)
* Working with resumes (PDF/DOCX parsing)
* Data visualization with `matplotlib`
* File uploads and processing
* Deployment on Render
* Environment variables and security best practices

---

## ✨ Future Improvements (Optional Ideas)

* Add email notifications for deadlines
* Integrate AI chat for resume tips
* Add LinkedIn job scraping and auto-fill
* Export full job tracker as Excel

---

## 📄 License

This project is open source and free to use.

---

## 🙌 Acknowledgements

Built by [Keerthana R](https://github.com/keertha2004) with 💙
If you found this useful, consider giving it a ⭐ on GitHub!

---

